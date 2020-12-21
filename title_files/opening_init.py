import pygame, random
import title_files.general_functions as gf
from .settings import Settings
from .opening_screen_data import OpeningScreen
from .rock_paper_scissors import FirstTurnCard
from .card_image import CardImage
from .zone_gui import ZoneGUI, SpellZoneGUI, GraveyardGUI, DeckGUI, FieldGUI
from .health_bars import HealthBar
from .selected_card_options import SelectedCardOptionsBox, SelectedCardOptionsBoxContents, SelectedFieldMonsterBox, SelectedFieldMonsterBoxContents, SelectedFieldSpellBoxContents, SelectedFieldSpellTrapBox
from .card_info import CardDescPanel
from classes.db_connect import conn, c
from classes.game import Game
from classes.data_surfaces import DataSurface, DataSurfaceText
from classes.trunk_card_panel import TrunkCardPanel, DeckCard
from classes.card import MonsterCard, SpellCard, TrapCard

        
class FusionOrderBox(DataSurface):
    def __init__(self, screen, dimensions, x_pos, y_pos, color, text, is_active, font, card, opacity=False, index=None):
        super().__init__(screen, dimensions, x_pos, y_pos, color)
        self.text = None
        self.blitted_text = None
        self.is_active = is_active
        self.font = font
        self.card = card
        self.changeText(text, color)
        if index != None:
            self.index = index 
            
    def changeText(self, text, color):
        self.text = text       
        self.blitted_text = self.font.render(self.text, True, Settings.WHITE) 
        self.area.fill(color)
       
    def blit(self):
        self.area.blit(self.blitted_text, [6, 2])
        self.screen.blit(self.area, self.rect)
        
def init_opening_screen():
    pygame.init()
    game_settings = Settings()
    screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))
    opening_screen = OpeningScreen(screen)
    load_opening_screen(game_settings, screen, opening_screen)
    
def load_opening_screen(game_settings, screen, opening_screen):
    V = 0
    myevent = pygame.USEREVENT + 1
    pygame.time.set_timer(myevent, 2000)
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for button in opening_screen.buttons:
            if button.rect.collidepoint(mouse_pos):
                opening_screen.selector.changeSelectedButton(button)
            else:
                button.is_selected = False
                button.changeSelectionImage()

        if opening_screen.buttons[0].is_selected == False and opening_screen.buttons[1].is_selected == False:
            opening_screen.selector.selected_button = None
                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in opening_screen.buttons:
                        if button.rect.collidepoint(mouse_pos):
                            if button.name == "new game button":
                                gf.fade(game_settings.screen_width, game_settings.screen_height, screen, opening_screen)
                                loadNewGameScreen(game_settings, screen, opening_screen)
                            else:
                                gf.fade(game_settings.screen_width, game_settings.screen_height, screen, opening_screen)
                                loadSavedFilesScreen(game_settings, screen, opening_screen)
            elif event.type == myevent:
                if V == 0:
                    V = 1
            """
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    opening_screen.selector.changeSelectedButton(opening_screen.returnNewGameBtn())
                elif event.key == pygame.K_DOWN:
                    opening_screen.selector.changeSelectedButton(opening_screen.returnLoadGameBtn())
            """
                
        opening_screen.blit()

        if opening_screen.is_darkened:
            for button in opening_screen.buttons:
                button.blit()
            
        pygame.display.flip()
        
        if V == 1:
            if not opening_screen.is_darkened:
                V = 0
                opening_screen.changeScreen()                          

def loadNewGameScreen(game_settings, screen, opening_screen):
    font = pygame.font.Font(None, 33)    
    text_width, text_height = font.size("ENTER YOUR NAME")  
    text = font.render("ENTER YOUR NAME", True, Settings.WHITE)
    
    name_box = pygame.image.load("images/new_game_name.png")  
    name_string = ""
    temp = ""
         
    proceed_box = DataSurfaceText(screen, [100, 50], 585, 400, (74, 68, 45), "Proceed", Settings.WHITE, True, font)
    
    clock = pygame.time.Clock()

    while True:
        name_text = font.render(name_string, True, Settings.WHITE)
    
        mouse_pos = pygame.mouse.get_pos()
        mouse_click_status = pygame.mouse.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    name_string = name_string[:-1]
                else:
                    character = pygame.key.name(event.key)
                    if character == "caps lock" or "shift" in character:
                        temp = character
                                       
                    if character == "space":
                        character = " "
                    if len(character) > 1:
                        character = ""
                    
                    if temp != "":
                        if character != "" and character != " ":
                    #    temp = ""
                            character = character.upper()    
                            temp = ""
                        
                    name_string += character
     
                
          
        screen.fill(Settings.BLACK)
        screen.blit(name_box, [235, 200])
        screen.blit(text, [(400 - (text_width / 2)) + 235, 230])
        screen.blit(name_text, [280, 300])
        
        if len(name_string) > 0:
            if proceed_box.rect.collidepoint(mouse_pos):
                proceed_box.area.fill(Settings.GREEN)
                if mouse_click_status[0] == 1:
                    gf.fade(game_settings.screen_width, game_settings.screen_height, screen, opening_screen, flag=False)
                    storyScreen1(game_settings, screen, opening_screen)
            else:
                proceed_box.area.fill((74, 68, 45))
            
            proceed_box.blit()
            
        pygame.display.flip()
        clock.tick(60)

def storyScreen1(game_settings, screen, opening_screen):
    font = pygame.font.Font(None, 35)    

    clock = pygame.time.Clock()
    background = pygame.image.load("images/egyptian_background.jpg") 
    background = pygame.transform.scale(background, (1270, 419))
    next_button = pygame.image.load("images/next_button.png") 
    button_rect = next_button.get_rect()
    button_rect.x = 1185   
    button_rect.y = 565
    
    display_bg = True
    
    textBox = pygame.image.load("images/textBox.png") 
    
    initial_text = ""
    initial_delay_timer = pygame.time.get_ticks()
    initial_delay_timer2 = pygame.time.get_ticks()
    initial_delay_timer3 = pygame.time.get_ticks()
    initial_delay_timer4 = pygame.time.get_ticks()
    initial_delay_timer5 = pygame.time.get_ticks()
    
    text_flags = [False for _ in range(5)]

    text_render = font.render(initial_text, True, Settings.WHITE)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click_status = pygame.mouse.get_pressed()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(Settings.BLACK)
        
        if display_bg:
            screen.blit(background, [0, 0])
            
        screen.blit(textBox, [0, 419])
        screen.blit(text_render, [50, 480])
        
        first_text_appearance_timer = pygame.time.get_ticks()
        
        if first_text_appearance_timer - initial_delay_timer >= 2000: 
            if not text_flags[0]:
                text_render = font.render("In the days of Ancient Egypt...", True, Settings.WHITE)
                initial_delay_timer2 = gf.textBoxButtonActions(button_rect, next_button, screen, text_flags, mouse_click_status, mouse_pos, 0)
            
        if text_flags[0] and not text_flags[1]:
            delay = pygame.time.get_ticks()
            text_render = font.render("There existed a bitter rivalry between two princes...", True, Settings.WHITE)
            
            if delay - initial_delay_timer2 > 2000:
                initial_delay_timer3 = gf.textBoxButtonActions(button_rect, next_button, screen, text_flags, mouse_click_status, mouse_pos, 1)
                
        if text_flags[1] and not text_flags[2]:
            text_render = font.render("That was destined to last for thousands of years...", True, Settings.WHITE)
            delay = pygame.time.get_ticks()
            
            if delay - initial_delay_timer3 > 2000:
                initial_delay_timer4 = gf.textBoxButtonActions(button_rect, next_button, screen, text_flags, mouse_click_status, mouse_pos, 2)
                if initial_delay_timer4:
                    gf.fade(game_settings.screen_width, game_settings.screen_height, screen, opening_screen, flag=False)
                    background = pygame.image.load("images/alterWithItems.png") 
                    background = pygame.transform.scale(background, (1270, 419))
                
        if text_flags[2] and not text_flags[3]:
            text_render = font.render("Key to the rivalry was the race to acquire all of the legendary Millennium Items for himself.", True, Settings.WHITE)
            delay = pygame.time.get_ticks()
            
            if delay - initial_delay_timer4 > 2000:
                initial_delay_timer5 = gf.textBoxButtonActions(button_rect, next_button, screen, text_flags, mouse_click_status, mouse_pos, 3)
                if initial_delay_timer5:
                    gf.fade(game_settings.screen_width, game_settings.screen_height, screen, opening_screen, flag=False)
                    display_bg = False
                    
        if text_flags[3] and not text_flags[4]:
            text_render = font.render("And as their rivalry continues into the present age, who will incite the latest escalation?", True, Settings.WHITE)
            
        pygame.display.flip()
        clock.tick(60)

def freeDuelScreen(ACTIVE_PLAYER, game_settings, screen, opening_screen):
    c.execute("""
        SELECT
            *
        FROM
            ai_deck_categories
        """)

    clock = pygame.time.Clock()
    background = pygame.image.load("images/freeduelbg.png") 
    panel = pygame.image.load("images/freeDuelPanel.png") 
    
    ai_deck_categories_container = []
    deck_categories = c.fetchall()

    x_pos = 53
    y_pos = 105
    ctr = 0
    
    draw_image_on_panel = False
    panel_img = None
    
    small_font = pygame.font.Font(None, 25)  
    font = pygame.font.Font(None, 35)    
    text_width, text_height = 1, 1
    text_render = font.render("", True, Settings.WHITE)
    difficulty_text = font.render("Choose a Difficulty Level", True, Settings.WHITE)
    diff_text_width, diff_text_height = font.size("Choose a Difficulty Level")  
    
    small_text = ""
    has_selected_opponent = False
    
    proceed_box = DataSurfaceText(screen, [80, 40], 1045, 585, Settings.GRAY, "Cancel", Settings.WHITE, True, small_font)

    for category in deck_categories:
        cat_dict = dict()
        cat_dict["id"] = category[0]
        cat_dict["name"] = category[1]
        cat_dict["description"] = category[3]
        cat_dict["image"] = pygame.image.load(category[2])
        cat_dict["rect"] = cat_dict["image"].get_rect()
        cat_dict["rect"].x = x_pos
        cat_dict["rect"].y = y_pos
        
        ctr += 1
        ai_deck_categories_container.append(cat_dict)
        x_pos += 128
        
        if ctr % 6 == 0:
            x_pos = 53
            y_pos += 128
      
    difficulty_levels_container = []
    
    box_x_pos = 925
    box_y_pos = 400
    for i in range(8):
        if i == 4:
            box_x_pos = 925
            box_y_pos = 480
    
        box = DataSurfaceText(screen, [40, 40], box_x_pos, box_y_pos, Settings.RED, str(i + 1), Settings.WHITE, True, small_font)
        box_x_pos += 93
        difficulty_levels_container.append(box)
    selected_deck = None

    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click_status = pygame.mouse.get_pressed()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
              
        screen.blit(background, [0, 0])
        screen.blit(panel, [900, 0])
        
        for deck in ai_deck_categories_container:
            screen.blit(deck["image"], deck["rect"])
            
            if deck["rect"].collidepoint(mouse_pos):
                if not has_selected_opponent:
                    pygame.draw.rect(screen, Settings.GREEN, [deck["rect"].x, deck["rect"].y, 128, 128] , 1)
                    panel_img = deck["image"]
                    small_text = deck["description"]
                    text_render = font.render(deck["name"], True, Settings.WHITE)
                    text_width, text_height = font.size(deck["name"])  
                    draw_image_on_panel = True 
                
                    if mouse_click_status[0] == 1:
                        has_selected_opponent = True
                        selected_opponent_position = deck["rect"]
                        selected_deck = deck
            else:
                if not has_selected_opponent:
                    panel_img = None
                    draw_image_on_panel = False
                    text_render = font.render("", True, Settings.WHITE)
                    text_width, text_height = 1, 1
                    small_text = ""

            if draw_image_on_panel or has_selected_opponent:         
                if panel_img:
                    screen.blit(panel_img, [1021, 10])
                    screen.blit(text_render, [1085 - (text_width / 2), 150])
                    gf.bilt_long_text(screen, small_text, small_font, [920, 210], Settings.WHITE, 290, 17)
        
        if has_selected_opponent:
            pygame.draw.rect(screen, Settings.GREEN, [selected_opponent_position.x, selected_opponent_position.y, 128, 128] , 3)
            screen.blit(difficulty_text, [900 + (185 - (diff_text_width / 2)), 330])

            for box in difficulty_levels_container:
                if box.rect.collidepoint(mouse_pos):
                    box.area.fill(Settings.GREEN)
                    
                    if mouse_click_status[0] == 1:
                        gf.fade(game_settings.screen_width, game_settings.screen_height, screen, opening_screen, flag=False)
                        #goToLastSavedScreen(ACTIVE_PLAYER, screen, game_settings)
                        build_deck_screen(ACTIVE_PLAYER, game_settings, screen, opening_screen, enemy_deck=selected_deck["id"], enemy_level=box.text)
                else:
                    box.area.fill(Settings.RED)
            
                box.blit()

            if proceed_box.rect.collidepoint(mouse_pos):
                proceed_box.area.fill(Settings.GREEN)
                
                if mouse_click_status[0] == 1:
                    has_selected_opponent = False
            else:
                proceed_box.area.fill(Settings.GRAY)
                
            proceed_box.blit()
        
        pygame.display.flip()
        clock.tick(60)
  
def getTrunkCards(screen, small_font, game_settings, query_result):
    y_increment = 0
    trunk_card_results = []
    
    for card in query_result:

        card_categories = gf.getCardCategories(card[1])
        fusion_types_array = []

        for category in card_categories:
            fusion_type = category[0]
            fusion_types_array.append(fusion_type)

        if card[6] == "Monster":
            new_card = MonsterCard(card[1], card[5], card[7], card[8], None, card[9], card[10], card[11], card[12], card[16], card[17], card[13], fusion_types_array)
        else:
            if card[6] == "Spell":
                card_class = SpellCard
            else:
                card_class = TrapCard
            
            new_card = card_class(card[1], card[5], card[7], card[8], None, card[14], fusion_types_array)
                
        trunk_card_results.append(TrunkCardPanel(screen, new_card, pygame.font.Font(None, 25), small_font, 970, y_increment, Settings.LIGHT_YELLOW, card[2], game_settings, [270, 87]))    
        y_increment += 89
            
    return trunk_card_results
  
def filterSearch(player_id, screen, small_font, game_settings):
    def func(query_string):    
        c.execute(query_string, (player_id,))
        query_result = c.fetchall()
        return getTrunkCards(screen, small_font, game_settings, query_result)
    
    return func 
      
def getOrderColText(group_boxes):
    if group_boxes[0].is_selected:
        return "Name"
    elif group_boxes[1].is_selected:
        return "Card_Type, MONST_ATK"
    return "Card_Type, MONST_DEF"
  
def getSearchTextExtension(search_box_text):
    if len(search_box_text) > 0:
        return " AND Name LIKE '" + search_box_text + "%'"
    else:
        return ""
    
def getGroupingText(sort_boxes):
    if sort_boxes[0].is_selected:
        return "MONST_TYPE, "
    elif sort_boxes[1].is_selected:
        return "MONST_ATTR, "
    else:
        return ""
  
def getOrderingText(order_boxes):
    if order_boxes[0].is_selected:
        return "ASC"
    return "DESC"
  
def updatedTrunkCardResults(func, search_box_text, order_boxes, group_boxes, sort_boxes):
    search_text_extension = getSearchTextExtension(search_box_text)
    order_col = getOrderColText(group_boxes)
    ordering = getOrderingText(order_boxes)
    grouping = getGroupingText(sort_boxes)
    
    query_string = gf.getSearchTrunkQueryString(search_text_extension, order_col, ordering, grouping)
    return func(query_string)
  
def build_deck_screen(ACTIVE_PLAYER, game_settings, screen, opening_screen, enemy_deck=None, enemy_level=None):
    c.execute("""
        SELECT
            catlev_id
        FROM
            ai_deck_categories_levels
        WHERE
            cat_id = (?)
        AND 
            lev_id = (?)
        """, (enemy_deck, enemy_level))    
    
    catlev_id = c.fetchone()[0]

    clock = pygame.time.Clock()
    big_font = pygame.font.Font(None, 40)  
    medium_font = pygame.font.Font(None, 25) 

    small_font = pygame.font.SysFont("Trebuchet MS", 14)  
    group_font = pygame.font.Font(None, 30)  
    search_text_width, search_text_height = big_font.size("SEARCH")  
    search_txt = big_font.render("SEARCH", True, Settings.BLACK)
    name_txt = medium_font.render("Name:", True, Settings.BLACK)
    
    finish_editing_button = DataSurfaceText(screen, [150, 112], 335, 512, Settings.LIGHT_GRAY, "Finish deck edit", Settings.BLACK, True, medium_font)

    monster_number_tooltip = DataSurfaceText(screen, [60, 50], 257, 97.5, (186, 145, 74), "1", Settings.WHITE, True, medium_font)
    spell_number_tooltip = DataSurfaceText(screen, [60, 50], 257, 157.5, (1, 140, 116), "1", Settings.WHITE, True, medium_font)
    trap_number_tooltip = DataSurfaceText(screen, [60, 50], 257, 217.5, (153, 46, 123), "1", Settings.WHITE, True, medium_font)
    
    trunk_edit_tooltip = DataSurfaceText(screen, [230, 30], 335, 5, Settings.BLACK, "Trunk Edit Options", Settings.WHITE, True, group_font)
    
    group_boxes = []
    
    box = DataSurfaceText(screen, [120, 30], 580, 5, Settings.GREEN, "Alphabetically", Settings.BLACK, True, medium_font)
    box.is_selected = True
    group_boxes.append(box)
    box = DataSurfaceText(screen, [120, 30], 710, 5, Settings.LIGHT_GRAY, "By ATK", Settings.BLACK, True, medium_font)
    group_boxes.append(box)    
    box = DataSurfaceText(screen, [120, 30], 840, 5, Settings.LIGHT_GRAY, "By DEF", Settings.BLACK, True, medium_font)
    group_boxes.append(box)    
    
    order_boxes = []
    
    box = DataSurfaceText(screen, [120, 30], 710, 45, Settings.GREEN, "Ascending", Settings.BLACK, True, medium_font)
    box.is_selected = True
    order_boxes.append(box)
    box = DataSurfaceText(screen, [120, 30], 840, 45, Settings.LIGHT_GRAY, "Descending", Settings.BLACK, True, medium_font)
    order_boxes.append(box)
    
    sort_boxes = []
    
    box = DataSurfaceText(screen, [120, 30], 710, 85, Settings.LIGHT_GRAY, "By Type", Settings.BLACK, True, medium_font)
    sort_boxes.append(box)
    box = DataSurfaceText(screen, [120, 30], 840, 85, Settings.LIGHT_GRAY, "By Attribute", Settings.BLACK, True, medium_font)
    sort_boxes.append(box)
    
    name_search_surface = DataSurface(screen, [315, 26], 385, 87, Settings.WHITE)
    card_surface = DataSurface(screen, [248, 360], 0, 0, Settings.WHITE)
    card_desc_surface = DataSurface(screen, [325, 270], 0, 365, Settings.LIGHT_GRAY)
    card_info_panel = CardDescPanel(screen)
    card_name_font = pygame.font.SysFont("Segoe UI Symbol", 13)
    card_info_panel.setCardContent("", "", "", "", "", "", "", None, None, "")    
    card_layout = CardImage(card_surface.area, None, "images/cards/card_back.png", card_surface.rect.centerx, card_surface.rect.centery, None)

    search_surface = DataSurface(screen, [645, 120], 325, 0, Settings.YELLOW)

    trunk_cards = DataSurface(screen, [300, 635], 970, 0, Settings.LIGHT_YELLOW)

    search_box_text = ""
    
    filter_search_id_func = filterSearch(ACTIVE_PLAYER["ID"], screen, small_font, game_settings)
    query_string = gf.getSearchTrunkQueryString("", "Name", "ASC", "")
    trunk_card_results = filter_search_id_func(query_string)

    if trunk_card_results:
        top_box = trunk_card_results[0]
        bottom_box = trunk_card_results[-1]
    else:
        top_box = None
        bottom_box = None
    
    deck_background = pygame.image.load("images/hiddenFace.png")
    
    up_button_box = DataSurfaceText(screen, [30, 30], 1240, 0, Settings.RED, u"\u2605", Settings.BLACK, True, small_font)
    down_button_box = DataSurfaceText(screen, [30, 30], 1240, 605, Settings.RED, u"\u2605", Settings.BLACK, True, small_font)
    
    game_instance = Game(ACTIVE_PLAYER, 8000, 8000, catlev_id)    
    
    my_deck = gf.getMyDeck(ACTIVE_PLAYER["ID"])
    my_deck = gf.buildDeck(my_deck, game_instance.player)  
    gf.setDeckCompositionAmounts(my_deck, monster_number_tooltip, spell_number_tooltip, trap_number_tooltip)
    deck_images_container = gf.arrangeDeckGUI(my_deck)

    unique_num_of_cards_possessed = gf.get_unique_cards_possessed(ACTIVE_PLAYER["ID"])
    total_num_of_cards_possessed = gf.get_total_cards_possessed(ACTIVE_PLAYER["ID"], ACTIVE_PLAYER["Deck_ID"])
    
    unique_cards_render = medium_font.render("My unique cards: " + str(unique_num_of_cards_possessed), True, Settings.WHITE)
    total_cards_render = medium_font.render("Total cards possessed: " + str(total_num_of_cards_possessed), True, Settings.WHITE)
    
    max_cards_notice_render = medium_font.render("*Maximum of 3 cards with the same name in your deck*", True, Settings.WHITE)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click_status = pygame.mouse.get_pressed()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked_trunk = gf.clicked_trunk_or_deck_status(trunk_card_results, mouse_pos, lambda card_info, mouse_pos: card_info.rect.collidepoint(mouse_pos))
                    clicked_deck = gf.clicked_trunk_or_deck_status(deck_images_container, mouse_pos, lambda card_info, mouse_pos: card_info["rect"].collidepoint(mouse_pos))
                    clicked_btn_1 = gf.clicked_box_status_change(group_boxes, mouse_pos, lambda x, y: True)
                    clicked_btn_2 = gf.clicked_box_status_change(order_boxes, mouse_pos, lambda x, y: True)
                    clicked_btn_3 = gf.clicked_box_status_change(sort_boxes, mouse_pos, lambda box, clicked_box: box != clicked_box)

                    if clicked_btn_1 or clicked_btn_2 or clicked_btn_3:
                        trunk_card_results = updatedTrunkCardResults(filter_search_id_func, search_box_text, order_boxes, group_boxes, sort_boxes)
                        
                        if trunk_card_results:
                            top_box = trunk_card_results[0]
                            bottom_box = trunk_card_results[-1]
                            
                    if clicked_trunk:
                        trunk_to_deck_card_id = gf.getCardId(trunk_card_results, mouse_pos, lambda card_info, mouse_pos: card_info.rect.collidepoint(mouse_pos), lambda card_info: card_info.card.id, gf.check_card_quantity_in_deck_maker(ACTIVE_PLAYER["Deck_ID"]))
                        if trunk_to_deck_card_id:
                            gf.updateTrunkTable(trunk_to_deck_card_id, ACTIVE_PLAYER)
                            
                            trunk_card_results = updatedTrunkCardResults(filter_search_id_func, search_box_text, order_boxes, group_boxes, sort_boxes)
                            
                            if trunk_card_results:
                                top_box = trunk_card_results[0]
                                bottom_box = trunk_card_results[-1]
                                
                                my_deck = gf.getMyDeck(ACTIVE_PLAYER["ID"])
                                my_deck = gf.buildDeck(my_deck, game_instance.player)  
                                gf.setDeckCompositionAmounts(my_deck, monster_number_tooltip, spell_number_tooltip, trap_number_tooltip)
                                deck_images_container = gf.arrangeDeckGUI(my_deck)
                            
                    if clicked_deck:
                        deck_to_trunk_id = gf.getCardId(deck_images_container, mouse_pos, lambda card_info, mouse_pos: card_info["rect"].collidepoint(mouse_pos), lambda card_info: card_info["card"].id, lambda card_id: True)
                        gf.updateTrunkTable2(deck_to_trunk_id, ACTIVE_PLAYER)
                        
                        trunk_card_results = updatedTrunkCardResults(filter_search_id_func, search_box_text, order_boxes, group_boxes, sort_boxes)
                        
                        if trunk_card_results:
                            top_box = trunk_card_results[0]
                            bottom_box = trunk_card_results[-1]
                            
                            my_deck = gf.getMyDeck(ACTIVE_PLAYER["ID"])
                            my_deck = gf.buildDeck(my_deck, game_instance.player)  
                            gf.setDeckCompositionAmounts(my_deck, monster_number_tooltip, spell_number_tooltip, trap_number_tooltip)
                            deck_images_container = gf.arrangeDeckGUI(my_deck)
                        
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    search_box_text = search_box_text[:-1]
                else:
                    character = pygame.key.name(event.key)
                                       
                    if character == "space":
                        character = " "
                    if len(character) > 1:
                        character = ""                   
                        
                    search_box_text += character
                    
                trunk_card_results = updatedTrunkCardResults(filter_search_id_func, search_box_text, order_boxes, group_boxes, sort_boxes)
                
                if trunk_card_results:
                    top_box = trunk_card_results[0]
                    bottom_box = trunk_card_results[-1]
                    
        search_name_render = small_font.render(search_box_text, True, Settings.BLACK)

        trunk_cards.blit()

        for card_info in trunk_card_results:
            if card_info.rect.collidepoint(mouse_pos):
                card_info.area.fill(Settings.GREEN)            
                card_layout.changeImg(card_info.card.img)
                card_layout.card = card_info.card
                card_layout.card_type = card_info.card.card_type

                if card_info.card.card_type == "Monster":                   
                    card_type_info = "[Monster] " + card_info.card.monster_type + "/" + card_info.card.monster_attr 
                    monst_lvl_and_atk = "[" + u"\u2605" + str(card_info.card.level) + "]  " + str(card_info.card.atk_points) + "/" + str(card_info.card.def_points)
                    gs_text = "Guardian Stars:"
                    gs1_name = card_info.card.guardian_star_list[0].name
                    gs2_name = card_info.card.guardian_star_list[1].name
                    gs1_img = gf.getGuardianStarImg(card_info.card.guardian_star_list[0].name)
                    gs2_img = gf.getGuardianStarImg(card_info.card.guardian_star_list[1].name)
                else:
                    card_type_info = "[" + card_info.card.card_type + "] " + card_info.card.spell_or_trap_type
                    monst_lvl_and_atk = ""
                    gs_text = ""
                    gs1_name = ""
                    gs2_name = ""
                    gs1_img = None
                    gs2_img = None                   
                    
                card_info_panel.setCardContent(card_layout.card.name, gs_text, gs1_name, gs2_name, card_type_info, monst_lvl_and_atk, card_info.card.text, gs1_img, gs2_img, card_info.card.fusion_types_string)
                pygame.draw.rect(card_desc_surface.area, Settings.LIGHT_BLUE, [17.5, 17.5, 290, 22], 1)
            else:
                card_info.area.fill(Settings.LIGHT_YELLOW)
                #card_layout.reset()
                #card_info_panel.setCardContent("", "", "", "", "", "", "", None, None, "")
                
            card_info.blit()

        card_surface.blit()
        card_desc_surface.blit()
        
        if card_layout.card:
            if card_layout.card.card_type == "Monster":
                card_layout.blit(card_layout.card.atk_points, card_layout.card.def_points, Settings.BLACK)   
            else:
                card_layout.blit()
        else:
            card_layout.blit()

        search_surface.blit()
        screen.blit(search_txt, [325 + (192.5 - (search_text_width / 2)), 50])
        screen.blit(name_txt, [330, 93])
        name_search_surface.blit()
        screen.blit(search_name_render, [390, 90])      
        card_info_panel.blit(card_name_font, card_layout.card_type)
        screen.blit(deck_background, [325, 120])
         
        for card in deck_images_container:
            screen.blit(card["image"], card["rect"])   
                      
            if card["rect"].collidepoint(mouse_pos):
                pygame.draw.rect(screen, Settings.GREEN, [card["rect"].x, card["rect"].y, 60, 87], 2)
                
                card_layout.changeImg(card["card"].img)
                card_layout.card = card["card"]
                card_layout.card_type = card["card"].card_type
                
                if card["card"].card_type == "Monster":                         
                    card_layout.blit(card["card"].atk_points, card["card"].def_points, Settings.BLACK)
                    
                    card_type_info = "[Monster] " + card["card"].monster_type + "/" + card["card"].monster_attr 
                    monst_lvl_and_atk = "[" + u"\u2605" + str(card["card"].level) + "]  " + str(card["card"].atk_points) + "/" + str(card["card"].def_points)
                    gs_text = "Guardian Stars:"
                    gs1_name = card["card"].guardian_star_list[0].name
                    gs2_name = card["card"].guardian_star_list[1].name
                    gs1_img = gf.getGuardianStarImg(card["card"].guardian_star_list[0].name)
                    gs2_img = gf.getGuardianStarImg(card["card"].guardian_star_list[1].name)
                else:
                    card_type_info = "[" + card["card"].card_type + "] " + card["card"].spell_or_trap_type
                    card_layout.blit()
                    monst_lvl_and_atk = ""
                    gs_text = ""
                    gs1_name = ""
                    gs2_name = ""
                    gs1_img = None
                    gs2_img = None                   
                    
                card_info_panel.setCardContent(card["card"].name, gs_text, gs1_name, gs2_name, card_type_info, monst_lvl_and_atk, card["card"].text, gs1_img, gs2_img, card["card"].fusion_types_string)
                pygame.draw.rect(card_desc_surface.area, Settings.LIGHT_BLUE, [17.5, 17.5, 290, 22], 1)
            else:
                card_info.area.fill(Settings.LIGHT_YELLOW)

   
        gf.blit_boxes(group_boxes, mouse_pos)
        gf.blit_boxes(order_boxes, mouse_pos)
        gf.blit_boxes(sort_boxes, mouse_pos)
        
        if down_button_box.rect.collidepoint(mouse_pos):
            if bottom_box:
                if bottom_box.rect.y + 87 >= 635: 
                    if mouse_click_status[0] == 1:                     
                        for card_info in trunk_card_results:
                            card_info.rect.y -= 20
                    
        if up_button_box.rect.collidepoint(mouse_pos):
            if top_box:
                if top_box.rect.y < 0: 
                    if mouse_click_status[0] == 1:          
                        for card_info in trunk_card_results:
                            card_info.rect.y += 20                    

        up_button_box.blit()     
        down_button_box.blit()
        trunk_edit_tooltip.blit()
        monster_number_tooltip.blit()
        spell_number_tooltip.blit()
        trap_number_tooltip.blit()
        screen.blit(unique_cards_render, [500, 510])
        screen.blit(total_cards_render, [500, 535])
        screen.blit(max_cards_notice_render, [500, 575])
        
        if finish_editing_button.rect.collidepoint(mouse_pos):
            finish_editing_button.area.fill(Settings.GREEN)
            
            if mouse_click_status[0] == 1:
                gf.fade(game_settings.screen_width, game_settings.screen_height, screen, opening_screen, flag=False)
                goToLastSavedScreen(game_instance, ACTIVE_PLAYER, screen, game_settings)
        else:
            finish_editing_button.area.fill(Settings.LIGHT_GRAY)
        
        finish_editing_button.blit()
           
        #card_info_panel.blit(card_name_font, "Monster")       
        pygame.display.flip()
        clock.tick(60)

