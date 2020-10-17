import pygame, random
import title_files.general_functions as gf
from .settings import Settings

class ZoneGUI:
    def __init__(self, zone, screen, x_and_y_vals, flipped_x_and_y_vals, is_flipped, index, opposite_index, dimensions):
        self.screen = screen
        self.zone = zone
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.area = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.area.get_rect()
        self.screen_rect = screen.get_rect()
        self.x_and_y_vals = x_and_y_vals
        self.flipped_x_and_y_vals = flipped_x_and_y_vals
        self.rect.x = 1400
        self.rect.y = 900
        self.index = index
        self.opposite_index = opposite_index
        self.is_flipped = is_flipped
        self.set_current_position()
        self.color = None
        self.card_img = None
        self.gs_img = None
        self.card_img_rect = None
        self.disabled_for_attacks = False
        self.disabled_for_ai = False
        #self.opposite_zone = opposite_zone
        #self.area.fill(Settings.BLACK)
        #self.area.set_alpha(0)
        
        
        #self.area.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        
        self.font = pygame.font.Font(None, 50)
        self.name = str(self.index)
        self.zone.zone_gui = self
        
    def setZoneCardImg(self):
        #print(self.zone.getCardByIndex(0).guardian_star.name)
        if self.zone.getNumOfCardsContained() != 0:
            if not self.is_flipped:
                if self.zone.getCardByIndex(0).is_set:
                    self.card_img = pygame.transform.scale(pygame.image.load("images/cards/cover.jpg"), (75, 108))
                else:
                    self.card_img = pygame.transform.scale(pygame.image.load(self.zone.getCardByIndex(0).img), (75, 108))

                if not self.zone.getCardByIndex(0).in_atk_position:
                    self.card_img = pygame.transform.rotate(self.card_img, 90)

                    
                self.card_img_rect = self.card_img.get_rect()
                
                self.gs_img = pygame.transform.scale(gf.getGuardianStarImg(self.zone.getCardByIndex(0).guardian_star.name), (28, 28))
            else:
                if self.zone.getCardByIndex(0).is_set:                 
                    self.card_img = pygame.transform.scale(pygame.image.load("images/cards/cover.jpg"), (75, 108))
                else:
                    self.card_img = pygame.transform.scale(pygame.image.load(self.zone.getCardByIndex(0).img), (75, 108))
                    
                if not self.zone.getCardByIndex(0).in_atk_position:
                    self.card_img = pygame.transform.rotate(self.card_img, 90)
                    
                self.card_img = pygame.transform.flip(self.card_img, True, True)
                self.card_img_rect = self.card_img.get_rect()
                self.gs_img = pygame.transform.scale(gf.getGuardianStarImg(self.zone.getCardByIndex(0).guardian_star.name), (28, 28))
                #self.gs_img = pygame.transform.flip(self.gs_img, False, True)
        else:
            self.card_img = None
            self.card_img_rect = None
                
        self.area.fill((0, 0, 0, 0))
        #self.area.set_alpha(0)
        
    def blit(self, font):
        self.screen.blit(self.area, self.rect)
        
        if self.card_img:
            if self.zone.getCardByIndex(0).has_attacked:           
                pygame.draw.rect(self.area, (0, 0, 0, 125), [0, 0, 129.2, 111.75], 0)
                
            atk_val = str(self.zone.getCardByIndex(0).current_atk_points)
            def_val = str(self.zone.getCardByIndex(0).current_def_points)     
            atk_and_def_string = atk_val + "/" + def_val
            
            atk_width, atk_height = font.size(atk_val)  
            text_width, text_height = font.size(atk_and_def_string)   

            if self.zone.getCardByIndex(0).current_atk_points > self.zone.getCardByIndex(0).atk_points:
                atk_colors = Settings.DARK_GREEN
            elif self.zone.getCardByIndex(0).current_atk_points < self.zone.getCardByIndex(0).atk_points:
                atk_colors = Settings.RED
            else:
                atk_colors = Settings.WHITE
              
            if self.zone.getCardByIndex(0).current_def_points > self.zone.getCardByIndex(0).def_points:
                def_colors = Settings.DARK_GREEN
            elif self.zone.getCardByIndex(0).current_def_points < self.zone.getCardByIndex(0).def_points:
                def_colors = Settings.RED
            else:
                def_colors = Settings.WHITE
            
            atk_amount = font.render(atk_val, True, atk_colors)
            def_amount = font.render(def_val, True, def_colors)
            #atk_and_def_vals = font.render(atk_and_def_string, True, atk_and_def_colors)
 
            if self.zone.getCardByIndex(0).in_atk_position:
                self.area.blit(self.card_img, [28, 2])
            else:
                self.area.blit(self.card_img, [10.6, 18.375]) 

            #self.area.blit(self.card_img, [28, 2])
            if not self.zone.getCardByIndex(0).card_owner.is_ai:
                #(self.area.get_width()/2)-(text_width/2) 
                if not self.is_flipped:                  
                    self.area.blit(self.gs_img, [0, 2])
                    self.area.blit(atk_amount, [(self.area.get_width()/2)-(text_width/2) , self.area.get_height()-text_height])
                    self.area.blit(def_amount, [(self.area.get_width()/2)-(text_width/2) + ((atk_width)+10), self.area.get_height()-text_height])
                else:
                    self.area.blit(self.gs_img, [100, 80])
                    self.area.blit(atk_amount, [(self.area.get_width()/2)-(text_width/2) , 2])
                    self.area.blit(def_amount, [(self.area.get_width()/2)-(text_width/2) + ((atk_width)+10), 2])
            else:
                if not self.zone.getCardByIndex(0).is_set: 
                    if not self.is_flipped:
                        self.area.blit(self.gs_img, [0, 2])
                        self.area.blit(atk_amount, [(self.area.get_width()/2)-(text_width/2) , self.area.get_height()-text_height])
                        self.area.blit(def_amount, [(self.area.get_width()/2)-(text_width/2) + ((atk_width)+10), self.area.get_height()-text_height])
                    else:
                        self.area.blit(self.gs_img, [100, 80])
                        self.area.blit(atk_amount, [(self.area.get_width()/2)-(text_width/2) , 2])
                        self.area.blit(def_amount, [(self.area.get_width()/2)-(text_width/2) + ((atk_width)+10), 2])
                else:
                    if not self.is_flipped:
                        self.area.blit(self.gs_img, [0, 2])
                    else:
                        self.area.blit(self.gs_img, [100, 80])
    def flip(self):
        self.is_flipped = not self.is_flipped
        self.area.fill((0, 0, 0, 0))
      
    def set_current_position(self):
        if not self.is_flipped:          
            self.rect.x = self.flipped_x_and_y_vals[0]
            self.rect.y = self.flipped_x_and_y_vals[1]
        else:
            self.rect.x = self.x_and_y_vals[0]
            self.rect.y = self.x_and_y_vals[1]       
            
            
