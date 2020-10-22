import pygame

WHITE = (255, 255, 255) 
DISPLAY_CYCLES = 150

class TextBox:
    def __init__(self, position, screen):
        self.position = position
        self.screen = screen
        self.font = pygame.font.SysFont(None, 32) 
        self.text = self.font.render('', True, WHITE, WHITE)
        self.rect = self.text.get_rect()
        self.rect.center = self.position
        self.displayCycles = 0
        self.displayText = ''

    def showText(self, displayText):
        self.displayText = displayText
        self.text = self.font.render(self.displayText, True, WHITE)
        self.rect = self.text.get_rect()  
        self.rect.center = self.position
        self.displayCycles = 0

    def update(self):
        if self.displayCycles < DISPLAY_CYCLES:
            # Just redraw text.
            self.screen.blit(self.text, (0,0))
        else:
            # Fade out.
            self.text = self.font.render(self.displayText, True, self.__getFadedColor(self.displayCycles))
            self.rect = self.text.get_rect()  
            self.rect.center = self.position

            self.screen.blit(self.text, (0,0))
        
        self.displayCycles += 1

    def __getFadedColor(self, cycles):
        fadedColor = (WHITE[0] - (cycles - DISPLAY_CYCLES), WHITE[1] - (cycles - DISPLAY_CYCLES), WHITE[2] - (cycles - DISPLAY_CYCLES) )
        if fadedColor[0] < 0:
            return (0,0,0)
        else:
            return fadedColor

