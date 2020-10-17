#import jewgeeoh.classes.card 
import pygame
from classes.card import TrapCard

class MagicCylinder(TrapCard):
    will_animate = False
    
    def meets_threshold(self, card):
        return True

    def effect(self, testing=False, target=None):
        return True
            
    def guiScreen(self):
        return       
     
    def willTrigger(self, enemy_player, is_player=False):    
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