def loadSavedFilesScreen(game_settings, screen, opening_screen):
    data = loadSavedData()

    data_surface = DataSurface(screen, [500, 300], 0, 0, Settings.WHITE)
    data_surface.center()
    
    font = pygame.font.Font(None, 50)
    data_font = pygame.font.Font(None, 35)
    ctr = 0
    data_rows = []
    for row in data:
        data_row_dict = {}
        data_row_surface = DataSurface(screen, [500, 40], data_surface.rect.left, data_surface.rect.top+ctr, Settings.WHITE)
        data_row_dict["surface"] = data_row_surface
        text = data_font.render(row[1], True, Settings.GOLD)
        data_row_dict["info"] = {"name": row[1], "id": row[0], "deck_id": row[2]}
        data_row_dict["text"] = text
        data_rows.append(data_row_dict)
        ctr += 40

    buttons = []
    cancel_btn = DataSurface(screen, [150, 50], 700, 490, Settings.RED)
    load_btn = DataSurface(screen, [150, 50], 350, 490, Settings.GREEN)
    buttons.append(cancel_btn)
    buttons.append(load_btn)
    text = font.render("Load Saved Game", True, Settings.GOLD)
    cancel_btn_text = font.render("Go back", True, Settings.WHITE)
    load_btn_text = font.render("Load file", True, Settings.WHITE)
    has_selected_save_file = False
    ACTIVE_PLAYER = {}
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for btn in buttons:
                        if btn.rect.collidepoint(mouse_pos):
                            if btn == cancel_btn:
                                gf.fade(game_settings.screen_width, game_settings.screen_height, screen, opening_screen, False)
                                load_opening_screen(game_settings, screen, opening_screen)
                            else:
                                if has_selected_save_file:
                                    gf.fade(game_settings.screen_width, game_settings.screen_height, screen, opening_screen, False)
                                    freeDuelScreen(ACTIVE_PLAYER, game_settings, screen, opening_screen)
                                    #goToLastSavedScreen(ACTIVE_PLAYER, screen, game_settings)
                                
                    for data in data_rows:
                        if data["surface"].rect.collidepoint(mouse_pos):
                            data["surface"].selected()
                            has_selected_save_file = True
                            ACTIVE_PLAYER["ID"] = data["info"]["id"]
                            ACTIVE_PLAYER["Name"] = data["info"]["name"]
                            ACTIVE_PLAYER["Deck_ID"] = data["info"]["deck_id"]
                            for other_data in data_rows:
                                if other_data["surface"] != data["surface"]:
                                    other_data["surface"].is_selected = False
                                    other_data["surface"].area.fill((255, 255, 255))
                            #jej = font.render(str(data["info"]["id"]) + " " + data["info"]["name"] + " " + str(data["info"]["deck_id"]), True, Settings.GOLD)
                                    
        screen.fill(Settings.background)
        data_surface.blit()
        ctr = 0#data["surface"].rect.top
        for data in data_rows:
            pygame.draw.line(data["surface"].area, (0, 0, 0), [0, 37], [500, 37], 4)
            data["surface"].blit()
            data["surface"].area.blit(data["text"], [10, 10])

            #ctr += 5
        screen.blit(text, [50, 100])
        cancel_btn.blit()
        cancel_btn.area.blit(cancel_btn_text, [5, 10])
        if has_selected_save_file:
            load_btn.blit()
            load_btn.area.blit(load_btn_text, [5, 10])
        #print(data_surface.rect.left)
        pygame.display.flip()

def loadSavedData():
    c.execute("SELECT * FROM Player")
    return c.fetchall()
    
def goToLastSavedScreen(game_instance, player_dict, screen, game_settings):
    Game.game_over = False
    Game.current_turn = 1
    ai_choices = []
    player_choices = []
    
    scissors = FirstTurnCard(screen, "images/c1.jpg", "Scissors", 0)
    ai_choices.append(scissors)
    rock = FirstTurnCard(screen, "images/c2.jpg", "Rock", 0)
    ai_choices.append(rock)
    paper = FirstTurnCard(screen, "images/c3.jpg", "Paper", 0)
    ai_choices.append(paper)
    
    scissors = FirstTurnCard(screen, "images/f1.jpg", "Scissors", 400)
    rock = FirstTurnCard(screen, "images/f2.jpg", "Rock", 400)
    paper = FirstTurnCard(screen, "images/f3.jpg", "Paper", 400)
    
    player_choices.append(scissors)  
    player_choices.append(rock)
    player_choices.append(paper)

    initDuel(player_dict, screen, game_instance, player_choices, ai_choices, game_settings)
    
def initDuel(player_dict, screen, game_instance, player_choices, ai_choices, game_settings):
    #comp_choice = Game.FIRST_TURN_CHOICES[random.randint(1, 3)]
    comp_choice = Game.FIRST_TURN_CHOICES[1]
    repeat_process = False
    for card in ai_choices:
        if card.comparison_value == comp_choice:
            comp_choice = card
            break
            
    print("COMP CHOICE:", comp_choice.comparison_value)
    
    player_choices[1].rect.centerx = player_choices[1].screen_rect.centerx
    player_choices[0].rect.right = player_choices[1].rect.left - 30
    player_choices[2].rect.left = player_choices[1].rect.right + 30
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for card in player_choices:
                        if card.rect.collidepoint(mouse_pos):
                            result = game_instance.compareFirstTurnChoices(card.comparison_value, comp_choice.comparison_value)
                            playCompare(result, card, comp_choice, screen, player_dict, game_settings, game_instance)

                
        screen.fill(Settings.RED)
        
        for card in player_choices:
            card.blit()
            if card.rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, Settings.WHITE, [card.rect.x, card.rect.y, 89, 128] , 3)
                
        if repeat_process:
            pygame.time.wait(2000)
            initDuel(player_dict, screen, game_instance, player_choices, ai_choices, game_settings)           
        
        pygame.display.flip()
        
def playCompare(result, card, comp_choice, screen, player_dict, game_settings, game_instance):
    clock = pygame.time.Clock()
    card.rect.centerx = card.screen_rect.centerx
    card.rect.bottom = card.screen_rect.bottom - 30
    
    comp_choice.rect.top = comp_choice.screen_rect.top + 30
    comp_choice.rect.centerx = card.screen_rect.centerx
    card_speed = 5
    
    will_wait = True
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        screen.fill(Settings.RED)
        
        card.blit()
        comp_choice.blit()
        
        if card.rect.top <= comp_choice.rect.bottom or comp_choice.rect.bottom >= card.rect.top:
            if result == "repeat":
                card_speed *= -1
            else:
                card_speed = 0
                if result == "player":
                    game_instance.current_turn_player = game_instance.player
                    startDuelInit(screen, player_dict, game_instance, game_settings)
                    
                else:
                    game_instance.current_turn_player = game_instance.ai
                    pygame.time.wait(1000)
                    startDuelInit(screen, player_dict, game_instance, game_settings)
        
        if will_wait:
             pygame.time.wait(1500)
             will_wait = False
        
        card.rect.centery -= card_speed
        comp_choice.rect.centery += card_speed
        
        if result == "repeat":
            if comp_choice.rect.top < 0 and card.rect.bottom > game_settings.screen_height:
                goToLastSavedScreen(game_instance, player_dict, screen, game_settings)
        
        pygame.display.flip()
        clock.tick(60)

