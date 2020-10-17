import pygame
from .settings import Settings

class CardImage():
    def __init__(self, screen, card_type, path, x_pos, y_pos, card, card_index=None, in_hand=False):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.card_image = pygame.image.load(path)
        self.rect = self.card_image.get_rect()
        self.card_type = card_type
        self.font = pygame.font.Font("misc/Yu-Gi-Oh! ITC Stone Serif Small Caps Bold.ttf", 10)      
        self.rect.centerx = x_pos
        self.rect.centery = y_pos
        self.card_speed = 20
        self.is_small = False
        self.card = card
        self.in_hand = in_hand
        self.card_index = card_index
        self.is_visible = True
        self.contained = False
        self.is_fusing = False
        self.is_fusing_up = False
        self.is_fusing_down = False
        self.x_speed = 3
        self.y_speed = 3
        
    def reset(self):
        self.card_type = None
        self.card = None
        self.changeImg("images/cards/card_back.png")
        
    def setRect(self, x, y):
        self.rect.x = x
        self.rect.y = y
    
    def shake(self, x_limits_array, y_limits_array):
    
        self.rect.x -= self.x_speed
        self.rect.y -= self.y_speed
        
        if self.rect.left <= x_limits_array[0]:
            self.x_speed *= -1
        if self.rect.right >= x_limits_array[1]:
            self.x_speed *= -1
        
        if self.rect.top <= y_limits_array[0]:
            self.y_speed *= -1
        if self.rect.bottom >= y_limits_array[1]:
            self.y_speed *= -1
        
    def moveCardInHand(self):
        if self.in_hand:
            self.rect.centerx -= self.card_speed
        
    def changeImg(self, path):
        self.card_image = pygame.image.load(path)
        
    def transformSize(self, dimensions, x_and_y):
        self.card_image = pygame.transform.scale(self.card_image, dimensions)
        self.rect = self.card_image.get_rect() 
        self.rect.x = x_and_y[0]
        self.rect.y = x_and_y[1]
        self.font = pygame.font.Font(None, 10)  
        self.is_small = True
        
    def blit(self, atk_val=None, def_val=None, color=None):
        self.screen.blit(self.card_image, self.rect)
        
        if self.card_type != None and self.card_type == "Monster":
            rendered_values = "ATK/" + str(atk_val) + "  DEF/" + str(def_val)
            
            def_whole = "DEF/" + str(def_val)
            atk_whole = "ATK/" + str(atk_val)
            
            def_width, def_height = self.font.size(str(def_whole))  
            atk_width, atk_height = self.font.size(str(atk_whole))  
            text_width, text_height = self.font.size(rendered_values)
            
            if self.card.current_atk_points > self.card.atk_points:
                atk_color = Settings.DARK_GREEN
            elif self.card.current_atk_points < self.card.atk_points:
                atk_color = Settings.RED
            else:
                atk_color = Settings.BLACK
                
            if self.card.current_def_points > self.card.def_points:      
                def_color = Settings.DARK_GREEN
            elif self.card.current_def_points < self.card.def_points:
                def_color = Settings.RED
            else:
                def_color = Settings.BLACK
                
            atk_amount = self.font.render(str(atk_whole), True, atk_color)
            def_amount = self.font.render(str(def_whole), True, def_color)
            
            #text = self.font.render(rendered_values, True, atk_and_def_colors)
            if not self.is_small:
                #self.screen.blit(def_amount, [(self.rect.right-text_width)-23, self.rect.bottom-33])
                self.screen.blit(def_amount, [(self.rect.right-def_width)-23, self.rect.bottom-33])
                #self.screen.blit(atk_amount, [(((self.rect.right-def_width)-23)-(def_width))-5, self.rect.bottom-33])
                self.screen.blit(atk_amount, [(((self.rect.right-def_width)-23)-(atk_width))-5, self.rect.bottom-33])
            #else:
            #    self.screen.blit(def_amount, [(self.rect.right-text_width)-6, self.rect.bottom-10])