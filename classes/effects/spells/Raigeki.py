#import jewgeeoh.classes.card 
from .DarkHole import DarkHole

class Raigeki(DarkHole):
    def effect(self, testing=False):
        opponent_monsters = [zone.cards_contained[0] for zone in self.card_owner.opponent.duelist_zone.getAttr("monster_card_zones") if zone.getNumOfCardsContained() == 1]
        if opponent_monsters:
            if not testing:
                return self.destroyCard(opponent_monsters)
            else:
                return True
        else:
            return False

