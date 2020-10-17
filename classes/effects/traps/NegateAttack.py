#import jewgeeoh.classes.card 
import pygame
from classes.card import TrapCard

class NegateAttack(TrapCard):
    will_animate = False
    
    def __init__(self, id, name, img, text, duelist, spell_or_trap_type, fusion_types_array):
        super().__init__(id, name, img, text, duelist, spell_or_trap_type, fusion_types_array)
        self.enemy_monster_list = None

    def meets_threshold(self, card):
        return True

    def effect(self, testing=False, target=None):
        for monster in self.enemy_monster_list:
            monster.has_attacked = True
        return True
            
    def guiScreen(self):
        return
        
    def get_enemy_monster_list(self, enemy_player):
        monsters_on_field = []      

        for monster_zone in enemy_player.player_monster_zones_array:
            if monster_zone.zone.getNumOfCardsContained() == 1:
                monsters_on_field.append(monster_zone.zone.getCardByIndex(0))     
                
        return monsters_on_field
     
    def willTrigger(self, enemy_player, is_player=False):
        self.enemy_monster_list = self.get_enemy_monster_list(enemy_player)
    
        if enemy_player.is_attacking:
            return True
        else:
            return False
                      
    def aiUseCondition(self, game_instance):
        return self.willTrigger(game_instance.player)
        
    def getTarget(self, target):
        return target
        
    def activate(self, target):
        super().activate()
        return self.effect(target=target)
