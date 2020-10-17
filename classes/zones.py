from .card import Card, MonsterCard, SpellOrTrapCard, SpellCard, FieldSpellCard, TrapCard

class Zone(object):
    abbreviation = ""
    contains_multiple_cards = False
    accepts_spells_and_traps = True
    accepts_monsters = True
    accepts_field_cards = True

    def getAbbreviation(self):
        if self.getNumOfCardsContained() == 0:
            return self.abbreviation
        else:
            return self.__str__()
    
    def getCards(self):
        return self.cards_contained
    
    def __init__(self):
        self.cards_contained = []
        self.zone_gui = None

    def getLastCard(self):
        return self.cards_contained[-1]
        
    def getCardByIndex(self, index):
        return self.cards_contained[index]

    def getNumOfCardsContained(self):
        return len(self.cards_contained)

    def placedCardAction(self, card):
        self.cards_contained.append(card)
        return True
    
    def placeCardToZone(self, card):
        if not self.contains_multiple_cards:
            if self.getNumOfCardsContained() == 0:
                self.cards_contained.append(card)
                card.setZone(self)
                card.in_hand = False
                return True
            else:
                self.removeCardFromZone(self.cards_contained[0], "To graveyard")
                card.setZone(self)
                return self.placedCardAction(card)
        else:
            card.setZone(self)
            self.cards_contained.append(card)
            return True
            
    def removeCardFromZone(self, card, mode):
        if card in self.cards_contained:
            
            removed_card = self.cards_contained.pop(self.cards_contained.index(card))
            removed_card.removeFromPlace(mode)
            return True
        else:
            return False

    def activateSetSpellOrTrap(self):
        pass

    def __str__(self):
        if self.getNumOfCardsContained() == 0:
            return "[Empty Zone]"
        elif self.getNumOfCardsContained() == 1:
            if self.cards_contained[0].is_set:
                return "??"
            else:
                return self.cards_contained[0].name[:2]

class MultipleCardZone(Zone):
    contains_multiple_cards = True
    cards_face_down = True

    def getAbbreviation(self):
        return None

    def activateSetSpellOrTrap(self):
        return None

class DeckZone(MultipleCardZone):
    def __init__(self, deck):
        self.deck = deck
        self.deck.shuffle()
        self.cards_contained = deck.cards

    def placeCardToZone(self):
        return None

    def removeCardFromZone(self):
        return None

class GraveyardAndBanishedZone(MultipleCardZone):
    cards_face_down = False
    """
    def removeCardFromZone(self, card, mode):
        print('wew')
        if card in self.cards_contained:
            removed_card = self.cards_contained.pop(self.cards_contained.index(card))
            removed_card.removeFromPlace(mode)
            self.zone_gui.setZoneCardImg()
            return True
        else:
            return False
    """
class MonsterZone(Zone):
    abbreviation = "MZ"
    accepts_spells_and_traps = False
    accepts_field_cards = False

    def activateSetSpellOrTrap(self):
        return None

class SpellAndTrapZone(Zone):
    abbreviation = "ST"
    accepts_monsters = False
    accepts_field_cards = False

    def placedCardAction(self, card):
        return False

class FieldCardZone(Zone):
    abbreviation = "FZ"
    accepts_spells_and_traps = False
    accepts_monsters = False

    def activateSetSpellOrTrap(self):
        pass
        
"""
x = Zone()
print(x.cards_contained)
print()
x.removeCardFromZone(x.cards_contained[0], "To graveyard")
print(x.cards_contained)
"""
