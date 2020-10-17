#import jewgeeoh.classes.card 
import pygame
from ..destroy_card import DestroyCardSpell

class HeavyStorm(DestroyCardSpell):
    def effect(self, testing=False):
        player_spells = [zone.cards_contained[0] for zone in self.card_owner.duelist_zone.getAttr("spell_and_trap_card_zones") if zone.getNumOfCardsContained() == 1]
        opponent_spells = [zone.cards_contained[0] for zone in self.card_owner.opponent.duelist_zone.getAttr("spell_and_trap_card_zones") if zone.getNumOfCardsContained() == 1]
        player_field = []
        opponent_field = []
        
        if self.card_owner.opponent.duelist_zone.getAttr("field_card_zone").getNumOfCardsContained() == 1: 
            player_field.append(self.card_owner.opponent.duelist_zone.getAttr("field_card_zone").getCardByIndex(0))

        if self.card_owner.opponent.duelist_zone.getAttr("field_card_zone").getNumOfCardsContained() == 1:
            opponent_field.append(self.card_owner.opponent.duelist_zone.getAttr("field_card_zone").getCardByIndex(0))
        
        available_spells_traps = (player_spells + opponent_spells + player_field + opponent_field)
        
        if available_spells_traps:
            if not testing:
                return self.destroyCard(available_spells_traps)
            else:
                return True
        else:
            return False
            
    def guiScreen(self):
        return
            
    def aiUseCondition(self, game_instance):
        player_spells_on_field = []

        for spell_zone in game_instance.player.duelist_zone.getAttr("spell_and_trap_card_zones") + [game_instance.player.duelist_zone.getAttr("field_card_zone")]:
            if spell_zone.getNumOfCardsContained() == 1:
                player_spells_on_field.append(spell_zone.getCardByIndex(0))       
       
        if len(player_spells_on_field) == 0:
            return False      
        
        if len(player_spells_on_field) < 2:
            return False

        return True
