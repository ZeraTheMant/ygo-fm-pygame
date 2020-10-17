#import jewgeeoh.classes.card 
from ..card import SpellCard


class EquipSpellCard(SpellCard):
    EXCLUSIVE_TO_CERTAIN_TYPES_OR_ATTRS = False
    EXCLUSIVE_TYPES = []
    EXCLUSIVE_ATTRS = []
    ATK_BONUS = 0
    DEF_BONUS = 0
    REQUIRES_TARGET_MONSTER = True
    
 
    def __init__(self, id, name, img, text, duelist, spell_or_trap_type, fusion_types_array):
        super().__init__(id, name, img, text, duelist, spell_or_trap_type, fusion_types_array)
        self.equipped_monster = None

    def equip(self, target_monster):
        self.equipped_monster = target_monster
        self.equipped_monster.equip_cards.append(self)

    def effect(self, testing=False):  
        if self.equipped_monster:
            self.equipped_monster.current_atk_points += self.ATK_BONUS
            self.equipped_monster.current_def_points += self.DEF_BONUS
        return True
        
    def sendToGrave(self, owner):
        if self.equipped_monster:
            if self.current_zone:
                self.current_zone.cards_contained.remove(self)
            self.equipped_monster.current_atk_points -= self.ATK_BONUS
            self.equipped_monster.current_def_points -= self.DEF_BONUS  
            #self.equipped_monster.equip_cards.remove(self)
            self.equipped_monster = None
            
        super().sendToGrave(owner)
        
    def getMyFieldMonsters(self):
        return [zone.getCardByIndex(0) for zone in self.card_owner.duelist_zone.monster_card_zones if zone.getNumOfCardsContained() == 1]
        
    def guiScreen(self):
        return    
        
    def aiUseCondition(self, game_instance):
        return self.willActivate()
    
    def aiGetEquipTarget(self):
        my_field_monsters = self.getMyFieldMonsters()
        return self.getStrongestAiValidMonster(my_field_monsters)
        
    def getStrongestAiValidMonster(self, my_field_monsters):
        strongest_value = 0
        strongest_card = None
        
        for monster in my_field_monsters:
            if monster.current_atk_points >= strongest_value:
                strongest_value = monster.current_atk_points
                strongest_card = monster
                
        return strongest_card
        
    def getValidEquipTargets(self, monster_list):  
        if self.EXCLUSIVE_TO_CERTAIN_TYPES_OR_ATTRS:   
            valid_target_list = []
        
            for monster in monster_list:
                if monster.monster_type in self.EXCLUSIVE_TYPES:
                    valid_target_list.append(monster)
                    
                if monster.monster_attr in self.EXCLUSIVE_ATTRS:
                    valid_target_list.append(monster)
  
            return valid_target_list
        else:
            return monster_list
    
    def willActivate(self):
        my_field_monsters = self.getMyFieldMonsters()
        
        if len(my_field_monsters) < 1:
            return False
        else:
            if self.EXCLUSIVE_TO_CERTAIN_TYPES_OR_ATTRS:
                valid_target_list = self.getValidEquipTargets(my_field_monsters)
                if len(valid_target_list) < 1:
                    return False
                
        return True      

    def activate(self):
        super().activate()
        self.effect()        
