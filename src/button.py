import pygame

class Button:
    def __init__(self, x, y, sheet):
        self.x = x
        self.y = y
        self.sheet = sheet
        self.sheet_width = 48
        self.sheet_height = 16
        self.scale = 4
        self.width = self.sheet_width * self.scale
        self.height = self.sheet_height * self.scale
        self.colorkey = (0, 0, 0)
        self.imgs = []
        self.len = 3
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.clicked = False
        self.hover = False

    def get_images(self, img_count):
        image = pygame.Surface((self.sheet_width, self.sheet_height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((img_count * self.sheet_width), 0, self.sheet_width, self.sheet_height))
        image = pygame.transform.scale(image, (self.width, self.height))
        image.set_colorkey(self.colorkey)

        return image
    
    def draw(self, win):

        for i in range(self.len):
            self.imgs.append(self.get_images(i))
           
        if not self.clicked and not self.hover:
            win.blit(self.imgs[0], (self.x, self.y))

        if self.rect.collidepoint(pygame.mouse.get_pos()) and not self.clicked:
            self.hover = True
            win.blit(self.imgs[2], (self.x, self.y))

        elif self.clicked:
            win.blit(self.imgs[1], (self.x, self.y))

        else:
            self.hover = False
            self.clicked = False
            