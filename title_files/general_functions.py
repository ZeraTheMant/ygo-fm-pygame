import pygame, random, itertools
from .settings import Settings
from .card_image import CardImage
from classes.guardian_stars import Guardian_Stars_Container
from classes.card import *
from classes.db_connect import conn, c

from classes.card import Card, MonsterCard, SpellOrTrapCard, SpellCard, FieldSpellCard, TrapCard
from importlib import import_module

zha = pygame.Surface([129, 80])
wxx = pygame.Surface([129, 80])
zha_rect = zha.get_rect()

def getHighestValueOfCard(card):
    highest_val = card.atk_points
    if card.atk_points < card.def_points:
        highest_val = card.def_points
    return highest_val

def getAvgValueOfCard(card):
    card_highest_val = card.atk_points
    initial_avg = (card.atk_points + card.def_points) / 2
    
    if card_highest_val - initial_avg:
        initial_avg = card_highest_val
    
    return initial_avg
    
def getStrongerCard(card1, card2):
    card1_highest_val = getHighestValueOfCard(card1.card)
    card2_highest_val = getHighestValueOfCard(card2.card)
    
    if card1_highest_val > card2_highest_val:
        return card1
    elif card2_highest_val > card1_highest_val:
        return card2
    else:
        if card1.card.def_points > card2.card.def_points:
            return card1
        elif card1.card.def_points < card2.card.def_points:
            return card2
        else:
            return random.choice([card1, card2])
 
  
def fuseCards(card1, card2, current_turn_player, screen, func, flag):
    """
    if not flag:
        if card1.card.name == card2.card.name:
            card1 = fuseCards(card1, card1, current_turn_player, screen, func, True)
    """
    c.execute("""
        SELECT 
            Fusion_Classification_Names.FCN_ID 
        FROM 
            Fusion_Classification_Names 
        INNER JOIN 
            Card_Fusion_Classifications
        ON
            Card_Fusion_Classifications.FCN_ID = Fusion_Classification_Names.FCN_ID
        WHERE
            Card_Fusion_Classifications.Card_ID = (?)""", (card1.card.id,))
            
    card1_categories = c.fetchall()

    c.execute("""
        SELECT 
            Fusion_Classification_Names.FCN_ID 
        FROM 
            Fusion_Classification_Names 
        INNER JOIN 
            Card_Fusion_Classifications
        ON
            Card_Fusion_Classifications.FCN_ID = Fusion_Classification_Names.FCN_ID
        WHERE
            Card_Fusion_Classifications.Card_ID = (?)""", (card2.card.id,))
            
    card2_categories = c.fetchall()
    
    
    for card1_category in card1_categories:
        for card2_category in card2_categories:
            c.execute("""
                SELECT
                    FL_ID
                FROM 
                    Fusion_List
                WHERE
                    (FCN_ID1 = (?) AND FCN_ID2 = (?))
                OR
                    (FCN_ID1 = (?) AND FCN_ID2 = (?))""", (card1_category[0], card2_category[0], card2_category[0], card1_category[0],))
                
            fusion_list = c.fetchall()
            if len(fusion_list) > 0:
                fl_id = fusion_list[0][0]
                card1_highest_val = getAvgValueOfCard(card1.card)
                card2_highest_val = getAvgValueOfCard(card2.card)

                total_avg = (card1_highest_val + card2_highest_val) / 2

                c.execute("""
                    SELECT
                        CFT_ID
                    FROM
                        Card_Fusion_Thresholds
                    WHERE
                        (?) >= Min_Value
                    AND
                        (?) <= Max_Value""", (total_avg, total_avg,))
                
                result = c.fetchone()
                if result:
                    cft_id = result[0]
                    c.execute("""
                        SELECT
                            *
                        FROM
                            Fusion_Probabilities
                        WHERE
                            CFT_ID = (?)
                        AND
                            FL_ID = (?)
                        ORDER BY 
                            Probability ASC""", (cft_id, fl_id,))
                            
                    possible_cards = c.fetchall()
                    if len(possible_cards) > 0:
                        return func(possible_cards, card1, card2, current_turn_player, screen, flag)

    if flag:
        return getStrongerCard(card1, card2), False
    else:
        return None, False

def createFusedCard(possible_cards, card1, card2, current_turn_player, screen, flag):
    random_num = random.randint(1, 100)
    probability = 0
    for card in possible_cards:
        probability += card[4]
        if random_num <= probability:
            
            c.execute("""
                SELECT
                    Cards.*,
                    Fusion_Classification_Names.Name,
                    Card_Fusion_Classifications.Priority
                FROM
                    Cards
                INNER JOIN
                    Card_Fusion_Classifications
                ON
                    Card_Fusion_Classifications.Card_ID = Cards.Card_ID
                INNER JOIN
                    Fusion_Classification_Names
                ON
                    Fusion_Classification_Names.FCN_ID = Card_Fusion_Classifications.FCN_ID
                WHERE
                    Cards.Card_ID = (?)
                ORDER BY
                    Card_Fusion_Classifications.Priority ASC""", (card[3],))
            results = c.fetchall()
            result = results[0]
            fusion_list_array = []
            for x in range(len(results)):
                item = results[x][15]
                fusion_list_array.append(item)
            
            """
            if flag:
                if card1.card.name == card2.card.name:
                    if card1.card.name != result[1]:
                        new_card = MonsterCard(result[0], result[1], result[3], result[4], current_turn_player, result[5], result[6], result[7], result[8], result[12], result[13], result[9], fusion_list_array)
                        fused_card = CardImage(screen, new_card.card_type, new_card.img, 0, 0, new_card)
                        return fused_card, True
            """

            if card1.card.atk_points < result[7] and card2.card.atk_points < result[7] and card1.card.name != card2.card.name:  
                
                if result[2] == "Monster":
                    new_card = MonsterCard(result[0], result[1], result[3], result[4], current_turn_player, result[5], result[6], result[7], result[8], result[12], result[13], result[9], fusion_list_array)
                elif result[2] == "Spell":
                    module_string_name = result[14]
                    moduleName = import_module("classes.effects.spells." + module_string_name)
                    className = getattr(moduleName, module_string_name)
                    new_card = className(result[0],
                                         result[1],
                                         result[3],                             
                                         result[4],
                                         current_turn_player,
                                         result[10],
                                         fusion_list_array
                                         ) 

                fused_card = CardImage(screen, new_card.card_type, new_card.img, 0, 0, new_card)
                #fused_card.setRect(673.5, 137.5)
                return fused_card, True
    if flag:
        return getStrongerCard(card1, card2), False
    else:
        return None, False
    
def fuseCardsLoop(array, current_turn_player, screen, created_cards_array, flag):
    if len(array) == 0:
        return None, []
    elif len(array) == 1:
        return array[0], created_cards_array
    else:
        new_card, did_fuse = fuseCards(array[0], array[1], current_turn_player, screen, createFusedCard, flag)
        if not flag:
            if new_card:
                created_cards_array.append({"fused_card": new_card, "card1": array[0], "card2": array[1], "did_fuse": did_fuse})
            del array[0]
            del array[0]    
            if new_card:
                array.insert(0, new_card)
        else:
            created_cards_array.append({"fused_card": new_card, "card1": array[0], "card2": array[1], "did_fuse": did_fuse})
            del array[0]
            del array[0]    
            array.insert(0, new_card)
        return fuseCardsLoop(array, current_turn_player, screen, created_cards_array, flag)

def getFusionResultPrep(up_fusion_order_box_array, down_fusion_order_box_array, last_monster_fused, current_turn_player, screen, flag):    
    fused_up_array_result, fused_up_array = fuseCardsLoop(up_fusion_order_box_array, current_turn_player, screen, [], flag)

    fused_down_array_result, fused_down_array = fuseCardsLoop(down_fusion_order_box_array, current_turn_player, screen, [], flag)
    if not flag:
        if fused_up_array_result == None or fused_down_array_result == None:
            return None, None
            
    if fused_up_array_result and fused_down_array_result:
        sent_cards = [fused_up_array_result, fused_down_array_result]
    elif fused_up_array_result and fused_down_array_result == None:
        sent_cards = [fused_up_array_result]
    elif fused_up_array_result == None and fused_down_array_result:
        sent_cards = [fused_down_array_result]
            
    return fuseCardsLoop(sent_cards + last_monster_fused, current_turn_player, screen, fused_up_array + fused_down_array, flag)

    #return None, None
    
def chooseCardToFuse(option_text, selected_card, selected_card_option_box, fuse_up_ctr, fuse_down_ctr):
    x = fuse_up_ctr
    y = fuse_down_ctr
    selected_card_option_box.card = None
    selected_card_option_box.options = []
    selected_card.is_fusing = True
    if option_text == "Fuse Up":
        selected_card.rect.y = 510
        selected_card.is_fusing_up = True
        x += 1
    else:
        selected_card.rect.y = 570
        selected_card.is_fusing_down = True
        y += 1
    return x, y

def resetMisc(selected_field_card_option_box, selected_field_spell_trap_card_option_box, card_layout, card_info_panel):
    selected_field_card_option_box.card = None
    selected_field_spell_trap_card_option_box.card = None
    
    card_layout.reset()
    card_info_panel.setCardContent("", "", "", "", "", "", "", None, None, "")
    
def endPhaseBuildCardsInHand(game_instance, cards, ai_delay_start_timer, screen):
    cards_in_hand = game_instance.current_turn_player.getCardsInHand()
    
    if game_instance.current_turn_player == game_instance.player:
        cards = game_instance.player.cards_gui
    else:
        ai_delay_start_timer = pygame.time.get_ticks()   
        cards = game_instance.ai.cards_gui
    
    myctr = 0

    for card in cards_in_hand:

        if not card.bound_to_gui:
        
            if game_instance.current_turn_player == game_instance.player:
                card_in_hand_img = card.img
            else:
                card_in_hand_img = "images/cards/cover.jpg"
        
            card.bound_to_gui = True
            new_card = CardImage(screen, card.card_type, card_in_hand_img, 0, 0, card, card_index=myctr, in_hand=True)
            new_card.transformSize((149, 216), (2000, 540))
            cards.append(new_card)
        myctr += 1
    return cards
    
