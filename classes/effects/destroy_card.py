#import jewgeeoh.classes.card 
from ..card import SpellCard, FieldSpellCard, TrapCard
from title_files.general_functions import sortMonsterListWeakestToStrongest

class DestroyCardSpell(SpellCard):
    def destroyCard(self, cards_list):
        for card in cards_list:
            for equip in card.equip_cards:
                equip.sendToGrave(card.card_owner)
        
            card.current_zone.removeCardFromZone(card, "To graveyard")
        return True
        
    def activate(self):
        super().activate()
        self.effect()

class DestroyCardTrap(TrapCard):
    def destroyCard(self, cards_list):
        for card in cards_list:
            card.current_zone.removeCardFromZone(card, "To graveyard")
        return True
        
    def getStrongestMonster(self, enemy_monster_list, filter_func):
        sorted_list = sortMonsterListWeakestToStrongest(enemy_monster_list, filter_func)
        try:
            return sorted_list[-1]
        except IndexError:
            return None
        
    def activate(self):
        super().activate()
        
    def meets_threshold(self, card):
        return True
