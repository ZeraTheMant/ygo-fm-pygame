import pygame
from title_files.settings import Settings

class DataSurface():
    def __init__(self, screen, dimensions, x_pos, y_pos, color, opacity=False, index=None):
        self.screen = screen
        self.area = pygame.Surface(dimensions)
        self.rect = self.area.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.color = color
        
        if index != None:
            self.index = index
            
        self.is_selected = False
        if opacity:
            self.area.set_alpha(128)
        
        self.area.fill(self.color)

    def center(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

    def blit(self):
        self.screen.blit(self.area, self.rect)

    def selected(self):
        self.is_selected = True
        self.area.fill((255, 255, 0))

        
class DataSurfaceText(DataSurface):   
    def __init__(self, screen, dimensions, x_pos, y_pos, color, text, text_color, is_active, font, opacity=False, index=None):
        super().__init__(screen, dimensions, x_pos, y_pos, color)
        self.text = text
        self.is_active = is_active
        self.font = font     
        self.text_width, self.text_height = self.font.size(text)
        self.text_color = text_color
        self.text_render = self.font.render(text, True, self.text_color)
 
    def changeText(self, text):
        self.area.fill((0, 0, 0, 0))
        self.text = text
        self.text_render = self.font.render(self.text, True, self.text_color)
        self.area.fill(self.color)
 
    def blit(self):
        self.area.blit(self.text_render , [(self.rect.width / 2) - (self.text_width / 2), (self.rect.height / 2) - (self.text_height / 2)])
        self.screen.blit(self.area, self.rect)
 
    def changeActiveStatus(self):
        self.is_active = not self.is_active
        
    def changeColor(self):
        if self.is_active:
            self.area.fill(Settings.YELLOW)
        else:
            self.area.fill(Settings.WHITE)