def startDuelInit(screen, player_dict, game_instance, game_settings):
    clock = pygame.time.Clock()
    card_surface = DataSurface(screen, [248, 360], 0, 0, Settings.WHITE)
    card_desc_surface = DataSurface(screen, [325, 270], 0, 365, Settings.LIGHT_GRAY)
    card_layout = CardImage(card_surface.area, None, "images/cards/card_back.png", card_surface.rect.centerx, card_surface.rect.centery, None)

    player_box_x_y = [385, 10]
    ai_box_x_y = [827.5, 10]
    current_box = player_box_x_y
    
    phealth = HealthBar(game_instance.player.getCurrentLifePointsAmount())
    xhealth = HealthBar(game_instance.ai.getCurrentLifePointsAmount())
    
    current_turn_box_dimensions = [current_box[0], current_box[1], 382.5, 50]
    current_turn_box_dimensions2 = [ai_box_x_y[0], ai_box_x_y[1], 382.5, 50]
    
    card_name_font = pygame.font.SysFont("Segoe UI Symbol", 13)  
    lp_font = pygame.font.Font(None, 25) 
    turn_font = pygame.font.Font(None, 50) 
    win_lose_font = pygame.font.Font(None, 135) 
    card_name = ""
    card_type_info = ""
    monst_lvl_and_atk = ""
    card_desc = ""
    gs_text = ""
    gs1_img = None
    gs2_img = None
    gs1_text = ""
    gs2_text = ""
    turn_dummy = 20
    zone_display_on = False
    spell_zone_display_on = False
    
    #card_in_hand_options_raised = False
    
    zone_lines_tuple = [603.7, 732.9, 862.1, 991.3]
    player_monster_zones_array = []
    player_spell_and_trap_zones_array = []
    
    ai_monster_zones_array = []
    ai_spell_and_trap_zones_array = []
    inner_zones = [474.5] + zone_lines_tuple
    
    selected_card_monster_zone_rects = []
    for zone in inner_zones:
        selected_card_monster_zone_rects.append(DataSurface(screen, [129.2, 111.75], zone, 312, Settings.GREEN, opacity=True))
    
    selected_card_spell_zone_rects = []
    for zone in inner_zones:
        selected_card_spell_zone_rects.append(DataSurface(screen, [129.2, 111.75], zone, 424.12, Settings.GREEN, opacity=True)) 
 
    zones_length = 4
    
    bool_val = False
    player_graveyard = game_instance.player.duelist_zone.getAttr("graveyard")
    ai_graveyard = game_instance.ai.duelist_zone.getAttr("graveyard")
    
    player_deck = game_instance.player.duelist_zone.getAttr("deck_zone")
    ai_deck = game_instance.ai.duelist_zone.getAttr("deck_zone")
    
    player_field = game_instance.player.duelist_zone.getAttr("field_card_zone")
    ai_field = game_instance.ai.duelist_zone.getAttr("field_card_zone")
    
    if game_instance.current_turn_player == game_instance.player:
        player_graveyard_gui = GraveyardGUI(player_graveyard, screen, [364.25, 186.62], [1130.25, 312.37], bool_val, 0, 0, [100, 111.75])
        ai_graveyard_gui = GraveyardGUI(ai_graveyard, screen, [364.25, 186.62], [1130.25, 312.37], not bool_val, 0, 0, [100, 111.75])
        
        player_deck_gui = DeckGUI(player_deck, screen, [364.25, 74.5], [1130.25, 424.12], bool_val, 0, 0, [100, 111.75])
        ai_deck_gui = DeckGUI(ai_deck, screen, [364.25, 74.5], [1130.25, 424.12], not bool_val, 0, 0, [100, 111.75])
        
        player_field_gui = FieldGUI(player_field, screen, [1130.25, 186.62], [364.25, 312.37], bool_val, 0, 0, [100, 111.75])
        ai_field_gui = FieldGUI(ai_field, screen, [1130.25, 186.62], [364.25, 312.37], not bool_val, 0, 0, [100, 111.75])
    else:
        player_graveyard_gui = GraveyardGUI(player_graveyard, screen, [364.25, 186.62], [1130.25, 312.37], not bool_val, 0, 0, [100, 111.75])
        ai_graveyard_gui = GraveyardGUI(ai_graveyard, screen, [364.25, 186.62], [1130.25, 312.37], bool_val, 0, 0, [100, 111.75])
        
        player_deck_gui = DeckGUI(player_deck, screen, [364.25, 74.5], [1130.25, 424.12], not bool_val, 0, 0, [100, 111.75])
        ai_deck_gui = DeckGUI(ai_deck, screen, [364.25, 74.5], [1130.25, 424.12], bool_val, 0, 0, [100, 111.75])
    
        player_field_gui = FieldGUI(player_field, screen, [1130.25, 186.62], [364.25, 312.37], not bool_val, 0, 0, [100, 111.75])
        ai_field_gui = FieldGUI(ai_field, screen, [1130.25, 186.62], [364.25, 312.37], bool_val, 0, 0, [100, 111.75])
    
    for x in range(len(inner_zones)):
        
        monster_zone = game_instance.player.duelist_zone.getAttr("monster_card_zones")[x]
        spell_and_trap_zone = game_instance.player.duelist_zone.getAttr("spell_and_trap_card_zones")[x]
        if game_instance.current_turn_player == game_instance.player:       
            monster_zone_gui = ZoneGUI(monster_zone, screen, [inner_zones[zones_length], 186.62], [inner_zones[x], 312.37], False, x, zones_length, [129.2, 111.75])
            spell_zone_gui = SpellZoneGUI(spell_and_trap_zone, screen, [inner_zones[zones_length], 74.5], [inner_zones[x], 424.12], False, x, zones_length, [129.2, 111.75])
        else:              
            monster_zone_gui = ZoneGUI(monster_zone, screen, [inner_zones[zones_length], 186.62], [inner_zones[x], 312.37], True, x, player_monster_zones_array, [129.2, 111.75]) 
            spell_zone_gui = SpellZoneGUI(spell_and_trap_zone, screen, [inner_zones[zones_length], 74.5], [inner_zones[x], 424.12], True, x, zones_length, [129.2, 111.75])            
        player_monster_zones_array.append(monster_zone_gui)
        player_spell_and_trap_zones_array.append(spell_zone_gui)
        
        monster_zone = game_instance.ai.duelist_zone.getAttr("monster_card_zones")[x]
        spell_and_trap_zone = game_instance.ai.duelist_zone.getAttr("spell_and_trap_card_zones")[x]       
        if game_instance.current_turn_player == game_instance.ai:            
            monster_zone_gui = ZoneGUI(monster_zone, screen, [inner_zones[zones_length], 186.62], [inner_zones[x], 312.37], False, x, zones_length, [129.2, 111.75])
            spell_zone_gui = SpellZoneGUI(spell_and_trap_zone, screen, [inner_zones[zones_length], 74.5], [inner_zones[x], 424.12], False, x, zones_length, [129.2, 111.75])
        else:     
            monster_zone_gui = ZoneGUI(monster_zone, screen, [inner_zones[zones_length], 186.62], [inner_zones[x], 312.37], True, x, zones_length, [129.2, 111.75])  
            spell_zone_gui = SpellZoneGUI(spell_and_trap_zone, screen, [inner_zones[zones_length], 74.5], [inner_zones[x], 424.12], True, x, zones_length, [129.2, 111.75])               
        ai_monster_zones_array.append(monster_zone_gui)
        ai_spell_and_trap_zones_array.append(spell_zone_gui)
        
        zones_length -= 1
        
    
    #892
    hand_cards_status = [{"x_position": 385, "card": None}, {"x_position": 554, "card": None}, {"x_position": 723, "card": None}, {"x_position": 892, "card": None}, {"x_position": 1061, "card": None}]
    
    selected_card_option_box = SelectedCardOptionsBox(screen, [149, 25])
    selected_field_card_option_box = SelectedFieldMonsterBox(screen, [129.2, 25])
    selected_field_spell_trap_card_option_box = SelectedFieldSpellTrapBox(screen, [129.2, 25])
    
    option_font = pygame.font.Font(None, 18)    
    trap_card_options = [SelectedCardOptionsBoxContents(selected_card_option_box.area, "Fuse Up", option_font, [149, 25]), SelectedCardOptionsBoxContents(selected_card_option_box.area, "Fuse Down", option_font, [149, 25]), SelectedCardOptionsBoxContents(selected_card_option_box.area, "Set", option_font, [149, 25])]
    spell_card_options = [SelectedCardOptionsBoxContents(selected_card_option_box.area, "Fuse Up", option_font, [149, 25]), SelectedCardOptionsBoxContents(selected_card_option_box.area, "Fuse Down", option_font, [149, 25]), SelectedCardOptionsBoxContents(selected_card_option_box.area, "Activate", option_font, [149, 25]), SelectedCardOptionsBoxContents(selected_card_option_box.area, "Set", option_font, [149, 25])]
    monster_card_options = [SelectedCardOptionsBoxContents(selected_card_option_box.area, "Fuse Up", option_font, [149, 25]), SelectedCardOptionsBoxContents(selected_card_option_box.area, "Fuse Down", option_font, [149, 25]), SelectedCardOptionsBoxContents(selected_card_option_box.area, "Summon", option_font, [149, 25]), SelectedCardOptionsBoxContents(selected_card_option_box.area, "Set", option_font, [149, 25])]
    card_fusing_options = [SelectedCardOptionsBoxContents(selected_card_option_box.area, "Cancel", option_font, [149, 25])]
    other_card_fusion_options = [SelectedCardOptionsBoxContents(selected_card_option_box.area, "Fuse Up", option_font, [149, 25]), SelectedCardOptionsBoxContents(selected_card_option_box.area, "Fuse Down", option_font, [149, 25])]
    
    spell_field_options = [SelectedFieldSpellBoxContents(selected_field_spell_trap_card_option_box.area, "Activate", option_font, [129.2, 25])]
    monster_field_options = [SelectedFieldMonsterBoxContents(selected_field_card_option_box.area, "Attack", option_font, [129.2, 25]), SelectedFieldMonsterBoxContents(selected_field_card_option_box.area, "Change Position", option_font, [129.2, 25])]
    
    game_instance.gameLoop()
    
    
    myevent = pygame.USEREVENT + 1
    pygame.time.set_timer(myevent, 500)
    V = 0

    if game_instance.current_turn_player == game_instance.player:
        cards = game_instance.player.cards_gui
    else:
        cards = game_instance.ai.cards_gui
    
    cards_in_hand = game_instance.current_turn_player.getCardsInHand()
    
    myctr = 0
    
    game_instance.player.player_monster_zones_array = player_monster_zones_array
    game_instance.ai.player_monster_zones_array = ai_monster_zones_array
    
    game_instance.player.player_spell_and_trap_zones_array = player_spell_and_trap_zones_array
    game_instance.ai.player_spell_and_trap_zones_array = ai_spell_and_trap_zones_array
    
    for card in cards_in_hand:
    #82x119
        if game_instance.current_turn_player == game_instance.player:
            card_in_hand_img = cards_in_hand[myctr].img
        else:
            card_in_hand_img = "images/cards/cover.jpg"
            
        cards_in_hand[myctr].bound_to_gui = True
        new_card = CardImage(screen, cards_in_hand[myctr].card_type, card_in_hand_img, 0, 0, cards_in_hand[myctr], card_index=myctr, in_hand=True)
        new_card.transformSize((149, 216), (2000, 540))
        myctr += 1
        cards.append(new_card)

           
        
    player_deck_gui.setZoneCardImg(lp_font)
    ai_deck_gui.setZoneCardImg(lp_font)
        
    selected_card = None
    selecting_zone = False
    guardian_star_display = False
    selected_zone = None
    
    selecting_trap_tooltip = "Select a trap card to activate by left clicking the card."
    select_equip_tooltip = "Select a monster to equip by left clicking the card."
    trap_card_tooltip = "ACTIVATE A TRAP CARD?"
    trap_tooltip_render = lp_font.render(trap_card_tooltip, True, Settings.RED)
    trap_tooltip_active = False
    
    guardian_star_tooltip = "SELECT A GUARDIAN STAR"
    gst_width, gst_height = lp_font.size(guardian_star_tooltip)
    gst_render = lp_font.render(guardian_star_tooltip, True, Settings.RED)#(game_settings.screen_height/2)-62.5
    select_guardian_star_block = DataSurface(screen, [350, 125], (325+(945/2))-175, 150, Settings.LIGHT_GRAY)#185
    left_gs_selection = DataSurface(select_guardian_star_block.area, [150, 50], 25, 60, Settings.WHITE, opacity=True, index=0)
    right_gs_selection = DataSurface(select_guardian_star_block.area, [150, 50], 175, 60, Settings.WHITE, opacity=True, index=1)
    card_info_panel = CardDescPanel(screen)
    card_name = ""
    selection_star1 = None
    selection_star1 = None
    star_name_1 = ""
    star_name_2 = ""
    
    selected_field_card = None
    selected_field_zone = None
    has_happened = False
    select_attack_target_delay_before = pygame.time.get_ticks()
    wack = 0
    whock = False
    attacking_card = None
    main_phase_block = DataSurfaceText(screen, [60, 50], (248+53.5)-30, 97.5, Settings.YELLOW, "MP", Settings.BLACK, True, lp_font)
    battle_phase_block = DataSurfaceText(screen, [60, 50], (248+53.5)-30, 157.5, Settings.WHITE, "BP", Settings.BLACK, False, lp_font)
    end_phase_block = DataSurfaceText(screen, [60, 50], (248+53.5)-30, 217.5, Settings.WHITE, "EP", Settings.BLACK, False, lp_font)
    #170 #182.5 #85
    selected_spell_zone = False
    place_spell_timer = pygame.time.get_ticks()
    place_spell_timer_interval3 = pygame.time.get_ticks()
    place_spell_timer_interval2 = pygame.time.get_ticks()
    spell_trap_card_activation_delay4 = pygame.time.get_ticks()
    spell_trap_card_activation_delay5 = pygame.time.get_ticks()
    
    spell_trap_card_activation_delay = pygame.time.get_ticks()
    activating_spell_trap_card = False
    spell_trap_card_activation_delay2 = pygame.time.get_ticks()
    #pygame.draw.rect(screen, Settings.RED, [673.5, 137.5, 248, 360], 0)
    activated_spell_or_trap_card_display = False
    activated_card_center_screen_img = CardImage(screen, "", "images/cards/cover.jpg", 673.5, 137.5, None)
    active_field_card_display = False
    active_field_card = None
    active_field_card_img = None
    atk_def_font = pygame.font.SysFont("Trebuchet MS", 20)    
    egyptian_background = pygame.image.load("images/egyptian_background.jpg")
    hand_card_index = None
    tunde = False
    bok = False
    ai_delay_start_timer = pygame.time.get_ticks()
    ai_playing = False
    ai_card_to_play = None
    ai_guardian_star_timer = pygame.time.get_ticks()
    ai_end_phase_timer = pygame.time.get_ticks()
    ai_end_phase = False
    ai_turn = False
    dog = pygame.time.get_ticks()  
    ai_selecting_card_in_hand = False
    ai_selected_card_in_hand_index = None
    eebeeto = pygame.time.get_ticks()
    ai_monster_zones_select = []
    zone_choice = None
    ai_field_actions = False
    ai_field_actions2 = False
    feck = pygame.time.get_ticks() 
    ai_monster_zones_ok = [False, False, False, False, False]
    ai_spell_zones_ok = [False, False, False, False, False]
    
    aa = pygame.time.get_ticks()
    bb = pygame.time.get_ticks()
    cc = pygame.time.get_ticks()
    dd = pygame.time.get_ticks()
    ee = pygame.time.get_ticks()
    
    ff = pygame.time.get_ticks()
    gg = pygame.time.get_ticks()
    hh = pygame.time.get_ticks()
    ii = pygame.time.get_ticks()
    jj = pygame.time.get_ticks() 
    z = pygame.time.get_ticks() 
    ai_spell_index = 0
    current_player_fusing = False
    fuse_up_ctr = 0
    fuse_down_ctr = 0
    up_fusion_order_box_array = []
    down_fusion_order_box_array = []
    fused_card = None
    hci_2 = None
    fusion_indices = None
    ai_selecting_card_in_hand2 = False
    ai_fuse_up_ctr, ai_fuse_down_ctr = 0, 0
    ai_fuse_card_ok = [False for x in range(5)]
    ai_fusing_flag = False
    provisional_fused_card = None
    actions3 = False
    ai_end_monsters_turn = False
    trap_activation_timer = pygame.time.get_ticks()
    trap_activating = False
    trap_activating_effect = False
    player_trap_selecting = False
    attacking_zone = None
    current_monster = None
    enemy_card = None
    trap_select_active = False
    player_activated_trap = None
    trapping = False
    summoning_trap_activation = False
    bobby = pygame.time.get_ticks()
    flagger = False
    ai_main_phase_end = False
    player_summoning_trap = False
    ai_activating_spell = False
    target_equip_mons_zone = -1
    
    ai_spell_spacing_timer = pygame.time.get_ticks()   
    ai_spell_spacing_timer_active = False 

    activate_delay = False
    activate_delay_timer = pygame.time.get_ticks()  
    activate_delay_duration = 0
    
    activating_from_hand = False
    select_player_equip_target = False
    player_valid_monsters = []
    player_equip_target_monster = None
    
    player_activating_spell_from_field = False
    spell_on_field_activation_delay = 0
    spell_on_field_activation_delay_timer_before = pygame.time.get_ticks()
    
    fuac = pygame.time.get_ticks() #test
    endGame = False
    endGameDelay = False
    endGameDelay2 = False
    
    endGameFlag = False
    
    endGameSurface = pygame.Surface((1270, 635), pygame.SRCALPHA)
    endGameSurface.fill((0,0,0,128)) 
    
    end_screen_delay_timer1 = pygame.time.get_ticks()
    end_screen_delay_timer2 = pygame.time.get_ticks()
    
    you_win_text = win_lose_font.render("YOU", True, Settings.RED)
    you_win_text_width, you_win_text_height = win_lose_font.size("YOU") 
    
    you_win_text_x = 635 - (you_win_text_width / 2)

    you_lose_text = win_lose_font.render("YOU", True, Settings.BLUE)
    you_lose_text_width, you_lose_text_height = win_lose_font.size("YOU")

    you_lose_text_x = 635 - (you_lose_text_width / 2)

    win_text = win_lose_font.render("WIN", True, Settings.RED)
    win_text_width, win_text_height = win_lose_font.size("WIN") 

    win_text_x = 635 - (win_text_width / 2)

    lose_text = win_lose_font.render("LOSE", True, Settings.BLUE)
    lose_text_width, lose_text_height = win_lose_font.size("LOSE") 

    lose_text_x = 635 - (lose_text_width / 2)
    
    upper_display_text = None
    upper_display_x = None
    
    upper_x = -10
    lower_x = 1270
    
    exit_screen_timer = pygame.time.get_ticks()
    activated_spell_or_trap_card_display_equip = False
    gbagbo = pygame.time.get_ticks()

    while not endGameFlag:        
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit() 
            elif event.type == myevent:
                if V == 0:
                    V = 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if current_player_fusing:
                        if (fuse_down_ctr > 1 or fuse_up_ctr > 1) or (fuse_down_ctr == 1 and fuse_up_ctr == 1):
                            zone_display_on = True
                            
                            selected_card_option_box.card = None
                            selected_card_option_box.options = []
                            selecting_zone = True   
                            
                            #fused_card = gf.fuseCards(up_fusion_order_box_array[0].card, down_fusion_order_box_array[0].card, game_instance.current_turn_player, screen)
                            
                elif event.key == pygame.K_ESCAPE:
                    endGame = True
                    if game_instance.current_turn_player.is_attacking:
                        game_instance.current_turn_player.is_attacking = False
                        
                        if game_instance.current_turn_player == game_instance.player:
                            for zone in ai_monster_zones_array:
                                if zone.card_img != None:
                                    zone.area.fill((0, 0, 0, 0))
                        else:
                            for zone in player_monster_zones_array:
                                if zone.card_img != None:
                                    zone.area.fill((0, 0, 0, 0))
                     
                    fuse_down_ctr = 0
                    fuse_up_ctr = 0
                    up_fusion_order_box_array = []
                    down_fusion_order_box_array = []
                    current_player_fusing = False
                    fused_card = None
                    
                    if game_instance.current_turn_player == game_instance.player:
                        my_array = game_instance.player.cards_gui
                    else:
                        my_array = game_instance.ai.cards_gui
                        
                    for card in my_array:
                        if card.is_fusing:
                            card.rect.y = 540
                            card.is_fusing = False
                            card.is_fusing_up = False
                            card.is_fusing_down = False
                     
                     
                    if selecting_zone:
                        for card in cards:
                            card.is_visible = True
                        selecting_zone = False
                        zone_display_on = False
                        spell_zone_display_on = False
                        guardian_star_display = False
                        selected_card = None
                        selection_star1 = None
                        selection_star1 = None
        
        screen.fill(Settings.DARK_BLUE)
        screen.blit(egyptian_background, [248, 0])
        card_surface.blit()
        card_desc_surface.blit()
        pygame.draw.rect(card_desc_surface.area, Settings.LIGHT_BLUE, [17.5, 17.5, 290, 22], 1)
        
        mouse_click_status = pygame.mouse.get_pressed()
        
        if game_instance.current_turn_player == game_instance.player: 
            if not main_phase_block.is_active and battle_phase_block.is_active:  
                if not game_instance.current_turn_player.is_attacking and not select_player_equip_target:
                    if end_phase_block.rect.collidepoint(mouse_pos) and not game_instance.game_over:
                        end_phase_block.area.fill(Settings.YELLOW)
                        if mouse_click_status[0] == 1:                      
                            game_instance.player.set_attacking_monster(None)
                            if game_instance.current_turn_player == game_instance.player:
                                my_array = game_instance.player.cards_gui
                            else:
                                my_array = game_instance.ai.cards_gui
                                
                            for card in my_array:
                                if card.is_fusing:
                                    card.rect.y = 540
                                    card.is_fusing = False
                                    card.is_fusing_up = False
                                    card.is_fusing_down = False                                                                  
                            summoning_trap_activation = False
                            gf.fade(game_settings.screen_width, game_settings.screen_height, screen, screen, flag=False)
                            gf.endPhaseCardsInHand(game_instance, cards, hand_cards_status)                      
                            gf.resetMisc(selected_field_card_option_box, selected_field_spell_trap_card_option_box, card_layout, card_info_panel)
                            selected_field_card = None
                            gf.endPhaseSendArray(game_instance, player_monster_zones_array, ai_monster_zones_array)
                            gf.changePhaseBlockStates(main_phase_block, battle_phase_block, end_phase_block)

                            game_instance.gameLoop()                       
                            hand_card_index = None
                            hci_2 = None
                            gf.resetFieldArrays(player_monster_zones_array, player_spell_and_trap_zones_array, player_graveyard_gui, player_deck_gui, player_field_gui, lp_font)
                            gf.resetFieldArrays(ai_monster_zones_array, ai_spell_and_trap_zones_array, ai_graveyard_gui, ai_deck_gui, ai_field_gui, lp_font)                                             
                            cards = gf.endPhaseBuildCardsInHand(game_instance, cards, ai_delay_start_timer, screen)   
                            bok = False
                            fused_card = None
                            for zone in ai_monster_zones_array:
                                zone.disabled_for_ai = False
                    else:
                        end_phase_block.area.fill(Settings.WHITE)

                    
        #if ai_turn:;
        if game_instance.current_turn_player == game_instance.ai and not game_instance.game_over:
            if not bok:
                for card in cards:
                    card.is_visible = True 
                ai_delay_start_timer_difference = pygame.time.get_ticks()

                time_waited = 5000
                if game_instance.current_turn == 1:
                    time_waited = 2000
                
                if ai_delay_start_timer_difference - ai_delay_start_timer >= time_waited:     
                    #cards = gf.aiEndPhase(game_instance)
                    #pass
                    tunde = True
                    bok = True
          
            if tunde:
                q = pygame.time.get_ticks()    
                dog = pygame.time.get_ticks()    
                if q - ai_delay_start_timer_difference >= 2500:   
                    tunde = False
                    #bok = False     
                    ai_turn = True
                    
                    if not game_instance.ai.has_played_a_card_this_turn:
                        ai_choice, provisional_fused_card = gf.getAICardToPlay(game_instance, ai_field_gui, player_monster_zones_array, ai_monster_zones_array, screen) 
                        if(type(ai_choice) is not list):
                            ai_card_to_play = ai_choice
                        else:
                            fusion_indices = ai_choice
                    else:
                        ai_card_to_play = None
                    
                    ai_selecting_card_in_hand = True             

                    
            if ai_turn:       
                x = pygame.time.get_ticks()

                ai_wait = 2800
                if fusion_indices:
                    if len(fusion_indices) == 4:
                        ai_wait = 5000
                    elif len(fusion_indices) == 3:
                        ai_wait = 4500
                    else:
                        ai_wait = 4000
                if x - q >= ai_wait:#2800:
                    zone_display_on = True
                    ai_turn = False
                    eebeeto = pygame.time.get_ticks()
                    
                    if ai_card_to_play:
                        if ai_card_to_play.card.card_type == "Monster":
                            if not gf.areMonsterZonesFull(ai_monster_zones_array):
                                ai_monster_zones_select = gf.getAiMonsterZoneToPlay(ai_monster_zones_array, screen, gf.getEmptyAiMonsterZone, ai_card_to_play, game_instance)
                            else:
                                ai_monster_zones_select = gf.getAiMonsterZoneToPlay(ai_monster_zones_array, screen, gf.getWeakestAiMonster, ai_card_to_play, game_instance)
                        elif ai_card_to_play.card.card_type == "Spell" or ai_card_to_play.card.card_type == "Trap" and ai_card_to_play.card.spell_or_trap_type != "Field":
                            ai_monster_zones_select = [zone.index for zone in ai_spell_and_trap_zones_array if zone.zone.getNumOfCardsContained() == 0]
                    else:
                        if not gf.areMonsterZonesFull(ai_monster_zones_array):
                            ai_monster_zones_select = gf.getAiMonsterZoneToPlay(ai_monster_zones_array, screen, gf.getEmptyAiMonsterZone, provisional_fused_card, game_instance)
                        else:
                            ai_monster_zones_select = gf.getAiMonsterZoneToPlay(ai_monster_zones_array, screen, gf.getWeakestAiMonster, provisional_fused_card, game_instance)
                        #ai_monster_zones_select = [zone.index for zone in ai_monster_zones_array if zone.zone.getNumOfCardsContained() == 0]
                    
                    zone_choice = random.choice(ai_monster_zones_select)

            
            if zone_display_on:
                vg = pygame.time.get_ticks()               
                
                wait_time = 2800
                
                if ai_card_to_play:
                    if ai_card_to_play.card.card_type == "Spell":
                        if ai_card_to_play.card.spell_or_trap_type == "Field":
                            wait_time = 0
                
                if vg - eebeeto >= wait_time:
                    zone_display_on = False

                    for zone in ai_spell_and_trap_zones_array:
                        if zone.zone.getNumOfCardsContained() != 1:
                            zone.area.fill((0, 0, 0, 0))
                            zone.blit() 
                    
                    if gf.isHandReady(cards):
                        ai_selecting_card_in_hand = False
                        if not ai_card_to_play and not ai_fusing_flag:
                            up_fusion_cards = [up_fusion_order_box_array[x].card for x in range(len(up_fusion_order_box_array))]
                            down_fusion_cards = [down_fusion_order_box_array[x].card for x in range(len(down_fusion_order_box_array))]
                            for card in up_fusion_cards + down_fusion_cards:
                                card.card.flip()
                            if ai_monster_zones_array[zone_choice].zone.getNumOfCardsContained() > 0:
                            
                                zone_monster_card = ai_monster_zones_array[zone_choice].zone.getCardByIndex(0)
                                zone_monster_img = CardImage(screen, zone_monster_card.card_type, zone_monster_card.img, 0, 0, zone_monster_card)
                                zone_monster_img.card.is_set = False
                                #zone_monster_card.sendToGrave(game_instance.ai)
                            
                                last_monster_fused = [zone_monster_img]
                            else:
                                last_monster_fused = []
                            fused_card, created_cards_array = gf.getFusionResultPrep(up_fusion_cards.copy(), down_fusion_cards.copy(), last_monster_fused, game_instance.current_turn_player, screen, True)

                            all_enemy_monsters = [zone for zone in player_monster_zones_array if zone.zone.getNumOfCardsContained() == 1 and zone.zone.getCardByIndex(0).card_type == "Monster"]
                            fused_card.card.guardian_star = gf.returnBestGuardianStar(fused_card.card.guardian_star_list, all_enemy_monsters)
                            fused_card.card.in_atk_position = True
                            gf.fade(game_settings.screen_width, game_settings.screen_height, screen, screen, flag=False)
                            for result in created_cards_array:
                                fusionScreen(fused_card, result, screen, clock, game_instance, game_settings)

                            star_name_1 = fused_card.card.guardian_star_list[0].name
                            star_name_2 = fused_card.card.guardian_star_list[1].name
                            selection_star1 = gf.getGuardianStarImg(star_name_1)
                            selection_star2 = gf.getGuardianStarImg(star_name_2)
                            
                            for choice in [left_gs_selection] + [right_gs_selection]:
                                if fused_card.card.guardian_star.gs_id == fused_card.card.guardian_star_list[choice.index].gs_id:
                                    choice.area.fill(Settings.YELLOW)
                                else:
                                    choice.area.fill(Settings.WHITE)
                            guardian_star_display = True
                            ai_fusing_flag = True
                            ai_playing = True                   
                            ai_guardian_star_timer = pygame.time.get_ticks()    
                            
                            for card in cards:
                                card.is_visible = False 

                        if ai_card_to_play:
                            if ai_card_to_play.card.card_type == "Monster":     

                                ai_card_to_play.card.is_set = True
                                guardian_star_display = True
                                star_name_1 = ai_card_to_play.card.guardian_star_list[0].name
                                star_name_2 = ai_card_to_play.card.guardian_star_list[1].name
                                selection_star1 = gf.getGuardianStarImg(star_name_1)
                                selection_star2 = gf.getGuardianStarImg(star_name_2)
                                
                                for choice in [left_gs_selection] + [right_gs_selection]:
                                    if ai_card_to_play.card.guardian_star.gs_id == ai_card_to_play.card.guardian_star_list[choice.index].gs_id:
                                        choice.area.fill(Settings.YELLOW)
                                    else:
                                        choice.area.fill(Settings.WHITE)
            
                            for card in cards:
                                card.is_visible = False 
                                
                            fuse_down_ctr = 0
                            fuse_up_ctr = 0
                            up_fusion_order_box_array = []
                            down_fusion_order_box_array = []
                            ai_playing = True                   
                            ai_guardian_star_timer = pygame.time.get_ticks()            

            if ai_playing:
                fuse_down_ctr = 0
                fuse_up_ctr = 0
                up_fusion_order_box_array = []
                down_fusion_order_box_array = []

                q = pygame.time.get_ticks()  
                if q - ai_guardian_star_timer >= 1000:

                    pygame.draw.rect(screen, Settings.RED, [hand_cards_status[zone_choice]["x_position"], 540, 149, 216], 5) 
                    #cards[ai_card_to_play.card_index].contained = False
                    #cards.pop(ai_card_to_play.card_index)                   
                    #hand_cards_status[ai_card_to_play.card_index]["card"] = None  

                    game_instance.ai.cards_gui = cards
                    if ai_card_to_play:
                        if ai_card_to_play.card.card_type == "Monster":
                            ai_monster_zones_array[zone_choice].zone.placeCardToZone(ai_card_to_play.card)
                            ai_monster_zones_array[zone_choice].setZoneCardImg()
                            
                            available_traps = gf.trap_trigger_check(ai_card_to_play.card, game_instance.current_turn_player.opponent, game_instance, attacked_monster=None)                                 
                            if len(available_traps) > 0:
                                player_summoning_trap = True
                                selected_field_card = ai_card_to_play.card
                                trap_tooltip_active = True
                                player_trap_selecting = True
                            else:
                                ai_main_phase_end = True
                                    
                        else:
                            if ai_card_to_play.card.spell_or_trap_type == "Field":
                                ai_field_gui.zone.placeCardToZone(ai_card_to_play.card)
                                ai_field_gui.setZoneCardImg()
                                selected_field_card = ai_card_to_play.card
                                
                                
                                if player_field_gui.zone.getNumOfCardsContained() == 1:
                                    if not player_field_gui.zone.getCardByIndex(0).is_set:
                                        player_field_gui.zone.removeCardFromZone(player_field_gui.zone.getCardByIndex(0), "To graveyard")
                                        player_field_gui.setZoneCardImg()
                                        player_graveyard_gui.setZoneCardImg(lp_font)
                                        active_field_card = None
                                        active_field_card_display = False
                                        
                                active_field_card = selected_field_card
                                activated_spell_or_trap_card_display = True
                                activated_card_center_screen_img.changeImg(active_field_card.img)
                                activated_card_center_screen_img.card_type = active_field_card.card_type
                                
                                activating_from_hand = True
                            else:
                                ai_spell_and_trap_zones_array[zone_choice].zone.placeCardToZone(ai_card_to_play.card)
                                ai_spell_and_trap_zones_array[zone_choice].setZoneCardImg()
                                
                                if not ai_card_to_play.card.set_for_ai:
                                    selected_field_card = ai_card_to_play.card
                                    activated_spell_or_trap_card_display = True
                                    activating_from_hand = True
                                
                                activated_card_center_screen_img.changeImg(ai_card_to_play.card.img)
                                activated_card_center_screen_img.card_type = ai_card_to_play.card.card_type
                            activated_card_center_screen_img.setRect(673.5, 137.5)
                            spell_trap_card_activation_delay4 = pygame.time.get_ticks()
                            
                            if not activating_from_hand == True:
                                ai_main_phase_end = True
                        
                        for card in game_instance.ai.cards_in_hand:
                            if card == ai_card_to_play.card:
                                game_instance.ai.cards_in_hand.remove(card)
                                
                        for card in cards:
                            if card == ai_card_to_play:
                                cards.remove(card)
                                
                        game_instance.ai.cards_gui = cards
                    else:

                        ai_monster_zones_array[zone_choice].zone.placeCardToZone(fused_card.card)
                        ai_monster_zones_array[zone_choice].setZoneCardImg()
                                
                        available_traps = gf.trap_trigger_check(fused_card.card, game_instance.current_turn_player.opponent, game_instance, attacked_monster=None)                                 
                        if len(available_traps) > 0:
                            player_summoning_trap = True
                            selected_field_card = fused_card.card
                            trap_tooltip_active = True
                            player_trap_selecting = True
                                    
                                
                        for card in game_instance.ai.cards_gui.copy():
                            if card.is_fusing_up or card.is_fusing_down:
                                mycard = card.card
                                game_instance.ai.cards_gui.remove(card)
                                if mycard != fused_card.card:
                                    mycard.sendToGrave(game_instance.ai)
                                game_instance.ai.cards_in_hand.remove(mycard) 
                                for x in cards.copy():
                                    if x == card:
                                        x.contained = False
                                        #cards.remove(x)
                                        break
                                        
                                for y in hand_cards_status:
                                    if y["card"] == card:
                                        y["card"] = None
                                        break
                        
                        ai_graveyard_gui.setZoneCardImg(lp_font)
                        fuse_down_ctr = 0
                        fuse_up_ctr = 0
                        up_fusion_order_box_array = []
                        down_fusion_order_box_array = []
                        #zone_display_on = False
                    
                    main_phase_block.changeActiveStatus()
                    main_phase_block.changeColor()
                    
                    battle_phase_block.changeActiveStatus()
                    battle_phase_block.changeColor()  
                   
                        
                    game_instance.current_turn_player.has_played_a_card_this_turn = True
                    guardian_star_display = False
                    ai_playing = False
                    ai_field_actions = True
                    ai_main_phase_end = True

                
            if ai_end_phase and not game_instance.game_over:
                q = pygame.time.get_ticks()  
                if q - ai_end_phase_timer >= 1500:
                    current_player_fusing = False
                    provisional_fused_card = None
                    fused_card = None
                    ai_card_to_play = None
                    fusion_indices = None
                    ai_fusing_flag = False
                    ai_fuse_card_ok = [False for x in range(5)]
                    ai_end_monsters_turn = False
                    selected_field_card = None
                    trap_tooltip_active = False
                    ai_card_to_play = None
                    ai_fuse_down_ctr = 0
                    ai_fuse_up_ctr = 0
                    up_fusion_order_box_array = []
                    down_fusion_order_box_array = []
                    game_instance.ai.set_attacking_monster(None)
                    ai_main_phase_end = False
                    game_instance.ai.is_attacking = False
                    
                    if game_instance.current_turn_player == game_instance.player:
                        my_array = game_instance.player.cards_gui
                    else:
                        my_array = game_instance.ai.cards_gui
                        
                    for card in my_array:
                        if card.is_fusing:
                            card.rect.y = 540
                            card.is_fusing = False
                            card.is_fusing_up = False
                            card.is_fusing_down = False
                
                    attacking_zone = None
                    ai_turn = False
                    gf.fade(game_settings.screen_width, game_settings.screen_height, screen, screen, flag=False)
                    gf.endPhaseCardsInHand(game_instance, cards, hand_cards_status)                      
                    gf.resetMisc(selected_field_card_option_box, selected_field_spell_trap_card_option_box, card_layout, card_info_panel)
                    summoning_trap_activation = False
                    gf.endPhaseSendArray(game_instance, player_monster_zones_array, ai_monster_zones_array)
                    gf.changePhaseBlockStates(main_phase_block, battle_phase_block, end_phase_block)
                    
                    game_instance.gameLoop()                       
                    
                    gf.resetFieldArrays(player_monster_zones_array, player_spell_and_trap_zones_array, player_graveyard_gui, player_deck_gui, player_field_gui, lp_font)
                    gf.resetFieldArrays(ai_monster_zones_array, ai_spell_and_trap_zones_array, ai_graveyard_gui, ai_deck_gui, ai_field_gui, lp_font)                                             
                    cards = gf.endPhaseBuildCardsInHand(game_instance, cards, ai_delay_start_timer, screen)   
                    
                    for zone in ai_monster_zones_array:
                        zone.disabled_for_ai = False
                    
                    ai_end_phase = False
                    
                    ai_monster_zones_ok = [False, False, False, False, False]
                    ai_spell_zones_ok = [False, False, False, False, False]
    
                    aa = pygame.time.get_ticks()
                    bb = pygame.time.get_ticks()
                    cc = pygame.time.get_ticks()
                    dd = pygame.time.get_ticks()
                    ee = pygame.time.get_ticks()
                    
                    ff = pygame.time.get_ticks()
                    gg = pygame.time.get_ticks()
                    hh = pygame.time.get_ticks()
                    ii = pygame.time.get_ticks()
                    jj = pygame.time.get_ticks()                             
      
        if select_player_equip_target:
            for zone in player_monster_zones_array:
                 if zone.zone.getNumOfCardsContained() == 1:
                    if zone.zone.getCardByIndex(0) in player_valid_monsters:
                        zone.area.fill((0, 255, 0))
                        zone.blit(lp_font)
              
                    if zone.rect.collidepoint(mouse_pos) and not game_instance.game_over:           
                        if mouse_click_status[0] == 1: 
                            select_player_equip_target = False
                            player_equip_target_monster = zone.zone.getCardByIndex(0)
                            zone.area.fill((0, 0, 0, 0))
                            activate_delay = True                         
                            activate_delay_timer = pygame.time.get_ticks() 
                            
                            player_equip_target_monster.is_set = False
                            for zone in player_monster_zones_array:
                                zone.setZoneCardImg()
                            selected_field_card.equip(player_equip_target_monster)
   
        if game_instance.current_turn_player.is_attacking:
            if game_instance.current_turn_player == game_instance.player:
          
                if not gf.isEnemyMonsterZoneEmpty(ai_monster_zones_array):
                    for zone in ai_monster_zones_array:
                        if zone.card_img != None:
                            zone.area.fill(Settings.GREEN)
                            zone.blit(lp_font)   
                else:
                    game_instance.current_turn_player.attacking_monster = selected_field_card

                    available_traps = gf.trap_trigger_check(selected_field_card, game_instance.current_turn_player.opponent, game_instance, attacked_monster=None)                                
                    if len(available_traps) > 0:
                        ai_trap_to_be_used = gf.get_ai_trap_to_be_used(selected_field_card, available_traps, game_instance)   

                        if ai_trap_to_be_used:   
                            #print(ai_trap_to_be_used)
                            ai_trap_to_be_used.is_set = False
                            
                            for zone in ai_spell_and_trap_zones_array:
                                zone.setZoneCardImg()
                            
                            trap_activation_timer = pygame.time.get_ticks()
                            game_instance.current_turn_player.is_attacking = False
                            
                            activated_card_center_screen_img.changeImg(ai_trap_to_be_used.img)
                            activated_card_center_screen_img.card_type = ai_trap_to_be_used.card_type
                            activated_card_center_screen_img.setRect(673.5, 137.5)
                            spell_trap_card_activation_delay = pygame.time.get_ticks()
                            activating_spell_trap_card = True
                            trap_activating = True
                        else:     
                            gf.fade(game_settings.screen_width, game_settings.screen_height, screen, screen, flag=False)
                            winning_card = battleScreen(game_settings, game_instance, clock, screen, selected_field_card, None, selected_field_card_option_box, lp_font) 
               
                            for card in player_graveyard_gui.zone.getCards() + ai_graveyard_gui.zone.getCards():
                                if card.card_type == "Monster":
                                    card.resetStatus()
                                
                            gf.calculate_life_points(winning_card, game_instance, xhealth, phealth)                                           
                    else:
                        gf.fade(game_settings.screen_width, game_settings.screen_height, screen, screen, flag=False)                          
                        winning_card = battleScreen(game_settings, game_instance, clock, screen, selected_field_card, None, selected_field_card_option_box, lp_font) 
           
                        for card in player_graveyard_gui.zone.getCards() + ai_graveyard_gui.zone.getCards():
                            if card.card_type == "Monster":
                                card.resetStatus()
                            
                        gf.calculate_life_points(winning_card, game_instance, xhealth, phealth)  

                    if game_instance.player.life_points == 0:
                        endGame = True
                        game_instance.endGame("No life points left.", game_instance.player)
                        #goToLastSavedScreen(player_dict, screen, game_settings)
                    elif game_instance.ai.life_points == 0:
                        endGame = True
                        game_instance.endGame("No life points left.", game_instance.ai)
                        #goToLastSavedScreen(player_dict, screen, game_settings
                        
   
        if game_instance.current_turn_player == game_instance.player:
            if selected_field_card_option_box.card != None:       
                for option in selected_field_card_option_box.options:
                    option.setPos(game_instance.current_turn, selected_field_card_option_box.card.zone.getCardByIndex(0))
                    #selected_field_card_options_pointers = (mouse_pos[0]-selected_field_card_option_box.rect.x, mouse_pos[1]-selected_field_card_option_box.rect.y)
                    if option.rect.collidepoint(selected_field_card_options_pointers) and not game_instance.game_over:
                        #whock = True
                        option.setBgColor(Settings.GOLD)
                        selected_field_zone = selected_field_card_option_box.card
                        if selected_field_zone:    
                            if not trap_activating_effect and not flagger:
                                if mouse_click_status[0] == 1:
                                    selected_field_card = selected_field_card_option_box.card.zone.getCardByIndex(0)
                                
                                    selected_field_card_option_box.options = []
                                    if option.text == "Attack":
                                        select_attack_target_delay_before = pygame.time.get_ticks()
                                        if selected_field_card.in_atk_position:
                                            game_instance.current_turn_player.is_attacking = True                                  
                                    else:
                                        if not has_happened:
                                            selected_field_card.in_atk_position = not selected_field_card.in_atk_position
                                            selected_field_zone.setZoneCardImg()
                                            selected_field_card_option_box.options = []
                                            #selected_field_card_option_box.getArea(game_instance.current_turn)
                                            has_happened = True
                                            
                                    for zone in player_monster_zones_array + ai_monster_zones_array + player_spell_and_trap_zones_array + ai_spell_and_trap_zones_array:
                                        zone.setZoneCardImg()
                                        
                                    equip_zones = [zone for zone in player_spell_and_trap_zones_array + ai_spell_and_trap_zones_array if zone.zone.getNumOfCardsContained() == 1 and zone.zone.getCardByIndex(0).spell_or_trap_type == "Equip" and zone.zone.getCardByIndex(0).equipped_monster]                          
                                    for zone in equip_zones:
                                        if zone.zone.getCardByIndex(0).equipped_monster:
                                            if zone.zone.getCardByIndex(0).equipped_monster.current_zone == None:
                                                zone.zone.removeCardFromZone(zone.zone.getCardByIndex(0), "To graveyard")
                                                zone.setZoneCardImg()        
                                    
                                    player_field_gui.setZoneCardImg()
                                    ai_field_gui.setZoneCardImg()
                                    player_graveyard_gui.setZoneCardImg(lp_font)
                                    ai_graveyard_gui.setZoneCardImg(lp_font)                                                           
                                                            
                                    break
                                if mouse_click_status[0] == 0:
                                    if option.text != "Attack":
                                        has_happened = False
                                        break
                    else:
                        option.setBgColor(Settings.LIGHT_GRAY) 
   
      
        if active_field_card_display:
            screen.blit(active_field_card_img, [474.5, 74.5])
            #pygame.draw.rect(screen, Settings.RED, [474.5, 74.5, 645, 460], 0)
                              
        for zone in player_monster_zones_array:
            zone.blit(atk_def_font)
            gf.changeDisplayCard(activated_spell_or_trap_card_display, select_player_equip_target, flagger, trap_activating, mouse_click_status, trapping, zone, mouse_pos, card_layout, card_info_panel, selected_field_card_option_box, game_instance.current_turn, monster_field_options, game_instance, battle_phase_block.is_active, selected_field_card)
            
        for zone in player_spell_and_trap_zones_array:
            if trapping:
                if not player_activated_trap:
                    player_activated_trap = gf.changeDisplayCard(activated_spell_or_trap_card_display, select_player_equip_target, flagger, trap_activating, mouse_click_status, trapping, zone, mouse_pos, card_layout, card_info_panel, selected_field_spell_trap_card_option_box, game_instance.current_turn, spell_field_options, game_instance, battle_phase_block.is_active, selected_field_card)
                  
                else:
                    trap_activating = True
                    ai_trap_to_be_used = player_activated_trap
                    trapping = False
                    player_activated_trap = None
                    fuac = pygame.time.get_ticks()
                    activated_card_center_screen_img.changeImg(ai_trap_to_be_used.img)
                    activated_card_center_screen_img.card_type = ai_trap_to_be_used.card_type
                    activated_card_center_screen_img.setRect(673.5, 137.5)
                    spell_trap_card_activation_delay = pygame.time.get_ticks()
                    activating_spell_trap_card = True
            else:
                gf.changeDisplayCard(activated_spell_or_trap_card_display, select_player_equip_target, flagger, trap_activating, mouse_click_status, trapping, zone, mouse_pos, card_layout, card_info_panel, selected_field_spell_trap_card_option_box, game_instance.current_turn, spell_field_options, game_instance, battle_phase_block.is_active, selected_field_card)
            zone.blit()
        
        for zone in ai_spell_and_trap_zones_array:
            zone.blit()
            gf.changeDisplayCard(activated_spell_or_trap_card_display, select_player_equip_target, flagger, trap_activating, mouse_click_status, trapping, zone, mouse_pos, card_layout, card_info_panel, selected_field_spell_trap_card_option_box, game_instance.current_turn, spell_field_options, game_instance, battle_phase_block.is_active, selected_field_card)
            
        for zone in ai_monster_zones_array:
            zone.blit(atk_def_font)
            gf.changeDisplayCard(activated_spell_or_trap_card_display, select_player_equip_target, flagger, trap_activating, mouse_click_status, trapping, zone, mouse_pos, card_layout, card_info_panel, selected_field_card_option_box, game_instance.current_turn, monster_field_options, game_instance, battle_phase_block.is_active, selected_field_card)                

            
        player_graveyard_gui.blit()
        gf.graveyardDisplay(player_graveyard_gui, card_layout, card_info_panel, mouse_pos)          
        player_deck_gui.blit()
        player_field_gui.blit()

        
        ai_graveyard_gui.blit()
        gf.graveyardDisplay(ai_graveyard_gui, card_layout, card_info_panel, mouse_pos)   
        ai_deck_gui.blit()  
        ai_field_gui.blit()  
   
        
        
        if spell_zone_display_on:
            #for zone in selected_card_spell_zone_rects:
            for i in range(len(selected_card_spell_zone_rects)):
                if game_instance.current_turn_player == game_instance.player:
                    spell_and_trap_card_zones_in_question = player_spell_and_trap_zones_array
                else:
                    spell_and_trap_card_zones_in_question = ai_spell_and_trap_zones_array
                
                if spell_and_trap_card_zones_in_question[i].zone.getNumOfCardsContained() == 0:
                    if selected_card_spell_zone_rects[i].rect.collidepoint(mouse_pos) and not game_instance.game_over:
                        selected_card_spell_zone_rects[i].color = Settings.YELLOW
                    else:
                        selected_card_spell_zone_rects[i].color = Settings.GREEN
                else:
                    selected_card_spell_zone_rects[i].color = Settings.BLACK
                selected_card_spell_zone_rects[i].area.fill(selected_card_spell_zone_rects[i].color)
                selected_card_spell_zone_rects[i].blit()
                
            if mouse_click_status[0] == 1:
                place_spell_timer_interval3 = pygame.time.get_ticks()
                if place_spell_timer_interval3 - place_spell_timer_interval2 >= 200:
                    if game_instance.current_turn_player == game_instance.player:
                        spell_zones = player_spell_and_trap_zones_array
                    else:
                        spell_zones = ai_spell_and_trap_zones_array
                    
                    for zone in spell_zones:
                        #if zone.rect.collidepoint((mouse_pos[0], mouse_pos[1]-127)):
                        if zone.rect.collidepoint(mouse_pos) and not game_instance.game_over:
                            if spell_zones[zone.index].zone.getNumOfCardsContained() == 0:
                                selected_zone = zone.index
                                selected_spell_zone = True
                                place_spell_timer = pygame.time.get_ticks()
                            break
                
        if zone_display_on:
            
            if game_instance.current_turn_player == game_instance.player:
                for zone in selected_card_monster_zone_rects:
                    if game_instance.current_turn_player == game_instance.player:
                        if zone.rect.collidepoint(mouse_pos) and not game_instance.game_over:
                            zone.color = Settings.YELLOW
                        else:
                            zone.color = Settings.GREEN
                    zone.area.fill(zone.color)
                    zone.blit()
            else:
                if ai_card_to_play:
                    if (ai_card_to_play.card.card_type == "Spell" or ai_card_to_play.card.card_type == "Trap" and not ai_card_to_play.card.spell_or_trap_type == "Field") or (ai_card_to_play.card.card_type == "Monster"):
           
                        if ai_card_to_play.card.card_type == "Monster":
                            for zone in selected_card_monster_zone_rects:
                                zone.area.fill((0, 255, 0, 100))
                                zone.blit()                         
                        else: #ai_card_to_play.card.card_type == "Spell":                   
                            for zone in ai_spell_and_trap_zones_array:
                                if zone.zone.getNumOfCardsContained() != 1:
                                    zone.area.fill((0, 255, 0, 100))
                                    zone.blit() 
                        
                        if game_instance.current_turn_player == game_instance.ai:
                            if ai_card_to_play.card_type == "Monster":
                                if vg - eebeeto >= 400 and vg - eebeeto < 800:#540
                                    pygame.draw.rect(screen, Settings.RED, [ai_monster_zones_array[0].rect.x, ai_monster_zones_array[0].rect.y, 129.2, 111.75], 5)
                                elif vg - eebeeto >= 800 and vg - eebeeto < 1200:
                                    pygame.draw.rect(screen, Settings.RED, [ai_monster_zones_array[1].rect.x, ai_monster_zones_array[1].rect.y, 129.2, 111.75], 5)
                                elif vg - eebeeto >= 1200 and vg - eebeeto < 1600:
                                    pygame.draw.rect(screen, Settings.RED, [ai_monster_zones_array[2].rect.x, ai_monster_zones_array[2].rect.y, 129.2, 111.75], 5)
                                elif vg - eebeeto >= 1600 and vg - eebeeto < 2000:
                                    pygame.draw.rect(screen, Settings.RED, [ai_monster_zones_array[3].rect.x, ai_monster_zones_array[3].rect.y, 129.2, 111.75], 5)
                                elif vg - eebeeto >= 2000 and vg - eebeeto < 2400:
                                    pygame.draw.rect(screen, Settings.RED, [ai_monster_zones_array[4].rect.x, ai_monster_zones_array[4].rect.y, 129.2, 111.75], 5)
                                elif vg - eebeeto >= 2400 and vg - eebeeto < 2800:
                                    if ai_card_to_play:
                                        pygame.draw.rect(screen, Settings.RED, [ai_monster_zones_array[zone_choice].rect.x, ai_monster_zones_array[zone_choice].rect.y, 129.2, 111.75], 5)        
                            else:
                                if ai_card_to_play.card.spell_or_trap_type == "Normal" or ai_card_to_play.card.spell_or_trap_type == "Counter" or ai_card_to_play.card.spell_or_trap_type == "Equip" or ai_card_to_play.card_type == "Trap":
                                    if vg - eebeeto >= 400 and vg - eebeeto < 800:#540
                                        pygame.draw.rect(screen, Settings.RED, [ai_spell_and_trap_zones_array[0].rect.x, ai_spell_and_trap_zones_array[0].rect.y, 129.2, 111.75], 5)
                                    elif vg - eebeeto >= 800 and vg - eebeeto < 1200:
                                        pygame.draw.rect(screen, Settings.RED, [ai_spell_and_trap_zones_array[1].rect.x, ai_spell_and_trap_zones_array[1].rect.y, 129.2, 111.75], 5)
                                    elif vg - eebeeto >= 1200 and vg - eebeeto < 1600:
                                        pygame.draw.rect(screen, Settings.RED, [ai_spell_and_trap_zones_array[2].rect.x, ai_spell_and_trap_zones_array[2].rect.y, 129.2, 111.75], 5)
                                    elif vg - eebeeto >= 1600 and vg - eebeeto < 2000:
                                        pygame.draw.rect(screen, Settings.RED, [ai_spell_and_trap_zones_array[3].rect.x, ai_spell_and_trap_zones_array[3].rect.y, 129.2, 111.75], 5)
                                    elif vg - eebeeto >= 2000 and vg - eebeeto < 2400:
                                        pygame.draw.rect(screen, Settings.RED, [ai_spell_and_trap_zones_array[4].rect.x, ai_spell_and_trap_zones_array[4].rect.y, 129.2, 111.75], 5)
                                    elif vg - eebeeto >= 2400 and vg - eebeeto < 2800:
                                        if ai_card_to_play:
                                            pygame.draw.rect(screen, Settings.RED, [ai_spell_and_trap_zones_array[zone_choice].rect.x, ai_spell_and_trap_zones_array[zone_choice].rect.y, 129.2, 111.75], 5)   
                else:
                    for zone in selected_card_monster_zone_rects:
                        zone.area.fill((0, 255, 0, 100))
                        zone.blit()   
                        
                    if vg - eebeeto >= 400 and vg - eebeeto < 800:#540
                        pygame.draw.rect(screen, Settings.RED, [ai_monster_zones_array[0].rect.x, ai_monster_zones_array[0].rect.y, 129.2, 111.75], 5)
                    elif vg - eebeeto >= 800 and vg - eebeeto < 1200:
                        pygame.draw.rect(screen, Settings.RED, [ai_monster_zones_array[1].rect.x, ai_monster_zones_array[1].rect.y, 129.2, 111.75], 5)
                    elif vg - eebeeto >= 1200 and vg - eebeeto < 1600:
                        pygame.draw.rect(screen, Settings.RED, [ai_monster_zones_array[2].rect.x, ai_monster_zones_array[2].rect.y, 129.2, 111.75], 5)
                    elif vg - eebeeto >= 1600 and vg - eebeeto < 2000:
                        pygame.draw.rect(screen, Settings.RED, [ai_monster_zones_array[3].rect.x, ai_monster_zones_array[3].rect.y, 129.2, 111.75], 5)
                    elif vg - eebeeto >= 2000 and vg - eebeeto < 2400:
                        pygame.draw.rect(screen, Settings.RED, [ai_monster_zones_array[4].rect.x, ai_monster_zones_array[4].rect.y, 129.2, 111.75], 5)
                    elif vg - eebeeto >= 2400 and vg - eebeeto < 2800:
                        pygame.draw.rect(screen, Settings.RED, [ai_monster_zones_array[zone_choice].rect.x, ai_monster_zones_array[zone_choice].rect.y, 129.2, 111.75], 5)    

            if mouse_click_status[0] == 1:
                if game_instance.current_turn_player == game_instance.player:
                    for zone in player_monster_zones_array:
                        #if zone.rect.collidepoint((mouse_pos[0], mouse_pos[1]-127)):
                        if zone.rect.collidepoint(mouse_pos) and not game_instance.game_over:
                            if not guardian_star_display:
                                selected_zone = zone.index
              #brazilianbull bobbyadore roxy cameron
                            if current_player_fusing:
    
                                current_player_fusing = False
                                selecting_zone = False
                                up_fusion_cards = [up_fusion_order_box_array[x].card for x in range(len(up_fusion_order_box_array))]
                                down_fusion_cards = [down_fusion_order_box_array[x].card for x in range(len(down_fusion_order_box_array))]
                                
                                if player_monster_zones_array[selected_zone].zone.getNumOfCardsContained() == 1:
                                    last_monster_fused_field = player_monster_zones_array[selected_zone].zone.getCardByIndex(0)
                                    player_monster_zones_array[selected_zone].zone.cards_contained = []
                                    last_monster_fused_img = CardImage(screen, last_monster_fused_field.card_type, last_monster_fused_field.img, 0, 0, last_monster_fused_field)
                                    last_monster_fused_img.card.is_set = False
                                    player_monster_zones_array[selected_zone].setZoneCardImg()
                                    last_monster_fused = [last_monster_fused_img]
                                else:
                                    last_monster_fused = []
                                
                                fused_card, created_cards_array = gf.getFusionResultPrep(up_fusion_cards.copy(), down_fusion_cards.copy(), last_monster_fused, game_instance.current_turn_player, screen, True)
                                fused_card.card.in_atk_position = True
                                gf.fade(game_settings.screen_width, game_settings.screen_height, screen, screen, flag=False)
                                for result in created_cards_array:
                                    fusionScreen(fused_card, result, screen, clock, game_instance, game_settings)
                                #current_player_fusing = False
                                if selected_zone != None:
                                    guardian_star_display = True
                                    star_name_1 = fused_card.card.guardian_star_list[0].name
                                    star_name_2 = fused_card.card.guardian_star_list[1].name
                                    selection_star1 = gf.getGuardianStarImg(star_name_1)
                                    selection_star2 = gf.getGuardianStarImg(star_name_2)
                                game_instance.player.has_played_a_card_this_turn = True
                                
                                for card in game_instance.player.cards_gui.copy():
                                    if card.is_fusing_up or card.is_fusing_down:
                                        mycard = card.card
                                        game_instance.player.cards_gui.remove(card)
                                        if mycard != fused_card.card:
                                            mycard.sendToGrave(game_instance.player)
                                        game_instance.player.cards_in_hand.remove(mycard) 
                                        for x in cards.copy():
                                            if x == card:
                                                x.contained = False
                                                #cards.remove(x)
                                                break
                                                
                                        for y in hand_cards_status:
                                            if y["card"] == card:
                                                y["card"] = None
                                                break
                                
                                player_graveyard_gui.setZoneCardImg(lp_font)
                                fuse_down_ctr = 0
                                fuse_up_ctr = 0
                                up_fusion_order_box_array = []
                                down_fusion_order_box_array = []
                                zone_display_on = False
                            else:
                                if player_monster_zones_array[selected_zone].zone.getNumOfCardsContained() == 1:
                                    selecting_zone = False
                                    
                                    last_monster_fused_field = player_monster_zones_array[selected_zone].zone.getCardByIndex(0)
                                    player_monster_zones_array[selected_zone].zone.cards_contained = []
                                    last_monster_fused_img = CardImage(screen, last_monster_fused_field.card_type, last_monster_fused_field.img, 0, 0, last_monster_fused_field)
                                    last_monster_fused_img.card.is_set = False
                                    player_monster_zones_array[selected_zone].setZoneCardImg()
                                    
                                    last_monster_fused = [last_monster_fused_img]
                                    
                                    fused_card, created_cards_array = gf.getFusionResultPrep([selected_card], [], last_monster_fused, game_instance.current_turn_player, screen, True)
                                    fused_card.card.in_atk_position = True
                                    gf.fade(game_settings.screen_width, game_settings.screen_height, screen, screen, flag=False)
                                    for result in created_cards_array:
                                        fusionScreen(fused_card, result, screen, clock, game_instance, game_settings)
                                    #current_player_fusing = False
                                    if selected_zone != None:
                                        guardian_star_display = True
                                        star_name_1 = fused_card.card.guardian_star_list[0].name
                                        star_name_2 = fused_card.card.guardian_star_list[1].name
                                        selection_star1 = gf.getGuardianStarImg(star_name_1)
                                        selection_star2 = gf.getGuardianStarImg(star_name_2)
                                    game_instance.player.has_played_a_card_this_turn = True
                                    
                                    if fused_card.card != last_monster_fused_img.card:
                                        player_graveyard_gui.zone.placeCardToZone(last_monster_fused_img.card)

                                    if fused_card.card != selected_card.card:
                                        mycard = selected_card.card
                                        mycard.sendToGrave(game_instance.player)
                                        """
                                        for card in game_instance.player.cards_gui.copy():
                                            if card == selected_card:
                                                mycard = card.card
                                                game_instance.player.cards_gui.remove(card)
                                                mycard.sendToGrave(game_instance.player)
                                                game_instance.player.cards_in_hand.remove(mycard) 
                                                for x in cards.copy():
                                                    if x == card:
                                                        x.contained = False
                                                        #cards.remove(x)
                                                        break
                                                        
                                                for y in hand_cards_status:
                                                    if y["card"] == card:
                                                        y["card"] = None
                                                        break
                                                break
                                        """
                                    
                                    player_graveyard_gui.setZoneCardImg(lp_font)
                                else:
                                    if selected_zone != None:
                                        guardian_star_display = True
                                        star_name_1 = selected_card.card.guardian_star_list[0].name
                                        star_name_2 = selected_card.card.guardian_star_list[1].name
                                        selection_star1 = gf.getGuardianStarImg(star_name_1)
                                        selection_star2 = gf.getGuardianStarImg(star_name_2)

        
        main_phase_block.blit()
        battle_phase_block.blit()
        end_phase_block.blit()
        gf.drawBoard(screen, zone_lines_tuple)
        
        for zone in player_monster_zones_array:
            gf.changeDisplayCard(activated_spell_or_trap_card_display, select_player_equip_target, flagger, trap_activating, mouse_click_status, trapping, zone, mouse_pos, card_layout, card_info_panel, selected_field_card_option_box, game_instance.current_turn, monster_field_options, game_instance, battle_phase_block.is_active, selected_field_card)       

        for zone in ai_spell_and_trap_zones_array:
            gf.changeDisplayCard(activated_spell_or_trap_card_display, select_player_equip_target, flagger, trap_activating, mouse_click_status, trapping, zone, mouse_pos, card_layout, card_info_panel, selected_field_spell_trap_card_option_box, game_instance.current_turn, spell_field_options, game_instance, battle_phase_block.is_active, selected_field_card)
            
        gf.changeDisplayCard(activated_spell_or_trap_card_display, select_player_equip_target, flagger, trap_activating, mouse_click_status, trapping, player_field_gui, mouse_pos, card_layout, card_info_panel, selected_field_spell_trap_card_option_box, game_instance.current_turn, spell_field_options, game_instance, battle_phase_block.is_active, selected_field_card)   
        gf.changeDisplayCard(activated_spell_or_trap_card_display, select_player_equip_target, flagger, trap_activating, mouse_click_status, trapping, ai_field_gui, mouse_pos, card_layout, card_info_panel, selected_field_spell_trap_card_option_box, game_instance.current_turn, spell_field_options, game_instance, battle_phase_block.is_active, selected_field_card)                  
           
        selected_field_card_options_pointers = (mouse_pos[0]-selected_field_card_option_box.rect.x, mouse_pos[1]-selected_field_card_option_box.rect.y)
        selected_field_spell_trap_card_options_pointers = (mouse_pos[0]-selected_field_spell_trap_card_option_box.rect.x, mouse_pos[1]-selected_field_spell_trap_card_option_box.rect.y)
        #if game_instance.current_turn_player == game_instance.player:
        
        if player_activating_spell_from_field:
            spell_on_field_activation_delay_timer_after = pygame.time.get_ticks()      
            if spell_on_field_activation_delay_timer_after - spell_on_field_activation_delay_timer_before >= spell_on_field_activation_delay:
                #if not selected_field_card.has_been_activated:
                selected_field_card.is_set = False
                selected_field_card.current_zone.zone_gui.setZoneCardImg()

                if selected_field_card.spell_or_trap_type == "Field":

                    enemy_field_zone = player_field_gui
                    enemy_graveyard = player_graveyard_gui

                    if game_instance.current_turn_player == game_instance.player:
                        enemy_field_zone = ai_field_gui
                        enemy_graveyard = ai_graveyard_gui

                    if enemy_field_zone.zone.getNumOfCardsContained() == 1:
                        if not enemy_field_zone.zone.getCardByIndex(0).is_set:
                            enemy_field_zone.zone.removeCardFromZone(enemy_field_zone.zone.getCardByIndex(0), "To graveyard")
                            enemy_field_zone.setZoneCardImg()
                            enemy_graveyard.setZoneCardImg(lp_font)
                            active_field_card = None

                if selected_field_card.spell_or_trap_type == "Equip":
                    select_player_equip_target = True
                    
                    player_monsters = selected_field_card.getMyFieldMonsters()
                    player_valid_monsters = selected_field_card.getValidEquipTargets(player_monsters)                            
                else:
                    activate_delay = True                         
                    activate_delay_timer = pygame.time.get_ticks() 
                player_activating_spell_from_field = False
                """
                activated_card_center_screen_img.changeImg(selected_field_card.img)
                activated_card_center_screen_img.card_type = selected_field_card.card_type
                activated_card_center_screen_img.setRect(673.5, 137.5)
                spell_trap_card_activation_delay = pygame.time.get_ticks()
                activating_spell_trap_card = True
                selected_field_card.is_set = False
                selected_field_card.current_zone.zone_gui.setZoneCardImg()
                #selected_field_card.card_owner.duelist_zone.getAttr("graveyard").zone_gui.setZoneCardImg(lp_font)
                
                active_field_card = selected_field_card
                #activated_spell_or_trap_card_display = True
                #spell_trap_card_activation_delay4 = pygame.time.get_ticks()
                                        """        
        
        if selected_field_spell_trap_card_option_box.card != None:
            for option in selected_field_spell_trap_card_option_box.options:
                #if selected_field_spell_trap_card_option_box.card.zone.getCardByIndex(0).spell_or_trap_type != "Equip":
                option.setPos()
                if option.rect.collidepoint(selected_field_spell_trap_card_options_pointers) and not game_instance.game_over:
                    option.setBgColor(Settings.GOLD)
                    selected_field_zone = selected_field_spell_trap_card_option_box.card
                    if selected_field_zone:
              
                        if not trap_activating_effect:
    
                            if mouse_click_status[0] == 1:
                                if not flagger:
                                    if option.text == "Activate":             
                                        selected_field_card = selected_field_spell_trap_card_option_box.card.zone.getCardByIndex(0)
                                        if selected_field_card.spell_or_trap_type != "Equip":
                                            spell_on_field_activation_delay = 0
                                        else:
                                            spell_on_field_activation_delay = 150
                                            
                                        spell_on_field_activation_delay_timer_before = pygame.time.get_ticks()
                                        player_activating_spell_from_field = True
                                        break
                                        

        if activating_spell_trap_card:
            flagger = True
            spell_trap_card_activation_delay2 = pygame.time.get_ticks()
            if spell_trap_card_activation_delay2-spell_trap_card_activation_delay >= 500:
                activated_spell_or_trap_card_display = True
                spell_trap_card_activation_delay4 = pygame.time.get_ticks()
                activating_spell_trap_card = False
                """
                selected_field_card.activate()
                selected_field_card.current_zone.zone_gui.setZoneCardImg(lp_font)
                selected_field_spell_trap_card_option_box.card = None
                """
             
        if trap_activating_effect and not activating_spell_trap_card:
            qqoq = pygame.time.get_ticks()
            if qqoq - trap_activation_timer > 1000:  

                gf.fade(game_settings.screen_width, game_settings.screen_height, screen, screen, flag=False)

                attacking_card = gf.get_attacking_card_status_after_trap_effect(selected_field_card, ai_trap_to_be_used)

                if attacking_card:
                    trap_fades = True
                else:
                    trap_fades = False
                
                if ai_trap_to_be_used.will_animate:
                    spell_trap_animation_screen(game_settings, clock, screen, selected_field_card, ai_trap_to_be_used, trap_fail=trap_fades)

                #attacking_card = gf.get_attacking_card_status_after_trap_effect(selected_field_card, ai_trap_to_be_used)                                                         
                
                for zone in player_monster_zones_array + ai_monster_zones_array + player_spell_and_trap_zones_array + ai_spell_and_trap_zones_array:
                    zone.setZoneCardImg()
                
                player_field_gui.setZoneCardImg()
                ai_field_gui.setZoneCardImg()
                player_graveyard_gui.setZoneCardImg(lp_font)
                ai_graveyard_gui.setZoneCardImg(lp_font)

                if attacking_card:   
                    attacking_card.is_set = False

                    for zone in ai_monster_zones_array + player_monster_zones_array:
                        zone.setZoneCardImg()
                    
                    if not summoning_trap_activation:
                        if not selected_field_card.has_attacked:
                            if ai_trap_to_be_used.name == "Magic Cylinder":
                                enemy_card = None
                                attacking_card.card_owner = game_instance.current_turn_player.opponent
                                
                            winning_card = battleScreen(game_settings, game_instance, clock, screen, selected_field_card, None, selected_field_card_option_box, lp_font) 
                       
                            for zone in player_monster_zones_array + ai_monster_zones_array + player_spell_and_trap_zones_array + ai_spell_and_trap_zones_array:
                                zone.setZoneCardImg()
                                
                            equip_zones = [zone for zone in player_spell_and_trap_zones_array + ai_spell_and_trap_zones_array if zone.zone.getNumOfCardsContained() == 1 and zone.zone.getCardByIndex(0).spell_or_trap_type == "Equip" and zone.zone.getCardByIndex(0).equipped_monster]                          
                            for zone in equip_zones:
                                if zone.zone.getCardByIndex(0).equipped_monster:
                                    if zone.zone.getCardByIndex(0).equipped_monster.current_zone == None:
                                        zone.zone.removeCardFromZone(zone.zone.getCardByIndex(0), "To graveyard")
                                        zone.setZoneCardImg()    
                            
                            player_field_gui.setZoneCardImg()
                            ai_field_gui.setZoneCardImg()
                            player_graveyard_gui.setZoneCardImg(lp_font)
                            ai_graveyard_gui.setZoneCardImg(lp_font)
                        else:
                            winning_card = selected_field_card

                        for card in player_graveyard_gui.zone.getCards() + ai_graveyard_gui.zone.getCards():
                            if card.card_type == "Monster":
                                card.resetStatus()                        
                            
                        gf.calculate_life_points(winning_card, game_instance, xhealth, phealth)
                        
                        if ai_trap_to_be_used.name == "Magic Cylinder":
                            attacking_card.card_owner = game_instance.current_turn_player
                            
                        game_instance.current_turn_player.is_attacking = False 
                else:         
                    gf.resetMisc(selected_field_card_option_box, selected_field_spell_trap_card_option_box, card_layout, card_info_panel)                                             
                    zone_display_on = False
                    game_instance.current_turn_player.is_attacking = False                                                
                    
                    if game_instance.player.life_points == 0:
                        endGame = True
                        game_instance.endGame("No life points left.", game_instance.player)
                        #goToLastSavedScreen(player_dict, screen, game_settings)
                    elif game_instance.ai.life_points == 0:
                        endGame = True
                        game_instance.endGame("No life points left.", game_instance.ai)
                        #goToLastSavedScreen(player_dict, screen, game_settings)

                    gf.reset_field(player_graveyard_gui.zone.getCards() + ai_graveyard_gui.zone.getCards(), game_instance, ai_monster_zones_array, player_monster_zones_array)
                    screen.fill(Settings.BLACK)
                    
                for zone in player_monster_zones_array:
                    zone.setZoneCardImg()
                player_graveyard_gui.setZoneCardImg(lp_font)
      
                trap_activating_effect = False
                trap_activating = False
                attacking_zone = None
                
                summoning_trap_activation = False
                
                for zone in ai_monster_zones_array:
                    if zone.zone.getNumOfCardsContained() == 1:
                        zone.zone.getCardByIndex(0).just_placed_in_field = False  

                
                if trap_select_active:
                    trap_select_active = False
                    actions3 = False
                    ai_field_actions2 = True
                    
                    for zone in player_spell_and_trap_zones_array:
                        if zone.zone.getNumOfCardsContained() == 1:
                            zone.color = (0, 0, 0, 0)
                            zone.area.fill((0, 0, 0, 0))
                            zone.blit() 
                            
                            
                if game_instance.player.life_points == 0:
                    endGame = True
                    game_instance.endGame("No life points left.", game_instance.player)
                    #goToLastSavedScreen(player_dict, screen, game_settings)
                    
                elif game_instance.ai.life_points == 0:
                    endGame = True
                    game_instance.endGame("No life points left.", game_instance.ai)
         
        if game_instance.current_turn_player.is_attacking:
            if game_instance.current_turn_player == game_instance.player:
                array = ai_monster_zones_array
            else:
                array = player_monster_zones_array
            select_attack_target_delay_after = pygame.time.get_ticks()


            for zone in array:
                if zone.card_img != None:
                    if zone.rect.collidepoint(mouse_pos) and not game_instance.game_over:
                        if mouse_click_status[0] == 1:
                            if select_attack_target_delay_after-select_attack_target_delay_before >= 100:  
                                available_traps = gf.trap_trigger_check(selected_field_card, game_instance.current_turn_player.opponent, game_instance, attacked_monster=zone.zone.getCardByIndex(0))                                 
                                if len(available_traps) > 0:
                                    ai_trap_to_be_used = gf.get_ai_trap_to_be_used(selected_field_card, available_traps, game_instance,  attacked_monster=zone.zone.getCardByIndex(0))                                      
                                    if ai_trap_to_be_used:   

                                        ai_trap_to_be_used.is_set = False
                                        
                                        for zone in ai_spell_and_trap_zones_array:
                                            zone.setZoneCardImg()
                                        
                                        trap_activation_timer = pygame.time.get_ticks()
                                        game_instance.current_turn_player.is_attacking = False
                                        
                                        activated_card_center_screen_img.changeImg(ai_trap_to_be_used.img)
                                        activated_card_center_screen_img.card_type = ai_trap_to_be_used.card_type
                                        activated_card_center_screen_img.setRect(673.5, 137.5)
                                        spell_trap_card_activation_delay = pygame.time.get_ticks()
                                        activating_spell_trap_card = True
                                        trap_activating = True       
                                    else:
                                        gf.fade(game_settings.screen_width, game_settings.screen_height, screen, screen, flag=False)
                                        winning_card = battleScreen(game_settings, game_instance, clock, screen, selected_field_card, zone.zone.getCardByIndex(0), selected_field_card_option_box, lp_font)
                                        if winning_card:
                                            if winning_card.card_owner == game_instance.player:
                                                xhealth.setHealth(game_instance.ai.life_points)
                                            else:
                                                phealth.setHealth(game_instance.player.life_points)
                                                
                                        for card in player_graveyard_gui.zone.getCards() + ai_graveyard_gui.zone.getCards():
                                            if card.card_type == "Monster":
                                                card.resetStatus()
                                        
                                        for zone in player_monster_zones_array + ai_monster_zones_array + player_spell_and_trap_zones_array + ai_spell_and_trap_zones_array:
                                            zone.setZoneCardImg()
                                            
                                        equip_zones = [zone for zone in player_spell_and_trap_zones_array + ai_spell_and_trap_zones_array if zone.zone.getNumOfCardsContained() == 1 and zone.zone.getCardByIndex(0).spell_or_trap_type == "Equip" and zone.zone.getCardByIndex(0).equipped_monster]                          
                                        for zone in equip_zones:
                                            if zone.zone.getCardByIndex(0).equipped_monster:
                                                if zone.zone.getCardByIndex(0).equipped_monster.current_zone == None:
                                                    zone.zone.removeCardFromZone(zone.zone.getCardByIndex(0), "To graveyard")
                                                    zone.setZoneCardImg()    
                            
                                        player_field_gui.setZoneCardImg()
                                        ai_field_gui.setZoneCardImg()
                                        player_graveyard_gui.setZoneCardImg(lp_font)
                                        ai_graveyard_gui.setZoneCardImg(lp_font)
                                                                                                                 
                                        
                                        if game_instance.current_turn_player == game_instance.player:
                                            for zone in ai_monster_zones_array:
                                                if zone.card_img != None:
                                                    zone.area.fill((0, 0, 0, 0))
                                        else:
                                            for zone in player_monster_zones_array:
                                                if zone.card_img != None:
                                                    zone.area.fill((0, 0, 0, 0))  
                                        screen.fill(Settings.BLACK)
                                else:
                                    gf.fade(game_settings.screen_width, game_settings.screen_height, screen, screen, flag=False)
                                    winning_card = battleScreen(game_settings, game_instance, clock, screen, selected_field_card, zone.zone.getCardByIndex(0), selected_field_card_option_box, lp_font)
                                    if winning_card:
                                        if winning_card.card_owner == game_instance.player:
                                            xhealth.setHealth(game_instance.ai.life_points)
                                        else:
                                            phealth.setHealth(game_instance.player.life_points)
                                            
                                      
                                    equip_zones = [zone for zone in player_spell_and_trap_zones_array + ai_spell_and_trap_zones_array if zone.zone.getNumOfCardsContained() == 1 and zone.zone.getCardByIndex(0).spell_or_trap_type == "Equip" and zone.zone.getCardByIndex(0).equipped_monster]                          
                                    for zone in equip_zones:
                                        if zone.zone.getCardByIndex(0).equipped_monster:
                                            if zone.zone.getCardByIndex(0).equipped_monster.current_zone == None:
                                                zone.zone.removeCardFromZone(zone.zone.getCardByIndex(0), "To graveyard")
                                                zone.setZoneCardImg()    

                                    player_graveyard_gui.setZoneCardImg(lp_font)
                                    ai_graveyard_gui.setZoneCardImg(lp_font)
                                    
                                    for zone in player_monster_zones_array + ai_monster_zones_array + player_spell_and_trap_zones_array + ai_spell_and_trap_zones_array:
                                            zone.setZoneCardImg()
                            
                                    player_field_gui.setZoneCardImg()
                                    ai_field_gui.setZoneCardImg()

                                            
                                    for card in player_graveyard_gui.zone.getCards() + ai_graveyard_gui.zone.getCards():
                                        if card.card_type == "Monster":
                                            card.resetStatus()
                                    
                                    if game_instance.player.life_points == 0:
                                        endGame = True
                                        game_instance.endGame("No life points left.", game_instance.player)
                                        #goToLastSavedScreen(player_dict, screen, game_settings)
                                        
                                    elif game_instance.ai.life_points == 0:
                                        endGame = True
                                        game_instance.endGame("No life points left.", game_instance.ai)
                                        #goToLastSavedScreen(player_dict, screen, game_settings)                                                                              
                                    
                                    if game_instance.current_turn_player == game_instance.player:
                                        for zone in ai_monster_zones_array:
                                            if zone.card_img != None:
                                                zone.area.fill((0, 0, 0, 0))
                                    else:
                                        for zone in player_monster_zones_array:
                                            if zone.card_img != None:
                                                zone.area.fill((0, 0, 0, 0))  
                                    screen.fill(Settings.BLACK)
                                    
                                  
                                if game_instance.player.life_points == 0:
                                    endGame = True
                                    game_instance.endGame("No life points left.", game_instance.player)
                                    #goToLastSavedScreen(player_dict, screen, game_settings)
                                    
                                elif game_instance.ai.life_points == 0:
                                    endGame = True
                                    game_instance.endGame("No life points left.", game_instance.ai)
                                    #goToLastSavedScreen(player_dict, screen, game_settings)     
        
        zod = (mouse_pos[0]-select_guardian_star_block.rect.x, mouse_pos[1]-select_guardian_star_block.rect.y)
        
        if selected_spell_zone:
            place_spell_timer_interval = pygame.time.get_ticks()
            
            if place_spell_timer_interval - place_spell_timer >= 100:
                if selected_zone != None and selected_card.card.spell_or_trap_type != "Field": #or selected_card.card.spell_or_trap_type == "Counter":  #and selected_card.card.card_type == "Spell"          
                    selecting_zone = False
                    spell_zone_display_on = False  
                    selected_spell_zone = False
                    ctr = 0
                    x = 0
                    for card in cards:
                        if card == selected_card:
                            x = ctr
                        else:
                            card.is_visible = True
                        ctr += 1

                    for x in range(len(game_instance.current_turn_player.cards_in_hand)):
                        if game_instance.current_turn_player.cards_in_hand[x] == selected_card.card:
                            game_instance.current_turn_player.cards_in_hand.pop(x)
                            break

                    if hand_card_index == 4:
                        real_index = 0
                    elif hand_card_index == 3:
                        real_index = 1
                    elif hand_card_index == 2:
                        real_index = 2
                    elif hand_card_index == 1:
                        real_index = 3
                    else:
                        real_index = 4
                    cards[hand_card_index].contained = False
                    cards.pop(hand_card_index)                   
                    hand_cards_status[hand_card_index]["card"] = None 

                    
                    """
                    if game_instance.current_turn < 3:
                        cards.pop(real_index)                   
                        hand_cards_status[real_index]["card"] = None
                    else:
                        cards.pop(hand_card_index)                   
                        hand_cards_status[hand_card_index]["card"] = None     
                    """
                    if game_instance.current_turn_player == game_instance.player:
                        game_instance.player.cards_gui = cards
                        player_spell_and_trap_zones_array[selected_zone].zone.placeCardToZone(selected_card.card)
                        player_spell_and_trap_zones_array[selected_zone].setZoneCardImg()
                        selected_field_card = player_spell_and_trap_zones_array[selected_zone].zone.getCardByIndex(0)
                        
                        for card in game_instance.player.cards_in_hand:
                            if card == selected_card.card:
                                game_instance.player.cards_in_hand.remove(card)
                    else:
                        game_instance.ai.cards_gui = cards
                        #if selected_field_card_option_box.card:
                        ai_spell_and_trap_zones_array[selected_zone].zone.placeCardToZone(selected_card.card)
                        ai_spell_and_trap_zones_array[selected_zone].setZoneCardImg()
                        selected_field_card = ai_spell_and_trap_zones_array[selected_zone].zone.getCardByIndex(0)
                        
                        for card in game_instance.ai.cards_in_hand:
                            if card == selected_card.card:
                                game_instance.ai.cards_in_hand.remove(card)                                                       
                     

                    game_instance.current_turn_player.has_played_a_card_this_turn = True
                    
                    main_phase_block.changeActiveStatus()
                    main_phase_block.changeColor()
                    
                    battle_phase_block.changeActiveStatus()
                    battle_phase_block.changeColor()   
                    selected_zone = None                        

                    if not selected_field_card.is_set:     
                        
                        if selected_field_card.spell_or_trap_type == "Equip":
                            select_player_equip_target = True
                            
                            player_monsters = selected_field_card.getMyFieldMonsters()
                            player_valid_monsters = selected_field_card.getValidEquipTargets(player_monsters)                            
                        else:
                            activate_delay = True                         
                            activate_delay_timer = pygame.time.get_ticks()     
                        """
                        activated_card_center_screen_img.changeImg(selected_field_card.img)
                        activated_card_center_screen_img.card_type = selected_field_card.card_type
                        activated_card_center_screen_img.setRect(673.5, 137.5)
                    
                        spell_trap_card_activation_delay = pygame.time.get_ticks()
                        activating_spell_trap_card = True
                        selected_field_card.is_set = False
                        selected_field_card.current_zone.zone_gui.setZoneCardImg()

                        activated_spell_or_trap_card_display = True
                        spell_trap_card_activation_delay4 = pygame.time.get_ticks()
                        activating_spell_trap_card = False
                        """
                    
     
        
        if guardian_star_display:
            if game_instance.current_turn_player == game_instance.player:
                for choice in [left_gs_selection] + [right_gs_selection]:
                    if choice.rect.collidepoint(zod) and not game_instance.game_over:
                        choice.color = Settings.YELLOW
                        choice.area.fill(choice.color)
                        
                        if mouse_click_status[0] == 1:
                        
                            trap_potential_monster_target = None
                        
                            if fused_card:
                                fused_card.card.guardian_star = fused_card.card.guardian_star_list[choice.index]
                                trap_potential_monster_target = fused_card.card
                            else:
                                selected_card.card.guardian_star = selected_card.card.guardian_star_list[choice.index]
                                trap_potential_monster_target = selected_card.card
                     
                            trap_potential_monster_target.just_placed_in_field = True
                     
                            selecting_zone = False
                            zone_display_on = False
                            guardian_star_display = False
                            
                            ctr = 0
                            x = 0
                            for card in cards:
                                if card == selected_card:
                                    x = ctr
                                else:
                                    card.is_visible = True
                                ctr += 1
     
                            for x in range(len(game_instance.current_turn_player.cards_in_hand)):
                                if game_instance.current_turn_player.cards_in_hand[x] == selected_card.card:
                                    game_instance.current_turn_player.cards_in_hand.pop(x)
                                    break

                            if hand_card_index == 4:
                                real_index = 0
                            elif hand_card_index == 3:
                                real_index = 1
                            elif hand_card_index == 2:
                                real_index = 2
                            elif hand_card_index == 1:
                                real_index = 3
                            else:
                                real_index = 4
                            if hand_card_index != None:    
                                cards[hand_card_index].contained = False
                                cards.pop(hand_card_index)                   
                                hand_cards_status[hand_card_index]["card"] = None  

                            if game_instance.current_turn_player == game_instance.player:
                                game_instance.player.cards_gui = cards
                                
                                if fused_card:
                                    player_monster_zones_array[selected_zone].zone.placeCardToZone(fused_card.card)
                                    player_monster_zones_array[selected_zone].setZoneCardImg()                                
                                else:
                                    player_monster_zones_array[selected_zone].zone.placeCardToZone(selected_card.card)
                                    player_monster_zones_array[selected_zone].setZoneCardImg()
                                
                                for card in game_instance.player.cards_in_hand:
                                    if card == selected_card.card:
                                        game_instance.player.cards_in_hand.remove(card)
                            else:
                                game_instance.ai.cards_gui = cards

                                if fused_card:
                                    ai_monster_zones_array[selected_zone].zone.placeCardToZone(fused_card.card)
                                    ai_monster_zones_array[selected_zone].setZoneCardImg()                                   
                                else:
                                    ai_monster_zones_array[selected_zone].zone.placeCardToZone(selected_card.card)
                                    ai_monster_zones_array[selected_zone].setZoneCardImg()

                                for card in game_instance.ai.cards_in_hand:
                                    if card == selected_card.card:
                                        game_instance.ai.cards_in_hand.remove(card)
                            
                            available_traps = gf.trap_trigger_check(trap_potential_monster_target, game_instance.current_turn_player.opponent, game_instance, attacked_monster=None)                                 
                            if len(available_traps) > 0:
                                if game_instance.current_turn_player == game_instance.player:
                                    summoning_trap_activation = True
                                    selected_field_card = trap_potential_monster_target
                                
                                    ai_trap_to_be_used = gf.get_ai_trap_to_be_used(trap_potential_monster_target, available_traps, game_instance,  attacked_monster=None)  
                                    ai_trap_to_be_used.is_set = False
                                    
                                    for zone in ai_spell_and_trap_zones_array:
                                        zone.setZoneCardImg()
                                        
                                    trap_activation_timer = pygame.time.get_ticks()
                                        
                                    activated_card_center_screen_img.changeImg(ai_trap_to_be_used.img)
                                    activated_card_center_screen_img.card_type = ai_trap_to_be_used.card_type
                                    activated_card_center_screen_img.setRect(673.5, 137.5)
                                    spell_trap_card_activation_delay = pygame.time.get_ticks()
                                    activating_spell_trap_card = True
                                    trap_activating = True              
                                else:
                                    trap_tooltip_active = True
                                    player_trap_selecting = True
                            
                            game_instance.current_turn_player.has_played_a_card_this_turn = True
                            
                            main_phase_block.changeActiveStatus()
                            main_phase_block.changeColor()
                            
                            battle_phase_block.changeActiveStatus()
                            battle_phase_block.changeColor()
                    else:
                        choice.color = Settings.WHITE
                        choice.area.fill(choice.color)
             
            select_guardian_star_block.blit()
            left_gs_selection.blit()
            right_gs_selection.blit()
            
            if selection_star1 and selection_star2:           
                rendered_star_name_1 = lp_font.render(star_name_1, True, Settings.BLACK)
                rendered_star_name_2 = lp_font.render(star_name_2, True, Settings.BLACK)
                screen.blit(rendered_star_name_1, [(select_guardian_star_block.rect.x+left_gs_selection.rect.x)+60, (select_guardian_star_block.rect.y+left_gs_selection.rect.y)+18])
                screen.blit(rendered_star_name_2, [(select_guardian_star_block.rect.x+right_gs_selection.rect.x)+60, (select_guardian_star_block.rect.y+right_gs_selection.rect.y)+18])
                
                screen.blit(selection_star1, [select_guardian_star_block.rect.x+left_gs_selection.rect.x, select_guardian_star_block.rect.y+left_gs_selection.rect.y])
                screen.blit(selection_star2, [select_guardian_star_block.rect.x+right_gs_selection.rect.x, select_guardian_star_block.rect.y+right_gs_selection.rect.y])
        
                pygame.draw.rect(screen, Settings.BLACK, [select_guardian_star_block.rect.x+25, select_guardian_star_block.rect.y+60, 150, 50], 1)
                pygame.draw.rect(screen, Settings.BLACK, [select_guardian_star_block.rect.x+175, select_guardian_star_block.rect.y+60, 150, 50], 1)
             
                screen.blit(gst_render, [(325+(945/2))-(gst_width/2), 165])
        #select_guardian_star_block = DataSurface(screen, [400, 125], (325+(945/2))-200, (game_settings.screen_height/2)-62.5, Settings.LIGHT_GRAY, opacity=True)
 
        if trap_tooltip_active:              
            for choice in [left_gs_selection] + [right_gs_selection]:
                if choice.rect.collidepoint(zod) and not game_instance.game_over:
                    choice.color = Settings.YELLOW
                    choice.area.fill(choice.color)
                    
                    if mouse_click_status[0] == 1:
                        if choice.index == 1:
                            if not ai_main_phase_end:
                                ai_main_phase_end = True
                                
                                for zone in ai_monster_zones_array:
                                    if zone.zone.getNumOfCardsContained() == 1:
                                        zone.zone.getCardByIndex(0).just_placed_in_field = False  
                        
                            trap_tooltip_active = False
                                   
                            if actions3:
                                gf.fade(game_settings.screen_width, game_settings.screen_height, screen, screen, flag=False)
                                winning_card = battleScreen(game_settings, game_instance, clock, screen, zone_monster, enemy_card, selected_field_card_option_box, lp_font)
                                
                                for zone in player_monster_zones_array + ai_monster_zones_array + player_spell_and_trap_zones_array + ai_spell_and_trap_zones_array:
                                    zone.setZoneCardImg()
                                    
                                equip_zones = [zone for zone in player_spell_and_trap_zones_array + ai_spell_and_trap_zones_array if zone.zone.getNumOfCardsContained() == 1 and zone.zone.getCardByIndex(0).spell_or_trap_type == "Equip" and zone.zone.getCardByIndex(0).equipped_monster]                          
                                for zone in equip_zones:
                                    if zone.zone.getCardByIndex(0).equipped_monster:
                                        if zone.zone.getCardByIndex(0).equipped_monster.current_zone == None:
                                            zone.zone.removeCardFromZone(zone.zone.getCardByIndex(0), "To graveyard")
                                            zone.setZoneCardImg()    
                                
                                player_field_gui.setZoneCardImg()
                                ai_field_gui.setZoneCardImg()
                                player_graveyard_gui.setZoneCardImg(lp_font)
                                ai_graveyard_gui.setZoneCardImg(lp_font)
                                
                                ai_monster_zones_ok = [False for _ in range(5)]
                                actions3 = False
                                ai_field_actions2 = True
                                
                                if winning_card.card_owner == game_instance.player:
                                    xhealth.setHealth(game_instance.ai.life_points)
                                else:
                                    phealth.setHealth(game_instance.player.life_points) 
                                    
                                    
                                        
                                player_summoning_trap = False
                        else:                   
                            trapping = True
                            trap_tooltip_active = False
                            trap_select_active = True
                            for zone in player_spell_and_trap_zones_array:
                                if zone.zone.getNumOfCardsContained() == 1:
                                    zone_card = zone.zone.getCardByIndex(0)
                                    if zone_card.card_type == "Trap":
                                        if zone_card.willTrigger(game_instance.ai, is_player=True):
                                            zone.color = Settings.GREEN
                                            zone.area.fill((0, 255, 0))
                                            zone.blit()   
                            
                            if player_summoning_trap:
                                summoning_trap_activation = True
                                player_summoning_trap = False
                else:
                        choice.color = Settings.WHITE
                        choice.area.fill(choice.color)
                        
            select_guardian_star_block.blit()
            left_gs_selection.blit()
            right_gs_selection.blit()
            screen.blit(trap_tooltip_render, [(325+(945/2))-(gst_width/2), 165])
            
            yes_render = lp_font.render("Yes", True, Settings.BLACK)
            no_render = lp_font.render("No", True, Settings.BLACK)

            screen.blit(yes_render, [(select_guardian_star_block.rect.x+left_gs_selection.rect.x)+60, (select_guardian_star_block.rect.y+left_gs_selection.rect.y)+18])
            screen.blit(no_render, [(select_guardian_star_block.rect.x+right_gs_selection.rect.x)+60, (select_guardian_star_block.rect.y+right_gs_selection.rect.y)+18])
        
            pygame.draw.rect(screen, Settings.BLACK, [select_guardian_star_block.rect.x+25, select_guardian_star_block.rect.y+60, 150, 50], 1)
            pygame.draw.rect(screen, Settings.BLACK, [select_guardian_star_block.rect.x+175, select_guardian_star_block.rect.y+60, 150, 50], 1)             
        
        selected_cards_in_hand = 0
        
        if trap_select_active:
            tt_width, tt_height = option_font.size(selecting_trap_tooltip)
            pygame.draw.rect(screen, Settings.LIGHT_GRAY, [(325+(945/2))-(tt_width/2), 70, tt_width, tt_height+20])
            my_tooltip = option_font.render(selecting_trap_tooltip, True, Settings.BLACK)
            screen.blit(my_tooltip, [(325+(945/2))-(tt_width/2), 70+((tt_height+10)/2)])        
            
        if not game_instance.current_turn_player.has_played_a_card_this_turn:
            for x in range(len(cards)):

                cards[0].rect.centerx -= cards[0].card_speed
        
                if len(cards) > 0: 
                    if cards[0].rect.right <= 800:
                        cards[1].rect.centerx -= cards[1].card_speed
                        if cards[0].rect.left <= hand_cards_status[0]["x_position"]:
                            cards[0].card_speed = 0
                            cards[0].rect.left = hand_cards_status[0]["x_position"]
                            cards[0].contained = True
                            hand_cards_status[0]["card"] = cards[0]

                if len(cards) > 1:                     
                    if cards[1].rect.right <= 800:
                        cards[2].rect.centerx -= cards[2].card_speed
                        if cards[1].rect.left <= hand_cards_status[1]["x_position"]:
                            cards[1].card_speed = 0
                            cards[1].rect.left = hand_cards_status[1]["x_position"]
                            cards[1].contained = True
                            hand_cards_status[1]["card"] = cards[1]
                    
                if len(cards) > 2:                     
                    if cards[2].rect.right <= 1200:
                        cards[3].rect.centerx -= cards[3].card_speed
                        if cards[2].rect.left <= hand_cards_status[2]["x_position"]:
                            cards[2].card_speed = 0
                            cards[2].rect.left = hand_cards_status[2]["x_position"]
                            cards[2].contained = True
                            hand_cards_status[2]["card"] = cards[2]
                
                if len(cards) > 3:            
                    if cards[3].rect.right <= 1200:
                        if len(cards) > 4:
                            cards[4].rect.centerx -= cards[4].card_speed     
                        if cards[3].rect.left <= hand_cards_status[3]["x_position"]:
                            cards[3].card_speed = 0
                            cards[3].rect.left = hand_cards_status[3]["x_position"]
                            cards[3].contained = True
                            hand_cards_status[3]["card"] = cards[3]
                
                if len(cards) > 4:
                    if cards[4].rect.right <= 1200:
                        if cards[4].rect.left <= hand_cards_status[4]["x_position"]:
                            cards[4].card_speed = 0
                            cards[4].rect.left = hand_cards_status[4]["x_position"]
                            cards[4].contained = True
                            hand_cards_status[4]["card"] = cards[4]
                
                if cards[x].is_visible:
                    if cards[x].rect.collidepoint(mouse_pos) and not game_instance.game_over:
                        #pygame.draw.rect(screen, Settings.WHITE, [cards[x].rect.x, cards[x].rect.y, 149, 216] , 3)
                        if cards[x].card.card_owner == game_instance.player or cards[x].card.is_set == False:
                            card_layout.card_type = cards[x].card_type
                            card_layout.card = cards[x].card
                            card_layout.changeImg(cards[x].card.img)
                        else:
                            card_layout.card_type = None
                            card_layout.card = None
                            card_layout.changeImg("images/cards/card_back.png")
                            
                        card_name = cards[x].card.name
                        card_desc = cards[x].card.text
                        
                        selected_cards_in_hand += 1
                        
                        if not zone_display_on:
                            selected_card_option_box.is_selected = True
                            selected_card_option_box.card = cards[x]
                            
                            if game_instance.current_turn_player == game_instance.player:
                                selected_card_option_box.getArea(player_spell_and_trap_zones_array, fuse_up_ctr, fuse_down_ctr)
                            else:
                                selected_card_option_box.getArea(ai_spell_and_trap_zones_array, fuse_up_ctr, fuse_down_ctr)

                            for option in monster_card_options:
                                option.screen = selected_card_option_box.area
                            for option in trap_card_options:
                                option.screen = selected_card_option_box.area
                            for option in spell_card_options:
                                option.screen = selected_card_option_box.area
                            for option in other_card_fusion_options:
                                option.screen = selected_card_option_box.area
                            card_fusing_options[0].screen = selected_card_option_box.area
                        
                        if cards[x].card_type == "Monster":
                            if fuse_up_ctr > 0 or fuse_down_ctr > 0:
                                if not zone_display_on:
                                    if not cards[x].is_fusing:
                                        selected_card_option_box.options = other_card_fusion_options
                                    else:
                                        selected_card_option_box.options = card_fusing_options
                            else:
                                if not zone_display_on:
                                    if not cards[x].is_fusing:
                                        selected_card_option_box.options = monster_card_options
                                    else:
                                        selected_card_option_box.options = card_fusing_options
                            card_type_info = "[Monster] " + cards[x].card.monster_type + "/" + cards[x].card.monster_attr 
                            monst_lvl_and_atk = "[" + u"\u2605" + str(cards[x].card.level) + "]  " + str(cards[x].card.atk_points) + "/" + str(cards[x].card.def_points)
                            gs_text = "Guardian Stars:" 
                            gs1_img = gf.getGuardianStarImg(cards[x].card.guardian_star_list[0].name)
                            gs2_img = gf.getGuardianStarImg(cards[x].card.guardian_star_list[1].name)
                            gs1_text = cards[x].card.guardian_star_list[0].name
                            gs2_text = cards[x].card.guardian_star_list[1].name
                            
                            card_info_panel.setCardContent(card_name, gs_text, gs1_text, gs2_text, card_type_info, monst_lvl_and_atk, card_desc, gs1_img, gs2_img, cards[x].card.fusion_types_string)
                        else:
                            if fuse_up_ctr > 0 or fuse_down_ctr > 0:
                                if not zone_display_on:
                                    if not cards[x].is_fusing:
                                        selected_card_option_box.options = other_card_fusion_options
                                    else:
                                        selected_card_option_box.options = card_fusing_options
                            else:
                                if not zone_display_on:
                                    if not cards[x].is_fusing:
                                        if cards[x].card_type == "Trap":
                                            selected_card_option_box.options = trap_card_options
                                        else: 
                                            if not cards[x].card.spell_or_trap_type == "Equip":
                                                selected_card_option_box.options = spell_card_options
                                            else:
                                                if cards[x].card.willActivate():
                                                    selected_card_option_box.options = spell_card_options
                                                else:
                                                    selected_card_option_box.options = trap_card_options
                                    else:
                                        selected_card_option_box.options = card_fusing_options
                                
                            card_type_info = "[" + cards[x].card.card_type + "] " + cards[x].card.spell_or_trap_type
                            monst_lvl_and_atk = ""
                            gs_text = ""
                            card_info_panel.setCardContent(card_name, "", "", "", card_type_info, "", card_desc, None, None, cards[x].card.fusion_types_string)
                        #selected_card_option_box.card = None

                if cards[x].is_visible:
                    if cards[x].card_type == "Monster":
                        cards[x].blit(cards[x].card.current_atk_points, cards[x].card.current_def_points, Settings.BLACK)
                    else:
                        cards[x].blit()  
 
        if ai_selecting_card_in_hand:
            z = pygame.time.get_ticks() 
            if z - q >= 400:#540
                ai_selecting_card_in_hand = False
                ai_selecting_card_in_hand2 = True
                
        if ai_selecting_card_in_hand2:
            ve = pygame.time.get_ticks()
            if ve - z >= 400 and ve - z < 800:
                if not ai_fuse_card_ok[0]:
                    if fusion_indices:                   
                        if 0 in fusion_indices:
                            position = fusion_indices.index(0)
                            fused_material = game_instance.ai.cards_gui[0]
                            myIndex = game_instance.ai.cards_gui[0].card_index                        
                            if position == 0 or position == 1:
                                ai_fuse_up_ctr, ai_fuse_down_ctr = gf.chooseCardToFuse("Fuse Up", fused_material, selected_card_option_box, ai_fuse_up_ctr, ai_fuse_down_ctr)
                                ai_fuse_card_ok[0] = True
                                text = ai_fuse_up_ctr
                                color = Settings.BLUE
                                fusion_order_box = FusionOrderBox(screen, [20, 20], fused_material.rect.x-7, fused_material.rect.y-7, color, str(text), True, lp_font, fused_material, index=myIndex)    
                                up_fusion_order_box_array.append(fusion_order_box)
                            else:
                                ai_fuse_up_ctr, ai_fuse_down_ctr = gf.chooseCardToFuse("Fuse Down", fused_material, selected_card_option_box, fuse_up_ctr, fuse_down_ctr)
                                ai_fuse_card_ok[0] = True
                                text = ai_fuse_down_ctr
                                color = Settings.GOLD
                                fusion_order_box = FusionOrderBox(screen, [20, 20], fused_material.rect.x-7, fused_material.rect.y-7, color, str(text), True, lp_font, fused_material, index=myIndex)
                                down_fusion_order_box_array.append(fusion_order_box)
                        else:
                            ai_fuse_card_ok[0] = True
                            
                pygame.draw.rect(screen, Settings.RED, [hand_cards_status[0]["x_position"], 540, 149, 216], 5)
            elif ve - z >= 800 and ve - z < 1200:
                if not ai_fuse_card_ok[1] and ai_fuse_card_ok[0]:
                    if fusion_indices:
                        if 1 in fusion_indices:
                            position = fusion_indices.index(1)
                            fused_material = game_instance.ai.cards_gui[1]
                            myIndex = game_instance.ai.cards_gui[1].card_index                        
                            if position == 0 or position == 1:
                                ai_fuse_up_ctr, ai_fuse_down_ctr = gf.chooseCardToFuse("Fuse Up", fused_material, selected_card_option_box, ai_fuse_up_ctr, ai_fuse_down_ctr)                                                       
                                ai_fuse_card_ok[1] = True
                                text = ai_fuse_up_ctr
                                color = Settings.BLUE
                                fusion_order_box = FusionOrderBox(screen, [20, 20], fused_material.rect.x-7, fused_material.rect.y-7, color, str(text), True, lp_font, fused_material, index=myIndex)    
                                up_fusion_order_box_array.append(fusion_order_box)
                            else:
                                ai_fuse_up_ctr, ai_fuse_down_ctr = gf.chooseCardToFuse("Fuse Down", fused_material, selected_card_option_box, ai_fuse_up_ctr, ai_fuse_down_ctr)
                                ai_fuse_card_ok[1] = True
                                text = ai_fuse_down_ctr
                                color = Settings.GOLD
                                fusion_order_box = FusionOrderBox(screen, [20, 20], fused_material.rect.x-7, fused_material.rect.y-7, color, str(text), True, lp_font, fused_material, index=myIndex)
                                down_fusion_order_box_array.append(fusion_order_box)
                        else:
                            ai_fuse_card_ok[1] = True
            
                pygame.draw.rect(screen, Settings.RED, [hand_cards_status[1]["x_position"], 540, 149, 216], 5)
            elif ve - z >= 1200 and ve - z < 1600:
                if not ai_fuse_card_ok[2] and ai_fuse_card_ok[1]:
                    if fusion_indices:
                        if 2 in fusion_indices:
                            position = fusion_indices.index(2)
                            fused_material = game_instance.ai.cards_gui[2]
                            myIndex = game_instance.ai.cards_gui[2].card_index                        
                            if position == 0 or position == 1:
                                ai_fuse_up_ctr, fuse_down_ctr = gf.chooseCardToFuse("Fuse Up", fused_material, selected_card_option_box, ai_fuse_up_ctr, ai_fuse_down_ctr)                              
                                ai_fuse_card_ok[2] = True
                                text = ai_fuse_up_ctr
                                color = Settings.BLUE
                                fusion_order_box = FusionOrderBox(screen, [20, 20], fused_material.rect.x-7, fused_material.rect.y-7, color, str(text), True, lp_font, fused_material, index=myIndex)    
                                up_fusion_order_box_array.append(fusion_order_box)
                            else:
                                ai_fuse_up_ctr, ai_fuse_down_ctr = gf.chooseCardToFuse("Fuse Down", fused_material, selected_card_option_box, ai_fuse_up_ctr, ai_fuse_down_ctr)                        
                                ai_fuse_card_ok[2] = True
                                text = ai_fuse_down_ctr
                                color = Settings.GOLD
                                fusion_order_box = FusionOrderBox(screen, [20, 20], fused_material.rect.x-7, fused_material.rect.y-7, color, str(text), True, lp_font, fused_material, index=myIndex)
                                down_fusion_order_box_array.append(fusion_order_box)
                        else:
                            ai_fuse_card_ok[2] = True
            
                pygame.draw.rect(screen, Settings.RED, [hand_cards_status[2]["x_position"], 540, 149, 216], 5)
            elif ve - z >= 1600 and ve - z < 2000:
                if not ai_fuse_card_ok[3] and ai_fuse_card_ok[2]:
                    if fusion_indices:
                        if 3 in fusion_indices:
                            position = fusion_indices.index(3)
                            fused_material = game_instance.ai.cards_gui[3]
                            myIndex = game_instance.ai.cards_gui[3].card_index                        
                            if position == 0 or position == 1:
                                ai_fuse_up_ctr, ai_fuse_down_ctr = gf.chooseCardToFuse("Fuse Up", fused_material, selected_card_option_box, ai_fuse_up_ctr, ai_fuse_down_ctr)      
                                ai_fuse_card_ok[3] = True
                                text = ai_fuse_up_ctr
                                color = Settings.BLUE
                                fusion_order_box = FusionOrderBox(screen, [20, 20], fused_material.rect.x-7, fused_material.rect.y-7, color, str(text), True, lp_font, fused_material, index=myIndex)    
                                up_fusion_order_box_array.append(fusion_order_box)
                            else:
                                ai_fuse_up_ctr, ai_fuse_down_ctr = gf.chooseCardToFuse("Fuse Down", fused_material, selected_card_option_box, ai_fuse_up_ctr, ai_fuse_down_ctr)      
                                ai_fuse_card_ok[3] = True
                                text = ai_fuse_down_ctr
                                color = Settings.GOLD
                                fusion_order_box = FusionOrderBox(screen, [20, 20], fused_material.rect.x-7, fused_material.rect.y-7, color, str(text), True, lp_font, fused_material, index=myIndex)
                                down_fusion_order_box_array.append(fusion_order_box)                            
                        else:
                            ai_fuse_card_ok[3] = True
            
                pygame.draw.rect(screen, Settings.RED, [hand_cards_status[3]["x_position"], 540, 149, 216], 5)
            elif ve - z >= 2000 and ve - z < 2400:
                if not ai_fuse_card_ok[4] and ai_fuse_card_ok[3]:
                    if fusion_indices:
                        if 4 in fusion_indices:
                            position = fusion_indices.index(4)
                            fused_material = game_instance.ai.cards_gui[4]
                            myIndex = game_instance.ai.cards_gui[4].card_index                        
                            if position == 0 or position == 1:
                                ai_fuse_up_ctr, ai_fuse_down_ctr = gf.chooseCardToFuse("Fuse Up", fused_material, selected_card_option_box, ai_fuse_up_ctr, ai_fuse_down_ctr)      
                                ai_fuse_card_ok[4] = True
                                text = ai_fuse_up_ctr
                                color = Settings.BLUE
                                fusion_order_box = FusionOrderBox(screen, [20, 20], fused_material.rect.x-7, fused_material.rect.y-7, color, str(text), True, lp_font, fused_material, index=myIndex)    
                                up_fusion_order_box_array.append(fusion_order_box)
                            else:
                                ai_fuse_up_ctr, ai_fuse_down_ctr = gf.chooseCardToFuse("Fuse Down", fused_material, selected_card_option_box, ai_fuse_up_ctr, ai_fuse_down_ctr)      
                                ai_fuse_card_ok[4] = True
                                text = ai_fuse_down_ctr
                                color = Settings.GOLD
                                fusion_order_box = FusionOrderBox(screen, [20, 20], fused_material.rect.x-7, fused_material.rect.y-7, color, str(text), True, lp_font, fused_material, index=myIndex)
                                down_fusion_order_box_array.append(fusion_order_box)        
                        else:
                            ai_fuse_card_ok[4] = True
            
                pygame.draw.rect(screen, Settings.RED, [hand_cards_status[4]["x_position"], 540, 149, 216], 5) 
            elif ve - z >= 2400 and ve - z < 2800:
                if ai_card_to_play:
                    pygame.draw.rect(screen, Settings.RED, [hand_cards_status[ai_card_to_play.card_index]["x_position"], 540, 149, 216], 5) 
        
