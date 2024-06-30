import pygame

class Scope:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.width, self.height = 48, 48
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.img = pygame.transform.scale(pygame.image.load("assets/images/target.png"), (48, 48))
        self.moving = False
        self.scope_sound = pygame.mixer.Sound("assets/sounds/scope-moving.mp3")
        self.visible = True

    def draw(self, win):
        if self.visible:
            win.blit(self.img, (self.x, self.y))
