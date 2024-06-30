import pygame

class Label:
    def __init__(self, text, value, color, size):
        self.text = text
        self.value = value
        self.text_color = color
        self.size = size
        self.font = pygame.font.Font("assets/fonts/karmatic.ttf", self.size)

    def render(self, win, pos):
        text_surface = self.font.render(f"{self.text}{self.value}", True, self.text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = pos
        win.blit(text_surface, text_rect)

    def update(self, value):
        self.value = value