#ai_monster_zones_ok
        if ai_field_actions2 and not game_instance.game_over:
        
            ai_monsters_per_zone = gf.get_monsters_on_field(ai_monster_zones_array, lambda card: not card.has_attacked) #or card.in_atk_position)
            guac = pygame.time.get_ticks()
   
            if game_instance.current_turn == 1:
                ai_end_monsters_turn = True
                ai_field_actions2 = False 
                ai_end_phase_timer = pygame.time.get_ticks()  
                ai_end_phase = True                   
            else:
                if len(ai_monsters_per_zone) > 0:             
                    ai_monster_zones_ok = [False for _ in range(5)]
          
                    if guac-fuac <= 400:
                        guac = pygame.time.get_ticks()

                    enemy_monsters_per_zone = gf.get_monsters_on_field(player_monster_zones_array)                    
                    current_monster = gf.get_ai_zone_current_monster(ai_monsters_per_zone, enemy_monsters_per_zone)
                else:
                    ai_end_monsters_turn = True
                
                if guac-fuac >= 400:
                    actions3 = True
                    ai_field_actions2 = False
                
        if actions3:
            if game_instance.current_turn != 1:
                if player_trap_selecting:
                    if attacking_zone:
                        pygame.draw.rect(screen, Settings.RED, [ai_monster_zones_array[attacking_zone].rect.x, ai_monster_zones_array[attacking_zone].rect.y, 129.2, 111.75], 5)  
            
                if not ai_monster_zones_ok[0]:
                    if not trap_tooltip_active and not trapping:
                        pygame.draw.rect(screen, Settings.RED, [ai_monster_zones_array[0].rect.x, ai_monster_zones_array[0].rect.y, 129.2, 111.75], 5)  
                    aa = pygame.time.get_ticks()

                    if aa-fuac >= 800:
               
                        if ai_monster_zones_array[0].zone.getNumOfCardsContained() == 1:

                            if not ai_monster_zones_array[0].disabled_for_ai:
                                enemy_monsters_per_zone = gf.get_monsters_on_field(player_monster_zones_array)
                                if ai_monster_zones_array[0].zone.getCardByIndex(0) == current_monster:
                                    current_monster_zone = ai_monster_zones_array[0]
                                    zone_monster = current_monster_zone.zone.getCardByIndex(0)
                                    winning_card = None
                                    target_monster = gf.monsterAction(current_monster_zone, player_monster_zones_array, screen, ai_monster_zones_array, 4, card_layout, card_surface, card_desc_surface, player_spell_and_trap_zones_array, ai_spell_and_trap_zones_array, zone_lines_tuple, player_graveyard_gui, ai_graveyard_gui, card_info_panel, phealth, xhealth, card_name_font, lp_font, game_instance.player.name, game_instance.ai.name, current_turn_box_dimensions, current_turn_box_dimensions2, game_instance, ai_field_gui, player_field_gui, egyptian_background, ai_deck_gui, player_deck_gui, main_phase_block, battle_phase_block, end_phase_block, ee, turn_text_width, turn_text, 0, active_field_card_img, active_field_card_display)  
                                    ai_monsters_per_zone.remove(current_monster)        
                                    if target_monster == None:
                                        if game_instance.current_turn == 1:
                                            if zone_monster.current_def_points > zone_monster.current_atk_points:
                                                zone_monster.in_atk_position = not zone_monster.in_atk_position
                                                current_monster_zone.setZoneCardImg()
                                        ai_monster_zones_ok[0] = True
                                    else:        
                                                  
                                        game_instance.ai.is_attacking = True
                                        if target_monster == "Direct attack":
                                            enemy_card = None
                                        else:
                                            enemy_card = target_monster.zone.getCardByIndex(0)
                                            
                                        player_traps = gf.trap_trigger_check(zone_monster, game_instance.player, game_instance, attacked_monster=enemy_card) 

                                        if len(player_traps) > 0:
                                            trap_tooltip_active = True
                                            player_trap_selecting = True
   
                                            if not player_trap_selecting:
                                            
                                                gf.fade(game_settings.screen_width, game_settings.screen_height, screen, screen, flag=False)
                                                winning_card = battleScreen(game_settings, game_instance, clock, screen, zone_monster, enemy_card, selected_field_card_option_box, lp_font)
                                                ai_monster_zones_ok[0] = True
                          
                                            else:    
                                                selected_field_card = zone_monster    
                                                ai_monster_zones_ok[0] = False
                                                attacking_zone = 0
                                            
                                        else:
                       
                                            gf.fade(game_settings.screen_width, game_settings.screen_height, screen, screen, flag=False)                                          
                                            winning_card = battleScreen(game_settings, game_instance, clock, screen, zone_monster, enemy_card, selected_field_card_option_box, lp_font)
                                            ai_monster_zones_ok[0] = True
        
                                    for zone in player_monster_zones_array + ai_monster_zones_array + player_spell_and_trap_zones_array + ai_spell_and_trap_zones_array:
                                        zone.setZoneCardImg()
                                        
                                    equip_zones = [zone for zone in player_spell_and_trap_zones_array + ai_spell_and_trap_zones_array if zone.zone.getNumOfCardsContained() == 1 and zone.zone.getCardByIndex(0).spell_or_trap_type == "Equip" and zone.zone.getCardByIndex(0).equipped_monster]                          
                                    for zone in equip_zones:
                                        if zone.zone.getCardByIndex(0).equipped_monster:
                                            if zone.zone.getCardByIndex(0).equipped_monster.current_zone == None:
                                                zone.zone.removeCardFromZone(zone.zone.getCardByIndex(0), "To graveyard")
                                                zone.setZoneCardImg()                                            
                        
                                    player_field_gui.setZoneCardImg()
                                    ai_field_gui.setZoneCardImg()
                                    player_graveyard_gui.setZoneCardImg(lp_font)
                                    ai_graveyard_gui.setZoneCardImg(lp_font)
        
                                    if winning_card:
                                        if winning_card.card_owner == game_instance.player:
                                            xhealth.setHealth(game_instance.ai.life_points)
                                        else:
                                            phealth.setHealth(game_instance.player.life_points)                                                            
                                    
                                    if game_instance.player.life_points == 0:
                                        endGame = True
                                        game_instance.endGame("No life points left.", game_instance.player)
                                        #goToLastSavedScreen(player_dict, screen, game_settings)
                                        
                                    elif game_instance.ai.life_points == 0:
                                        endGame = True
                                        game_instance.endGame("No life points left.", game_instance.ai)

                                    actions3 = False
                                    ai_field_actions2 = True                                    
                                else:
                                    ai_monster_zones_ok[0] = True
                                aa = pygame.time.get_ticks()
                            else:
                                ai_monster_zones_ok[0] = True     
                        else:
                            ai_monster_zones_ok[0] = True

                if not ai_monster_zones_ok[1] and ai_monster_zones_ok[0]:
                    bb = pygame.time.get_ticks()
                    if not trap_tooltip_active and not trapping:
                        pygame.draw.rect(screen, Settings.RED, [ai_monster_zones_array[1].rect.x, ai_monster_zones_array[1].rect.y, 129.2, 111.75], 5) 
                    if bb-aa >= 600:#600:

                        if ai_monster_zones_array[1].zone.getNumOfCardsContained() == 1:

                            if not ai_monster_zones_array[1].disabled_for_ai:
                                if ai_monster_zones_array[1].zone.getCardByIndex(0) == current_monster:
                                    current_monster_zone = ai_monster_zones_array[1]
                                    zone_monster = current_monster_zone.zone.getCardByIndex(0)
                                    winning_card = None


                                    target_monster = gf.monsterAction(current_monster_zone, player_monster_zones_array, screen, ai_monster_zones_array, 4, card_layout, card_surface, card_desc_surface, player_spell_and_trap_zones_array, ai_spell_and_trap_zones_array, zone_lines_tuple, player_graveyard_gui, ai_graveyard_gui, card_info_panel, phealth, xhealth, card_name_font, lp_font, game_instance.player.name, game_instance.ai.name, current_turn_box_dimensions, current_turn_box_dimensions2, game_instance, ai_field_gui, player_field_gui, egyptian_background, ai_deck_gui, player_deck_gui, main_phase_block, battle_phase_block, end_phase_block, ee, turn_text_width, turn_text, 1, active_field_card_img, active_field_card_display)  
                                    ai_monsters_per_zone.remove(current_monster)
                                    if target_monster == None:
                                        if game_instance.current_turn == 1:
                                            if zone_monster.current_def_points > zone_monster.current_atk_points:
                                                zone_monster.in_atk_position = not zone_monster.in_atk_position
                                                current_monster_zone.setZoneCardImg()
                                        ai_monster_zones_ok[1] = True
                                    else:         
                                        game_instance.ai.is_attacking = True
                                        if target_monster == "Direct attack":
                                            enemy_card = None
                                        else:
                                            enemy_card = target_monster.zone.getCardByIndex(0)
                                            
                                        player_traps = gf.trap_trigger_check(zone_monster, game_instance.player, game_instance, attacked_monster=enemy_card) 
                                                       
                                        if len(player_traps) > 0:
                                            trap_tooltip_active = True
                                            player_trap_selecting = True
               
                                            if not player_trap_selecting:
                                                gf.fade(game_settings.screen_width, game_settings.screen_height, screen, screen, flag=False)
                                                winning_card = battleScreen(game_settings, game_instance, clock, screen, zone_monster, enemy_card, selected_field_card_option_box, lp_font)
                                                ai_monster_zones_ok[1] = True
                                   
                                            else:
                                                selected_field_card = zone_monster                            
                                                ai_monster_zones_ok[1] = False
                                                attacking_zone = 1
                           
                                        else:    
                    
                                            gf.fade(game_settings.screen_width, game_settings.screen_height, screen, screen, flag=False)                                   
                                            winning_card = battleScreen(game_settings, game_instance, clock, screen, zone_monster, enemy_card, selected_field_card_option_box, lp_font)
                                            ai_monster_zones_ok[1] = True  
                                            
                                    for zone in player_monster_zones_array + ai_monster_zones_array + player_spell_and_trap_zones_array + ai_spell_and_trap_zones_array:
                                        zone.setZoneCardImg()
                                        
                                    equip_zones = [zone for zone in player_spell_and_trap_zones_array + ai_spell_and_trap_zones_array if zone.zone.getNumOfCardsContained() == 1 and zone.zone.getCardByIndex(0).spell_or_trap_type == "Equip" and zone.zone.getCardByIndex(0).equipped_monster]                          
                                    for zone in equip_zones:
                                        if zone.zone.getCardByIndex(0).equipped_monster:
                                            if zone.zone.getCardByIndex(0).equipped_monster.current_zone == None:
                                                zone.zone.removeCardFromZone(zone.zone.getCardByIndex(0), "To graveyard")
                                                zone.setZoneCardImg()                                            
                        
                                    player_field_gui.setZoneCardImg()
                                    ai_field_gui.setZoneCardImg()
                                    player_graveyard_gui.setZoneCardImg(lp_font)
                                    ai_graveyard_gui.setZoneCardImg(lp_font)                                           
                                            
                                    if winning_card:
                                        if winning_card.card_owner == game_instance.player:
                                            xhealth.setHealth(game_instance.ai.life_points)
                                        else:
                                            phealth.setHealth(game_instance.player.life_points)
                                    
                                    if game_instance.player.life_points == 0:
                                        endGame = True
                                        game_instance.endGame("No life points left.", game_instance.player)
                                        #goToLastSavedScreen(player_dict, screen, game_settings)
                                        
                                    elif game_instance.ai.life_points == 0:
                                        endGame = True
                                        game_instance.endGame("No life points left.", game_instance.ai)
                                        
                                    actions3 = False
                                    ai_field_actions2 = True                                      
                                else:
                                    ai_monster_zones_ok[1] = True                                    
                                bb = pygame.time.get_ticks()
                            else:
                                ai_monster_zones_ok[1] = True     
                        else:
                            ai_monster_zones_ok[1] = True

                if not ai_monster_zones_ok[2] and ai_monster_zones_ok[1]: 

                    cc = pygame.time.get_ticks()
                    if not trap_tooltip_active and not trapping:
                        pygame.draw.rect(screen, Settings.RED, [ai_monster_zones_array[2].rect.x, ai_monster_zones_array[2].rect.y, 129.2, 111.75], 5)    
                    if cc-bb >= 600:      
                        if ai_monster_zones_array[2].zone.getNumOfCardsContained() == 1:                  
                            if not ai_monster_zones_array[2].disabled_for_ai:
                                if ai_monster_zones_array[2].zone.getCardByIndex(0) == current_monster:
                                    current_monster_zone = ai_monster_zones_array[2]
                                    zone_monster = current_monster_zone.zone.getCardByIndex(0)
                                    winning_card = None


                                    target_monster = gf.monsterAction(current_monster_zone, player_monster_zones_array, screen, ai_monster_zones_array, 4, card_layout, card_surface, card_desc_surface, player_spell_and_trap_zones_array, ai_spell_and_trap_zones_array, zone_lines_tuple, player_graveyard_gui, ai_graveyard_gui, card_info_panel, phealth, xhealth, card_name_font, lp_font, game_instance.player.name, game_instance.ai.name, current_turn_box_dimensions, current_turn_box_dimensions2, game_instance, ai_field_gui, player_field_gui, egyptian_background, ai_deck_gui, player_deck_gui, main_phase_block, battle_phase_block, end_phase_block, ee, turn_text_width, turn_text, 2, active_field_card_img, active_field_card_display)  
                                    ai_monsters_per_zone.remove(current_monster)
                                    if target_monster == None:
                                        if game_instance.current_turn == 1:
                                            if zone_monster.current_def_points > zone_monster.current_atk_points:
                                                zone_monster.in_atk_position = not zone_monster.in_atk_position
                                                current_monster_zone.setZoneCardImg()                                                                
                                        ai_monster_zones_ok[2] = True
                                    else:           
              
                                        game_instance.ai.is_attacking = True
                                        if target_monster == "Direct attack":
                                            enemy_card = None
                                        else:
                                            enemy_card = target_monster.zone.getCardByIndex(0)
                                            
                                        player_traps = gf.trap_trigger_check(zone_monster, game_instance.player, game_instance, attacked_monster=enemy_card) 
                                                 
                                        if len(player_traps) > 0:
                                            trap_tooltip_active = True
                                            player_trap_selecting = True
                
                                            if not player_trap_selecting:
                                                gf.fade(game_settings.screen_width, game_settings.screen_height, screen, screen, flag=False)
                                                winning_card = battleScreen(game_settings, game_instance, clock, screen, zone_monster, enemy_card, selected_field_card_option_box, lp_font)
                                                ai_monster_zones_ok[2] = True
                         
                                            else:
                                                selected_field_card = zone_monster              
                                                ai_monster_zones_ok[2] = False   
                                                attacking_zone = 2
                          
                                        else:   
                        
                                            gf.fade(game_settings.screen_width, game_settings.screen_height, screen, screen, flag=False)                                        
                                            winning_card = battleScreen(game_settings, game_instance, clock, screen, zone_monster, enemy_card, selected_field_card_option_box, lp_font)
                                            ai_monster_zones_ok[2] = True      
                                            
                                    for zone in player_monster_zones_array + ai_monster_zones_array + player_spell_and_trap_zones_array + ai_spell_and_trap_zones_array:
                                        zone.setZoneCardImg()
                                        
                                    equip_zones = [zone for zone in player_spell_and_trap_zones_array + ai_spell_and_trap_zones_array if zone.zone.getNumOfCardsContained() == 1 and zone.zone.getCardByIndex(0).spell_or_trap_type == "Equip" and zone.zone.getCardByIndex(0).equipped_monster]                          
                                    for zone in equip_zones:
                                        if zone.zone.getCardByIndex(0).equipped_monster:
                                            if zone.zone.getCardByIndex(0).equipped_monster.current_zone == None:
                                                zone.zone.removeCardFromZone(zone.zone.getCardByIndex(0), "To graveyard")
                                                zone.setZoneCardImg()                                            
                        
                                    player_field_gui.setZoneCardImg()
                                    ai_field_gui.setZoneCardImg()
                                    player_graveyard_gui.setZoneCardImg(lp_font)
                                    ai_graveyard_gui.setZoneCardImg(lp_font)                                            
                                            
                                    if winning_card:
                                        if winning_card.card_owner == game_instance.player:
                                            xhealth.setHealth(game_instance.ai.life_points)
                                        else:
                                            phealth.setHealth(game_instance.player.life_points)
                                    
                                    if game_instance.player.life_points == 0:
                                        endGame = True
                                        game_instance.endGame("No life points left.", game_instance.player)
                                        #goToLastSavedScreen(player_dict, screen, game_settings)
                                        
                                    elif game_instance.ai.life_points == 0:
                                        endGame = True
                                        game_instance.endGame("No life points left.", game_instance.ai)  

                                    actions3 = False
                                    ai_field_actions2 = True                                      
                                else:
                                    ai_monster_zones_ok[2] = True                                     
                                cc = pygame.time.get_ticks()
                            else:
                                ai_monster_zones_ok[2] = True     
                        else:
                            ai_monster_zones_ok[2] = True               
                if not ai_monster_zones_ok[3] and ai_monster_zones_ok[2]: 
                    dd = pygame.time.get_ticks()
                    if not trap_tooltip_active and not trapping:
                        pygame.draw.rect(screen, Settings.RED, [ai_monster_zones_array[3].rect.x, ai_monster_zones_array[3].rect.y, 129.2, 111.75], 5)       
                    if dd-cc >= 600:
                        if ai_monster_zones_array[3].zone.getNumOfCardsContained() == 1:
                            if not ai_monster_zones_array[3].disabled_for_ai:
                                if ai_monster_zones_array[3].zone.getCardByIndex(0) == current_monster:
        
                                    current_monster_zone = ai_monster_zones_array[3]
                                    zone_monster = current_monster_zone.zone.getCardByIndex(0)
                                    winning_card = None


                                    target_monster = gf.monsterAction(current_monster_zone, player_monster_zones_array, screen, ai_monster_zones_array, 4, card_layout, card_surface, card_desc_surface, player_spell_and_trap_zones_array, ai_spell_and_trap_zones_array, zone_lines_tuple, player_graveyard_gui, ai_graveyard_gui, card_info_panel, phealth, xhealth, card_name_font, lp_font, game_instance.player.name, game_instance.ai.name, current_turn_box_dimensions, current_turn_box_dimensions2, game_instance, ai_field_gui, player_field_gui, egyptian_background, ai_deck_gui, player_deck_gui, main_phase_block, battle_phase_block, end_phase_block, ee, turn_text_width, turn_text, 3, active_field_card_img, active_field_card_display)  
                                    ai_monsters_per_zone.remove(current_monster)
                                    if target_monster == None:
                                        if game_instance.current_turn == 1:
                                            if zone_monster.current_def_points > zone_monster.current_atk_points:
                                                zone_monster.in_atk_position = not zone_monster.in_atk_position
                                                current_monster_zone.setZoneCardImg()                                
                                        ai_monster_zones_ok[3] = True
                                    else:         
             
                                        game_instance.ai.is_attacking = True
                                        if target_monster == "Direct attack":
                                            enemy_card = None
                                        else:
                                            enemy_card = target_monster.zone.getCardByIndex(0)
                                            
                                        player_traps = gf.trap_trigger_check(zone_monster, game_instance.player, game_instance, attacked_monster=enemy_card) 
                                                                                                            
                                        if len(player_traps) > 0:
                                            trap_tooltip_active = True
                                            player_trap_selecting = True
                                    
                                            if not player_trap_selecting:
                                                gf.fade(game_settings.screen_width, game_settings.screen_height, screen, screen, flag=False)
                                                winning_card = battleScreen(game_settings, game_instance, clock, screen, zone_monster, enemy_card, selected_field_card_option_box, lp_font)
                                                ai_monster_zones_ok[3] = True
                                   
                                            else:
                                                selected_field_card = zone_monster                               
                                                ai_monster_zones_ok[3] = False 
                                                attacking_zone = 3
                              
                                        else:    
         
                                            gf.fade(game_settings.screen_width, game_settings.screen_height, screen, screen, flag=False)
                                            winning_card = battleScreen(game_settings, game_instance, clock, screen, zone_monster, enemy_card, selected_field_card_option_box, lp_font)
                                            ai_monster_zones_ok[3] = True      
                                            
                                    for zone in player_monster_zones_array + ai_monster_zones_array + player_spell_and_trap_zones_array + ai_spell_and_trap_zones_array:
                                        zone.setZoneCardImg()
                                        
                                    equip_zones = [zone for zone in player_spell_and_trap_zones_array + ai_spell_and_trap_zones_array if zone.zone.getNumOfCardsContained() == 1 and zone.zone.getCardByIndex(0).spell_or_trap_type == "Equip" and zone.zone.getCardByIndex(0).equipped_monster]                          
                                    for zone in equip_zones:
                                        if zone.zone.getCardByIndex(0).equipped_monster:
                                            if zone.zone.getCardByIndex(0).equipped_monster.current_zone == None:
                                                zone.zone.removeCardFromZone(zone.zone.getCardByIndex(0), "To graveyard")
                                                zone.setZoneCardImg()                                            
                        
                                    player_field_gui.setZoneCardImg()
                                    ai_field_gui.setZoneCardImg()
                                    player_graveyard_gui.setZoneCardImg(lp_font)
                                    ai_graveyard_gui.setZoneCardImg(lp_font)                                            
                                            
                                    if winning_card:
                                        if winning_card.card_owner == game_instance.player:
                                            xhealth.setHealth(game_instance.ai.life_points)
                                        else:
                                            phealth.setHealth(game_instance.player.life_points)
                                            
                                    if game_instance.player.life_points == 0:
                                        endGame = True
                                        game_instance.endGame("No life points left.", game_instance.player)
                                        #goToLastSavedScreen(player_dict, screen, game_settings)
                                        
                                    elif game_instance.ai.life_points == 0:
                                        endGame = True
                                        game_instance.endGame("No life points left.", game_instance.ai)     

                                    actions3 = False
                                    ai_field_actions2 = True                                      
                                else:
                                    ai_monster_zones_ok[3] = True                                     
                                dd = pygame.time.get_ticks()
                            else:
                                ai_monster_zones_ok[3] = True     
                        else:
                            ai_monster_zones_ok[3] = True                        
                if not ai_monster_zones_ok[4] and ai_monster_zones_ok[3]:                
                    ee = pygame.time.get_ticks()  
                    if not trap_tooltip_active and not trapping:
                        pygame.draw.rect(screen, Settings.RED, [ai_monster_zones_array[4].rect.x, ai_monster_zones_array[4].rect.y, 129.2, 111.75], 5)      

                    if ee-dd >= 600:
                        if ai_monster_zones_array[4].zone.getNumOfCardsContained() == 1:

                            if not ai_monster_zones_array[4].disabled_for_ai:
                                if ai_monster_zones_array[4].zone.getCardByIndex(0) == current_monster:
                                    current_monster_zone = ai_monster_zones_array[4]
                                    zone_monster = current_monster_zone.zone.getCardByIndex(0)
                                    winning_card = None
        
      
                                    target_monster = gf.monsterAction(current_monster_zone, player_monster_zones_array, screen, ai_monster_zones_array, 4, card_layout, card_surface, card_desc_surface, player_spell_and_trap_zones_array, ai_spell_and_trap_zones_array, zone_lines_tuple, player_graveyard_gui, ai_graveyard_gui, card_info_panel, phealth, xhealth, card_name_font, lp_font, game_instance.player.name, game_instance.ai.name, current_turn_box_dimensions, current_turn_box_dimensions2, game_instance, ai_field_gui, player_field_gui, egyptian_background, ai_deck_gui, player_deck_gui, main_phase_block, battle_phase_block, end_phase_block, ee, turn_text_width, turn_text, 4, active_field_card_img, active_field_card_display)  
                                    ai_monsters_per_zone.remove(current_monster)
                                    if target_monster == None:
                                        if game_instance.current_turn == 1:
                                            if zone_monster.current_def_points > zone_monster.current_atk_points:
                                                zone_monster.in_atk_position = not zone_monster.in_atk_position
                                                current_monster_zone.setZoneCardImg()                                
                                        ai_monster_zones_ok[4] = True
                                        ai_end_monsters_turn = True
                                    else:     

                                        game_instance.ai.is_attacking = True
                                        if target_monster == "Direct attack":
                                            enemy_card = None
                                        else:
                                            enemy_card = target_monster.zone.getCardByIndex(0)
                                            
                                        player_traps = gf.trap_trigger_check(zone_monster, game_instance.player, game_instance, attacked_monster=enemy_card) 
                                 
                                        if len(player_traps) > 0:
                                            trap_tooltip_active = True
                                            player_trap_selecting = True
                                 
                                            if not player_trap_selecting:
                                                gf.fade(game_settings.screen_width, game_settings.screen_height, screen, screen, flag=False)
                                                winning_card = battleScreen(game_settings, game_instance, clock, screen, zone_monster, enemy_card, selected_field_card_option_box, lp_font)
                                                ai_monster_zones_ok[4] = True  
                                     
                                            else:
                                                selected_field_card = zone_monster                        
                                                ai_monster_zones_ok[4] = False
                                                attacking_zone = 4
                                       
                                        else:   
              
                                            gf.fade(game_settings.screen_width, game_settings.screen_height, screen, screen, flag=False)                                        
                                            winning_card = battleScreen(game_settings, game_instance, clock, screen, zone_monster, enemy_card, selected_field_card_option_box, lp_font)
                                            
                                            ai_monster_zones_ok[4] = True
                                            
                                    for zone in player_monster_zones_array + ai_monster_zones_array + player_spell_and_trap_zones_array + ai_spell_and_trap_zones_array:
                                        zone.setZoneCardImg()
                                        
                                    equip_zones = [zone for zone in player_spell_and_trap_zones_array + ai_spell_and_trap_zones_array if zone.zone.getNumOfCardsContained() == 1 and zone.zone.getCardByIndex(0).spell_or_trap_type == "Equip" and zone.zone.getCardByIndex(0).equipped_monster]                          
                                    for zone in equip_zones:
                                        if zone.zone.getCardByIndex(0).equipped_monster:
                                            if zone.zone.getCardByIndex(0).equipped_monster.current_zone == None:
                                                zone.zone.removeCardFromZone(zone.zone.getCardByIndex(0), "To graveyard")
                                                zone.setZoneCardImg()                                            
                        
                                    player_field_gui.setZoneCardImg()
                                    ai_field_gui.setZoneCardImg()
                                    player_graveyard_gui.setZoneCardImg(lp_font)
                                    ai_graveyard_gui.setZoneCardImg(lp_font)
                                    
                                    if winning_card:
                                        if winning_card.card_owner == game_instance.player:
                                            xhealth.setHealth(game_instance.ai.life_points)
                                        else:
                                            phealth.setHealth(game_instance.player.life_points)
                                            

                                    
                                    if game_instance.player.life_points == 0:
                                        endGame = True
                                        game_instance.endGame("No life points left.", game_instance.player)
                                        #goToLastSavedScreen(player_dict, screen, game_settings)
                                        
                                    elif game_instance.ai.life_points == 0:
                                        endGame = True
                                        game_instance.endGame("No life points left.", game_instance.ai) 

                                    if not player_trap_selecting:
                                        actions3 = False
                                        ai_field_actions2 = True                                      
                                else:
                                    ai_monster_zones_ok[4] = True                                          
                                ee = pygame.time.get_ticks()  
                            else:
                                ai_monster_zones_ok[4] = True     
                        else:
                            ai_monster_zones_ok[4] = True  
            else:
                ai_monster_zones_ok = [True for _ in range(5)]

            if ai_end_monsters_turn and ai_monster_zones_ok[0] and ai_monster_zones_ok[1] and ai_monster_zones_ok[2] and ai_monster_zones_ok[3] and ai_monster_zones_ok[4] and len(ai_monsters_per_zone) == 0:
                actions3 = False
                ai_end_phase_timer = pygame.time.get_ticks()  
                ai_end_phase = True           
            
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
         
        selected_card_options_pointers = (mouse_pos[0]-selected_card_option_box.rect.x, mouse_pos[1]-selected_card_option_box.rect.y)
        
        for option in selected_card_option_box.options:
            option.setPos(selected_card_option_box.card.card)
            if option.rect.collidepoint(selected_card_options_pointers) and not game_instance.game_over:
                option.setBgColor(Settings.GOLD)
                if mouse_click_status[0] == 1:
                    if not selecting_zone:
                        selected_card = selected_card_option_box.card
                        if option.text == "Set" or option.text == "Summon" or option.text == "Activate":
                            hand_card_index = selected_card.card_index
                        if option.text != "Cancel":
                            if selected_card_option_box.card.card.card_type == "Monster":
                                if option.text == "Set" or option.text == "Summon":
                          
                                    zone_display_on = True
                                    
                                    if option.text == "Set":
                                        selected_card.card.is_set = True
                                    else:   
                                        selected_card.card.is_set = False
                                        
                                    selected_card_option_box.card = None
                                    selected_card_option_box.options = []
                                    selecting_zone = True     
                                 
                                    fuse_down_ctr = 0
                                    fuse_up_ctr = 0
                                    up_fusion_order_box_array = []
                                    down_fusion_order_box_array = []
                                    current_player_fusing = False 
                                 
                                else:
                                    fuse_up_ctr, fuse_down_ctr = gf.chooseCardToFuse(option.text, selected_card, selected_card_option_box, fuse_up_ctr, fuse_down_ctr)
                                    myIndex = selected_card.card_index
                                    if option.text == "Fuse Up":
                                        text = fuse_up_ctr
                                        color = Settings.BLUE
                                        fusion_order_box = FusionOrderBox(screen, [20, 20], selected_card.rect.x-7, selected_card.rect.y-7, color, str(text), True, lp_font, selected_card, index=myIndex)    
                                        up_fusion_order_box_array.append(fusion_order_box)
                                    else:
                                        text = fuse_down_ctr
                                        color = Settings.GOLD
                                        fusion_order_box = FusionOrderBox(screen, [20, 20], selected_card.rect.x-7, selected_card.rect.y-7, color, str(text), True, lp_font, selected_card, index=myIndex)
                                        down_fusion_order_box_array.append(fusion_order_box)


                            else:#elif selected_card_option_box.card.card.card_type == "Spell":
                            
                            
                                if option.text == "Set" or option.text == "Activate":
                                    place_spell_timer_interval2 = pygame.time.get_ticks()
                                    
                                    fuse_down_ctr = 0
                                    fuse_up_ctr = 0
                                    up_fusion_order_box_array = []
                                    down_fusion_order_box_array = []
                                    current_player_fusing = False 
                                    
                                    if selected_card_option_box.card.card.spell_or_trap_type != "Field":
                                        spell_zone_display_on = True
                                        
                                        if option.text == "Set":
                                            selected_card.card.is_set = True
                                        else:                                  
                                            selected_card.card.is_set = False
                                        
                                        #for card in cards:
                                        #    card.is_visible = False
                                        
                                        selected_card_option_box.card = None
                                        selected_card_option_box.options = []
                                        selecting_zone = True  
                                    elif selected_card_option_box.card.card.spell_or_trap_type == "Field":
                                        current_player_grave = None
                                        
                                        
                                        if hand_card_index == 4:
                                            real_index = 0
                                        elif hand_card_index == 3:
                                            real_index = 1
                                        elif hand_card_index == 2:
                                            real_index = 2
                                        elif hand_card_index == 1:
                                            real_index = 3
                                        else:
                                            real_index = 4
                                        cards[hand_card_index].contained = False
                                        cards.pop(hand_card_index)   
                                        hand_cards_status[hand_card_index]["card"] = None    
                                            
                                        if game_instance.current_turn_player == game_instance.player:
                                            game_instance.player.cards_gui = cards
                                            for card in game_instance.player.cards_in_hand:

                                                if card == selected_card.card:
                                                    game_instance.player.cards_in_hand.remove(card)
                                        else:
                                            game_instance.ai.cards_gui = cards
                                            for card in game_instance.ai.cards_in_hand:
                                                if card == selected_card.card:
                                                    game_instance.ai.cards_in_hand.remove(card)
        
                                            
                                        if option.text == "Set":
                                            selected_card.card.is_set = True

                                            current_player_field_zone = player_field_gui
                                            current_player_grave = player_graveyard_gui
                                            if game_instance.current_turn_player == game_instance.ai:
                                                current_player_field_zone = ai_field_gui
                                                current_player_grave = ai_graveyard_gui
                                            if current_player_field_zone.zone.getNumOfCardsContained() == 1:    
                                                #current_player_field_zone.zone.removeCardFromZone(current_player_field_zone.zone.getCardByIndex(0), "To graveyard")
                                                #current_player_field_zone.zone.placeCardToZone(selected_card.card)
                                                current_player_field_zone.setZoneCardImg()
                                                current_player_grave.setZoneCardImg(lp_font)
                                                active_field_card_display = False
                                                active_field_card = None
                                        else:
                                            selected_card.card.is_set = False
                                            selected_field_card = selected_card.card   
                                            if selected_field_card.spell_or_trap_type == "Field":
                                            
                                                enemy_field_zone = player_field_gui
                                                enemy_graveyard = player_graveyard_gui
                                                current_player_grave = ai_graveyard_gui
                                                #current_player_field_zone = ai_graveyard_gui
                                                if game_instance.current_turn_player == game_instance.player:
                                                    enemy_field_zone = ai_field_gui
                                                    enemy_graveyard = ai_graveyard_gui
                                                    current_player_grave = player_graveyard_gui
                                                    #current_player_field_zone = player_graveyard_gui
                                                """
                                                if current_player_field_zone.zone.getNumOfCardsContained() == 1:  
                                                    current_player_field_zone.zone.removeCardFromZone(current_player_field_zone.zone.getCardByIndex(0), "To graveyard")
                                                    current_player_field_zone.zone.placeCardToZone(selected_card.card)
                                                    current_player_field_zone.setZoneCardImg()
                                                    current_player_grave.setZoneCardImg(lp_font)
                                                    active_field_card_display = False
                                                    active_field_card = None
                                                """
                                                if enemy_field_zone.zone.getNumOfCardsContained() == 1:
                                                    if not enemy_field_zone.zone.getCardByIndex(0).is_set:
                                                        enemy_field_zone.zone.removeCardFromZone(enemy_field_zone.zone.getCardByIndex(0), "To graveyard")
                                                        enemy_field_zone.setZoneCardImg()
                                                        enemy_graveyard.setZoneCardImg(lp_font)
                                                        active_field_card = None
                                                        active_field_card_display = False

                                            if selected_field_card.spell_or_trap_type == "Equip":
                                                activate_delay_duration = 3000#1500
                                            else:
                                                activate_delay_duration = 0
                                                
                                            activate_delay_timer = pygame.time.get_ticks()                                         
                                            activate_delay = True
                                            active_field_card = selected_field_card
                                            """
                                            activated_spell_or_trap_card_display = True
                                            activated_card_center_screen_img.changeImg(selected_field_card.img)
                                            activated_card_center_screen_img.card_type = selected_field_card.card_type
                                            activated_card_center_screen_img.setRect(673.5, 137.5)
                                            spell_trap_card_activation_delay4 = pygame.time.get_ticks()
                                            """
                                        

                                        
                                        #for card in cards:
                                            #card.is_visible = False
                                        
                                        selected_card_option_box.card = None
                                        selected_card_option_box.options = []
                                        
                                        if game_instance.current_turn_player == game_instance.player:
                                            field_zone = player_field_gui
                                        else:
                                            field_zone = ai_field_gui
                                            
                                        if field_zone.zone.getNumOfCardsContained() == 1:  
                                            #field_zone.zone.removeCardFromZone(field_zone.zone.getCardByIndex(0), "To graveyard")
                                            field_zone.zone.placeCardToZone(selected_card.card)
                                            current_player_grave.setZoneCardImg(lp_font)
                                            field_zone.setZoneCardImg()
                                        else:    
                                            field_zone.zone.placeCardToZone(selected_card.card)
                                            field_zone.setZoneCardImg()
                                        
                                        game_instance.current_turn_player.has_played_a_card_this_turn = True
                                
                                        main_phase_block.changeActiveStatus()
                                        main_phase_block.changeColor()
                                        
                                        battle_phase_block.changeActiveStatus()
                                        battle_phase_block.changeColor()
                                else:
                                    fuse_up_ctr, fuse_down_ctr = gf.chooseCardToFuse(option.text, selected_card, selected_card_option_box, fuse_up_ctr, fuse_down_ctr)
                                    myIndex = selected_card.card_index
                                    if option.text == "Fuse Up":
                                        text = fuse_up_ctr
                                        color = Settings.BLUE
                                        fusion_order_box = FusionOrderBox(screen, [20, 20], selected_card.rect.x-7, selected_card.rect.y-7, color, str(text), True, lp_font, selected_card, index=myIndex)    
                                        up_fusion_order_box_array.append(fusion_order_box)
                                    else:
                                        text = fuse_down_ctr
                                        color = Settings.GOLD
                                        fusion_order_box = FusionOrderBox(screen, [20, 20], selected_card.rect.x-7, selected_card.rect.y-7, color, str(text), True, lp_font, selected_card, index=myIndex)
                                        down_fusion_order_box_array.append(fusion_order_box)
                                          
                        else:
                            selected_card.rect.y = 540
                            
                            if selected_card.is_fusing_up:
                                fuse_up_ctr -= 1
                                
                                myIndex = selected_card.card_index
                                
                                for box in up_fusion_order_box_array.copy():
                                    if box.index == myIndex:
                                        up_fusion_order_box_array.remove(box)
                                        
                                for i in range(1, len(up_fusion_order_box_array)+1):
                                    up_fusion_order_box_array[i-1].changeText(str(i), Settings.BLUE)
                             
                            if selected_card.is_fusing_down:       
                                fuse_down_ctr -= 1
                                myIndex = selected_card.card_index
                                for box in down_fusion_order_box_array.copy():
                                    if box.index == myIndex:
                                        down_fusion_order_box_array.remove(box)                               
                                for i in range(1, len(down_fusion_order_box_array)+1):
                                    down_fusion_order_box_array[i-1].changeText(str(i), Settings.GOLD)
                                    
                                    
                            selected_card.is_fusing = False
                            selected_card.is_fusing_up = False
                            selected_card.is_fusing_down = False
                        break
            else:
                option.setBgColor(Settings.LIGHT_GRAY)                   
        
        if fuse_down_ctr != 0 or fuse_up_ctr != 0:
            current_player_fusing = True
        else:
            current_player_fusing = False
        
        if selecting_zone or game_instance.current_turn_player.is_attacking or current_player_fusing:
            if zone_display_on or game_instance.current_turn_player.is_attacking or spell_zone_display_on:
                displayed_tooltip = "Select an available zone indicated by the highlighted zones. To cancel, press the ESC key."
            elif fuse_down_ctr != 0 or fuse_up_ctr != 0:
                displayed_tooltip = "Select at least 2 cards to begin fusing. Press the Spacebar to finish the fusing process. To cancel, press the ESC key."
            tt_width, tt_height = option_font.size(displayed_tooltip)
            pygame.draw.rect(screen, Settings.LIGHT_GRAY, [(325+(945/2))-(tt_width/2), 70, tt_width, tt_height+20])
            my_tooltip = option_font.render(displayed_tooltip, True, Settings.BLACK)
            screen.blit(my_tooltip, [(325+(945/2))-(tt_width/2), 70+((tt_height+10)/2)])
            
            if game_instance.current_turn_player.is_attacking:
                if game_instance.current_turn_player == game_instance.player:
                    pygame.draw.rect(screen, Settings.GREEN, [selected_field_zone.rect.x, selected_field_zone.rect.y, selected_field_zone.area.get_width(), selected_field_zone.area.get_height()], 2)
            
            
        if game_instance.current_turn_player == game_instance.player:
            if gf.isHandReady(cards):
                if selected_cards_in_hand > 0:
                    if not selecting_zone:
                        selected_card_option_box.blit()
                else:
                    if selected_card_option_box.area != None:
                        if selected_card_option_box.rect.collidepoint(mouse_pos) and not game_instance.game_over:
                            if not selecting_zone:
                                selected_card_option_box.blit()
                    else:
                        selected_card_option_box.options = []
        else:
            if ai_field_actions and not game_instance.game_over:

                if ai_main_phase_end:
                    feck = pygame.time.get_ticks()  
                    
                    if activated_spell_or_trap_card_display or activate_delay:
                        pygame.draw.rect(screen, Settings.RED, [ai_spell_and_trap_zones_array[ai_spell_index].rect.x, ai_spell_and_trap_zones_array[ai_spell_index].rect.y, 129.2, 111.75], 5)           
                        if selected_field_card:
                            if selected_field_card.spell_or_trap_type == "Equip":
                                pygame.draw.rect(screen, Settings.RED, [ai_monster_zones_array[target_equip_mons_zone].rect.x, ai_monster_zones_array[target_equip_mons_zone].rect.y, 129.2, 111.75], 5) 
                    
                    if feck - q >= 1000:
                        if not gf.isEnemyMonsterZoneEmpty(ai_spell_and_trap_zones_array):
                            if not activate_delay and not ai_spell_zones_ok[0] and not activated_spell_or_trap_card_display and not ai_spell_spacing_timer_active:
                                pygame.draw.rect(screen, Settings.RED, [ai_spell_and_trap_zones_array[0].rect.x, ai_spell_and_trap_zones_array[0].rect.y, 129.2, 111.75], 5)                
                                ff = pygame.time.get_ticks()
                                if ff-q >= 1400:
                                    if ai_spell_and_trap_zones_array[0].zone.getNumOfCardsContained() == 1:
                                        if not activate_delay and not activated_spell_or_trap_card_display_equip:   
                                            set_spell_card = ai_spell_and_trap_zones_array[0].zone.getCardByIndex(0)

                                            if not set_spell_card.has_been_activated and set_spell_card.aiUseCondition(game_instance) and set_spell_card.card_type == "Spell" and not ai_activating_spell:
                                                ai_spell_index = 0
                                                set_spell_card.is_set = False
                                                ai_spell_and_trap_zones_array[0].setZoneCardImg()
                                                selected_field_card = set_spell_card
                                                
                                                
                                                if set_spell_card.spell_or_trap_type == "Equip":
                                                    equip_target = set_spell_card.aiGetEquipTarget()
                                                    set_spell_card.equip(equip_target)
                                                    
                                                    equip_target.is_set = False
                                                    
                                                    for zone in ai_monster_zones_array:
                                                        if zone.zone.getNumOfCardsContained() == 1:
                                                            contained_monster = zone.zone.getCardByIndex(0)
                                                            if contained_monster == equip_target:
                                                                target_equip_mons_zone = zone.index
                                                                zone.setZoneCardImg()
                                                                activate_delay_duration = 1500
                                                else:
                                                    activate_delay_duration = 0   

                                                activate_delay_timer = pygame.time.get_ticks()                                         
                                                activate_delay = True
                                            else:
                                                ai_spell_zones_ok[0] = True
                                        else:
                                            ai_spell_zones_ok[0] = True
                                    else:
                                        ai_spell_zones_ok[0] = True  
                            if not activate_delay and not ai_spell_zones_ok[1] and ai_spell_zones_ok[0] and not ai_spell_spacing_timer_active and not activated_spell_or_trap_card_display:
                                pygame.draw.rect(screen, Settings.RED, [ai_spell_and_trap_zones_array[1].rect.x, ai_spell_and_trap_zones_array[1].rect.y, 129.2, 111.75], 5)                
                                gg = pygame.time.get_ticks()
                                if gg-ff >= 400:
                                    if ai_spell_and_trap_zones_array[1].zone.getNumOfCardsContained() == 1:
                                        if not activate_delay and not activated_spell_or_trap_card_display_equip:
                                            set_spell_card = ai_spell_and_trap_zones_array[1].zone.getCardByIndex(0)
                                            if not set_spell_card.has_been_activated and set_spell_card.aiUseCondition(game_instance) and set_spell_card.card_type == "Spell" and not ai_activating_spell:
                                                ai_spell_index = 1
                                                set_spell_card.is_set = False
                                                ai_spell_and_trap_zones_array[1].setZoneCardImg()
                                                selected_field_card = set_spell_card
                                                
                                                
                                                if set_spell_card.spell_or_trap_type == "Equip":
                                                    equip_target = set_spell_card.aiGetEquipTarget()
                                                    set_spell_card.equip(equip_target)
                                                    
                                                    equip_target.is_set = False
                                                    
                                                    for zone in ai_monster_zones_array:
                                                        if zone.zone.getNumOfCardsContained() == 1:
                                                            contained_monster = zone.zone.getCardByIndex(0)
                                                            if contained_monster == equip_target:
                                                                target_equip_mons_zone = zone.index
                                                                zone.setZoneCardImg()
                                                                activate_delay_duration = 1500
                                                else:
                                                    activate_delay_duration = 0  
                                                    
                                                activate_delay_timer = pygame.time.get_ticks()  
                                                activate_delay = True 
                                            else:
                                                ai_spell_zones_ok[1] = True
                                        else:
                                            ai_spell_zones_ok[1] = True
                                    else:
                                        ai_spell_zones_ok[1] = True                               
                            if not activate_delay and not ai_spell_zones_ok[2] and ai_spell_zones_ok[1] and not ai_spell_spacing_timer_active and not activated_spell_or_trap_card_display:
                                pygame.draw.rect(screen, Settings.RED, [ai_spell_and_trap_zones_array[2].rect.x, ai_spell_and_trap_zones_array[2].rect.y, 129.2, 111.75], 5)                
                                hh = pygame.time.get_ticks()
                                if hh-gg >= 400:
                                    if ai_spell_and_trap_zones_array[2].zone.getNumOfCardsContained() == 1:
                                        if not activate_delay and not activated_spell_or_trap_card_display_equip:
                                            set_spell_card = ai_spell_and_trap_zones_array[2].zone.getCardByIndex(0)
                                            if not set_spell_card.has_been_activated and set_spell_card.aiUseCondition(game_instance) and set_spell_card.card_type == "Spell" and not ai_activating_spell:
                                                ai_spell_index = 2
                                                set_spell_card.is_set = False
                                                ai_spell_and_trap_zones_array[2].setZoneCardImg()
                                                selected_field_card = set_spell_card
                                                
                                                
                                                if set_spell_card.spell_or_trap_type == "Equip":
                                                    equip_target = set_spell_card.aiGetEquipTarget()
                                                    set_spell_card.equip(equip_target)
                                                    
                                                    equip_target.is_set = False
                                                    
                                                    for zone in ai_monster_zones_array:
                                                        if zone.zone.getNumOfCardsContained() == 1:
                                                            contained_monster = zone.zone.getCardByIndex(0)
                                                            if contained_monster == equip_target:
                                                                target_equip_mons_zone = zone.index
                                                                zone.setZoneCardImg()
                                                                activate_delay_duration = 1500
                                                else:
                                                    activate_delay_duration = 0  
                                                    
                                                activate_delay_timer = pygame.time.get_ticks()  
                                                activate_delay = True  
                                            else:
                                                ai_spell_zones_ok[2] = True
                                        else:
                                            ai_spell_zones_ok[2] = True
                                    else:
                                        ai_spell_zones_ok[2] = True                                                                
                            if not activate_delay and not ai_spell_zones_ok[3] and ai_spell_zones_ok[2] and not ai_spell_spacing_timer_active and not activated_spell_or_trap_card_display:
                                pygame.draw.rect(screen, Settings.RED, [ai_spell_and_trap_zones_array[3].rect.x, ai_spell_and_trap_zones_array[3].rect.y, 129.2, 111.75], 5)                
                                ii = pygame.time.get_ticks()
                                if ii-hh >= 400:
                                    if ai_spell_and_trap_zones_array[3].zone.getNumOfCardsContained() == 1:
                                        if not activate_delay and not activated_spell_or_trap_card_display_equip:
                                            set_spell_card = ai_spell_and_trap_zones_array[3].zone.getCardByIndex(0)
                                            if not set_spell_card.has_been_activated and set_spell_card.aiUseCondition(game_instance) and set_spell_card.card_type == "Spell" and not ai_activating_spell:
                                                ai_spell_index = 3
                                                set_spell_card.is_set = False
                                                ai_spell_and_trap_zones_array[3].setZoneCardImg()
                                                selected_field_card = set_spell_card
                                                
                                                if set_spell_card.spell_or_trap_type == "Equip":
                                                    equip_target = set_spell_card.aiGetEquipTarget()
                                                    set_spell_card.equip(equip_target)
                                                    
                                                    equip_target.is_set = False
                                                    
                                                    for zone in ai_monster_zones_array:
                                                        if zone.zone.getNumOfCardsContained() == 1:
                                                            contained_monster = zone.zone.getCardByIndex(0)
                                                            if contained_monster == equip_target:
                                                                target_equip_mons_zone = zone.index
                                                                zone.setZoneCardImg()
                                                                activate_delay_duration = 1500
                                                else:
                                                    activate_delay_duration = 0 
                                                    
                                                activate_delay_timer = pygame.time.get_ticks()  
                                                activate_delay = True  
                                            else:
                                                ai_spell_zones_ok[3] = True
                                        else:
                                            ai_spell_zones_ok[3] = True
                                    else:
                                        ai_spell_zones_ok[3] = True
                            if not activate_delay and not ai_spell_zones_ok[4] and ai_spell_zones_ok[3] and not ai_spell_spacing_timer_active and not activated_spell_or_trap_card_display:
                                pygame.draw.rect(screen, Settings.RED, [ai_spell_and_trap_zones_array[4].rect.x, ai_spell_and_trap_zones_array[4].rect.y, 129.2, 111.75], 5)                
                                jj = pygame.time.get_ticks()
                                if jj-ii >= 400:
                                    if ai_spell_and_trap_zones_array[4].zone.getNumOfCardsContained() == 1:
                                        if not activate_delay and not activated_spell_or_trap_card_display_equip:
                                            set_spell_card = ai_spell_and_trap_zones_array[4].zone.getCardByIndex(0)
                                            if not set_spell_card.has_been_activated and set_spell_card.aiUseCondition(game_instance) and set_spell_card.card_type == "Spell" and not ai_activating_spell:
                                                ai_spell_index = 4
                                                set_spell_card.is_set = False
                                                ai_spell_and_trap_zones_array[4].setZoneCardImg()
                                                selected_field_card = set_spell_card
                                                
                                                
                                                if set_spell_card.spell_or_trap_type == "Equip":
                                                    equip_target = set_spell_card.aiGetEquipTarget()
                                                    set_spell_card.equip(equip_target)
                                                    
                                                    equip_target.is_set = False
                                                    
                                                    for zone in ai_monster_zones_array:
                                                        if zone.zone.getNumOfCardsContained() == 1:
                                                            contained_monster = zone.zone.getCardByIndex(0)
                                                            if contained_monster == equip_target:
                                                                target_equip_mons_zone = zone.index
                                                                zone.setZoneCardImg()
                                                                activate_delay_duration = 1500
                                                else:
                                                    activate_delay_duration = 0  
                                                activate_delay_timer = pygame.time.get_ticks()                                             
                                                activate_delay = True
                                            else:
                                                ai_spell_zones_ok[4] = True
                                        else:
                                            ai_spell_zones_ok[4] = True
                                    else:
                                        ai_spell_zones_ok[4] = True 
                            if ai_spell_zones_ok[4] and ai_spell_zones_ok[3] and ai_spell_zones_ok[2] and ai_spell_zones_ok[1] and ai_spell_zones_ok[0]: 

                                ai_field_actions = False
                                ai_field_actions2 = True
                                fuac = pygame.time.get_ticks()
                        else:
                            ai_field_actions = False
                            ai_field_actions2 = True        
                            fuac = pygame.time.get_ticks()                 
        
        if current_player_fusing or fusion_indices:
            for box in down_fusion_order_box_array + up_fusion_order_box_array:
                box.blit()
        
        card_info_panel.blit(card_name_font, card_layout.card_type)
        turn_text_width, turn_text_height = turn_font.size(str(game_instance.current_turn))
        turn_text = turn_font.render(str(game_instance.current_turn), True, Settings.WHITE)
        
        pygame.draw.rect(screen, Settings.RED, current_turn_box_dimensions, 1)
        pygame.draw.rect(screen, Settings.RED, current_turn_box_dimensions2, 1)
            
        gf.drawHealthBars(phealth, xhealth, screen, card_name_font, lp_font, game_instance.player.name, game_instance.ai.name)
        screen.blit(turn_text, [797.5-(turn_text_width/2), 17])
        
        if activated_spell_or_trap_card_display:
            #pygame.draw.rect(screen, Settings.RED, [673.5, 137.5, 248, 360], 0)
            spell_trap_card_activation_delay5 = pygame.time.get_ticks()
            activated_card_center_screen_img.blit() 
            if spell_trap_card_activation_delay5 - spell_trap_card_activation_delay4 >= 1000:
                if not trap_activating:
   
                    selected_field_card.activate()
                    
                    equip_zones = [zone for zone in player_spell_and_trap_zones_array + ai_spell_and_trap_zones_array if zone.zone.getNumOfCardsContained() == 1 and zone.zone.getCardByIndex(0).spell_or_trap_type == "Equip" and zone.zone.getCardByIndex(0).equipped_monster]                          
                    for zone in equip_zones:
                        if zone.zone.getCardByIndex(0).equipped_monster:
                            if zone.zone.getCardByIndex(0).equipped_monster.current_zone == None:
                                zone.zone.removeCardFromZone(zone.zone.getCardByIndex(0), "To graveyard")
                                zone.setZoneCardImg()                                            
    

                    
                    for zone in player_monster_zones_array + ai_monster_zones_array + player_spell_and_trap_zones_array + ai_spell_and_trap_zones_array:
                        zone.setZoneCardImg()
                    
                    player_field_gui.setZoneCardImg()
                    ai_field_gui.setZoneCardImg()
                    player_graveyard_gui.setZoneCardImg(lp_font)
                    ai_graveyard_gui.setZoneCardImg(lp_font)
                    
                    if selected_field_card.spell_or_trap_type == "Normal":
                        selected_field_card.current_zone.zone_gui.setZoneCardImg(lp_font)
                    selected_field_spell_trap_card_option_box.card = None
                    selected_field_card_option_box.card = None
                    gf.fade(game_settings.screen_width, game_settings.screen_height, screen, screen, flag=False)
                    
                    if selected_field_card.will_animate:
                        if selected_field_card.single_card_animation:
                            single_spell_trap_animation_screen(game_settings, clock, screen, selected_field_card)
                
                    #selected_field_card.guiScreen()
                    
                    if selected_field_card.spell_or_trap_type == "Field":
                        if active_field_card:
                            active_field_card_display = True
                            active_field_card_img = pygame.image.load(gf.getFieldCardImg(active_field_card.id))
                            
                    ai_activating_spell = False
                else:
                    trap_activating_effect = True 

                selected_field_card.has_been_activated = True        
                flagger = False    
                activated_spell_or_trap_card_display = False           
                player_graveyard_gui.setZoneCardImg(lp_font)
                ai_graveyard_gui.setZoneCardImg(lp_font)
                                              
                for card in player_graveyard_gui.zone.getCards() + ai_graveyard_gui.zone.getCards():
                    if card.card_type == "Monster":
                        card.resetStatus()
                        
                if activating_from_hand == True:
                    ai_main_phase_end = True     
                    activating_from_hand = False
                    
                if game_instance.current_turn_player == game_instance.ai:
                    if not trap_select_active:
                        if selected_field_card.spell_or_trap_type != "Field":     
                            ai_spell_zones_ok[ai_spell_index] = True
                            
                else:
                    if selected_field_card.card_type != "Monster":
                        if selected_field_card.spell_or_trap_type != "Equip":
                            player_equip_target_monster = None   

                xhealth.setHealth(game_instance.ai.life_points)
                phealth.setHealth(game_instance.player.life_points)
                
                if game_instance.ai.life_points > game_instance.ai.starting_life_points:
                    xhealth.full_health = game_instance.ai.life_points

                if game_instance.player.life_points > game_instance.player.starting_life_points:
                    phealth.full_health = game_instance.player.life_points
                #effectScreen(selected_field_card)
                activated_spell_or_trap_card_display_equip = False
                
                if game_instance.player.life_points == 0:
                    endGame = True
                    game_instance.endGame("No life points left.", game_instance.player)
                    #goToLastSavedScreen(player_dict, screen, game_settings)
                    
                elif game_instance.ai.life_points == 0:
                    endGame = True
                    game_instance.endGame("No life points left.", game_instance.ai)
        
        if select_player_equip_target:
            tt_width, tt_height = option_font.size(select_equip_tooltip)
            pygame.draw.rect(screen, Settings.LIGHT_GRAY, [(325+(945/2))-(tt_width/2), 70, tt_width, tt_height+20])
            my_tooltip = option_font.render(select_equip_tooltip, True, Settings.BLACK)
            screen.blit(my_tooltip, [(325+(945/2))-(tt_width/2), 70+((tt_height+10)/2)])  
         
        
        if activate_delay == True:
            activated_card_center_screen_img.changeImg(selected_field_card.img)
            activated_card_center_screen_img.card_type = selected_field_card.card_type
            activated_card_center_screen_img.setRect(673.5, 137.5)
            bogbog = pygame.time.get_ticks()
            if bogbog - activate_delay_timer >= activate_delay_duration:
           
                activated_spell_or_trap_card_display_equip = True 
                gbagbo = pygame.time.get_ticks()
                #activated_spell_or_trap_card_display = True                           
                activate_delay = False

        if endGame or endGameDelay or endGameDelay2:
            screen.blit(endGameSurface, (0, 0))

        if endGame:
            end_screen_delay_timer1 = pygame.time.get_ticks()
            endGame = False
            endGameDelay = True
            if game_instance.winner == game_instance.player:
                upper_display_text = you_win_text
                upper_display_x = you_win_text_x
                
                lower_display_text = win_text
                lower_display_x = win_text_x
            else:
                upper_display_text = you_lose_text
                upper_display_x = you_lose_text_x
                
                lower_display_text = lose_text
                lower_display_x = lose_text_x            
            
        if endGameDelay:
            end_screen_delay_timer2 = pygame.time.get_ticks()
            if end_screen_delay_timer2 - end_screen_delay_timer1 >= 2000:
                if upper_x < upper_display_x:
                    screen.blit(upper_display_text, [upper_x, 140])
                    upper_x += 12
                else:
                    screen.blit(upper_display_text, [upper_display_x, 140])
                    
                if lower_x > lower_display_x:
                    screen.blit(lower_display_text, [lower_x, 340])
                    lower_x -= 15                 
                else:
                    screen.blit(lower_display_text, [lower_display_x, 340])
                    exit_screen_timer = pygame.time.get_ticks()
                    endGameDelay2 = True
                    endGameDelay = False
                    
        if endGameDelay2:
            screen.blit(upper_display_text, [upper_display_x, 140])
            screen.blit(lower_display_text, [lower_display_x, 340])
            
            timer = pygame.time.get_ticks()
            if timer - exit_screen_timer >= 2500:
                gf.fade(game_settings.screen_width, game_settings.screen_height, screen, screen, flag=False)
                duel_results_screen(game_instance, screen, card_desc_surface, card_info_panel, card_layout, card_surface)
       
        if activated_spell_or_trap_card_display_equip:
            activated_card_center_screen_img.blit() 
            gbagbo2 = pygame.time.get_ticks()
                    
            if gbagbo2 - gbagbo >= 500:
                if game_instance.current_turn_player == game_instance.ai:
                    if ai_spell_index == 0:
                        ff = pygame.time.get_ticks()
                        spell_trap_card_activation_delay4 = feck
                    elif ai_spell_index == 1:
                        gg = pygame.time.get_ticks()    
                        spell_trap_card_activation_delay4 = ff                    
                    elif ai_spell_index == 2:
                        hh = pygame.time.get_ticks()  
                        spell_trap_card_activation_delay4 = gg                    
                    elif ai_spell_index == 3:
                        ii = pygame.time.get_ticks() 
                        spell_trap_card_activation_delay4 = hh
                    elif ai_spell_index == 4:
                        jj = pygame.time.get_ticks()    
                        spell_trap_card_activation_delay4 = ii                    
                    ai_activating_spell = True
                else:
                    spell_trap_card_activation_delay4 = pygame.time.get_ticks()
                    
                activated_spell_or_trap_card_display = True       
                activated_spell_or_trap_card_display_equip = False
       
        pygame.display.flip()
        clock.tick(60)