def resetFieldArrays(monster_zones, spell_and_trap_zones, graveyard_zone, deck_zone, field_zone, lp_font):
    for zone in monster_zones + spell_and_trap_zones:
        zone.flip()
        zone.set_current_position()
        if zone.card_img:
            zone.setZoneCardImg()
        if zone.zone.getNumOfCardsContained() == 1:
            zone.zone.getCardByIndex(0).just_placed_in_field = False
            
    graveyard_zone.flip()
    graveyard_zone.set_current_position()
    graveyard_zone.setZoneCardImg(lp_font)
    
    deck_zone.flip()
    deck_zone.set_current_position()
    deck_zone.setZoneCardImg(lp_font)
    
    field_zone.flip()
    field_zone.set_current_position()
    field_zone.setZoneCardImg()    
    
def changePhaseBlockStates(main_phase_block, battle_phase_block, end_phase_block):
    main_phase_block.is_active = True
    battle_phase_block.is_active = False
    end_phase_block.is_active = False
    battle_phase_block.changeColor()
    main_phase_block.changeColor()
    end_phase_block.changeColor()

def endPhaseSendArray(game_instance, player_monster_zones_array, ai_monster_zones_array):
    if game_instance.current_turn_player == game_instance.player:
        sent_array = player_monster_zones_array
    else:
        sent_array = ai_monster_zones_array
    
    game_instance.endPhase(sent_array)

def endPhaseCardsInHand(game_instance, cards, hand_cards_status):
    for i in range(len(cards)):
        cards[i].card_index = i
        hand_cards_status[i]["card"] = cards[i]
        cards[i].rect.left = hand_cards_status[i]["x_position"]
    
    game_instance.current_turn_player.cards_gui = cards

def areMonsterZonesEmpty(monster_zones):
    for zone in monster_zones:
        if zone.zone.getNumOfCardsContained() != 0:
            return False
    return True
   
def monsterZoneAvailable(monster_zones):
    for zone in monster_zones:
        if zone.zone.getNumOfCardsContained() == 0:
            return True
    return False
   
def getGameEnderMonster(game_instance):
    for card in game_instance.ai.cards_gui:
        if card.card.card_type == "Monster":
            if card.card.current_atk_points >= game_instance.player.life_points:
                card.card.guardian_star = random.choice(card.card.guardian_star_list)
                return card
    return None

def getGameEnterMonster2(game_instance, player_monster_zones_array):
    face_up_atk_pos_player_monsters = [zone.zone.getCardByIndex(0) for zone in player_monster_zones_array if zone.zone.getNumOfCardsContained() == 1 and zone.zone.getCardByIndex(0).card_type == "Monster" and zone.zone.getCardByIndex(0).is_set == False and zone.zone.getCardByIndex(0).in_atk_position]
    for card in game_instance.ai.cards_gui:
        for enemy_monster in face_up_atk_pos_player_monsters:
            if card.card.current_atk_points - enemy_monster.card.current_atk_points >= game_instance.player.life_points:
                card.card.guardian_star = random.choice(card.card.guardian_star_list)
                return card
    return None

def isHandReady(cards):
    for card in cards:
        if not card.contained or card.card_speed != 0:
            return False
    return True
    
def getHighestValueMonsterInHand(cards_in_hand, is_atk):
    highest_val_card = None
    highest_val = 0  
    for card in cards_in_hand:
        if card.card_type == "Monster":
            if is_atk:
                if card.card.current_atk_points >= highest_val:
                    highest_val_card = card
                    highest_val = card.card.current_atk_points
            else:
                if card.card.current_def_points >= highest_val:
                    highest_val_card = card
                    highest_val = card.card.current_def_points
    return highest_val_card
    
def getHighestValueMonsterInHand2(cards_in_hand):
    highest_val_card = None
    highest_val = 0  
    for card in cards_in_hand:
        if card.card_type == "Monster":
            if card.in_atk_position:
                if card.current_atk_points >= highest_val:
                    highest_val_card = card
                    highest_val = card.current_atk_points
            else:
                if card.current_def_points >= highest_val:
                    highest_val_card = card
                    highest_val = card.current_def_points
    return highest_val_card

def guardianStarComparison(mycard, highest_val_enemy_monster):
    if mycard.card.guardian_star_list[0].getStrongerAgainstId() == highest_val_enemy_monster.guardian_star.getId():
        mycard.card.guardian_star = Guardian_Stars_Container.returnGuardianStarById(mycard.card.guardian_star_list[0].gs_id)
        return mycard
    elif mycard.card.guardian_star_list[1].getStrongerAgainstId() == highest_val_enemy_monster.guardian_star.getId():
        mycard.card.guardian_star = Guardian_Stars_Container.returnGuardianStarById(mycard.card.guardian_star_list[1].gs_id)
        return mycard
    elif mycard.card.guardian_star_list[0].getWeakerAgainstId() != highest_val_enemy_monster.guardian_star.getId():
        mycard.card.guardian_star = Guardian_Stars_Container.returnGuardianStarById(mycard.card.guardian_star_list[0].gs_id)
        return mycard
    elif mycard.card.guardian_star_list[1].getWeakerAgainstId() != highest_val_enemy_monster.guardian_star.getId():
        mycard.card.guardian_star = Guardian_Stars_Container.returnGuardianStarById(mycard.card.guardian_star_list[1].gs_id)
        return mycard

def returnBestGuardianStar(gs_list, enemy_monsters):
    first_gs_strong_ctr = 0
    second_gs_strong_ctr = 0
    
    for monster in enemy_monsters:
        if gs_list[0].getId() == monster.zone.getCardByIndex(0).guardian_star.getStrongerAgainstId():
            first_gs_strong_ctr += 1
        if gs_list[1].getId() == monster.zone.getCardByIndex(0).guardian_star.getStrongerAgainstId():
            second_gs_strong_ctr += 1  
        """
        if gs_list[0].getId() == monster.zone.getCardByIndex(0).guardian_star.getWeakerAgainstId():
            first_gs_strong_ctr -= 1  
        if gs_list[1].getId() == monster.zone.getCardByIndex(0).guardian_star.getWeakerAgainstId():
            second_gs_strong_ctr -= 1              
        """

        
    if first_gs_strong_ctr > second_gs_strong_ctr:
        return gs_list[1]
    elif second_gs_strong_ctr > first_gs_strong_ctr:
        return gs_list[0]
    else:
        return random.choice(gs_list)
   
def getMostViableMonsterInHand(ai_cards_in_hand, player_monster_zones_array, pma_copy):

    #all_enemy_monsters = [zone.zone.getCardByIndex(0) for zone in player_monster_zones_array if zone.zone.getNumOfCardsContained() == 1 and zone.zone.getCardByIndex(0).card_type == "Monster"]
    face_up_player_monsters = [zone.zone.getCardByIndex(0) for zone in player_monster_zones_array if zone.zone.getNumOfCardsContained() == 1 and zone.zone.getCardByIndex(0).card_type == "Monster" and zone.zone.getCardByIndex(0).is_set == False]

    if len(face_up_player_monsters) == 0:

        for card in player_monster_zones_array:
            for mycard in ai_cards_in_hand:
                if mycard.card_type == "Monster":
                    if mycard.card.guardian_star_list[0].getStrongerAgainstId() == card.zone.getCardByIndex(0).guardian_star.getId():
                        mycard.card.guardian_star = Guardian_Stars_Container.returnGuardianStarById(mycard.card.guardian_star_list[0].getId())
                        return mycard
                    elif mycard.card.guardian_star_list[1].getStrongerAgainstId() == card.zone.getCardByIndex(0).guardian_star.getId():       
                        mycard.card.guardian_star = Guardian_Stars_Container.returnGuardianStarById(mycard.card.guardian_star_list[1].getId())
                        return mycard  

        
        if len(player_monster_zones_array) > 0:
            highest_atk_monster_in_hand = getHighestValueMonsterInHand(ai_cards_in_hand, True)
            highest_def_monster_in_hand = getHighestValueMonsterInHand(ai_cards_in_hand, False)
            if highest_atk_monster_in_hand.card.current_atk_points > highest_def_monster_in_hand.card.current_def_points:
                highest_atk_monster_in_hand.card.guardian_star = returnBestGuardianStar(highest_atk_monster_in_hand.card.guardian_star_list, pma_copy)
                return highest_atk_monster_in_hand
            elif highest_atk_monster_in_hand.card.current_atk_points < highest_def_monster_in_hand.card.current_def_points:                  
                highest_def_monster_in_hand.card.guardian_star = returnBestGuardianStar(highest_def_monster_in_hand.card.guardian_star_list, pma_copy)
                return highest_def_monster_in_hand
            else:
                highest_atk_monster_in_hand.card.guardian_star = returnBestGuardianStar(highest_atk_monster_in_hand.card.guardian_star_list, pma_copy)
                return highest_atk_monster_in_hand
        else:
            ai_random_card = random.choice(ai_cards_in_hand)
            ai_random_card.card.guardian_star = random.choice(ai_random_card.card.guardian_star_list)

            ai_random_card.card.is_set = True
            return ai_random_card
    else:

        #highest_atk_monster_in_hand = getHighestValueMonsterInHand(ai_cards_in_hand, True)
        highest_val_enemy_monster = getHighestValueMonsterInHand2(face_up_player_monsters)
        if highest_val_enemy_monster.in_atk_position:
            value = highest_val_enemy_monster.current_atk_points
        else:
            value = highest_val_enemy_monster.current_def_points
        
        for mycard in ai_cards_in_hand:
            if mycard.card_type == "Monster":
                if mycard.card.current_atk_points > value:
                    return guardianStarComparison(mycard, highest_val_enemy_monster)
                else:
                    if mycard.card.guardian_star_list[0].getStrongerAgainstId() == highest_val_enemy_monster.guardian_star.getId():
                        if mycard.card.current_atk_points + 500 > highest_val_enemy_monster.current_atk_points:
                            mycard.card.guardian_star = Guardian_Stars_Container.returnGuardianStarById(mycard.card.guardian_star_list[0].gs_id)
                            return mycard
                    elif mycard.card.guardian_star_list[1].getStrongerAgainstId() == highest_val_enemy_monster.guardian_star.getId():
                        if mycard.card.current_atk_points + 500 > highest_val_enemy_monster.current_atk_points:
                            mycard.card.guardian_star = Guardian_Stars_Container.returnGuardianStarById(mycard.card.guardian_star_list[1].gs_id)
                            return mycard 

        for card in player_monster_zones_array:
            if card.zone.getCardByIndex(0) == highest_val_enemy_monster:
                player_monster_zones_array.remove(card)
        return getMostViableMonsterInHand(ai_cards_in_hand, player_monster_zones_array, pma_copy)

