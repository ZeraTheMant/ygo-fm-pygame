from .zones import Zone, MultipleCardZone, DeckZone, GraveyardAndBanishedZone, MonsterZone, SpellAndTrapZone, FieldCardZone

class DuelistZone(object):
    def __init__(self, deck):
        self.deck_zone = DeckZone(deck)
        self.graveyard = GraveyardAndBanishedZone()
        self.banished_zone = GraveyardAndBanishedZone()
        self.field_card_zone = FieldCardZone()
        self.monster_card_zones = [MonsterZone() for _ in range(5)]
        self.spell_and_trap_card_zones = [SpellAndTrapZone() for _ in range(5)]

    def getAttr(self, attr_name):
        for attr, val in self.__dict__.items():
            if attr == attr_name:
                return val

class Field(object):
    def __init__(self, player, AI):
        self.player = player
        self.ai = AI

##        self.fillDeck(self.player)
##        self.fillDeck(self.ai)
##
##    def fillDeck(self, duelist):
##        for card in duelist.deck.getCards():
##            duelist.duelist_zone.deck_zone.placeCardToZone(card)

    def getLenStr(self, cards_contained):
        if cards_contained < 10:
            return str(cards_contained) + " " 
        else:
            return str(cards_contained)

    def drawField(self):
        PD = self.player.duelist_zone.deck_zone.getNumOfCardsContained()
        PG = self.player.duelist_zone.graveyard.getNumOfCardsContained()
        PB = self.player.duelist_zone.banished_zone.getNumOfCardsContained()
        PF = self.player.duelist_zone.field_card_zone.getAbbreviation()
        PMZ = self.player.duelist_zone.getAttr("monster_card_zones")
        PSZ = self.player.duelist_zone.getAttr("spell_and_trap_card_zones")
        PLP = self.player.getCurrentLifePointsAmount()

        CD = self.ai.duelist_zone.deck_zone.getNumOfCardsContained()
        CG = self.ai.duelist_zone.graveyard.getNumOfCardsContained()
        CB = self.ai.duelist_zone.banished_zone.getNumOfCardsContained()
        CF = self.ai.duelist_zone.field_card_zone.getAbbreviation()
        CMZ = self.ai.duelist_zone.getAttr("monster_card_zones")
        CSZ = self.ai.duelist_zone.getAttr("spell_and_trap_card_zones")
        CLP = self.ai.getCurrentLifePointsAmount()

        print("\n\nLife points")
        print(self.player.name + ": " + str(PLP))
        print(self.ai.name + ": " + str(CLP))
        print("\n\n\t DUEL!!! \n")
        
        print("*******************************")
        print("*    *    *    *    *    *    *")
        print("* " + self.getLenStr(CD) + " * " + CSZ[4].getAbbreviation() + " * " + CSZ[3].getAbbreviation() + " * " + CSZ[2].getAbbreviation() + " * " + CSZ[1].getAbbreviation() + " * " + CSZ[0].getAbbreviation() + " *")
        print("*    *    *    *    *    *    *")
        print("************************************")
        print("*    *    *    *    *    *    *    *")
        print("* " + self.getLenStr(CG) + " * " + CMZ[4].getAbbreviation() + " * " + CMZ[3].getAbbreviation() + " * " + CMZ[2].getAbbreviation() + " * " + CMZ[1].getAbbreviation() + " * " + CMZ[0].getAbbreviation() + " * " + CF + " *")
        print("*    *    *    *    *    *    *    *")
        print("************************************")
        print("*    *")
        print("* " + self.getLenStr(CB) +" *")
        print("*    *")
        print("******")
        print("                              ******")
        print("                              *    *")
        print("                              * " + self.getLenStr(PB) + " *")
        print("                              *    *")
        print("************************************")
        print("*    *    *    *    *    *    *    *")
        print("* " + PF + " * " + PMZ[0].getAbbreviation() + " * " + PMZ[1].getAbbreviation() + " * " + PMZ[2].getAbbreviation() + " * " + PMZ[3].getAbbreviation() + " * " + PMZ[4].getAbbreviation() + " * " + self.getLenStr(PG) + " *")
        print("*    *    *    *    *    *    *    *")
        print("************************************")
        print("     *    *    *    *    *    *    *")
        print("     * " + PSZ[0].getAbbreviation() + " * " + PSZ[1].getAbbreviation() + " * " + PSZ[2].getAbbreviation() + " * " + PSZ[3].getAbbreviation() + " * " + PSZ[4].getAbbreviation() + " * " + self.getLenStr(PD) + " *")
        print("     *    *    *    *    *    *    *")
        print("     *******************************")