def duel_results_screen(game_instance, screen, card_desc_surface, card_info_panel, card_layout, card_surface):
    smaller_font = pygame.font.Font(None, 30) 
    small_font = pygame.font.Font(None, 38) 
    clock = pygame.time.Clock()
    results_graphic = pygame.image.load("images/results_graphic.png") 
    cards_used_box = pygame.image.load("images/cards_used.png")
    remaining_lp_box = pygame.image.load("images/remaining_lp.png")
    duel_skill_box = pygame.image.load("images/duel_skill.png")
    card_name_font = pygame.font.SysFont("Segoe UI Symbol", 13)   
 
    player_cards_used = len(game_instance.player.deck.getCards())   
    ai_cards_used = len(game_instance.ai.deck.getCards())
    
    player_lp = str(game_instance.player.life_points)
    player_lp_width, player_lp_height = small_font.size(player_lp)
    
    ai_lp = str(game_instance.ai.life_points)
    ai_lp_width, ai_lp_height = small_font.size(ai_lp)
    
    ai_lp_x = 1090 - (ai_lp_width / 2)
    ai_cards_used_x = 1077
    if ai_cards_used < 10:
        ai_cards_used_x = 1085
    
    player_lp_x = 908 - (player_lp_width / 2)    
    player_cards_used_x = 895
    if player_cards_used < 10:
        player_cards_used_x = 903 

    if game_instance.winner == game_instance.player:
        player_color = Settings.WHITE
        ai_color = Settings.GRAY
        winner = "YOU"
    else:
        player_color = Settings.GRAY         
        ai_color = Settings.WHITE
        winner = "COM"
        
    player_cards_render = small_font.render(str(player_cards_used), True, player_color)
    ai_cards_render = small_font.render(str(ai_cards_used), True, ai_color)
    
    player_lp_render = small_font.render(player_lp, True, player_color)
    ai_lp_render = small_font.render(ai_lp, True, ai_color)
    
    turn_render = smaller_font.render("Duel ended at turn " + str(game_instance.current_turn), True, Settings.WHITE) 
    winner_render = smaller_font.render("Winner    -  -  -    " + winner, True, Settings.WHITE) 
    card_layout.reset()
    
    duel_skill, pow_or_tec = gf.get_duel_skill_img_name(game_instance)
    
    duel_skill_img = pygame.image.load("images/EndCards/" + duel_skill)
    pow_or_tec_image = None
    if pow_or_tec:
        pow_or_tec_image = pygame.image.load("images/EndCards/" + pow_or_tec)
    
    if duel_skill != "loser.png":
        card_won = gf.get_post_duel_card_prize(gf.get_duel_skill_id(duel_skill, pow_or_tec), game_instance.ai.deck.deck_id)
        card_layout.card_type = card_won.card_type
        card_layout.card = card_won
        card_layout.changeImg(card_won.img)
        
        if card_won.card_type == "Monster":
            card_type_info = "[Monster] " + card_won.monster_type + "/" + card_won.monster_attr 
            monst_lvl_and_atk = "[" + u"\u2605" + str(card_won.level) + "]  " + str(card_won.atk_points) + "/" + str(card_won.def_points)
            gs1_img = gf.getGuardianStarImg(card_won.guardian_star_list[0].name)
            gs2_img = gf.getGuardianStarImg(card_won.guardian_star_list[1].name)
            card_info_panel.setCardContent(card_won.name, "Guadian Stars:", card_won.guardian_star_list[0].name, card_won.guardian_star_list[1].name, card_type_info, monst_lvl_and_atk, card_won.text, gs1_img, gs2_img, card_won.fusion_types_string)        
        else:
            card_type_info = "[" + card_won.card_type + "] " + card_won.spell_or_trap_type
            card_info_panel.setCardContent(card_won.name, "", "", "", card_type_info, "", card_won.text, None, None, card_won.fusion_types_string)
            
    while True:        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit() 

        card_desc_surface.blit()
        
        if duel_skill != "loser.png":
            card_info_panel.blit(card_name_font, card_won.card_type)
            if card_won.card_type == "Monster":
                card_layout.blit(card_won.atk_points, card_won.def_points)
            else:
                card_layout.blit()
        else:
            card_layout.blit()
            
        card_surface.blit() 
 
        screen.blit(results_graphic, [(635 - 292) + 163, 15])
        screen.blit(cards_used_box, [(635 - 361) + 163, 130])     
        screen.blit(remaining_lp_box, [(635 - 361) + 163, 230])
        screen.blit(duel_skill_box, [(635 - 361) + 163, 450])
        
        screen.blit(player_cards_render, [player_cards_used_x, 165])
        screen.blit(ai_cards_render, [ai_cards_used_x, 165])
        
        screen.blit(player_lp_render, [player_lp_x, 263])
        screen.blit(ai_lp_render, [ai_lp_x, 263])
        
        screen.blit(turn_render, [(635 - 361) + 163, 320])
        screen.blit(winner_render, [930, 320])
        
        screen.blit(duel_skill_img, [950, 430])
        
        if pow_or_tec_image:
            screen.blit(pow_or_tec_image, [860, 420])
        
        pygame.display.flip()
                
        clock.tick(60) 