def hasFieldCardInHand(my_cards_in_hand):
    for card in my_cards_in_hand:
        if card.card.card_type == "Spell":
            if card.card.spell_or_trap_type == "Field":
                return True
    return False
    
def hasSpellOrTrapCardInHand(my_cards_in_hand):
    for card in my_cards_in_hand:
        if card.card.card_type == "Spell" or card.card.card_type == "Trap":
            if card.card.spell_or_trap_type != "Field":
                return True
    return False

def getFieldCardInHand(my_cards_in_hand):
    for card in my_cards_in_hand:
        if card.card.card_type == "Spell":
            if card.card.spell_or_trap_type == "Field":
                return card
    return None

def willAISurviveTurn(player_monster_zones_array, ai_life_points):
    total_enemy_atk_points = 0
    
    for zone in player_monster_zones_array:
        if zone.zone.getNumOfCardsContained() == 1:
            monster = zone.zone.getCardByIndex(0)
            if not monster.is_set:
                total_enemy_atk_points += monster.current_atk_points
    
    return total_enemy_atk_points < ai_life_points

def aiChooseSpellOrTrapCard(game_instance):
    spell_or_trap_cards_in_hand = [card_gui for card_gui in game_instance.ai.cards_gui if card_gui.card.card_type == "Spell" or card_gui.card.card_type == "Trap" and card_gui.card.spell_or_trap_type != "Field"]
    
    if willAISurviveTurn(game_instance.player.player_monster_zones_array, game_instance.ai.life_points):   
        for card in spell_or_trap_cards_in_hand:
            if card.card.card_type == "Spell":
                if card.card.spell_or_trap_type != "Equip":
                    if card.card.aiUseCondition(game_instance):
                        card.card.set_for_ai = False
                        return card
                else:
                    card.card.set_for_ai = True
                    card.card.is_set = True
                    return card

        spell_or_trap_cards_in_hand[0].card.is_set = True
        return spell_or_trap_cards_in_hand[0]    

    return None
 
def getLoopRange(outer_loop):
    if outer_loop == 4:
        return 6
    elif outer_loop == 3:
        return 3
    else:
        return 1

def getDownFusionBoxArrayAndIndices(permutations_array, outer_loop, ctr, ai_cards, indices): 

    if outer_loop == 4:
        indices.append(permutations_array[ctr][0])
        indices.append(permutations_array[ctr][1])
        return [ai_cards[permutations_array[ctr][0]], ai_cards[permutations_array[ctr][1]]], indices
    elif outer_loop == 3:
        indices.append(permutations_array[0])
        return [ai_cards[permutations_array[0]]], indices
    else:
        return [], indices
        
def getPermutationsArray(x, y, outer_loop):
    indexes = [0, 1, 2, 3, 4]
    permutations_array = []
    
    if outer_loop == 4:
        indexes.remove(x)
        indexes.remove(y)
        permutations_array = list(itertools.permutations(indexes))
    else:   
        for i in range(getLoopRange(outer_loop)):
            if indexes[i] != x and indexes[i] != y:
                permutations_array.append(indexes[i])

    return permutations_array
        
def selectedFusionIndices(possible_cards_container):
    strongest_atk = 0
    strongest_card = None
    strongest_card_indices = None
    strongest_card_img = None
    for i in range(len(possible_cards_container)):
        card = possible_cards_container[i]["card"].card
        if card.atk_points > strongest_atk:
            strongest_atk = card.atk_points
            strongest_card = card

            strongest_card_img = possible_cards_container[i]["card"]
            strongest_card_indices = possible_cards_container[i]["indices"]
    return strongest_card_indices, strongest_card_img
        
def getFusionIndices(ai_cards, current_turn_player, screen):
    for outer_loop in range(4, 1, -1):
        possible_cards_container = []

        for x in range(len(ai_cards)):
            card_1 = ai_cards[x]
            for y in range(1, len(ai_cards)):
                card_2 = ai_cards[y-1]
                if card_2 == card_1:
                    continue
                else:      
                    permutations_array = getPermutationsArray(x, y-1, outer_loop)

                    for inner_loop in range(getLoopRange(outer_loop)):
                        down_fusion_order_box_array, indices = getDownFusionBoxArrayAndIndices(permutations_array, outer_loop, inner_loop, ai_cards, [x, y-1])
                        
                        upper_array = [card_1, card_2]
                        
                        if outer_loop == 2:
                            upper_array = [card_1]
                            down_fusion_order_box_array = [card_2]
                        
                        fused_card, created_cards_array = getFusionResultPrep(upper_array, down_fusion_order_box_array, [], current_turn_player, screen, False)      

                        if fused_card:

                            possible_cards_container.append({
                                "card": fused_card,
                                "indices": indices 
                            })

        if len(possible_cards_container) > 0:

            return selectedFusionIndices(possible_cards_container)

    return None, None            
    
def getAICardToPlay(game_instance, ai_field_gui, player_monster_zones_array, ai_monster_zones_array, screen):
    if areMonsterZonesEmpty(player_monster_zones_array):
        
        played_spell_or_trap_card = None
        if hasSpellOrTrapCardInHand(game_instance.ai.cards_gui):
            played_spell_or_trap_card = aiChooseSpellOrTrapCard(game_instance)
        
        if played_spell_or_trap_card:
            #if played_spell_or_trap_card.aiUseCondition(game_instance):
            return played_spell_or_trap_card, None
        
        if monsterZoneAvailable(ai_monster_zones_array):
            game_ender_monster = getGameEnderMonster(game_instance)
            if game_ender_monster != None:
                return game_ender_monster, None
            else:
                fusion_indices, provisional_fused_card = getFusionIndices(game_instance.ai.cards_gui, game_instance.current_turn_player, screen)          
                
                if fusion_indices:             
                    return fusion_indices, provisional_fused_card
                else:
                    highest_val_card = getHighestValueMonsterInHand(game_instance.ai.cards_gui, True)
                    if highest_val_card:
                        highest_val_card.card.guardian_star = returnBestGuardianStar(highest_val_card.card.guardian_star_list, [])
                        return highest_val_card, None
                    else:
                        spell_or_trap_card = random.choice(game_instance.ai.cards_gui)
                        spell_or_trap_card.card.is_set = True
                        return spell_or_trap_card, None
    else:
        #if monsterZoneAvailable(ai_monster_zones_array):
        played_spell_or_trap_card = None
        game_ender_monster = getGameEnderMonster(game_instance)
        if game_ender_monster != None:
            return game_ender_monster, None
        else:
            if hasFieldCardInHand(game_instance.ai.cards_gui):
                ai_field_zone = game_instance.ai.duelist_zone.getAttr("field_card_zone")
                if ai_field_zone.getNumOfCardsContained() == 0:
                    if willAISurviveTurn(player_monster_zones_array, game_instance.ai.life_points):
                        return getFieldCardInHand(game_instance.ai.cards_gui), None
               
            if hasSpellOrTrapCardInHand(game_instance.ai.cards_gui):
                played_spell_or_trap_card = aiChooseSpellOrTrapCard(game_instance)
            
            if played_spell_or_trap_card:
                return played_spell_or_trap_card, None
            else:

                fusion_indices, provisional_fused_card = getFusionIndices(game_instance.ai.cards_gui, game_instance.current_turn_player, screen)    
                if fusion_indices:
                    return fusion_indices, provisional_fused_card
                else:
                    has_monster = False
                    for card in game_instance.ai.cards_gui:
                        if card.card.card_type == "Monster":
                            has_monster = True
                            break
                        
                    if not has_monster:
                        random_card = random.choice(game_instance.ai.cards_gui)
                        random_card.card.is_set = True
                        return random_card, None
                    else:
                        all_enemy_monsters = [zone for zone in player_monster_zones_array if zone.zone.getNumOfCardsContained() == 1 and zone.zone.getCardByIndex(0).card_type == "Monster"]                    
                        return getMostViableMonsterInHand(game_instance.ai.cards_gui, all_enemy_monsters, all_enemy_monsters.copy()), None
        #else:        
        
def monsterIsWeakerThanEveryMonster(monster, player_monster_zones_array):
    ctr = 0
    for zone in player_monster_zones_array:
        if zone.zone.getNumOfCardsContained() == 1:
            looped_monster = zone.zone.getCardByIndex(0)
            if not looped_monster.is_set:
                if looped_monster.in_atk_position:
                    compared_value = looped_monster.current_atk_points
                else:
                    compared_value = looped_monster.current_def_points
                if looped_monster.guardian_star.getId() == monster.guardian_star.getStrongerAgainstId():
                    if monster.current_atk_points + 500 > compared_value:
                        return False
                if looped_monster.guardian_star.getId() == monster.guardian_star.getWeakerAgainstId():
                    if monster.current_atk_points > compared_value + 500:
                        return False
                if monster.current_atk_points > compared_value:
                    return False
            else:
                ctr += 1
            
    if ctr > 0:
        return False
    else:
        return True

