#import jewgeeoh.classes.card 
import pygame
from ..destroy_card import DestroyCardSpell

class DarkHole(DestroyCardSpell):
    def effect(self, testing=False):
        player_monsters = [zone.cards_contained[0] for zone in self.card_owner.duelist_zone.getAttr("monster_card_zones") if zone.getNumOfCardsContained() == 1]
        opponent_monsters = [zone.cards_contained[0] for zone in self.card_owner.opponent.duelist_zone.getAttr("monster_card_zones") if zone.getNumOfCardsContained() == 1]
        available_monsters = (player_monsters + opponent_monsters)
        if available_monsters:
            if not testing:
                return self.destroyCard(available_monsters)
            else:
                return True
        else:
            return False
            
    def guiScreen(self):
        return
            
    def aiUseCondition(self, game_instance):
        player_monsters_on_field = []
        ai_monsters_on_field = []

        for monster_zone in game_instance.player.player_monster_zones_array:
            if monster_zone.zone.getNumOfCardsContained() == 1:
                player_monsters_on_field.append(monster_zone.zone.getCardByIndex(0))

        for monster_zone in game_instance.ai.player_monster_zones_array:
            if monster_zone.zone.getNumOfCardsContained() == 1:
                ai_monsters_on_field.append(monster_zone.zone.getCardByIndex(0))   

        if len(player_monsters_on_field) == 0:
            return False
       
        strongest_enemy_monster = None
        strongest_enemy_val = 0
        
        for monster in player_monsters_on_field:
            current_val = 0
            
            if not monster.is_set:  
                if monster.current_atk_points > monster.current_def_points:
                    current_val = monster.current_atk_points
                elif monster.current_atk_points < monster.current_def_points:
                    current_val = monster.current_def_points
                else:
                    current_val = monster.current_atk_points
                
            if current_val > strongest_enemy_val:
                strongest_enemy_val = current_val
                strongest_enemy_monster = monster
 
        if strongest_enemy_val >= game_instance.ai.life_points:
            return True       
 
        for monster in ai_monsters_on_field:
            if monster.current_atk_points > strongest_enemy_val:
                return False

        for card in game_instance.ai.cards_in_hand:
            if card.card_type == "Monster":
                #print(str(len(game_instance.ai.cards_in_hand)) + " " + str(card.current_atk_points) + " " + str(strongest_enemy_val))
                if card.current_atk_points > strongest_enemy_val and strongest_enemy_val > 0:
                    return False
        
        if len(player_monsters_on_field) - len(ai_monsters_on_field) < 2:
            return False
            for card in game_instance.ai.cards_in_hand:
                if card.card_type == "Monster":
                    #print(str(len(game_instance.ai.cards_in_hand)) + " " + str(card.current_atk_points) + " " + str(strongest_enemy_val))
                    if card.current_atk_points > strongest_enemy_val and strongest_enemy_val > 0:
                        return False
                                
        return True