def game_over_screen(game_instance, screen):
    clock = pygame.time.Clock()
    background = pygame.image.load("images/gameover.png") 
    
    while True:        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit() 

        screen.blit(background, [0, 0])
        pygame.display.flip()
                
        clock.tick(60)                


def single_spell_trap_animation_screen(game_settings, clock, screen, spell_or_trap_card):
    font = pygame.font.Font("misc/digital-7.ttf", 100)  
    
    pause = 2000  
    pausing = True
    effecting = False
    
    lp_change_text_upper = None
    lp_change_text_lower = None
    
    lp_upper_text = None
    lp_lower_text = None
    
    if spell_or_trap_card.AFFECTS_OPPONENT:
        if spell_or_trap_card.OWNER_LP_CHANGE == 0:
            lp_change_text_upper = spell_or_trap_card.OPPONENT_LP_CHANGE * spell_or_trap_card.card_owner.opponent.starting_life_points
        else:
            lp_change_text_upper = spell_or_trap_card.OWNER_LP_CHANGE * spell_or_trap_card.card_owner.starting_life_points
            lp_change_text_lower = spell_or_trap_card.OPPONENT_LP_CHANGE * spell_or_trap_card.card_owner.opponent.starting_life_points
    else:
        lp_change_text_upper = spell_or_trap_card.OWNER_LP_CHANGE * spell_or_trap_card.card_owner.starting_life_points
     
    lp_upper_string = str(int(lp_change_text_upper))
    lp_upper_width, lp_upper_height = font.size(lp_upper_string)
    
    if lp_change_text_upper < 0:
        color = Settings.RED
    else:
        color = Settings.GREEN
        lp_upper_string = "+" + lp_upper_string
    lp_upper_text = font.render(lp_upper_string, True, color)
    
    if lp_change_text_lower:
        lp_lower_string = str(int(lp_change_text_lower))
        lp_upper_width, lp_upper_height = font.size(lp_lower_string)
        
        if lp_change_text_lower < 0:
            color = Settings.RED
        else:
            color = Settings.GREEN
            lp_lower_string = "+" + lp_lower_string
        lp_lower_text = font.render(lp_lower_string, True, color)    

    
    last = pygame.time.get_ticks()
    now = pygame.time.get_ticks()
    
    spell_or_trap_card_img = CardImage(screen, spell_or_trap_card.card_type, spell_or_trap_card.img, 200, 137.5, spell_or_trap_card)
    spell_or_trap_card_img.setRect(331, 137.5)   

    while True:        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()   

        if pausing:
            now = pygame.time.get_ticks()
            if now - last >= pause:
                pausing = False
                effecting = True
    
        screen.fill(Settings.BLACK)
    
        if effecting:
            return
            
        if lp_upper_text and not lp_lower_text:
            screen.blit(lp_upper_text, [720.5, 280.0]) 
        else:
            screen.blit(lp_upper_text, [720.5, 200.0]) 
            screen.blit(lp_lower_text, [720.5, 350.0]) 
        
        spell_or_trap_card_img.blit()
        pygame.display.flip()
                
        clock.tick(60)