def getTargetMonster(monster, player_zones):
    target_monster = None
    strongest_enemy_value = 0
    for monster_zone in player_zones:
        if monster_zone.zone.getNumOfCardsContained() == 1:
            gs_bonus = 0
            looped_monster = monster_zone.zone.getCardByIndex(0)
            if not looped_monster.is_set:            
                if looped_monster.guardian_star.getId() == monster.guardian_star.getStrongerAgainstId():
                    gs_bonus = 500
                if looped_monster.guardian_star.getId() == monster.guardian_star.getWeakerAgainstId():
                    gs_bonus = -500
                    
                if looped_monster.in_atk_position:
                    current_val = looped_monster.current_atk_points
                else:
                    current_val = looped_monster.current_def_points
        
                if monster.current_atk_points + gs_bonus > current_val:
                    if strongest_enemy_value < current_val:
                        strongest_enemy_value = current_val
                        target_monster = monster_zone

    neutral_set_enemy_monsters = []
    unfavorable_set_enemy_monsters = []
    if target_monster == None:
        for monster_zone in player_zones:
            if monster_zone.zone.getNumOfCardsContained() == 1:
                looped_monster = monster_zone.zone.getCardByIndex(0)
                if looped_monster.is_set:   
                    if looped_monster.guardian_star.getId() == monster.guardian_star.getStrongerAgainstId():
                        return monster_zone
                    if looped_monster.guardian_star.getId() == monster.guardian_star.getWeakerAgainstId():
                        unfavorable_set_enemy_monsters.append(monster_zone)
                        continue
                    neutral_set_enemy_monsters.append(monster_zone)

        if len(neutral_set_enemy_monsters) == 0:
            if isEnemyMonsterZoneEmpty(player_zones):
                return None
            else:
                return random.choice(unfavorable_set_enemy_monsters)
        else:
            return random.choice(neutral_set_enemy_monsters)
            
    return target_monster

def guiAction(is_direct_attack, monster, player_monster_zones_array, screen, ai_monster_zones_array, my_index, card_layout, card_surface, card_desc_surface, player_spell_and_trap_zones_array, ai_spell_and_trap_zones_array, zone_lines_tuple, player_graveyard_gui, ai_graveyard_gui, card_info_panel, phealth, xhealth, card_name_font, lp_font, player_name, ai_name, current_turn_box_dimensions, current_turn_box_dimensions2, game_instance, ai_field_gui, player_field_gui, egyptian_background, ai_deck_gui, player_deck_gui, main_phase_block, battle_phase_block, end_phase_block, q, turn_text_width, turn_text, zone_index, active_field_card_img, active_field_card_display):
    clock = pygame.time.Clock()
    atk_def_font = pygame.font.SysFont("Trebuchet MS", 20)  
    my_monster = monster.zone.getCardByIndex(0)
    ai_monster_zones_ok = [False for x in range(5)]
    target_monster = getTargetMonster(my_monster, player_monster_zones_array)
    if target_monster != None:
        if not my_monster.in_atk_position:
            my_monster.in_atk_position = not my_monster.in_atk_position
            monster.setZoneCardImg()  

    if not is_direct_attack:
        for zone in player_monster_zones_array:
            if zone.zone.getNumOfCardsContained() == 1:
                zone.area.fill((0, 255, 0, 70)) 
        
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit() 
                
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(egyptian_background, [248, 0])
        v = pygame.time.get_ticks()

        if active_field_card_display:
            screen.blit(active_field_card_img, [474.5, 74.5])
        
        card_surface.blit()
        card_desc_surface.blit()
        
        for zone in player_monster_zones_array:
            zone.blit(atk_def_font)
            changeDisplayCard2(zone, card_layout, card_info_panel, mouse_pos, game_instance)   
            
        for zone in player_spell_and_trap_zones_array:
            zone.blit()
            changeDisplayCard2(zone, card_layout, card_info_panel, mouse_pos, game_instance)   
    
        for zone in ai_spell_and_trap_zones_array:
            zone.blit()
            changeDisplayCard2(zone, card_layout, card_info_panel, mouse_pos, game_instance)   
    
        for zone in ai_monster_zones_array:
            zone.blit(atk_def_font)
            changeDisplayCard2(zone, card_layout, card_info_panel, mouse_pos, game_instance)   
            
        graveyardDisplay(player_graveyard_gui, card_layout, card_info_panel, mouse_pos)   
        graveyardDisplay(ai_graveyard_gui, card_layout, card_info_panel, mouse_pos)   
        graveyardDisplay(player_field_gui, card_layout, card_info_panel, mouse_pos)   
        graveyardDisplay(ai_field_gui, card_layout, card_info_panel, mouse_pos)  

        player_graveyard_gui.blit()       
        player_deck_gui.blit()
        player_field_gui.blit()

        
        ai_graveyard_gui.blit()
        ai_deck_gui.blit()  
        ai_field_gui.blit() 
   
        main_phase_block.blit()
        battle_phase_block.blit()
        end_phase_block.blit()

        drawBoard(screen, zone_lines_tuple)   
        screen.blit(turn_text, [797.5-(turn_text_width/2), 17])
        pygame.draw.rect(screen, Settings.RED, [ai_monster_zones_array[zone_index].rect.x, ai_monster_zones_array[zone_index].rect.y, 129.2, 111.75], 5)  
        z = pygame.time.get_ticks() 
        
        if not is_direct_attack:
            if z - q >= 400 and z - q < 800:#540
                pygame.draw.rect(screen, Settings.RED, [player_monster_zones_array[4].rect.x, player_monster_zones_array[4].rect.y, 129.2, 111.75], 5)     
            elif z - q >= 800 and z - q < 1200:
                pygame.draw.rect(screen, Settings.RED, [player_monster_zones_array[3].rect.x, player_monster_zones_array[3].rect.y, 129.2, 111.75], 5)   
            elif z - q >= 1200 and z - q < 1600:
                pygame.draw.rect(screen, Settings.RED, [player_monster_zones_array[2].rect.x, player_monster_zones_array[2].rect.y, 129.2, 111.75], 5)   
            elif z - q >= 1600 and z - q < 2000:
                pygame.draw.rect(screen, Settings.RED, [player_monster_zones_array[1].rect.x, player_monster_zones_array[1].rect.y, 129.2, 111.75], 5)   
            elif z - q >= 2000 and z - q < 2400:
                pygame.draw.rect(screen, Settings.RED, [player_monster_zones_array[0].rect.x, player_monster_zones_array[0].rect.y, 129.2, 111.75], 5)   
            elif z - q >= 2400 and z - q < 2800:
                if target_monster:
                    pygame.draw.rect(screen, Settings.RED, [player_monster_zones_array[target_monster.index].rect.x, player_monster_zones_array[target_monster.index].rect.y, 129.2, 111.75], 5)   
            elif z - q >= 2800 and z - q < 3200:
                break
        else:
            if z - q >= 300:
                break
        
        pygame.draw.rect(screen, Settings.RED, current_turn_box_dimensions, 1)
        pygame.draw.rect(screen, Settings.RED, current_turn_box_dimensions2, 1)
        drawHealthBars(phealth, xhealth, screen, card_name_font, lp_font, player_name, ai_name)            
        card_info_panel.blit(card_name_font, card_layout.card_type)
         
        if card_layout.card_type == "Monster":
            if card_layout.card.current_zone == None:
                if card_layout.card.in_hand:
                    card_layout.blit(card_layout.card.current_atk_points, card_layout.card.current_def_points, Settings.BLACK)
                else:
                    card_layout.blit(card_layout.card.atk_points, card_layout.card.def_points, Settings.BLACK)
            else:
                card_layout.blit(card_layout.card.current_atk_points, card_layout.card.current_def_points, Settings.BLACK)
        else:
            card_layout.blit()
            
        pygame.display.flip()
        clock.tick(60)
    
    for zone in player_monster_zones_array:
        zone.area.fill((0, 0, 0, 0)) 
        pygame.display.flip()
        clock.tick(60)
    
    if not is_direct_attack:
        return target_monster
    else:
        return "Direct attack"
    
def monsterAction(monster, player_monster_zones_array, screen, ai_monster_zones_array, my_index, card_layout, card_surface, card_desc_surface, player_spell_and_trap_zones_array, ai_spell_and_trap_zones_array, zone_lines_tuple, player_graveyard_gui, ai_graveyard_gui, card_info_panel, phealth, xhealth, card_name_font, lp_font, player_name, ai_name, current_turn_box_dimensions, current_turn_box_dimensions2, game_instance, ai_field_gui, player_field_gui, egyptian_background, ai_deck_gui, player_deck_gui, main_phase_block, battle_phase_block, end_phase_block, q, turn_text_width, turn_text, zone_index, active_field_card_img, active_field_card_display):
    monster.disabled_for_ai = True
    
    if game_instance.current_turn == 1:
        return None
    
    q = pygame.time.get_ticks()
    v = pygame.time.get_ticks()  
    my_monster = monster.zone.getCardByIndex(0)
    
    if isEnemyMonsterZoneEmpty(player_monster_zones_array):
        if not my_monster.in_atk_position:
            my_monster.in_atk_position = not my_monster.in_atk_position
            monster.setZoneCardImg()
        return guiAction(True, monster, player_monster_zones_array, screen, ai_monster_zones_array, my_index, card_layout, card_surface, card_desc_surface, player_spell_and_trap_zones_array, ai_spell_and_trap_zones_array, zone_lines_tuple, player_graveyard_gui, ai_graveyard_gui, card_info_panel, phealth, xhealth, card_name_font, lp_font, player_name, ai_name, current_turn_box_dimensions, current_turn_box_dimensions2, game_instance, ai_field_gui, player_field_gui, egyptian_background, ai_deck_gui, player_deck_gui, main_phase_block, battle_phase_block, end_phase_block, q, turn_text_width, turn_text, zone_index, active_field_card_img, active_field_card_display)
    else:   
        if monsterIsWeakerThanEveryMonster(my_monster, player_monster_zones_array):
            if my_monster.in_atk_position:
                my_monster.in_atk_position = not my_monster.in_atk_position
                monster.setZoneCardImg()
            my_monster.has_attacked = True
            return None
        else:
            return guiAction(False, monster, player_monster_zones_array, screen, ai_monster_zones_array, my_index, card_layout, card_surface, card_desc_surface, player_spell_and_trap_zones_array, ai_spell_and_trap_zones_array, zone_lines_tuple, player_graveyard_gui, ai_graveyard_gui, card_info_panel, phealth, xhealth, card_name_font, lp_font, player_name, ai_name, current_turn_box_dimensions, current_turn_box_dimensions2, game_instance, ai_field_gui, player_field_gui, egyptian_background, ai_deck_gui, player_deck_gui, main_phase_block, battle_phase_block, end_phase_block, q, turn_text_width, turn_text, zone_index, active_field_card_img, active_field_card_display)

