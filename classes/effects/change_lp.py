#import jewgeeoh.classes.card 
from ..card import SpellCard


class LifePointsChanger(SpellCard):    
    will_animate = True
    single_card_animation = True
 
    POSITIVE_CHANGE = True
    AFFECTS_OPPONENT = False
    OWNER_LP_CHANGE = 0
    OPPONENT_LP_CHANGE = 0

    def effect(self, testing=False):   
        self.card_owner.life_points += (self.card_owner.starting_life_points * self.OWNER_LP_CHANGE)
        
        if self.AFFECTS_OPPONENT:
            damage = self.card_owner.opponent.starting_life_points * self.OPPONENT_LP_CHANGE
            self.card_owner.opponent.life_points += round(damage)
            
            if self.card_owner.opponent.life_points < 0:
                self.card_owner.opponent.life_points = 0
        return True      
        
    def guiScreen(self):
        return    
        
    def get_opponent_monsters(self, monster_zone_array):
        valid_monsters = []
    
        for zone in monster_zone_array:
            if zone.zone.getNumOfCardsContained() == 1:
                valid_monsters.append(zone.zone.getCardByIndex(0))
                
        return valid_monsters
        
    def aiUseCondition(self, game_instance):
        if not self.POSITIVE_CHANGE:
            if game_instance.player.life_points - (game_instance.player.starting_life_points * self.OPPONENT_LP_CHANGE) <= 0:
                return True
    
        opponent_monsters = self.get_opponent_monsters(game_instance.ai.player_monster_zones_array)
        face_up_monsters_atk_total = 0
        
        if len(opponent_monsters) > 0:
            if self.POSITIVE_CHANGE:
                change = self.OWNER_LP_CHANGE
            else:
                change = 0
                
            for monster in opponent_monsters:
                face_up_monsters_atk_total += monster.current_atk_points
                
            if game_instance.ai.life_points + (game_instance.ai_starting_life_points * change) <= face_up_monsters_atk_total + 1000:
                return False
        
        return self.willActivate()       
    
    def willActivate(self):
        return True      

    def activate(self):
        super().activate()
        self.effect()        
