#import jewgeeoh.classes.card 
import pygame
from ..destroy_card import DestroyCardTrap

filter_func = lambda card: not card.is_set or card.in_atk_position

class TrapHole(DestroyCardTrap):
    will_animate = True
    min_threshold = 1000
    max_threshold = 99999

    def effect(self, testing=False, target=None):
        return self.destroyCard([target])
            
    def guiScreen(self):
        return   
        
    def get_enemy_monster_list(self, enemy_player, filter_func=lambda card: True):
        monsters_on_field = []      

        for monster_zone in enemy_player.player_monster_zones_array:
            if monster_zone.zone.getNumOfCardsContained() == 1:
                if filter_func(monster_zone.zone.getCardByIndex(0)):
                    monsters_on_field.append(monster_zone.zone.getCardByIndex(0))     
                
        return monsters_on_field
     
    def willTrigger(self, enemy_player, is_player=False):  
        set_enemy_just_placed_monsters = self.get_enemy_monster_list(enemy_player, filter_func=lambda card: card.just_placed_in_field)
        if len(set_enemy_just_placed_monsters) > 0:
            card = set_enemy_just_placed_monsters[0]
            if card.is_set:
                return True
            else:
                if card.current_atk_points >= TrapHole.min_threshold and card.current_atk_points <= TrapHole.max_threshold:
                    return True
                else:
                    return False
        else:
            return False
                      
    def aiUseCondition(self, game_instance):
        return self.willTrigger(game_instance.player)
        
    def getTarget(self, target):
        return target
        
    def activate(self, target):
        super().activate()
        return self.effect(target=target)
        
    def meets_threshold(self, card):
        if card.current_atk_points >= TrapHole.min_threshold and card.current_atk_points <= TrapHole.max_threshold:
            return True
        return False