def spell_trap_animation_screen(game_settings, clock, screen, monster_card, spell_or_trap_card, trap_fail=False):
    font = pygame.font.Font("misc/digital-7.ttf", 100)  
    
    last = pygame.time.get_ticks()
    now = pygame.time.get_ticks()

    fade = pygame.Surface((248, 360))

    pause = 1000    
    pausing = True
    fading = False
    
    monster_card_img = CardImage(screen, monster_card.card_type, monster_card.img, 200, 137.5, monster_card)
    spell_or_trap_card_img = CardImage(screen, spell_or_trap_card.card_type, spell_or_trap_card.img, 700, 137.5, spell_or_trap_card) 

    spell_or_trap_card_img.setRect(691, 137.5)
    monster_card_img.setRect(331, 137.5)    
    
    fade = pygame.Surface((248, 360))
    fade.fill((0, 0, 0))
    fade_rect = fade.get_rect()
    fade_rect.x = -1000
    fade_rect.y = -1000    
    
    while True:        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit() 
                
        if pausing:
            now = pygame.time.get_ticks()
            if now - last >= pause:
                pausing = False
                fading = True
                
        if fading:
            fade_timer_after = pygame.time.get_ticks()
            
            if not trap_fail:
                fade_rect.x = monster_card_img.rect.x
                fade_rect.y = monster_card_img.rect.y
            else:
                fade_rect.x = spell_or_trap_card_img.rect.x
                fade_rect.y = spell_or_trap_card_img.rect.y
            
            for alpha in range(0, 300, 5):
                fade.set_alpha(alpha)
                screen.fill(Settings.BLACK)
                monster_card_img.blit(atk_val=monster_card.current_atk_points, def_val=monster_card.current_def_points, color=Settings.BLACK)
                spell_or_trap_card_img.blit()
                screen.blit(fade, fade_rect)
                pygame.display.flip()
                
            return
                
        if not fading:
            screen.fill(Settings.BLACK)
            monster_card_img.blit(atk_val=monster_card.current_atk_points, def_val=monster_card.current_def_points, color=Settings.BLACK)
            spell_or_trap_card_img.blit()
            pygame.display.flip()
                
        clock.tick(60)
                
        
