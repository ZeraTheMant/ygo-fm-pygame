import pygame
from .settings import Settings
import title_files.general_functions as gf

class CardDescPanel(object):
    def __init__(self, screen):
        self.screen = screen
        self.card_name_text = ""
        self.guardian_stars_text = ""
        self.gs1_text_render = ""
        self.gs2_text_render = ""
        self.card_type_info = ""
        self.monst_lvl_text = ""
        self.card_desc = ""
        self.fusion_types = ""
        self.gs1_img = None
        self.gs2_img = None
        self.smaller_font = pygame.font.SysFont("Segoe UI Symbol", 11)  
        
    def setCardContent(self, card_name_text, guardian_stars_text, gs1_text_render, gs2_text_render, card_type_info, monst_lvl_text, card_desc, gs1_img, gs2_img, fusion_types_string):
        self.card_name_text = card_name_text
        self.guardian_stars_text = guardian_stars_text
        self.gs1_text_render = gs1_text_render
        self.gs2_text_render = gs2_text_render
        self.card_type_info = card_type_info
        self.monst_lvl_text = monst_lvl_text
        self.card_desc = card_desc
        self.gs1_img = gs1_img
        self.gs2_img = gs2_img   
        self.fusion_types = fusion_types_string
        
    def blit(self, card_name_font, card_type):
        card_name_text_width, card_name_text_height = card_name_font.size(self.card_name_text)
        card_name_text = card_name_font.render(self.card_name_text, True, Settings.BLACK)
        
        guardian_stars_text = card_name_font.render(self.guardian_stars_text, True, Settings.BLUE)
        gs1_text_render = card_name_font.render(self.gs1_text_render, True, Settings.BLUE)
        gs2_text_render = card_name_font.render(self.gs2_text_render, True, Settings.BLUE)
        card_type_text = card_name_font.render(self.card_type_info, True, Settings.BLUE)
        monst_lvl_text = card_name_font.render(self.monst_lvl_text, True, Settings.BLUE)
        fusion_types = self.smaller_font.render(self.fusion_types, True, Settings.BLUE)
        
        if card_type == "Monster":
            self.screen.blit(monst_lvl_text, [25, 440])
            self.screen.blit(guardian_stars_text, [25, 465])
            self.screen.blit(self.gs1_img, [125, 445])
            self.screen.blit(self.gs2_img, [215, 445])
            self.screen.blit(gs1_text_render, [166, 465])
            self.screen.blit(gs2_text_render, [256, 465])
            self.screen.blit(fusion_types, [25, 495])
            gf.bilt_long_text(self.screen, self.card_desc, card_name_font, [25, 520])#495

        else:
            gf.bilt_long_text(self.screen, self.card_desc, card_name_font, [25, 440])        
        
        self.screen.blit(card_name_text, [162.5-(card_name_text_width/2), 382])
        self.screen.blit(card_type_text, [25, 415])
        