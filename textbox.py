import pygame

WHITE = (255, 255, 255)
DISPLAY_CYCLES = 150


class TextBox:
    def __init__(self, position, screen, fontSize=32, maxDisplayCycles=DISPLAY_CYCLES):
        self.position = position
        self.screen = screen
        self.font = pygame.font.SysFont(None, fontSize)
        self.text = self.font.render("", True, WHITE)
        self.rect = self.text.get_rect()
        self.rect.center = self.position
        self.maxDisplayCycles = maxDisplayCycles
        self.displayCycles = 0
        self.displayText = ""

    def showText(self, displayText):
        self.displayText = displayText
        self.text = self.font.render(self.displayText, True, WHITE)
        self.rect = self.text.get_rect()
        self.rect.center = self.position

        self.displayCycles = 0

    def setPosition(self, position):
        self.position = position

    def update(self):
        if self.displayCycles < self.maxDisplayCycles:
            # Just redraw text.
            self.screen.blit(self.text, self.position)
        else:
            # Fade out.
            self.text = self.font.render(
                self.displayText, True, self.__getFadedColor(self.displayCycles)
            )
            self.rect = self.text.get_rect()
            self.rect.center = self.position

            self.screen.blit(self.text, self.position)

        self.displayCycles += 1

    def __getFadedColor(self, cycles):
        fadedColor = (
            WHITE[0] - (cycles - self.maxDisplayCycles),
            WHITE[1] - (cycles - self.maxDisplayCycles),
            WHITE[2] - (cycles - self.maxDisplayCycles),
        )
        if fadedColor[0] < 0:
            return (0, 0, 0)
        else:
            return fadedColor
