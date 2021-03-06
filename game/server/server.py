from os import listdir
from os.path import isfile, join

from twisted.protocols import basic
from twisted.internet import protocol
import json
import uuid
import traceback
from pprint import pprint
from game.server.client import Client
from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol

dataDir = './data/basic'

class PublicProtocol(basic.Int32StringReceiver):
    def __init__(self, connection):
        self.clientConnection = connection

    def send(self, data):
        self.sendString(json.dumps(data).encode('utf-8'))

    def connectionMade(self):
       self.ip = self.transport.getPeer().host
       self.send({
            'type': 'welcome'
        })

    def terminate(self, message):
        self.send(message)
        self.transport.loseConnection()

    def stringReceived(self, message):
        print(message)
        try:
            data = json.loads(message)
            response = self.clientConnection.handleMessage(data, self)
            if(response):
                self.send(response)

        except Exception as e:
            try: 
                self.terminate(e.message)
            except:
                pass
            traceback.print_exception(Exception, e, None)
            #self.transport.loseConnection()


class ClientConnection:
    def __init__(self, manager):
        self.state = 'unregistered'
        self.manager = manager
        self.id = 'unknown';

    def handleMessage(self, data, messanger):

        print(messanger)
        print(data)
        if data['type'] == "listMatches":
            return {
                'type': 'matchList',
                'matches': self.manager.list_matches()
            }

        if data['type'] == "listMaps":
            onlyFiles = [f for f in listdir("./data/basic/scenarios".format(dataDir))]
            return {
                'type': 'mapList',
                'maps': list(map(lambda x: {'name': x}, onlyFiles))
            }

        if data['type'] == "register":
            if self.state == 'registered':
                raise Exception('error, repeated registration')
            else:
                if 'playerId' in data and data['playerId'] in self.manager.clients:
                    self.manager.clients[str(data['playerId'])].socket = messanger
                    self.id = data['playerId']
                else:
                    new_client = Client(messanger)
                    self.id = new_client.id_string
                    self.manager.clients[new_client.id_string] = new_client
                    self.state = 'registered'
                return {
                    'type': 'accept', 'playerId': str(self.id)
                }

        if 'playerId' in data:
            client = self.manager.clients[data['playerId']]

        if 'matchId' in data:
            self.manager.pass_to_match(data['matchId'], client, data)

        if data['type'] == "create":
            if 'scenario' in data:
                scenario = data['scenario']
            else:
                scenario = 'default.json'
            match_id = self.manager.create_match(client, scenario)
            return self.manager.matches[match_id].metadata('matchCreated')


class WSP(WebSocketServerProtocol):
    def __init__(self):
        WebSocketServerProtocol.__init__(self)
        self.clientConnection = None

    def send(self, response):
        self.sendMessage(json.dumps(response).encode('utf-8'))

    def terminate(self, message):
        self.send(message)
        self.transport.loseConnection()

    def onConnect(self, request):
        self.ip = request.peer.split(':')[1]
        print("some request connected {}".format(request))

    def onOpen(self):
        self.send({
            'type': 'welcome'
        })

    def onMessage(self, payload, isBinary):
        try:
            data = json.loads(payload)
            response = self.clientConnection.handleMessage(data, self)
            if(response):
                self.send(response)

        except Exception as e:
            try: 
                self.terminate(e.message)
            except:
                pass
            traceback.print_exception(Exception, e, None)


class WebSocketServer(WebSocketServerFactory):
    protocol = WSP
    def __init__(self, url, manager, connectionClass=ClientConnection):
        WebSocketServerFactory.__init__(self, url)
        self.manager = manager
        self.connectionClass = connectionClass

    def buildProtocol(self, addr):
        val = super().buildProtocol(addr)
        val.clientConnection = self.connectionClass(self.manager)
        return val

class Server(protocol.Factory):
    def __init__(self, manager, serverClass=PublicProtocol, connectionClass=ClientConnection):
        self.manager = manager
        self.connectionClass = connectionClass

    def buildProtocol(self, addr):
        clientConnection = self.connectionClass(self.manager)
        return PublicProtocol(clientConnection)


class MatchManager:
    def __init__(self, match_type):
        self.match_type = match_type
        self.matches = {}
        self.clients = {}

    def get_match(self, match_id):
        return self.matches[match_id]

    def create_match(self, client, scenario):
        new_match = self.match_type(client, scenario) 
        self.matches[new_match.id_string] = new_match
        return new_match.id_string

    def list_matches(self):
        print(self.matches)
        return list(map(lambda x: x.metadata(), self.matches.values()))

    def pass_to_match(self, match_id, connection, data):
        if(data['type'] in ['join', 'action']):
            getattr(self.get_match(match_id), data['type'])(connection, data)

