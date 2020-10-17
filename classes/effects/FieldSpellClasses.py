#import jewgeeoh.classes.card 
from ..card import FieldSpellCard


class FieldBonusByType(FieldSpellCard):
    BENEFITTED_TYPES = []
    DECREASED_TYPES = []
    BONUS = 200
    
    def getAvailableMonsters(self):
        player_monsters_field = [zone.cards_contained[0] for zone in self.card_owner.duelist_zone.getAttr("monster_card_zones") if zone.getNumOfCardsContained() == 1 and (zone.cards_contained[0].getMonsterType() in self.BENEFITTED_TYPES or zone.cards_contained[0].getMonsterType() in self.DECREASED_TYPES)]
        opponent_monsters_field = [zone.cards_contained[0] for zone in self.card_owner.opponent.duelist_zone.getAttr("monster_card_zones") if zone.getNumOfCardsContained() == 1 and (zone.cards_contained[0].getMonsterType() in self.BENEFITTED_TYPES or zone.cards_contained[0].getMonsterType() in self.DECREASED_TYPES)]
        
        player_monsters_hand = [card for card in self.card_owner.getCardsInHand() if card.getType() == "Monster" and (card.getMonsterType() in self.BENEFITTED_TYPES or card.getMonsterType() in self.DECREASED_TYPES)]
        opponent_monsters_hand = [card for card in self.card_owner.opponent.getCardsInHand() if card.getType() == "Monster" and (card.getMonsterType() in self.BENEFITTED_TYPES or card.getMonsterType() in self.DECREASED_TYPES)]
         
        return player_monsters_field + opponent_monsters_field + player_monsters_hand + opponent_monsters_hand

    def implement_increase(self, amount, destroyed=False):
        available_monsters = self.getAvailableMonsters()
        
        for monster in available_monsters:
            print(monster.name, monster.affected_by_field)
            if not destroyed:
                if monster.getMonsterType() in self.BENEFITTED_TYPES and not monster.affected_by_field:
                    monster.increaseCurrentAtkPoints(amount)
                    monster.increaseCurrentDefPoints(amount)
                    monster.affected_by_field = True
                elif monster.getMonsterType() in self.DECREASED_TYPES and not monster.affected_by_field:
                    monster.increaseCurrentAtkPoints(-amount)
                    monster.increaseCurrentDefPoints(-amount)
                    monster.affected_by_field = True
            else:
                if monster.getMonsterType() in self.BENEFITTED_TYPES and monster.affected_by_field:
                    monster.increaseCurrentAtkPoints(amount)
                    monster.increaseCurrentDefPoints(amount)
                elif monster.getMonsterType() in self.DECREASED_TYPES and monster.affected_by_field:
                    monster.increaseCurrentAtkPoints(-amount)
                    monster.increaseCurrentDefPoints(-amount)
                monster.affected_by_field = False

    def effect(self, testing=False):   
        self.implement_increase(self.BONUS)
        return True
        
    def sendToGrave(self, owner):
        self.implement_increase(-self.BONUS, destroyed=True)
        super().sendToGrave(owner)      

    def activate(self):
        super().activate()
        self.effect()        

  
class FieldBonusByAttribute(FieldSpellCard):
    BENEFITTED_ATTRS = []
    DECREASED_ATTRS = []  
    ATK_AMOUNT = 0
    DEF_AMOUNT = 0
    
    def getAvailableMonsters(self):
        player_monsters_field = [zone.cards_contained[0] for zone in self.card_owner.duelist_zone.getAttr("monster_card_zones") if zone.getNumOfCardsContained() == 1 and (zone.cards_contained[0].getAttr() in self.BENEFITTED_ATTRS or zone.cards_contained[0].getAttr() in self.DECREASED_ATTRS)]
        opponent_monsters_field = [zone.cards_contained[0] for zone in self.card_owner.opponent.duelist_zone.getAttr("monster_card_zones") if zone.getNumOfCardsContained() == 1 and (zone.cards_contained[0].getAttr() in self.BENEFITTED_ATTRS or zone.cards_contained[0].getAttr() in self.DECREASED_ATTRS)]
        
        player_monsters_hand = [card for card in self.card_owner.getCardsInHand() if card.getType() == "Monster" and (card.getAttr() in self.BENEFITTED_ATTRS or card.getAttr() in self.DECREASED_ATTRS)]
        opponent_monsters_hand = [card for card in self.card_owner.opponent.getCardsInHand() if card.getType() == "Monster" and (card.getAttr() in self.BENEFITTED_ATTRS or card.getAttr() in self.DECREASED_ATTRS)]
         
        return player_monsters_field + opponent_monsters_field + player_monsters_hand + opponent_monsters_hand
    
    def implement_increase(self, atk_amount, def_amount, destroyed=False):
        available_monsters = self.getAvailableMonsters()

        for monster in available_monsters:
            if not destroyed:
                if monster.getAttr() in self.BENEFITTED_ATTRS and not monster.affected_by_field:
                    monster.increaseCurrentAtkPoints(atk_amount)
                    monster.increaseCurrentDefPoints(def_amount)
                    monster.affected_by_field = True
                elif monster.getAttr() in self.DECREASED_ATTRS and not monster.affected_by_field:
                    monster.increaseCurrentAtkPoints(-atk_amount)
                    monster.increaseCurrentDefPoints(-def_amount)
                    monster.affected_by_field = True
            else:
                if monster.getAttr() in self.BENEFITTED_ATTRS and monster.affected_by_field:
                    monster.increaseCurrentAtkPoints(atk_amount)
                    monster.increaseCurrentDefPoints(def_amount)
                elif monster.getAttr() in self.DECREASED_ATTRS and monster.affected_by_field:
                    monster.increaseCurrentAtkPoints(-atk_amount)
                    monster.increaseCurrentDefPoints(-def_amount)
                monster.affected_by_field = False
                
    def effect(self, testing=False):   
        self.implement_increase(self.ATK_AMOUNT, self.DEF_AMOUNT)
        return True
        
    def sendToGrave(self, owner):
        self.implement_increase(-self.ATK_AMOUNT, -self.DEF_AMOUNT, destroyed=True)
        super().sendToGrave(owner)
        
    def activate(self):
        super().activate()
        self.effect()