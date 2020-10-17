import pygame, random
from .settings import Settings

class SelectedCardOptionsBoxContents:
    def __init__(self, screen, text, font, dimensions):
        self.dimensions = dimensions
        self.screen = screen
        self.text = text
        self.area = pygame.Surface(dimensions)
        self.rect = self.area.get_rect()
        self.bg_color = Settings.LIGHT_GRAY        
        self.area.fill(self.bg_color)
        #self.area.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        self.font = font

        
        self.text_width, self.text_height = self.font.size(text)
        self.displayed_text = self.font.render(text, True, Settings.BLACK)
        
    def setPos(self, card):
        self.rect.x = 0
        self.screen_rect = self.screen.get_rect()
        if self.text == "Cancel":
            self.rect.y = self.screen_rect.y
        else:
            if self.text == "Set":
                self.rect.y = self.screen_rect.bottom-25
            
            if card.card_type == "Trap":
                if self.text == "Fuse Up":
                    self.rect.y = self.screen_rect.y
                elif self.text == "Fuse Down":
                    self.rect.y = self.screen_rect.top+25
            elif card.card_type == "Spell":
                if card.spell_or_trap_type != "Equip":
                    if self.text == "Fuse Up":
                        self.rect.y = self.screen_rect.y
                    elif self.text == "Fuse Down":
                        self.rect.y = self.screen_rect.top+25
                    elif self.text == "Activate":
                        self.rect.y = self.screen_rect.top+50
                else:
                    if card.willActivate():
                        if self.text == "Fuse Up":
                            self.rect.y = self.screen_rect.y
                        elif self.text == "Fuse Down":
                            self.rect.y = self.screen_rect.top+25
                        elif self.text == "Activate":
                            self.rect.y = self.screen_rect.top+50                    
                    else:
                        if self.text == "Fuse Up":
                            self.rect.y = self.screen_rect.y
                        elif self.text == "Fuse Down":
                            self.rect.y = self.screen_rect.top+25
            else:
                if self.text == "Fuse Up":
                    self.rect.y = self.screen_rect.y
                elif self.text == "Fuse Down":
                    self.rect.y = self.screen_rect.top+25
                elif self.text == "Summon":
                    self.rect.y = self.screen_rect.top+50
       
    def setBgColor(self, color):
        self.bg_color = color
        self.area.fill(self.bg_color)
       
    def blit(self): 
        pygame.draw.rect(self.area, Settings.BLACK, [0, 0, self.dimensions[0], 25], 1)
        self.area.blit(self.displayed_text, [(self.area.get_width()/2)-(self.text_width/2), (self.area.get_height()/2)-(self.text_height/2)])
        self.screen.blit(self.area, self.rect)

class SelectedCardOptionsBox:
    def __init__(self, screen, dimensions, card=None):
        self.dimensions = dimensions
        self.is_selected = False
        self.screen = screen
        self.card = card
        #self.area = None
        self.area = pygame.Surface(dimensions)
        self.rect = self.area.get_rect()
        self.rect.x = 0
        self.rect.y = 0     
        self.area.fill((255, 0, 0))
        self.options = []
        self.is_on = False
            
    def blit(self):
        if self.card != None:
            #print(self.card.card.name)
            for option in self.options:
                option.blit()
            self.screen.blit(self.area, self.rect)
            
    def getArea(self, spell_and_trap_zones_array, fuse_up_ctr, fuse_down_ctr):
        if self.card != None:
            if fuse_up_ctr > 0 or fuse_down_ctr > 0:
                if not self.card.is_fusing:
                    self.area = pygame.Surface([self.dimensions[0], 50])
                else:
                    self.area = pygame.Surface([self.dimensions[0], 25])
            else:         
                if not self.card.is_fusing:
                    if self.card.card.card_type == "Monster":
                        self.area = pygame.Surface([self.dimensions[0], 100])
                    else:
                        ctr = 0
                        for gui_zone in spell_and_trap_zones_array:
                            if gui_zone.zone.getNumOfCardsContained() == 1:
                                ctr += 1
                        if ctr != 4:
                            if self.card.card_type == "Spell":
                                if self.card.card.spell_or_trap_type == "Equip":
                                    if self.card.card.willActivate():
                                        self.area = pygame.Surface([self.dimensions[0], 100])
                                    else:
                                        self.area = pygame.Surface([self.dimensions[0], 75])                              
                                else:
                                    self.area = pygame.Surface([self.dimensions[0], 100])
                            else:
                                self.area = pygame.Surface([self.dimensions[0], 75])
                else:
                    self.area = pygame.Surface([self.dimensions[0], 25])
        
            if self.area != None:
                self.rect = self.area.get_rect()
                self.rect.x = self.card.rect.x
                self.rect.y = self.card.rect.y - self.area.get_height()
      
      
class SelectedFieldMonsterBox(SelectedCardOptionsBox):
    def getArea(self, round):
        if round == 1 or not self.card.zone.getCardByIndex(0).in_atk_position:
            self.area = pygame.Surface([self.dimensions[0], 25])
        else:
            self.area = pygame.Surface([self.dimensions[0], 50])
            
        #if not self.card.zone.getCardByIndex(0).in_atk_position:
        #    self.area = pygame.Surface([self.dimensions[0], 25])
            
        self.area.fill(Settings.LIGHT_GRAY)
        if self.area != None:
            self.rect = self.area.get_rect()
            self.rect.x = self.card.rect.x
            self.rect.y = self.card.rect.y - self.area.get_height()
            
class SelectedFieldSpellTrapBox(SelectedCardOptionsBox):
    def getArea(self):
        self.area = pygame.Surface([self.dimensions[0], 25])
            
        self.area.fill(Settings.LIGHT_GRAY)
        if self.area != None:
            self.rect = self.area.get_rect()
            self.rect.x = self.card.rect.x
            self.rect.y = self.card.rect.y - self.area.get_height()

class SelectedFieldMonsterBoxContents(SelectedCardOptionsBoxContents):  
    def setPos(self, current_turn, card):
        self.rect.x = 0
        self.screen_rect = self.screen.get_rect()
        
        if current_turn == 1 or not card.in_atk_position:
            if self.text == "Change Position":
                self.rect.y = self.screen_rect.y
            else:
                self.rect.y = 1000
        else:
            if self.text == "Attack":
                self.rect.y = self.screen_rect.y
            elif self.text == "Change Position":
                self.rect.y = self.screen_rect.y+25

class SelectedFieldSpellBoxContents(SelectedCardOptionsBoxContents):  
    def setPos(self):
        self.rect.x = 0
        self.screen_rect = self.screen.get_rect()
        

        if self.text == "Attack":
            self.rect.y = self.screen_rect.y
        elif self.text == "Change Position":
            self.rect.y = self.screen_rect.y+25