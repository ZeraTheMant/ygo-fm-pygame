from .deck import Deck
from .field import DuelistZone
from .card import FieldSpellCard
#from game import game_instance
import random, pygame

class Duelist(object):
    HAND_LIMIT = 5

    def __init__(self, deck_id, is_human, name, life_points, is_ai=False):
        self.name = name
        self.cards_in_hand = []
        self.cards_gui = []
        self.deck = Deck(deck_id, self, is_human)
        self.duelist_zone = DuelistZone(self.deck)
        self.life_points = life_points
        self.starting_life_points = life_points
        self.has_played_a_card_this_turn = False
        self.is_playing_this_turn = False
        self.opponent = None
        self.is_ai = is_ai
        self.is_attacking = False
        self.player_monster_zones_array = None
        self.player_spell_and_trap_zones_array = None
        self.attacking_monster = None

    def set_attacking_monster(self, val):
        self.attacking_monster = val

    def getCardsGUI(self):
        return self.cards_gui
        
    def getCardsInHand(self):
        return self.cards_in_hand
        
    def switchTurnStatus(self):
        self.is_playing_this_turn = not self.is_playing_this_turn
        
    def getCurrentLifePointsAmount(self):
        return self.life_points
        
    def changeLifePointsAmount(self, amount):
        self.life_points += amount
        if self.life_points <= 0:
            self.life_points = 0
            return True
        return False
        
    def setOpponent(self, opponent):
        self.opponent = opponent

    def discard(self, index):
        discarded_card = self.cards_in_hand.pop(index)
        discarded_card.sendToGrave(discarded_card.card_owner)

    def getLenOfCardsInHand(self):
        return len(self.cards_in_hand)

    def cancelFieldChoice(self, card_to_be_played, current_turn, cards_in_field):
        cards_in_field.append(card_to_be_played)
        self.chooseFieldAction(current_turn, cards_in_field)
               
    def chooseToAttack(self, attacking_card):
        available_monsters = [zone.cards_contained[0] for zone in self.opponent.duelist_zone.getAttr("monster_card_zones") if zone.getNumOfCardsContained() == 1]
        if len(available_monsters) > 0:
            self.showCardsInField(available_monsters, card=attacking_card)
            choice = int(input("Enter the index of the card to attack, to cancel, enter (999): "))
            if choice != 999:
                return attacking_card.attack(available_monsters[choice])

            else:
                return
        else:
            return attacking_card.attack(None)
               
    def chooseFieldAction(self, current_turn, cards_in_field):
        choice = int(input("Enter the index of the card to be played. To end the turn, enter (999): "))
        if choice == 999:
            return True
        else:
            card_to_be_played = cards_in_field.pop(choice)
            if card_to_be_played.card_type == "Spell":
                choice = int(input("Enter (1) to activate, (2) to cancel: "))
                if choice == 2:
                    self.cancelFieldChoice(card_to_be_played, current_turn, cards_in_field)
                else:
                    card_to_be_played.activate()
            else:
                if card_to_be_played.in_atk_position and current_turn != 1:
                    choice = int(input("Enter (1) to attack, (2) to change position, (3) to cancel: "))
                    if choice == 1:
                        return self.chooseToAttack(card_to_be_played)
                    elif choice == 2:
                        card_to_be_played.changePosition()
                    else:
                        self.cancelFieldChoice(card_to_be_played, current_turn, cards_in_field)
                else:
                    choice = int(input("Enter (1) to change position, (2) to cancel: "))
                    if choice == 1:
                        card_to_be_played.changePosition()
                    else:
                        self.cancelFieldChoice(card_to_be_played, current_turn, cards_in_field)
            return False

    def hasMonstersAndActivatableCards(self):
        field_card_zone = self.duelist_zone.getAttr("field_card_zone")
        if field_card_zone.getNumOfCardsContained() == 1:
            if field_card_zone.getCardByIndex(0).is_set:
                return True
        
        monster_zones = [zone for zone in self.duelist_zone.getAttr("monster_card_zones") if zone.getNumOfCardsContained() == 1]
        spell_and_trap_card_zones = [zone for zone in self.duelist_zone.getAttr("spell_and_trap_card_zones") if zone.getNumOfCardsContained() == 1 and zone.getCardByIndex(0).isActivationValid()]

        return len(monster_zones) > 0 or len(spell_and_trap_card_zones) > 0
            
    def chooseCardToPlay(self):
        if not self.has_played_a_card_this_turn:
            choice = int(input("Enter the index of the card to be played: "))
            card_to_be_played = self.cards_in_hand.pop(choice)
            if card_to_be_played.card_type == "Trap":
                choice = int(input("Enter (2) to set, enter (3) to cancel: "))
            elif card_to_be_played.card_type == "Spell":
                if card_to_be_played.isActivationValid():
                    choice = int(input("Enter (1) to activate, enter (2) to set, (3) to cancel: "))
                else:
                    choice = int(input("Enter (2) to set, enter (3) to cancel: "))
            else:
                choice = int(input("Enter (1) to summon, enter (2) to set, (3) to cancel: "))

            if choice == 3:
                self.cards_in_hand.append(card_to_be_played)
                self.showCards(self.cards_in_hand, "hand")
                self.chooseCardToPlay()
            else:
                self.playCard(card_to_be_played, choice)

    def showCardsInField(self, cards_list, card=None):
        self.showCards(cards_list, "field", card)
            
    def showCards(self, cards_list, mode, card=None):
        print()
        for x in range(len(cards_list)):
            if cards_list[x].card_type == "Monster":
                if mode == "hand":
                    additional_card_info = "Type: " + cards_list[x].monster_type + " ATTR: [" + cards_list[x].monster_attr + "] ATK: [" + str(cards_list[x].current_atk_points) + "] DEF: [" + str(cards_list[x].current_def_points) + "] LVL: [" + str(cards_list[x].level) + "] Guardian stars: [" + cards_list[x].guardian_star_list[0].getName() + ", " + cards_list[x].guardian_star_list[1].getName()  + "]"
                else:
                    if cards_list[x].in_atk_position:
                        position = "ATK"
                    else:
                        position = "DEF"
                        
                    if cards_list[x].card_owner == self.opponent:
                        gs_status_text = ""
                        if card:
                            gs_status_text = "No effect"
                            gs_status = card.checkGuardianStars(card, cards_list[x])
                            if gs_status == 1:
                                gs_status_text = "Weaker"
                            if gs_status == 2:
                                gs_status_text = "Stronger"
                        if not cards_list[x].is_set:              
                            additional_card_info = "Type: [" + cards_list[x].monster_type + "] ATTR: [" + cards_list[x].monster_attr + "] ATK: [" + str(cards_list[x].current_atk_points) + "] DEF: [" + str(cards_list[x].current_def_points) + "] LVL: [" + str(cards_list[x].level) + "] Guardian star: [" + cards_list[x].guardian_star.getName() + "] Position: [" + position + "] Guardian star status: [" + gs_status_text + "]"
                        else:
                            additional_card_info = "Type: [??] ATTR: [??] ATK: [??] DEF: [??] LVL: [??] Guardian star: [" + cards_list[x].guardian_star.getName() + "] Position: [" + position + "]"
                    else:
                        additional_card_info = "Type: " + cards_list[x].monster_type + " ATTR: [" + cards_list[x].monster_attr + "] ATK: [" + str(cards_list[x].current_atk_points) + "] DEF: [" + str(cards_list[x].current_def_points) + "] LVL: [" + str(cards_list[x].level) + "] Guardian star: [" + cards_list[x].guardian_star.getName() + "] Position: [" + position + "]"
            else:
                additional_card_info = "Type: [" + cards_list[x].spell_or_trap_type + "]"
                
            if cards_list[x].card_owner == self.opponent:
                if not cards_list[x].is_set: 
                    print("Index: " + str(x) + ". [" + cards_list[x].name + "] [" + cards_list[x].card_type + "] " + additional_card_info)
                else:
                    print("Index: " + str(x) + ". [??] [??] " + additional_card_info)
            else:
                print("Index: " + str(x) + ". [" + cards_list[x].name + "] [" + cards_list[x].card_type + "] " + additional_card_info)
            
    def showCardsInHand(self):
        self.showCards(self.cards_in_hand, "hand")

    def draw_phase_draw(self):
        if self.getLenOfCardsInHand() < Duelist.HAND_LIMIT:
            return self.generic_draw(Duelist.HAND_LIMIT-self.getLenOfCardsInHand())
        return None
        """
        elif self.getLenOfCardsInHand() > Duelist.HAND_LIMIT:
            indexes_of_cards_to_be_discarded = []
            current_hand = self.getLenOfCardsInHand()
            while current_hand > Duelist.HAND_LIMIT:
                print("You have " + str(current_hand) + " cards in hand currently. The limit is 5. Choose a card to discard.")
                choice = int(input("Enter card index: ")) 
                indexes_of_cards_to_be_discarded.append(self.cards_in_hand.index(choice))
                current_hand -= 1
            for index in indexes_of_cards_to_be_discarded:
                self.discard(index)
        """

    def generic_draw(self, num_of_cards_drawn):
        for _ in range(num_of_cards_drawn):
            drawn_card = self.deck.draw()
            if drawn_card != "You have no cards left to play.":
                self.cards_in_hand.append(drawn_card)
            else:
                break
        return drawn_card

    def addToHand(self, card):
        self.cards_in_hand.append(card)

    def playCard(self, card, mode):
        self.chooseZone(card)
        if mode == 2:
            card.set()
        else:
            if card.card_type == "Monster":
                card.normal_summon()
            else:
                card.activate()
        self.has_played_a_card_this_turn = True

    def chooseZone(self, card):
        #card.zone = field_card_zone
        if card.card_type == "Monster":
            monster_zones = self.duelist_zone.getAttr("monster_card_zones")
            print("Choose a monster zone.")
            ctr = 0
            for zone in monster_zones:
                print(ctr, zone)
                ctr += 1
            choice = int(input("Enter a monster zone: "))
            #card.zone = monster_zones[choice]
            monster_zones[choice].placeCardToZone(card)
        elif card.card_type == "Spell":
        
            if card.getSpellOrTrapType() == "Field":
                field_card_zone = self.duelist_zone.getAttr("field_card_zone")
                enemy_field_card_zone = self.opponent.duelist_zone.getAttr("field_card_zone")
                if enemy_field_card_zone.getNumOfCardsContained() > 0:
                    enemy_field_card = enemy_field_card_zone.getCardByIndex(0)
                    enemy_field_card_zone.removeCardFromZone(enemy_field_card, "To graveyard")
                field_card_zone.placeCardToZone(card)
            else:
                spell_zones = [zone for zone in self.duelist_zone.getAttr("spell_and_trap_card_zones") if zone.getNumOfCardsContained() == 0]
                print("Choose a spell zone.")
                ctr = 0
                for zone in spell_zones:
                    print(ctr, zone)
                    ctr += 1
                choice = int(input("Enter a spell zone: "))
                spell_zones[choice].placeCardToZone(card)
        #game_instance.field.drawField()
