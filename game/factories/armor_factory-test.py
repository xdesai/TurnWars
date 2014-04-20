from armor_factory import ArmorFactory
from nose.tools import assert_raises

class MockClass:
    health = 0
    name = ''

    def __init__(self, name, starting_health):
        self.health = starting_health
        self.name = name

    def get_value(self):
        return "{} {}".format(self.name, self.health)

def validate_test():
    factory_data = {
        'plate': {
            'starting_health': 200,
        },
        'fake': {
            'not_a_real_key': 10
        },
    }
    factory = ArmorFactory({}, MockClass)
    assert factory.validate_data(factory_data['plate']) == True
    assert factory.validate_data(factory_data['fake']) == False
    assert factory.validate_data([]) == False

def create_test():
    factory_data = {
        'plate': {
            'starting_health': 200,
        },
        'shirt': {
            'starting_health': 10
        },
    }
    factory = ArmorFactory(factory_data, MockClass)
    armor = factory.create('plate')
    assert armor.get_value() == 'plate 200'
    armor = factory.create('shirt')
    assert armor.get_value() == 'shirt 10'