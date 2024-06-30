import pygame

class TypeWriter:
    def __init__(self, text, x, y, color, speed, font):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.font = font
        self.text_displayed = ""
        self.index = 0

    def update(self):
        if self.index < len(self.text):
            self.text_displayed += self.text[self.index]
            self.index += 1

    def draw(self, win):
        self.text_render = self.font.render(self.text_displayed, True, self.color)
        win.blit(self.text_render, (self.x, self.y))

    def is_complete(self):
        return self.index >= len(self.text)

