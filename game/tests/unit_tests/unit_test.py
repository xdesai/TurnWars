from game.unit import Unit
from game.coordinate import Coordinate
from nose import with_setup


class MockArmor:

    def reset(self):
        self.health += 10

    def __init__(self, name, health):
        self.name = name
        self.health = health

    def do_damage(self, damage):
        self.health -= damage

    def get_health(self):
        return self.health

    def flat(self):
        return self.name


class MockTransport:

    def __init__(self, name, spaces_per_turn, fuel):
        self.spaces_left = spaces_per_turn
        self.spaces_per_turn = spaces_per_turn
        self.fuel = fuel
        self.name = name
        self.moved_this_turn = False

    def move(self, distance):
        self.spaces_left -= distance
        self.moved_this_turn = True

    def get_spaces_left(self):
        return self.spaces_left

    def flat(self):
        return self.name

    def reset(self):
        self.spaces_left = self.spaces_per_turn

    def has_moved(self):
        return self.moved_this_turn


class MockWeapon:

    def __init__(self, name, attack_strength):
        self.name = name
        self.attack_strength = attack_strength
        self.cannot_target = {}

    def get_attack_strength(self):
        return self.attack_strength

    def use(self):
        return

    def can_use(self, dist):
        return 1

    def get_strength(self):
        return self.attack_strength

    def flat(self):
        return self.name

    def reset(self):
        self.attack_strength += 10


def test_unit():
    unit = Unit('tank', MockTransport('tred', 5, 10), MockWeapon('cannon', 10),
                MockArmor('plate', 30), Coordinate(1, 4), 'dragon')
    unit.uid = 0
    return unit


def get_coordinate_test():
    unit = test_unit()
    coordinate = unit.get_coordinate()
    assert coordinate.x == 1
    assert coordinate.y == 4


def set_coordinate_test():
    unit = test_unit()
    unit.set_coordinate(Coordinate(5, 5))
    coordinate = unit.get_coordinate()
    assert coordinate.x == 5
    assert coordinate.y == 5


def move_test():
    unit = test_unit()
    assert unit.movement_range() == 5
    unit.move(Coordinate(5, 5), 3)
    assert unit.movement_range() == 2
    coordinate = unit.get_coordinate()
    assert coordinate.x == 5
    assert coordinate.y == 5
    assert not unit.can_move(5)
    assert not unit.can_move(2)


def attack_test():
    unit = test_unit()
    unit2 = test_unit()
    unit.attack(unit2)
    assert unit2.get_health() == 20


def damage_test():
    unit = test_unit()
    assert unit.get_health() == 30
    unit.do_damage(10)
    assert unit.get_health() == 20


def zero_health_test():
    unit = test_unit()
    assert not unit.is_dead()
    unit.do_damage(10)
    assert not unit.is_dead()
    unit.do_damage(10)
    assert not unit.is_dead()
    unit.do_damage(10)
    assert unit.is_dead()
    unit = Unit('tank', 'tred', 'cannon',
                MockArmor('plate', 0), Coordinate(1, 4), 'dragon')
    assert unit.is_dead()


def attack_strength_test():
    unit = test_unit()
    assert unit.get_attack_strength() == 10


def serialization_test():
    unit = test_unit()
    json_string = ('{"armor": "plate", "army": "dragon", '
        '"coordinate": {"x": 1, "y": 4}, "id": 0, "name": "tank", '
        '"transport": "tred", "weapon": "cannon"}')
    assert unit.as_json() == json_string


def reset_test():
    unit = test_unit()
    unit.transport.spaces_left = 0
    unit.weapon.attack_strength = 0
    unit.armor.health = 0
    unit.reset()
    assert unit.transport.spaces_left == 5
    assert unit.weapon.attack_strength == 10
    assert unit.armor.health == 10
