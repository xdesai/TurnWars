from unit import Unit
from coordinate import Coordinate
from nose import with_setup

class MockArmor:
    health = 0
    name = ''

    def do_damage(self, damage):
        self.health -= damage

    def get_health(self):
        return self.health

    def __init__(self, name, health):
        self.name = name
        self.health = health 

    def flat(self):
        return self.name

class MockTransport:
    name = ''
    spaces_left = 0
    spaces_per_turn = 0
    fuel = 0

    def __init__(self, name, spaces_per_turn, fuel):
        self.spaces_left = spaces_per_turn
        self.spaces_per_turn = spaces_per_turn
        self.fuel = fuel
        self.name = name

    def move(self, distance):
        self.spaces_left -= distance

    def get_spaces_left(self):
        return self.spaces_left

    def flat(self):
        return self.name

class MockWeapon:
    name = ''
    attack_strength = 0
    cannot_target = {}

    def get_attack_strength(self):
        return self.attack_strength

    def __init__(self, name, attack_strength):
        self.name = name
        self.attack_strength = attack_strength

    def flat(self):
        return self.name

def test_unit():
    return Unit('tank', MockTransport('tred', 5, 10), MockWeapon('cannon', 10),
                MockArmor('plate', 30), Coordinate(1,4), 'dragon')


def get_coordinate_test():
    unit = test_unit()
    coordinate = unit.get_coordinate()
    assert coordinate.x == 1
    assert coordinate.y == 4

def set_coordinate_test():
    unit = test_unit()
    unit.set_coordinate(Coordinate(5,5))
    coordinate = unit.get_coordinate()
    assert coordinate.x == 5
    assert coordinate.y == 5

def move_test():
    unit = test_unit()
    assert unit.movement_range() == 5
    unit.move(Coordinate(5,5), 3)
    assert unit.movement_range() == 2
    coordinate = unit.get_coordinate()
    assert coordinate.x == 5
    assert coordinate.y == 5
    assert unit.can_move(5) == False
    assert unit.can_move(2) == True

def damage_test():
    unit = test_unit()
    assert unit.get_health() == 30
    unit.do_damage(10)
    assert unit.get_health() == 20

def zero_health_test():
    unit = test_unit()
    assert unit.is_dead() == False
    unit.do_damage(10)
    assert unit.is_dead() == False
    unit.do_damage(10)
    assert unit.is_dead() == False
    unit.do_damage(10)
    assert unit.is_dead() == True
    unit = Unit('tank', 'tred', 'cannon', 
                MockArmor('plate', 0), Coordinate(1,4), 'dragon')
    assert unit.is_dead() == True

def attack_strength_test():
    unit = test_unit()
    assert unit.get_attack_strength() == 10

def serialization_test():
    unit = test_unit()
    assert unit.as_json() == '{"name": "tank", "army": "dragon", "armor": "plate", "weapon": "cannon", "coordinate": {"y": 4, "x": 1}, "transport": "tred"}'
