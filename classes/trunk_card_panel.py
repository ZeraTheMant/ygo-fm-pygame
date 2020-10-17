import pygame
from classes.data_surfaces import DataSurfaceText
from title_files.general_functions import getGuardianStarImg

class TrunkCardPanel(object):
    def __init__(self, screen, card, font, small_font, x_pos, y_pos, color, quantity, game_settings, area):
        self.card = card
        self.screen = screen
        self.area = pygame.Surface(area)
        self.rect = self.area.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.color = color
        self.area.fill(color)
        self.small_font = small_font
        self.quantity = str(quantity)
        self.card_image = pygame.transform.scale(pygame.image.load(card.img), (60, 87))
        self.font = font
    
        self.card_name_text = self.font.render(self.card.name, True, game_settings.BLACK)
        
        self.quantity_box = DataSurfaceText(self.area, [30, 30], 20, 28, color, self.quantity , game_settings.BLACK, True, small_font)
        
        self.text_info = ""
        
        self.gstar1 = None
        self.gstar2 = None
        
        if self.card.card_type == "Monster":
            self.text_info = "Lv. " + str(self.card.level) + "   " + str(self.card.atk_points) + "/" + str(self.card.def_points)
            monster_attr_type_txt = "[" + self.card.monster_attr + "] " + self.card.monster_type
            
            self.gstar1 = pygame.transform.scale(getGuardianStarImg(self.card.guardian_star_list[0].name), (27, 27))
            self.gstar2 = pygame.transform.scale(getGuardianStarImg(self.card.guardian_star_list[1].name), (27, 27))
            
            self.monster_attr_type = self.small_font.render(monster_attr_type_txt, True, game_settings.BLACK)
        else:
            self.text_info = self.card.card_type + "|" + self.card.spell_or_trap_type
            
        self.card_info_render = self.small_font.render(self.text_info, True, game_settings.BLACK)
        
    def blit(self):
        self.area.blit(self.card_image, [5, 0])
        self.quantity_box.blit()
        self.area.blit(self.card_name_text, [72, 10])
        self.area.blit(self.card_info_render, [72, 30])
        
        if self.card.card_type == "Monster":
            self.area.blit(self.gstar1, [72, 50])
            self.area.blit(self.gstar2, [105, 50])
            self.area.blit(self.monster_attr_type, [135, 53])
        
        self.screen.blit(self.area, self.rect)
      
      
class DeckCard(TrunkCardPanel):
    def blit(self):
        self.area.blit(self.card_image, [0, 0])
        self.screen.blit(self.area, self.rect)