def battleScreen(game_settings, game_instance, clock, screen, attacking_card, attacked_card, selected_field_card_option_box, lp_font):
    font = pygame.font.Font("misc/digital-7.ttf", 100)   
    
    last = pygame.time.get_ticks()
    now = pygame.time.get_ticks()
    new_now = pygame.time.get_ticks()
    pause = 1000
    shake_duration = 1000
    pausing = True
    shaking = False

    attacking_card_img = CardImage(screen, attacking_card.card_type, attacking_card.img, 200, 137.5, attacking_card)
    
    attacking_card_img.rect.x = 331#200
    attacking_card_img.rect.y = 137.5
    attacking_card_color = Settings.BLACK
    
    if attacked_card:
        attacked_card_img = CardImage(screen, attacked_card.card_type, attacked_card.img, 700, 137.5, attacked_card)   
        attacked_card_img.rect.x = 691
        attacked_card_img.rect.y = 137.5        
        attacked_card_color = Settings.BLACK
    
    star_bonus = 0
     
    if attacked_card:
        if attacking_card.guardian_star.gs_id == attacked_card.guardian_star.strong_against_id:
            attacked_card_color = Settings.DARK_GREEN
            star_bonus = 500
        elif attacking_card.guardian_star.gs_id == attacked_card.guardian_star.weak_against_id:
            attacking_card_color = Settings.DARK_GREEN
            star_bonus = 500
        
    battle_data = attacking_card.attack(attacked_card, selected_field_card_option_box, lp_font)#attacking_card.battle(attacking_card, attacked_card)
    winning_card = battle_data[0]
    damage_taken = battle_data[1]

    if damage_taken != 0:
        official_damage = str(abs(damage_taken))
        damage_text_width, damage_text_height = font.size(official_damage)
        damage_text = font.render(official_damage, True, Settings.RED)
    
    fade = pygame.Surface((248, 360))
  
  
    if attacked_card:
        if winning_card == attacking_card:
            losing_card = attacked_card_img
            losing_card_data = attacked_card
        elif winning_card == attacked_card:
            losing_card = attacking_card_img
            losing_card_data = attacking_card
        else:
            losing_card = None
            losing_card_data = None
            fade = pygame.Surface((game_settings.screen_width, game_settings.screen_height))
            
        if losing_card:
            losing_card_centerx = losing_card.rect.centerx
            losing_card_centery = losing_card.rect.centery

    fade.fill((0, 0, 0))
    fade_rect = fade.get_rect()
    fade_rect.x = -1000
    fade_rect.y = -1000
    
    fade_animation = False
    passed = False
    
    while True:        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit() 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if winning_card:
                        winning_card.increaseCurrentDefPoints(-star_bonus)
                        winning_card.increaseCurrentAtkPoints(-star_bonus)
                    return
                    
        if attacked_card:
            if pausing:
                now = pygame.time.get_ticks()
                if now - last >= pause:
                    pausing = False
                    shaking = True
        
            if shaking:
                new_now = pygame.time.get_ticks()
                if new_now - now <= shake_duration:
                
                    if losing_card == attacked_card_img:
                        losing_card.shake([680, 941], [127.5, 507.5])
                        if losing_card_data.destroyed_by_battle:
                            fade_animation = True
                    elif losing_card == attacking_card_img:
                        losing_card.shake([321, 581], [127.5, 507.5])
                        if losing_card_data.destroyed_by_battle:
                            fade_animation = True
                    else:
                        if attacked_card.in_atk_position and attacking_card.in_atk_position:
                            attacked_card_img.shake([680, 941], [127.5, 507.5])
                            attacking_card_img.shake([321, 581], [127.5, 507.5])
                            fade_animation = True
                else:
                    if losing_card:
                        if losing_card == attacked_card_img:
                            losing_card.setRect(691, 137.5)
                        else:
                            losing_card.setRect(331, 137.5)
                    else:
                        if attacked_card.in_atk_position and attacking_card.in_atk_position:
                            attacked_card_img.setRect(691, 137.5)
                            attacking_card_img.setRect(331, 137.5)
                    shaking = False
                    passed = True
            
            if fade_animation and not shaking:
                fade_now = pygame.time.get_ticks()
                if fade_now-new_now >= shake_duration:
                    if losing_card:
                        fade_rect.x = losing_card.rect.x
                        fade_rect.y = losing_card.rect.y
                    else:
                        fade_rect.x = 0
                        fade_rect.y = 0
                                     
                    for alpha in range(0, 300, 5):
                        if losing_card or attacked_card.in_atk_position and attacking_card.in_atk_position:
                            fade.set_alpha(alpha)
                            screen.fill(Settings.BLACK)
                            attacking_card_img.blit(atk_val=attacking_card.current_atk_points, def_val=attacking_card.current_def_points, color=attacking_card_color)
                            attacked_card_img.blit(atk_val=attacked_card.current_atk_points, def_val=attacked_card.current_def_points, color=attacked_card_color)
                            screen.blit(fade, fade_rect)
                            pygame.display.flip()
                            
                    if attacked_card.favorable_guardian_star_status or attacking_card.favorable_guardian_star_status: 
                        card_with_positive_gs_effects = None
                        
                        if attacked_card.favorable_guardian_star_status:
                            card_with_positive_gs_effects = attacked_card
                        elif attacking_card.favorable_guardian_star_status:
                            card_with_positive_gs_effects = attacking_card
                            
                        card_with_positive_gs_effects.increaseCurrentDefPoints(-star_bonus)
                        card_with_positive_gs_effects.increaseCurrentAtkPoints(-star_bonus)
                        
                        attacked_card.favorable_guardian_star_status = False
                        attacking_card.favorable_guardian_star_status = False
                            
                    if winning_card:                        
                        return winning_card
                    else:
                        return None
            else:         
                screen.fill(Settings.BLACK)
                attacking_card_img.blit(atk_val=attacking_card.current_atk_points, def_val=attacking_card.current_def_points, color=attacking_card_color)
                attacked_card_img.blit(atk_val=attacked_card.current_atk_points, def_val=attacked_card.current_def_points, color=attacked_card_color)
               
                if shaking:
                    if damage_taken != 0:
                        screen.blit(damage_text, [losing_card_centerx-(damage_text_width/2), losing_card_centery-(damage_text_height/2)]) 
                pygame.display.flip()
                if passed:
                
                    if attacked_card.favorable_guardian_star_status or attacking_card.favorable_guardian_star_status: 
                        card_with_positive_gs_effects = None
                        
                        if attacked_card.favorable_guardian_star_status:
                            card_with_positive_gs_effects = attacked_card
                        elif attacking_card.favorable_guardian_star_status:
                            card_with_positive_gs_effects = attacking_card
                            
                        card_with_positive_gs_effects.increaseCurrentDefPoints(-star_bonus)
                        card_with_positive_gs_effects.increaseCurrentAtkPoints(-star_bonus)
                        
                        attacked_card.favorable_guardian_star_status = False
                        attacking_card.favorable_guardian_star_status = False

                
                    fade_now = pygame.time.get_ticks()
                    if fade_now-new_now >= shake_duration:   
                        if winning_card:
                            #winning_card.increaseCurrentDefPoints(-star_bonus)
                            #winning_card.increaseCurrentAtkPoints(-star_bonus)
                            return winning_card
                        else:
                            return None    
        else:  
            screen.fill(Settings.BLACK)
            if pausing:
                now = pygame.time.get_ticks()
                if now - last >= pause:
                    pausing = False
                    shaking = True
                            
            if shaking:
                new_now = pygame.time.get_ticks()
                if new_now - now <= shake_duration:
                    if damage_taken != 0:
                        screen.blit(damage_text, [720.5, 280.0]) 
                    fade_animation = True
                    x_now =  pygame.time.get_ticks()
                    
            if fade_animation:
                fade_now = pygame.time.get_ticks()
                if fade_now-x_now >= shake_duration:
                    return attacking_card

            attacking_card_img.blit(atk_val=attacking_card.current_atk_points, def_val=attacking_card.current_def_points, color=attacking_card_color)
            pygame.display.flip()
                                  
        clock.tick(60)
        
def fusionScreen(fusion_result_card, result, screen, clock, game_instance, game_settings):
    card1 = result["card1"]
    card2 = result["card2"]
    
    card1.changeImg(card1.card.img)
    card2.changeImg(card2.card.img)
    
    card1.transformSize([149, 216], [235, 209.5])
    card2.transformSize([149, 216], [886, 209.5])
    
    did_fuse = result["did_fuse"]
    
    if did_fuse:
        fused_card = result["fused_card"]
        fused_card.rect.centerx = (1270 / 2)
        fused_card.rect.centery = (635 / 2)
    
    fusion_background = pygame.image.load("images/polymerization.png")
    
    pause = pygame.time.get_ticks()
    pause2 = pygame.time.get_ticks()
    cards_moving = False
    cards_stopped = False
    
    materials_blitting = True
    fused_card_blitting = False
    no_fusion_delay = False
    
    faded_card = None
    
    vhal = 50
    bounce = False
    
    while True:        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit() 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        
        screen.blit(fusion_background, [0, 0])
        
        if not cards_moving:
            x = pygame.time.get_ticks()
            if x-pause >= 1500:
                cards_moving = True
                
        if cards_moving and not cards_stopped:
            card1.rect.x += 10
            card2.rect.x -= 10
            
        if card1.rect.right >= card2.rect.left and not fused_card_blitting and not no_fusion_delay:
            card1.rect.x += 0
            card2.rect.x -= 0
            cards_stopped = True
            if did_fuse:
                gf.fade(game_settings.screen_width, game_settings.screen_height, screen, screen, flag=False)            
                materials_blitting = False
                fused_card_blitting = True
            else:
                stronger_card = gf.getStrongerCard(card1, card2)
                if stronger_card == card1:
                    faded_card = card2
                    vhal *= 1
                else:
                    faded_card = card1
                    vhal *= -1
                
                bounce = True            
                
                no_fusion_delay = True
                    
            pause2 = pygame.time.get_ticks()
        

        
        if bounce and faded_card:
            faded_card.rect.x += vhal
        
        if materials_blitting:
            card1.blit()
            card2.blit()
        
        if no_fusion_delay:
            x = pygame.time.get_ticks()
            if x-pause2 >= 2000:
                gf.fade(game_settings.screen_width, game_settings.screen_height, screen, screen, flag=False)
                return
        
        if fused_card_blitting and did_fuse:
            fused_card.blit(atk_val=fused_card.card.current_atk_points, def_val=fused_card.card.current_def_points)
            x = pygame.time.get_ticks()
            if x-pause2 >= 1500:
                gf.fade(game_settings.screen_width, game_settings.screen_height, screen, screen, flag=False)
                return
        
        pygame.display.flip()        
        clock.tick(60)