def getFieldCardImg(field_card_id):
    c.execute("""
        SELECT
            img
        FROM
            Field_Images
        WHERE field_card_id = (?)""", (field_card_id,))
    rows = c.fetchall()
    if len(rows) == 0:
        return None
    else:
        return rows[0][0]

def checkIfTrue(mouse_pos, zone, zha_rect, card, game_instance):
    if card == None:
        return zone.rect.collidepoint(mouse_pos)
    else:
        if card.zone.getNumOfCardsContained() > 0:
            if card.zone.getCardByIndex(0).card_owner == game_instance.current_turn_player.opponent:
                return zone.rect.collidepoint(mouse_pos)
            else:
                return zha_rect.collidepoint(mouse_pos)
        else:
            return False

def graveyardDisplay(zone, card_layout, card_info_panel, mouse_pos):
    if zone.rect.collidepoint(mouse_pos):
        if zone.zone.getNumOfCardsContained() > 0:
            zone_card = zone.zone.getCardByIndex(-1)          

            card_layout.card = zone_card
            card_layout.card_type = zone_card.card_type

            card_layout.changeImg(zone_card.img)
            card_name = zone_card.name
            card_desc = zone_card.text
            
            if zone_card.card_type == "Monster":          
                card_type_info = "[Monster] " + zone_card.monster_type + "/" + zone_card.monster_attr 
                monst_lvl_and_atk = "[" + u"\u2605" + str(zone_card.level) + "]  " + str(zone_card.atk_points) + "/" + str(zone_card.def_points)
                gs_text = "Guardian Stars:" 
                gs1_img = getGuardianStarImg(zone_card.guardian_star_list[0].name)
                gs2_img = getGuardianStarImg(zone_card.guardian_star_list[1].name)
                gs1_text = zone_card.guardian_star_list[0].name
                gs2_text = zone_card.guardian_star_list[1].name
                    

                                
                card_info_panel.setCardContent(card_name, gs_text, gs1_text, gs2_text, card_type_info, monst_lvl_and_atk, card_desc, gs1_img, gs2_img, zone_card.fusion_types_string)
            else:
                card_type_info = "[" + zone_card.card_type + "] " + zone_card.spell_or_trap_type
                monst_lvl_and_atk = ""
                gs_text = ""
                card_info_panel.setCardContent(card_name, "", "", "", card_type_info, "", card_desc, None, None, zone_card.fusion_types_string)

def changeDisplayCard2(zone, card_layout, card_info_panel, mouse_pos, game_instance):

    if zone.rect.collidepoint(mouse_pos):
        if zone.zone.getNumOfCardsContained() > 0:
            zone_card = zone.zone.getCardByIndex(0)          

            card_layout.card = zone_card
            card_layout.card_type = zone_card.card_type

            card_layout.changeImg(zone_card.img)
            card_name = zone_card.name
            card_desc = zone_card.text
            
            if zone_card.card_type == "Monster":          
                card_type_info = "[Monster] " + zone_card.monster_type + "/" + zone_card.monster_attr 
                monst_lvl_and_atk = "[" + u"\u2605" + str(zone_card.level) + "]  " + str(zone_card.atk_points) + "/" + str(zone_card.def_points)
                gs_text = "Guardian Stars:" 
                gs1_img = getGuardianStarImg(zone_card.guardian_star_list[0].name)
                gs2_img = getGuardianStarImg(zone_card.guardian_star_list[1].name)
                gs1_text = zone_card.guardian_star_list[0].name
                gs2_text = zone_card.guardian_star_list[1].name
                    
                selected_gs = zone_card.guardian_star.name
                
                color = Settings.YELLOW
                if game_instance.current_turn_player.is_attacking:
                    if zone_card.card_owner == game_instance.current_turn_player.opponent:
                        if attacking_card.guardian_star.gs_id == zone_card.guardian_star.strong_against_id:
                            color = Settings.RED
                        elif attacking_card.guardian_star.gs_id == zone_card.guardian_star.weak_against_id:
                            color = Settings.GREEN
                              
                if gs1_text == selected_gs:
                    pygame.draw.rect(card_info_panel.screen, color, [125, 445, 100, 50])
                else:
                    pygame.draw.rect(card_info_panel.screen, color, [215, 445, 100, 50])
                    
                card_info_panel.setCardContent(card_name, gs_text, gs1_text, gs2_text, card_type_info, monst_lvl_and_atk, card_desc, gs1_img, gs2_img, zone_card.fusion_types_string)
            else:
                card_type_info = "[" + zone_card.card_type + "] " + zone_card.spell_or_trap_type
                monst_lvl_and_atk = ""
                gs_text = ""
                card_info_panel.setCardContent(card_name, "", "", "", card_type_info, "", card_desc, None, None, zone_card.fusion_types_string)
            
def changeDisplayCard(activate_delay, select_player_equip_target, flagger, activated_spell_or_trap_card_display, mouse_click_status, trap_select_active, zone, mouse_pos, card_layout, card_info_panel, selected_field_card_option_box, turn, monster_field_options, game_instance, in_battle_phase, attacking_card):

    if zone.card_img != None:
        zha_rect.x = zone.rect.x
        zha_rect.y = zone.rect.y
        if checkIfTrue(mouse_pos, zone, zha_rect, selected_field_card_option_box.card, game_instance):
            """
            if selected_field_card_option_box.card != None:
                zone_card = zone.zone.getCardByIndex(0)   
                if selected_field_card_option_box.card.zone.getCardByIndex(0).name != zone_card.name:
                    zone_card = selected_field_card_option_box.card.zone.getCardByIndex(0)
            else:
            """         
            zone_card = zone.zone.getCardByIndex(0)          


            card_layout.card = zone_card
            card_layout.card_type = zone_card.card_type

            card_layout.changeImg(zone_card.img)
            card_name = zone_card.name
            card_desc = zone_card.text
                
            
            if zone.zone.getNumOfCardsContained() > 0:
                #if zone_card.card_owner == game_instance.player and game_instance.current_turn_player == game_instance.player:
                if in_battle_phase:
                    if zone_card.card_type == "Monster":  
                        if not game_instance.current_turn_player.is_attacking and not zone_card.has_attacked:
                            selected_field_card_option_box.is_selected = True
                            
                            selected_field_card_option_box.card = zone
                            selected_field_card_option_box.getArea(turn)
                            selected_field_card_option_box.is_on = True
             
                            
             
                            
                            #selected_field_card_option_box.card = cards[x]

                            if turn == 1:# or not zone_card.in_atk_position:
                                monster_field_options[1].screen = selected_field_card_option_box.area
                            else:
                                if not zone_card.in_atk_position:
                                    monster_field_options[1].screen = wxx
                                    monster_field_options[1].screen = selected_field_card_option_box.area
                                else:
                                    for option in monster_field_options:
                                        option.screen = selected_field_card_option_box.area
                            
                            selected_field_card_option_box.options = monster_field_options

                            

                            if zone_card.card_owner == game_instance.player:
                                if not activate_delay and not trap_select_active and not activated_spell_or_trap_card_display and not flagger and not select_player_equip_target:
                                    if game_instance.current_turn_player == game_instance.player:
                                        selected_field_card_option_box.blit()
                    else:
                        if zone_card.is_set:
                            selected_field_card_option_box.is_selected = True
                            
                            selected_field_card_option_box.card = zone
                            selected_field_card_option_box.getArea()
                            selected_field_card_option_box.is_on = True
                            
                            if zone_card.card_type != "Trap":
                                display_options = True
                                if zone_card.spell_or_trap_type == "Equip":
                                    if not zone_card.willActivate():
                                        display_options = False

                                if display_options:
                                    for option in monster_field_options:
                                        option.screen = selected_field_card_option_box.area
                                    selected_field_card_option_box.options = monster_field_options
                                
                                    if zone_card.card_owner == game_instance.player:
                                        if not select_player_equip_target and not trap_select_active and not activated_spell_or_trap_card_display and not flagger and game_instance.current_turn_player == game_instance.player:   
                                          selected_field_card_option_box.blit()
                                else:
                                    selected_field_card_option_box.card = None
                                    selected_field_card_option_box.options = []
            
            if zone_card.card_type == "Monster":   
                    
                card_type_info = "[Monster] " + zone_card.monster_type + "/" + zone_card.monster_attr 
                monst_lvl_and_atk = "[" + u"\u2605" + str(zone_card.level) + "]  " + str(zone_card.atk_points) + "/" + str(zone_card.def_points)
                gs_text = "Guardian Stars:" 
                gs1_img = getGuardianStarImg(zone_card.guardian_star_list[0].name)
                gs2_img = getGuardianStarImg(zone_card.guardian_star_list[1].name)
                gs1_text = zone_card.guardian_star_list[0].name
                gs2_text = zone_card.guardian_star_list[1].name

                selected_gs = zone_card.guardian_star.name
                
                color = Settings.YELLOW
                if game_instance.current_turn_player.is_attacking:
                    game_instance.current_turn_player.set_attacking_monster(attacking_card)
                    if zone_card.card_owner == game_instance.current_turn_player.opponent:
                        if attacking_card.guardian_star.gs_id == zone_card.guardian_star.strong_against_id:
                            color = Settings.RED
                        elif attacking_card.guardian_star.gs_id == zone_card.guardian_star.weak_against_id:
                            color = Settings.GREEN
                              
                if gs1_text == selected_gs:
                    pygame.draw.rect(card_info_panel.screen, color, [125, 445, 100, 50])
                else:
                    pygame.draw.rect(card_info_panel.screen, color, [215, 445, 100, 50])
                    
                card_info_panel.setCardContent(card_name, gs_text, gs1_text, gs2_text, card_type_info, monst_lvl_and_atk, card_desc, gs1_img, gs2_img, zone_card.fusion_types_string)
            else:
                card_type_info = "[" + zone_card.card_type + "] " + zone_card.spell_or_trap_type
                monst_lvl_and_atk = ""
                gs_text = ""
                card_info_panel.setCardContent(card_name, "", "", "", card_type_info, "", card_desc, None, None, zone_card.fusion_types_string)
        
            if trap_select_active:
                if game_instance.current_turn_player == game_instance.ai:
                    if mouse_click_status[0] == 1:
                        if zone_card.card_owner == game_instance.player:
                            if zone_card.card_type == "Trap":
                                if zone.color == (0, 255, 0):
                                    zone_card.is_set = False
                                    zone.setZoneCardImg()

                                    return zone_card
                
        else:
            #if game_instance.current_turn_player == game_instance.player:
            if not select_player_equip_target and not trap_select_active and not activated_spell_or_trap_card_display and not flagger and game_instance.current_turn_player == game_instance.player:
                if in_battle_phase:
                    if not game_instance.current_turn_player.is_attacking:
                        if selected_field_card_option_box.area != None:
                            if selected_field_card_option_box.rect.collidepoint(mouse_pos):
                                if selected_field_card_option_box.card == None:
                                    if game_instance.current_turn_player == game_instance.player:
                                        if selected_field_card_option_box.options != []:
                                            selected_field_card_option_box.blit()
                                else:
                                    if not selected_field_card_option_box.card.disabled_for_attacks:
                                        if game_instance.current_turn_player == game_instance.player:
                                            if selected_field_card_option_box.options != []:
                                                selected_field_card_option_box.blit()
                        else:
                            selected_field_card_option_box.options = []

                
