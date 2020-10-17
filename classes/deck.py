import random
from .db_connect import conn, c
from title_files.general_functions import buildDeck

class Deck(object):
    CARD_LIMIT = 40

    def __init__(self, deck_id, duelist, is_human):
        self.cards = []
        self.deck_id = deck_id
        self.build(duelist, is_human)
        
    def build(self, duelist, is_human):
        if is_human:
            c.execute("""
                SELECT
                    Cards.*,
                    Deck_Cards.Quantity
                FROM
                    Cards
                INNER JOIN
                    Deck_Cards
                ON
                    Cards.Card_ID = Deck_Cards.Card_ID
                WHERE Deck_Cards.Deck_ID = (?)
                ORDER BY
                    Cards.Card_ID DESC""", (self.deck_id,))          
        else:
            c.execute("""
                SELECT
                    Cards.*,
                    Opponent_Deck_Cards.Quantity
                FROM
                    Cards
                INNER JOIN
                    Opponent_Deck_Cards
                ON
                    Cards.Card_ID = Opponent_Deck_Cards.Card_ID
                WHERE Opponent_Deck_Cards.catlev_id = (?)
                ORDER BY
                    Cards.Card_ID DESC""", (self.deck_id,))   
        
        query_result = c.fetchall()
        self.cards = buildDeck(query_result, duelist)
        
        """
        for row in c.fetchall():
            for _ in range(row[15]):
                if row[2] == "Monster":
                    new_card = MonsterCard(row[0], row[1], row[3], row[4], duelist, row[5], row[6], row[7], row[8], row[12], row[13], row[9])
                elif row[2] == "Spell":
                    module_string_name = row[14]
                    moduleName = import_module("classes.effects.spells." + module_string_name)
                    className = getattr(moduleName, module_string_name)
                    new_card = className(row[0],
                                         row[1],
                                         row[3],                             
                                         row[4],
                                         duelist,
                                         row[10],
                                         )
                self.cards.append(new_card)
        """            
        #c.close()
        #conn.close()

    def getCards(self):
        return self.cards

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        try:
            card = self.cards.pop()
        except IndexError:
            return "You have no cards left to play."
        return card

"""
x = Deck(1)
for i in range(len(x.cards)):
    print(x.cards[i].name)

"""
