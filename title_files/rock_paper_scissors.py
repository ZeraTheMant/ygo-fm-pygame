import pygame

class FirstTurnCard:
    def __init__(self, screen, img, comparison_value, y_position):
        self.screen = screen
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.comparison_value = comparison_value
        self.rect.centery = y_position
        
    def blit(self):
        self.screen.blit(self.image, self.rect)
