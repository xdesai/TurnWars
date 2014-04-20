from weapon import Weapon, BadWeaponRequest, BadWeaponCreation
from nose.tools import assert_raises

def bad_constructor_test():
    assert_raises(BadWeaponCreation, Weapon, 'sword', -1, 4, {})
    assert_raises(BadWeaponCreation, Weapon, 'sword', 10, -4, {})

def use_test():
    weapon = Weapon('sword', 5, 4, {})
    assert weapon.uses == 5
    weapon.use(5)
    assert weapon.uses == 0
    assert_raises(BadWeaponRequest, weapon.use)
    assert weapon.can_use() == False

def targeting_test():
    weapon = Weapon('sword', 5, 4, {'plane':0})
    assert weapon.can_target('plane') == False

def serializable_test():
    weapon = Weapon('sword', 5, 4, {'plane':0})
    print weapon.as_json()
    assert weapon.as_json() == '{"attack_strength": 4, "name": "sword", "non_tragetables": {"plane": 0}}'
