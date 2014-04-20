from serializable import Serializable
class Unit(Serializable):
    dead = False
    name = ''
    transport = ''
    weapon = ''
    armor = ''
    coordinate = ''
    army = ''

    def __init__(self, name, transport, weapon, armor, coordinate, army):
        self.name = name
        self.transport = transport
        self.weapon = weapon
        self.armor = armor
        self.coordinate = coordinate
        self.army = army
        if(self.get_health() <= 0):
            self.dead = True

    def get_coordinate(self):
        return self.coordinate

    def set_coordinate(self, coordinate):
        self.coordinate = coordinate

    def move(self, coordinate, distance):
        self.transport.move(distance)
        return self.set_coordinate(coordinate)

    def do_damage(self, damage):
        self.armor.do_damage(damage)
        if(self.get_health() <= 0):
            self.dead = True

    def is_dead(self):
        return self.dead

    def get_health(self):
        return self.armor.get_health()

    def movement_range(self):
        return self.transport.get_spaces_left()

    def can_move(self, distance):
        return self.movement_range() >= distance

    def get_attack_strength(self):
        return self.weapon.get_attack_strength()

    def flat(self):
        return {
            'name': self.name,
            'transport': self.transport.flat(),
            'weapon': self.weapon.flat(),
            'armor': self.armor.flat(),
            'coordinate': self.coordinate.flat(),
            'army': self.army
        }
