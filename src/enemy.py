import pygame, random

class Enemy:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.width, self.height = 48, 48
        self.sheet_block_size = 32
        self.sheet = img
        self.speed = 4
        self.imgs_right = []
        self.imgs_left = []
        self.frames = 12
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.colorkey = (0, 0, 0)
        self.dirn = random.choice([0, 1])
        self.walkCount = 0
        self.visible = True
        self.to_animate = True

    def get_images(self, frame):
        image = pygame.Surface((self.sheet_block_size, self.sheet_block_size)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * self.sheet_block_size), 0, self.sheet_block_size, self.sheet_block_size))
        image = pygame.transform.scale(image, (self.width, self.height))
        image.set_colorkey(self.colorkey)

        return image
    
    def animation(self, win, boundary_right, boundary_left):

        for i in range(self.frames):
            self.imgs_right.append(self.get_images(i))

        for j in range(self.frames):
            img_left = pygame.transform.flip(self.get_images(j), True, False)
            img_left.set_colorkey(self.colorkey)
            self.imgs_left.append(img_left)

        if self.visible:
            if self.dirn == 0:
                self.x += self.speed

                if self.to_animate:    
                    win.blit(self.imgs_right[self.walkCount//3], (self.x, self.y))
                    self.walkCount += 1
                else:
                    win.blit(self.imgs_right[self.walkCount//3], (self.x, self.y))

                if self.walkCount + 1 >= 36:
                    self.walkCount = 0

                if self.x >= boundary_right:
                    self.dirn = 1

            if self.dirn == 1:
                self.x -= self.speed

                if self.to_animate:
                    win.blit(self.imgs_left[self.walkCount//3], (self.x, self.y))
                    self.walkCount += 1
                else:
                    win.blit(self.imgs_left[self.walkCount//3], (self.x, self.y))

                if self.walkCount + 1 >= 36:
                    self.walkCount = 0

                if self.x <= boundary_left:
                    self.dirn = 0
            