class SpellZoneGUI(ZoneGUI):
    def setZoneCardImg(self):
        if self.zone.getNumOfCardsContained() != 0:
            if not self.is_flipped:
                if self.zone.getCardByIndex(0).is_set:
                    self.card_img = pygame.transform.scale(pygame.image.load("images/cards/cover.jpg"), (75, 108))
                else:
                    self.card_img = pygame.transform.scale(pygame.image.load(self.zone.getCardByIndex(0).img), (75, 108))
                    
                self.card_img_rect = self.card_img.get_rect()
            else:
                if self.zone.getCardByIndex(0).is_set:                 
                    self.card_img = pygame.transform.scale(pygame.image.load("images/cards/cover.jpg"), (75, 108))
                else:
                    self.card_img = pygame.transform.scale(pygame.image.load(self.zone.getCardByIndex(0).img), (75, 108))
                    
                self.card_img = pygame.transform.flip(self.card_img, True, True)
                self.card_img_rect = self.card_img.get_rect()
        else:
            self.card_img = None
            self.card_img_rect = None
                
        self.area.fill((0, 0, 0, 0))

    def blit(self):
        self.screen.blit(self.area, self.rect)
        if self.card_img:
            self.area.blit(self.card_img, [28, 2])
            
class GraveyardGUI(ZoneGUI):
    def setZoneCardImg(self, font):
        if self.zone.getNumOfCardsContained() != 0:
            self.card_img = pygame.transform.scale(pygame.image.load(self.zone.getLastCard().img), (75, 108))  
            if self.is_flipped:                    
                self.card_img = pygame.transform.flip(self.card_img, True, True)
            self.card_img_rect = self.card_img.get_rect()
            
            cards_contained = str(self.zone.getNumOfCardsContained())
            
            self.text_width, self.text_height = font.size(cards_contained)    
            self.cards_contained_string = font.render(cards_contained, True, Settings.WHITE)
        else:
            self.card_img = None            
        self.area.fill((0, 0, 0, 0))

        
    def blit(self):
        self.screen.blit(self.area, self.rect)
        if self.card_img:
            self.area.blit(self.card_img, [12.5, 2])
            self.area.blit(self.cards_contained_string, [(self.area.get_width()/2)-(self.text_width/2), (self.area.get_height()/2)-(self.text_height/2)])

class FieldGUI(SpellZoneGUI):
    def blit(self):
        self.screen.blit(self.area, self.rect)
        if self.card_img:
            self.area.blit(self.card_img, [12.5, 2])
          
class DeckGUI(ZoneGUI):
    def __init__(self, zone, screen, x_and_y_vals, flipped_x_and_y_vals, is_flipped, index, opposite_index, dimensions):
        super().__init__(zone, screen, x_and_y_vals, flipped_x_and_y_vals, is_flipped, index, opposite_index, dimensions)
        self.cards_contained_string = None
        self.text_width = 0
        self.text_height = 0

    def setZoneCardImg(self, font):
        #print(self.zone.getNumOfCardsContained())
        if self.zone.getNumOfCardsContained() != 0:
            self.card_img = pygame.transform.scale(pygame.image.load("images/cards/cover.jpg"), (75, 108))  
            if self.is_flipped:                    
                self.card_img = pygame.transform.flip(self.card_img, True, True)
            self.card_img_rect = self.card_img.get_rect()
            
            cards_contained = str(self.zone.getNumOfCardsContained())
            
            self.text_width, self.text_height = font.size(cards_contained)    
            self.cards_contained_string = font.render(cards_contained, True, Settings.WHITE)
        else:
            self.card_img = None            
        self.area.fill((0, 0, 0, 0))
        
    def blit(self):
        self.screen.blit(self.area, self.rect)
        if self.card_img:
            self.area.blit(self.card_img, [12.5, 2])

            self.area.blit(self.cards_contained_string, [(self.area.get_width()/2)-(self.text_width/2), (self.area.get_height()/2)-(self.text_height/2)])