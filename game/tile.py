from game.serializable import Serializable


class Tile(Serializable):

    def __init__(self, tile_type, cover, non_passables, events):
        self.tile_type = tile_type
        self.cover = cover
        self.non_passables = non_passables
        self.events = events

    def flat(self):
        return self.tile_type

    def can_pass(self, name):
        return not (name in self.non_passables)

    def get_cover(self):
        return self.cover
