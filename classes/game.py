#from .player_init import ACTIVE_PLAYER
from .field import Field
from .duelist import Duelist
import random, pygame

class Game(object):
    current_turn = 1
    FIRST_TURN_CHOICES = {1: "Rock", 2: "Paper", 3: "Scissors"}
    game_over = False
    
    def __init__(self, player_dict, player_lp, ai_lp, opponent_catlev_id):
        self.player = Duelist(player_dict['Deck_ID'], True, player_dict['Name'], player_lp)
        self.ai = Duelist(opponent_catlev_id, False, "TEST_BOT", ai_lp, is_ai=True)
        self.player.setOpponent(self.ai)
        self.ai.setOpponent(self.player)
        
        self.field = Field(self.player, self.ai)
        self.current_turn_player = None
        self.winner = None
        
        #if not Game.game_over:
        #    self.getFirstTurnPlayer()
        #    self.gameLoop()

    def compareFirstTurnChoices(self, player_choice, comp_choice):
        #print("You chose " + player_choice + " and the computer chose " + comp_choice + ".")
        
        if player_choice == comp_choice:
            #print("It's a tie! Do it again.\n")
            return "repeat"
        else:
            if player_choice == "Rock" and comp_choice == "Paper":
                #print("The computer goes first.\n")
                return "computer"
            elif player_choice == "Rock" and comp_choice == "Scissors":
                #print("You go first.\n")
                return "player"
                self.current_turn_player = self.player
            elif player_choice == "Paper" and comp_choice == "Rock":
                #print("You go first.\n")
                return "player"
                self.current_turn_player = self.player
            elif player_choice == "Paper" and comp_choice == "Scissors":
                #print("The computer goes first.\n")
                return "computer"
            elif player_choice == "Scissors" and comp_choice == "Rock":
                #print("The computer goes first.\n")
                return "computer"
            else:
                #print("You go first.\n")
                return "player"

    def getFirstTurnPlayer(self):
        while True:
            try:
                comp_choice = Game.FIRST_TURN_CHOICES[random.randint(1, 3)]
                print("Decide who goes first.")
                player_choice = int(input("Enter (1) for Rock, (2) for Paper, and (3) for Scissors: "))
                if player_choice < 1 or player_choice > 3:
                    print("Please enter a valid choice.\n")
                else:
                    first_turn = self.compareFirstTurnChoices(Game.FIRST_TURN_CHOICES[player_choice], comp_choice)
                    if first_turn != "repeat":
                        if first_turn == "player":
                            self.player.is_playing_this_turn = True
                            self.current_turn_player = self.player
                        else:
                            self.ai.is_playing_this_turn = True
                            self.current_turn_player = self.ai
                        return
            except ValueError:
                print("Please enter a valid choice.\n")

    def endGame(self, mode, winner):
        self.game_over = True
        self.winner = winner.opponent

        if winner.opponent != self.player:
            print("You lose...")
            print("Reason: " + mode)
        else:
            print("You win!")
            print("Reason: " + mode)
        
    def battlePhase(self):
        pass

    def fieldActions(self):
        in_end_phase = False
        while not in_end_phase:
            available_monsters = [zone.cards_contained[0] for zone in self.current_turn_player.duelist_zone.getAttr("monster_card_zones") if zone.getNumOfCardsContained() == 1 and zone.cards_contained[0].has_attacked == False]
            available_spells_and_traps = [zone.cards_contained[0] for zone in self.current_turn_player.duelist_zone.getAttr("spell_and_trap_card_zones") if zone.getNumOfCardsContained() == 1 and zone.cards_contained[0].is_set == True and zone.cards_contained[0].card_type == "Spell"]
            if self.current_turn_player.duelist_zone.getAttr("field_card_zone").getNumOfCardsContained() == 1:
                field_card = self.current_turn_player.duelist_zone.getAttr("field_card_zone").cards_contained[0]
                if field_card.is_set:
                    available_spells_and_traps.append(field_card)
            
            available_cards = available_monsters + available_spells_and_traps
            
            if available_cards:
                if self.current_turn_player.hasMonstersAndActivatableCards():
                    self.current_turn_player.showCardsInField(available_cards)
                    in_end_phase = self.current_turn_player.chooseFieldAction(Game.current_turn, available_cards)
                    print(in_end_phase)
                    if in_end_phase == "Zero LP":

                        if self.player.getCurrentLifePointsAmount() == 0:
                            self.endGame("No life points left.", self.ai)
                        elif self.ai.getCurrentLifePointsAmount() == 0:
                            self.endGame("No life points left.", self.player)
                        break
                else:
                    in_end_phase = True
            else:
                in_end_phase = True
        self.endPhase()

    def endPhase(self, monsters_array):
        self.current_turn_player.has_played_a_card_this_turn = False
        """
        available_monsters = [zone.cards_contained[0] for zone in self.current_turn_player.duelist_zone.getAttr("monster_card_zones") if zone.getNumOfCardsContained() == 1]
        for monster in available_monsters:
            monster.has_attacked = False
            
        self.current_turn_player.switchTurnStatus()
        self.current_turn_player.opponent.switchTurnStatus()
        """
        for zone in monsters_array:
            if zone.card_img:
                zone.disabled_for_attacks = False
                zone.zone.getCardByIndex(0).has_attacked = False
        
        if self.current_turn_player == self.player:
            self.current_turn_player = self.ai
        else:
            self.current_turn_player = self.player
        Game.current_turn += 1  

    def gameLoop(self):
        #while not Game.game_over:
        
        field_card = None
        if self.current_turn_player.duelist_zone.getAttr("field_card_zone").getNumOfCardsContained() == 1:
            card = self.current_turn_player.duelist_zone.getAttr("field_card_zone").getCardByIndex(0)
            if not card.is_set:
                field_card = card
        if self.current_turn_player.opponent.duelist_zone.getAttr("field_card_zone").getNumOfCardsContained() == 1:
            card = self.current_turn_player.opponent.duelist_zone.getAttr("field_card_zone").getCardByIndex(0)
            if not card.is_set:
                field_card = card      
                
        #print("\n\nTurn " + str(Game.current_turn) + ", player: " + self.current_turn_player.name)
        draw_status = self.current_turn_player.draw_phase_draw()
        if field_card != None:
            field_card.effect()

        if draw_status != "You have no cards left to play.":
            #self.field.drawField()
            #self.current_turn_player.showCardsInHand()
            #self.current_turn_player.discard(choice)
            if not self.current_turn_player.has_played_a_card_this_turn:
                #self.current_turn_player.chooseCardToPlay()
                pass

            if self.current_turn_player.has_played_a_card_this_turn:
                self.fieldActions()
                #self.battlePhase()
            #self.endPhase()
            #Game.current_turn += 1               
        else:
            self.endGame("No cards left to draw.", self.current_turn_player.opponent)
       
            
#game_instance = Game()