def getGuardianStarImg(gs_name):
    result = None
    if gs_name == "Mercury":
        result = pygame.image.load("images/guardian_stars/0.png")
    elif gs_name == "Sun":
        result = pygame.image.load("images/guardian_stars/1.png")    
    elif gs_name == "Moon":
        result = pygame.image.load("images/guardian_stars/2.png")          
    elif gs_name == "Venus":
        result = pygame.image.load("images/guardian_stars/3.png")
    elif gs_name == "Mars":
        result = pygame.image.load("images/guardian_stars/4.png")
    elif gs_name == "Jupiter":
        result = pygame.image.load("images/guardian_stars/5.png")
    elif gs_name == "Saturn":
        result = pygame.image.load("images/guardian_stars/6.png")
    elif gs_name == "Uranus":
        result = pygame.image.load("images/guardian_stars/7.png")
    elif gs_name == "Pluto":
        result = pygame.image.load("images/guardian_stars/8.png")
    elif gs_name == "Neptune":
        result = pygame.image.load("images/guardian_stars/9.png")  

    return result

def bilt_long_text(surface, text, font, location, color=(0, 0, 0), break_width=225, height_increment=13):
    height = location[1]
    text_array = text.split(" ")
    length = len(text_array)
    while length > 0:
        line_text = ""
        phrase_width, phrase_height = font.size(line_text)

        while phrase_width < break_width:#250:
            if length > 0:
                line_text += text_array.pop(0) + " "
                phrase_width, phrase_height = font.size(line_text)
                length = len(text_array)
            else:
                break


        rendered_line = font.render(line_text, True, color)
        surface.blit(rendered_line, [location[0], height])
        height += height_increment

def fade(width, height, screen, opening_screen, flag=True):
    fade = pygame.Surface((width, height))
    fade.fill((0, 0, 0))
    for alpha in range(0, 300, 5):
        fade.set_alpha(alpha)

        if flag:
            opening_screen.blit()

            if opening_screen.is_darkened:
                for button in opening_screen.buttons:
                    button.blit()

        screen.blit(fade, (0, 0))
        
        pygame.display.update()
        #pygame.time.delay(1)


def drawBoard(screen, zone_lines_tuple):#646.05 #119.5 #0.03 #0.87 #14 #223.5 #461 #129.2
    pygame.draw.rect(screen, Settings.LIGHT_GRAY, [355, 40, 885, 530], 1)
    
    pygame.draw.rect(screen, Settings.LIGHT_GRAY, [474.5, 74.5, 646, 223.5], 1)
    pygame.draw.rect(screen, Settings.LIGHT_GRAY, [474.5, 312, 646, 223.5], 1)
    
    pygame.draw.line(screen, Settings.LIGHT_GRAY, [474.5, 186.25], [1120.4, 186.25], 1)
    pygame.draw.line(screen, Settings.LIGHT_GRAY, [474.5, 423.75], [1120.4, 423.75], 1)
    
    #for x in range(603.7, 992.3 , 129.2):
    for x in zone_lines_tuple:
        pygame.draw.line(screen, Settings.LIGHT_GRAY, [x, 74.5], [x, 296], 1)
        pygame.draw.line(screen, Settings.LIGHT_GRAY, [x, 312], [x, 533.5], 1)
        
    pygame.draw.rect(screen, Settings.LIGHT_GRAY, [364.25, 186.62, 100, 111.75], 1)
    pygame.draw.rect(screen, Settings.LIGHT_GRAY, [1130.25, 312.37, 100, 111.75], 1)
    
    pygame.draw.rect(screen, Settings.LIGHT_GRAY, [364.25, 74.5, 100, 111.75], 1)
    pygame.draw.rect(screen, Settings.LIGHT_GRAY, [1130.25, 424.12, 100, 111.75], 1)
    
    pygame.draw.rect(screen, Settings.LIGHT_GRAY, [364.25, 312.37, 100, 111.75], 1)
    pygame.draw.rect(screen, Settings.LIGHT_GRAY, [1130.25, 186.62, 100, 111.75], 1)
    """
    pygame.draw.line(screen, Settings.LIGHT_GRAY, [355, 570], [1240, 570] , 1)
    pygame.draw.line(screen, Settings.LIGHT_GRAY, [355, 570], [355, 40] , 1)
    pygame.draw.line(screen, Settings.LIGHT_GRAY, [355, 40], [1240, 40] , 1)
    pygame.draw.line(screen, Settings.LIGHT_GRAY, [1240, 40], [1240, 570] , 1)
    """
        
def drawHealthBars(player_health, enemy_health, screen, font, lp_font, player_name, enemy_name):
    bar_length = 367.5

    current_player_health_string = str(int(player_health.getCurrentHealth()))
    current_ai_health_string = str(int(enemy_health.getCurrentHealth()))

    text_width, text_height = lp_font.size(current_player_health_string)
    text_width2, text_height2 = lp_font.size(current_ai_health_string)

    text1 = lp_font.render(current_player_health_string, True, Settings.WHITE)
    text2 = lp_font.render(current_ai_health_string, True, Settings.WHITE)
    
    player_bar_name = font.render(player_name, True, Settings.WHITE)
    enemy_bar_name = font.render(enemy_name, True, Settings.WHITE)

    if player_health.getCurrentToFullHealthRatio() > 0.75:
        player_health_color = Settings.DARK_GREEN
    elif player_health.getCurrentToFullHealthRatio() > 0.50:
        player_health_color = Settings.DARK_YELLOW
    else:
        player_health_color = Settings.RED

    if enemy_health.getCurrentToFullHealthRatio() > 0.75:
        enemy_health_color = Settings.DARK_GREEN
    elif enemy_health.getCurrentToFullHealthRatio() > 0.50:
        enemy_health_color = Settings.DARK_YELLOW
    else:
        enemy_health_color = Settings.RED

    pygame.draw.rect(screen, Settings.BLUE, [390, 15, 371.5, 25], 3)
    pygame.draw.rect(screen, Settings.BLUE, [832.5, 15, 371.5, 25], 3)

    if player_health.getCurrentHealth() > 0:#367.5
        pygame.draw.rect(screen, player_health_color, [392, 17, bar_length * player_health.getCurrentToFullHealthRatio(), 21])
        #pygame.draw.rect(screen, player_health_color, (200, 25, , 25))

    if enemy_health.getCurrentHealth() > 0:
        pygame.draw.rect(screen, enemy_health_color, [834.5+(bar_length-(bar_length * enemy_health.getCurrentToFullHealthRatio())), 17, bar_length * enemy_health.getCurrentToFullHealthRatio(), 21])
        #pygame.draw.rect(screen, enemy_health_color, (500+(bar_length-(bar_length * enemy_health.getCurrentToFullHealthRatio())), 25, bar_length * enemy_health.getCurrentToFullHealthRatio(), 25))

    screen.blit(player_bar_name, [390, 40])
    screen.blit(enemy_bar_name, [832.5, 40])
    
    screen.blit(text1, [392+(191.25-(text_width/2)), 19])
    screen.blit(text2, [834.5+(191.25-(text_width2/2)), 19])        
    
def isEnemyMonsterZoneEmpty(highlighted_zones):
    for zone in highlighted_zones:
        if zone.zone.getNumOfCardsContained() > 0:
            return False
    return True
    
