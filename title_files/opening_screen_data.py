import pygame

class OpeningScreenButton:
    def __init__(self, name, is_selected, image, selected_image, screen, y_position):
        self.screen = screen
        self.name = name
        self.is_selected = is_selected
        self.image_string = image
        self.selected_image_string = selected_image
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = y_position

        self.changeSelectionImage()

    def blit(self):
        self.screen.blit(self.image, self.rect)

    def changeSelectionStatus(self):
        self.is_selected = not self.is_selected

    def changeSelectionImage(self):
        if self.is_selected:
            self.image = pygame.image.load(self.selected_image_string)
        else:
            self.image = pygame.image.load(self.image_string)
        self.rect.centerx = self.screen_rect.centerx

class NewGameButton(OpeningScreenButton):
    def __init__(self, screen):
        super().__init__("new game button", False, "images/new_game_unselected.png", "images/startNewGameButton.png", screen, 200)

    def select(self):
        print("new game")

class LoadGameButton(OpeningScreenButton):
    def __init__(self, screen):
        super().__init__("load game button", False, "images/load_game_unselected.png", "images/startLoadButton.png", screen, 300)

    def select(self):
        print("load_game")

#########################################################

class Selector:
    def __init__(self):
        self.selected_button = None

    def getSelectedButton(self):
        return self.selected_button

    def changeSelectedButton(self, selected_button):
        if self.selected_button == None:
            self.selected_button = selected_button
            self.selected_button.changeSelectionStatus()
            self.selected_button.changeSelectionImage()
        else:
            if self.selected_button != selected_button:
                self.selected_button.changeSelectionStatus()
                self.selected_button.changeSelectionImage()
                
                self.selected_button = selected_button

                self.selected_button.changeSelectionStatus()
                self.selected_button.changeSelectionImage()


#########################################################

class OpeningScreen:
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load("images/opening_screen.jpg")
        self.rect = self.screen.get_rect()
        self.is_darkened = False
        self.buttons = [NewGameButton(screen), LoadGameButton(screen)]
        self.selector = Selector()

    def returnNewGameBtn(self):
        return self.buttons[0]

    def returnLoadGameBtn(self):
        return self.buttons[1]

    def changeScreen(self):
        if not self.is_darkened:
            self.image = pygame.image.load("images/op_screen_dark.jpg")
        else:
            self.image = pygame.image.load("images/opening_screen.jpg")
        self.is_darkened = not self.is_darkened
            
    def blit(self):
        self.screen.blit(self.image, self.rect)
