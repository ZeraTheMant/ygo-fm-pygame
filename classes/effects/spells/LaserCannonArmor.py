from ..equip_spell_card import EquipSpellCard


class LaserCannonArmor(EquipSpellCard):
    EXCLUSIVE_TO_CERTAIN_TYPES_OR_ATTRS = True
    EXCLUSIVE_TYPES = ["Insect"]
    ATK_BONUS = 300
    DEF_BONUS = 300