def areMonsterZonesFull(monster_zones_array):
    ctr = 0
    for zone in monster_zones_array:
        if zone.zone.getNumOfCardsContained() > 0:
            ctr += 1
    return ctr == 5
    
def getEmptyAiMonsterZone(ai_monster_zones_array):
    return [zone.index for zone in ai_monster_zones_array if zone.zone.getNumOfCardsContained() == 0]
    
def getWeakestAiMonster(ai_monster_zones_array):
    weakest_val = 9999
    weakest_index = None
    for zone in ai_monster_zones_array:
        if zone.zone.getNumOfCardsContained() == 1:
            zone_card = zone.zone.getCardByIndex(0)
            
            if zone_card.in_atk_position:
                compared_val = zone_card.current_atk_points
            else:
                compared_val = zone_card.current_def_points
                
            if compared_val < weakest_val:
                compared_val = weakest_val
                weakest_index = zone.index
                
    return [weakest_index]
    
def getAiMonsterZoneToPlay(ai_monster_zones_array, screen, func, arbitrary_card_to_be_fused, game_instance):
    possible_fusion_results = []
    for zone in ai_monster_zones_array:
        if zone.zone.getNumOfCardsContained() == 1:
            zone_monster_card = zone.zone.getCardByIndex(0)
            zone_monster_img = CardImage(screen, zone_monster_card.card_type, zone_monster_card.img, 0, 0, zone_monster_card)
            if zone_monster_card.is_set:
                is_set = True
            else:
                is_set = False
            zone_monster_img.card.is_set = False
        
            result, x = fuseCards(arbitrary_card_to_be_fused, zone_monster_img, game_instance.current_turn_player, screen, createFusedCard, False)
            #del zone_monster_img
            if result:
                possible_fusion_results.append({
                    "card": result,
                    "indices": [zone.index] 
                })
            else:
                if is_set:
                    zone_monster_card.is_set = True
                

    if len(possible_fusion_results) > 0:
        ai_monster_zone_index, x = selectedFusionIndices(possible_fusion_results)
        ai_monster_zones_select = [ai_monster_zone_index[0]]
        #del x
    else:
        ai_monster_zones_select = func(ai_monster_zones_array)

    return ai_monster_zones_select
    
def get_monsters_on_field(monster_zones_array, filter_func=lambda card: True):
    monsters = []
    for zone in monster_zones_array:
        if zone.zone.getNumOfCardsContained() == 1:
            card = zone.zone.getCardByIndex(0)
            if filter_func(card):
                monsters.append(card)
    return monsters
  
def sortMonsterListWeakestToStrongest(monsters, filter_func=lambda card: True):
    sorted_list = []
    atk_list = []
    
    for monster in monsters:
        atk_list.append(monster.getAtkPoints(True))
        
    atk_list.sort()
    monsters_copy = monsters.copy()
    
    for i in range(len(atk_list)):
        for j in range(len(monsters_copy)):
            ai_monster = monsters_copy[j]
            ai_monster_atk = ai_monster.getAtkPoints(True)
            if atk_list[i] == ai_monster_atk:
                if filter_func(monsters_copy[j]):
                    sorted_list.append(monsters_copy[j])
                    monsters_copy.remove(monsters_copy[j])
                    break
                
    return sorted_list
  
def get_ai_zone_current_monster(ai_monsters_per_zone, player_monsters_per_zone):
    sorted_ai_monster_list_weakest_to_strongest = sortMonsterListWeakestToStrongest(ai_monsters_per_zone)

    for i in range(3):
        for ai_monster in sorted_ai_monster_list_weakest_to_strongest:
            for player_monster in player_monsters_per_zone:
                if ai_monster.checkGuardianStars(ai_monster, player_monster) == 2 and i < 2:
                    if i == 0:
                        if not player_monster.is_set:
                            if ai_monster.getAtkPoints(True) + 500 > player_monster.getAtkPoints(True):
                                return ai_monster
                    elif i == 1:
                        if player_monster.is_set:
                            return ai_monster     
                elif ai_monster.checkGuardianStars(ai_monster, player_monster) == 0 and i == 2:
                    if not player_monster.is_set:
                        if ai_monster.getAtkPoints(True) > player_monster.getAtkPoints(True):
                            return ai_monster 
                            
    return sorted_ai_monster_list_weakest_to_strongest[-1]
    
def trap_trigger_check(attacking_monster, opponent, game_instance, attacked_monster=None):
    opponent_trap_cards = get_monsters_on_field(opponent.player_spell_and_trap_zones_array, filter_func=lambda card: card.card_type == "Trap")
    available_traps = []

    if len(opponent_trap_cards) > 0:
        for card in opponent_trap_cards:
            if opponent == game_instance.ai:
                if card.aiUseCondition(game_instance):
                    available_traps.append(card)
            else:
                if card.willTrigger(game_instance.ai, is_player=True):
                    available_traps.append(card)
                    
    return available_traps       

def get_ai_trap_to_be_used(attacking_monster, available_traps, game_instance, attacked_monster=None):  
    for trap in available_traps:
        if trap.name == "Sakuretsu Armor":
            if attacked_monster:
                if trap.getStrongestMonster(get_monsters_on_field(game_instance.current_turn_player.player_monster_zones_array), lambda card: not card.is_set).name == attacked_monster.name:
                    return trap 
        elif trap.name == "Trap Hole":
            return trap
                
    return random.choice(available_traps)
    
def get_attacking_card_status_after_trap_effect(attacking_monster, trap_to_be_used):
    target_mons = trap_to_be_used.getTarget(attacking_monster)
    mons_zone = target_mons.current_zone
    if trap_to_be_used.meets_threshold(attacking_monster):
        if trap_to_be_used.activate(target=target_mons):
                if target_mons.current_zone == mons_zone:
                    if trap_to_be_used.name != "Magic Cylinder" and trap_to_be_used.name != "Heavy Storm":
                        trap_to_be_used.current_zone.removeCardFromZone(trap_to_be_used, "To graveyard")
                    return attacking_monster
                else:
                    return None
        else:
            if trap_to_be_used.name != "Magic Cylinder" and trap_to_be_used.name != "Heavy Storm":
                trap_to_be_used.current_zone.removeCardFromZone(trap_to_be_used, "To graveyard")
            return attacking_monster
    else:
        if trap_to_be_used.name != "Magic Cylinder" and trap_to_be_used.name != "Heavy Storm":
            trap_to_be_used.current_zone.removeCardFromZone(trap_to_be_used, "To graveyard")
        return attacking_monster
        
def calculate_life_points(winning_card, game_instance, xhealth, phealth):
    if winning_card.card_owner == game_instance.player:
        xhealth.setHealth(game_instance.ai.life_points)
    else:
        phealth.setHealth(game_instance.player.life_points)     
    
def reset_field(zones, game_instance, ai_monster_zones_array, player_monster_zones_array):
    for card in zones:
        if card.card_type == "Monster":
            card.resetStatus()
            
    if game_instance.current_turn_player == game_instance.player:
        for zone in ai_monster_zones_array:
            if zone.card_img != None:
                zone.area.fill((0, 0, 0, 0))
    else:
        for zone in player_monster_zones_array:
            if zone.card_img != None:
                zone.area.fill((0, 0, 0, 0))  
                
def textBoxButtonActions(button_rect, next_button, screen, text_flags, mouse_click_status, mouse_pos, index):
    if button_rect.collidepoint(mouse_pos):
        color = Settings.GREEN
        
        if mouse_click_status[0] == 1:
            text_flags[index] = True
            return pygame.time.get_ticks()
    else:
        color = Settings.WHITE
        
    pygame.draw.circle(screen, color, (1200, 580), 15)
    screen.blit(next_button, button_rect)
    
def blit_boxes(boxes, mouse_pos):
    for box in boxes:
        if not box.is_selected:
            if box.rect.collidepoint(mouse_pos):
                box.area.fill(Settings.GREEN)
                
            else:
                box.area.fill(Settings.LIGHT_GRAY)
            
        box.blit()
                 
def getCardCategories(card_id):
    c.execute("""
        SELECT
            Fusion_Classification_Names.Name,
            Card_Fusion_Classifications.Priority
        FROM
            Card_Fusion_Classifications
        INNER JOIN
            Fusion_Classification_Names
        ON
            Fusion_Classification_Names.FCN_ID = Card_Fusion_Classifications.FCN_ID
        WHERE
            Card_Fusion_Classifications.Card_ID = (?)
        ORDER BY
            Card_Fusion_Classifications.Priority ASC""", (card_id,))
            
    return c.fetchall()
    
def clicked_box_status_change(boxes, mouse_pos, func):
    for box in boxes:                    
        if box.rect.collidepoint(mouse_pos): 
            clicked_box = box
            for box in boxes:
                if func(box, clicked_box):
                    box.is_selected = False
                    box.area.fill(Settings.LIGHT_GRAY)   
                
            clicked_box.is_selected = not clicked_box.is_selected
           
            if clicked_box.is_selected:
                clicked_box.area.fill(Settings.GREEN)
            else:
                clicked_box.area.fill(Settings.LIGHT_GRAY)

            return True         
    
def getSearchTrunkQueryString(like_condition, order_col, ordering, grouping):
    base_string = "SELECT * FROM trunk INNER JOIN Cards ON trunk.card_id = Cards.Card_ID WHERE quantity > 0 AND trunk.player_id = (?)" + like_condition + " ORDER BY " + grouping + "" + order_col + " " + ordering
    return base_string
    
