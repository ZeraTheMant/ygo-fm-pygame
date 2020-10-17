#import jewgeeoh.classes.card 
import pygame
from ..destroy_card import DestroyCardTrap

filter_func = lambda card: not card.is_set or card.in_atk_position

class SakuretsuArmor(DestroyCardTrap):
    will_animate = True

    def effect(self, testing=False, target=None):
        return self.destroyCard([target])
            
    def guiScreen(self):
        return
        
    def get_enemy_monster_list(self, enemy_player):
        monsters_on_field = []      

        for monster_zone in enemy_player.player_monster_zones_array:
            if monster_zone.zone.getNumOfCardsContained() == 1:
                monsters_on_field.append(monster_zone.zone.getCardByIndex(0))     
                
        return monsters_on_field
     
    def willTrigger(self, enemy_player, is_player=False):
        if is_player:
            if enemy_player.is_attacking:
                return True
            else:
                return False
    
        enemy_monster_list = self.get_enemy_monster_list(enemy_player)
        if len(enemy_monster_list) > 0:

            strongest_monster = self.getStrongestMonster(enemy_monster_list, filter_func)
            
            if strongest_monster == None:
                return False
            
            if enemy_player.opponent.life_points <= strongest_monster.current_atk_points:
                return True

            if enemy_player.attacking_monster:
                if strongest_monster.name == enemy_player.attacking_monster.name:
                    return True
        return False
                      
    def aiUseCondition(self, game_instance):
        return self.willTrigger(game_instance.player)
        
    def getTarget(self, target):
        return target
        
    def activate(self, target):
        super().activate()
        return self.effect(target=target)