def getMyDeck(deck_id):
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
            Cards.Card_ID DESC""", (deck_id,))  
            
    return c.fetchall()
    
def buildDeck(query_result, duelist):
    deck = []

    query_result_length = len(query_result)
    ctr = 0
    while ctr < query_result_length:
        card_type = query_result[ctr][2]

        card_quantity = query_result[ctr][15]
        card_name = query_result[ctr][1]
        
        card_categories = getCardCategories(query_result[ctr][0])
        
        for _ in range(card_quantity):
            #if not is_human:
        
            if card_type == "Monster":
                fusion_types_array = []
                for category in card_categories:
                    fusion_type = category[0]
                    fusion_types_array.append(fusion_type)

                new_card = MonsterCard(query_result[ctr][0], query_result[ctr][1], query_result[ctr][3], query_result[ctr][4], duelist, query_result[ctr][5], query_result[ctr][6], query_result[ctr][7], query_result[ctr][8], query_result[ctr][12], query_result[ctr][13], query_result[ctr][9], fusion_types_array)
            elif card_type == "Spell" or card_type == "Trap":
                fusion_type = card_categories[0][0]
                module_string_name = query_result[ctr][14]
                
                if card_type == "Spell":
                    path = "classes.effects.spells."
                else:    
                    path = "classes.effects.traps."
                    
                moduleName = import_module(path + module_string_name)    
                className = getattr(moduleName, module_string_name)
                new_card = className(query_result[ctr][0],
                                     query_result[ctr][1],
                                     query_result[ctr][3],                             
                                     query_result[ctr][4],
                                     duelist,
                                     query_result[ctr][10],
                                     fusion_type
                                     )
        
            deck.append(new_card)
  
        ctr += 1
        
    return deck
    
def clicked_trunk_or_deck_status(trunk_or_deck_results, mouse_pos, func2):
    for card_info in trunk_or_deck_results:
        if func2(card_info, mouse_pos):
            return True
    return False
    
def check_card_quantity_in_deck_maker(deck_id):
    def func(card_id):
        c.execute("""
            SELECT
                Quantity
            FROM
                Deck_Cards
            WHERE Deck_ID = (?)
            AND Card_ID = (?)""", (deck_id, card_id))  
                
        result = c.fetchall()
        if len(result) == 0 or int(result[0][0]) < 3:
            return True
        return False
        
    return func
    
def getCardId(trunk_card_results, mouse_pos, func, func2, func3):
    for card_info in trunk_card_results:
        if func(card_info, mouse_pos):
            card_id = func2(card_info)
            if func3(card_id):
                return card_id
            
def updateTrunkTable(trunk_to_deck_card_id, player):
    c.execute("""
        UPDATE
            trunk
        SET
            quantity = quantity - 1
        WHERE quantity > 0
        AND
            card_id = (?)
        AND
            player_id = (?)""", (trunk_to_deck_card_id, player["ID"],))  
            
    c.execute("""
        SELECT
            *
        FROM
            Deck_Cards
        WHERE Deck_ID = (?)
        AND
            card_id = (?)""", (player["Deck_ID"], trunk_to_deck_card_id,))  
            
    result = c.fetchall()

    if len(result) > 0:
        c.execute("""
            UPDATE
                Deck_Cards
            SET
                Quantity = Quantity + 1
            WHERE
                card_id = (?)
            AND
                Deck_ID = (?)""", (trunk_to_deck_card_id, player["Deck_ID"],))      
    else:
        c.execute("""
            INSERT INTO
                Deck_Cards
                (
                    Deck_ID,
                    Card_ID,
                    Quantity
                )
            VALUES
                (
                    (?),
                    (?),
                    (?)
                )
            """, (player["Deck_ID"], trunk_to_deck_card_id, 1))  
        conn.commit()
   
def updateTrunkTable2(deck_to_trunk_card_id, player):
    c.execute("""
        UPDATE
            Deck_Cards
        SET
            Quantity = Quantity - 1
        WHERE
            card_id = (?)
        AND
            Deck_ID = (?)""", (deck_to_trunk_card_id, player["Deck_ID"],)) 
            
    c.execute("""
        SELECT
            Quantity
        FROM
            Deck_Cards
        WHERE
            card_id = (?)
        AND
            Deck_ID = (?)""", (deck_to_trunk_card_id, player["Deck_ID"],))   

    initial_res = c.fetchone()

    if int(initial_res[0]) == 0:
        c.execute("""
        DELETE FROM
            Deck_Cards
        WHERE
            card_id = (?)
        AND
            Deck_ID = (?)""", (deck_to_trunk_card_id, player["Deck_ID"],)) 
        conn.commit()

    c.execute("""
        UPDATE
            trunk
        SET
            quantity = quantity + 1
        WHERE
            card_id = (?)
        AND
            player_id = (?)""", (deck_to_trunk_card_id, player["ID"],))  
   
def arrangeDeckGUI(deck_list):
    deck_images_container = []
    deck_x = 332
    deck_y = 130
    deck_ctr = 0
    
    for card in deck_list:
        my_dict = dict()
        my_dict["card"] = card
        my_dict["image"] = pygame.transform.scale(pygame.image.load(card.img), (60, 87))
        my_dict["rect"] = my_dict["image"].get_rect()
        my_dict["rect"].x = deck_x
        my_dict["rect"].y = deck_y
        deck_images_container.append(my_dict)
        
        deck_ctr += 1
        deck_x += 63
        
        if deck_ctr % 10 == 0:
            deck_x = 332
            deck_y += 90
            
    return deck_images_container
    
def setDeckCompositionAmounts(my_deck, monster_number_tooltip, spell_number_tooltip, trap_number_tooltip):
    monsters_count = 0
    spells_count = 0
    traps_count = 0 
    
    for card in my_deck:
        if card.card_type == "Monster":
            monsters_count += 1
        elif card.card_type == "Spell":
            spells_count += 1
        else:    
            traps_count += 1
            
    monster_number_tooltip.changeText(str(monsters_count))
    spell_number_tooltip.changeText(str(spells_count))
    trap_number_tooltip.changeText(str(traps_count))
    
def get_unique_cards_possessed(player_id):
    c.execute("""
        SELECT
            COUNT(card_id) AS Unique_Cards
        FROM trunk
        WHERE
            player_id = (?)""", (player_id,)) 
            
    result = c.fetchone()
    return result[0]
    
def get_total_cards_possessed(player_id, deck_id):
    c.execute("""
        SELECT
            SUM(quantity) AS Total_Cards
        FROM trunk
        WHERE
            player_id = (?)
        UNION
        SELECT 
            SUM(Quantity) As Total_Cards
        FROM
            Deck_Cards
        WHERE
            Deck_ID = (?)""", (player_id, deck_id,))

    result = c.fetchall()  
    total = 0
    
    for item in result:
        total += item[0]
        
    return total
    
def get_duel_skill_img_name(game_instance):
    if game_instance.winner == game_instance.ai:
        return "loser.png", None
    else:
        if len(game_instance.ai.deck.getCards()) < 1:
            return "s_rank.png", "tec.png"
        
        if game_instance.current_turn <= 4 or len(game_instance.player.deck.getCards()) >= 33:
            if game_instance.current_turn <= 4 and len(game_instance.player.deck.getCards()) >= 33:
                return "s_rank.png", "pow.png"
            return "a_rank.png", "pow.png"
            
        if game_instance.current_turn <= 7 or len(game_instance.player.deck.getCards()) >= 26:  
            if game_instance.current_turn <= 7 and len(game_instance.player.deck.getCards()) >= 26: 
                return "a_rank.png", "pow.png"
            return "b_rank.png", "pow.png"
            
        if game_instance.current_turn <= 10 or len(game_instance.player.deck.getCards()) >= 20:  
            if game_instance.current_turn <= 10 and len(game_instance.player.deck.getCards()) >= 20: 
                return "b_rank.png", "pow.png"
            return "c_rank.png", "pow.png"
            
        if game_instance.current_turn <= 13 or len(game_instance.player.deck.getCards()) >= 14:
            if game_instance.current_turn <= 13 and len(game_instance.player.deck.getCards()) >= 14:
                return "c_rank.png", "pow.png"
            return "d_rank.png", "pow.png"
            
        return "d_rank.png", "pow.png"

def get_duel_skill_id(duel_skill, pow_or_tec):
    c.execute("""
        SELECT
            duel_skill_id
        FROM duel_skills
        WHERE
            rank = (?)
        AND
            category = (?)""", (duel_skill[:-4], pow_or_tec[:-4],))  
    
    query_result = c.fetchone()
    return query_result[0]
  
def get_card_from_percentage(query_result):
    chance = random.randint(1, 100)
    percentage = 0

    for tuple in query_result:
     percentage += tuple[1]
     if percentage >= chance:
        return tuple[0]
  
def get_post_duel_card_prize(duel_skill, deck_id):
    c.execute("""
        SELECT bounty_percentages.card_id, bounty_percentages.drop_chance_percentage 
        FROM bounty_percentages 
        INNER JOIN card_bounty_table
        ON
            card_bounty_table.bounty_id = bounty_percentages.bounty_id
        WHERE 
            bounty_percentages.bounty_id = (?)
        AND
            card_bounty_table.catlev_id = (?)
        ORDER BY bounty_percentages.drop_chance_percentage ASC""", (duel_skill, deck_id,))
        
    query_result = c.fetchall()
    
    card_id = get_card_from_percentage(query_result)

    c.execute("""
        SELECT
            *
        FROM Cards
        WHERE
            Card_ID = (?)""", (card_id,))
            
    query_result = c.fetchone()
    card_categories = getCardCategories(query_result[0])

    fusion_types_array = []
    for category in card_categories:
        fusion_type = category[0]
        fusion_types_array.append(fusion_type)

    if query_result[2] == "Monster":
        new_card = MonsterCard(query_result[0], query_result[1], query_result[3], query_result[4], None, query_result[5], query_result[6], query_result[7], query_result[8], query_result[12], query_result[13], query_result[9], fusion_types_array)
    else:
        if query_result[2] == "Spell":
            class_called = SpellCard
        else:
            class_called = TrapCard
            
        new_card = class_called(query_result[0], query_result[1], query_result[3], query_result[4], None, query_result[10], fusion_types_array)  
        
    return new_card