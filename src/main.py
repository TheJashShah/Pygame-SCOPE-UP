import pygame, random, math

import pygame.event

pygame.init()
pygame.mixer.init()

from scope import Scope
from enemy import Enemy
from button import Button
from label import Label

from main_menu import main_menu

from sine import sine
from control_texts import get_text, get_game_text

from typewriter import TypeWriter

def check_collision(o1, o2):
    return(
        o1.x < o2.x + o2.width and
        o1.x + o1.width > o2.x and
        o1.y < o2.y + o2.height and 
        o1.y + o1.height > o2.y
    )

class Main:
    def __init__(self):
        self.width, self.height = 720, 750
        self.grid_width, self.grid_height = 720, 720
        self.win = pygame.display.set_mode((self.width, self.height))
        self.title = pygame.display.set_caption("SCOPE-UP!")
        self.surface = pygame.Surface((self.grid_width, self.grid_height))
        self.clock = pygame.time.Clock()
        self.Running = False
        self.FPS = 60
        self.color = (240, 200, 200)
        self.line_color = (255, 255, 255)
        self.block_size = 48
        self.scope = Scope(48, 48, self.block_size)
        self.icon = pygame.display.set_icon(self.scope.img)
        self.enemy_list = []
        self.time_since_enemy_generation = pygame.time.get_ticks()
        self.screen_shake = 0
        self.offset = [0, 0]
        self.hit_sound = pygame.mixer.Sound("assets/sounds/hit.mp3")
        self.time_difference = 5000
        self.enemy_one_img = pygame.image.load("assets/images/enemy_1.png").convert_alpha()
        self.enemy_two_img = pygame.image.load("assets/images/enemy_2.png").convert_alpha()
        self.enemy_three_img = pygame.image.load("assets/images/enemy_3.png").convert_alpha()
        self.score = 0
        self.kills = 0
        self.pos = pygame.mouse.get_pos()
        self.play_btn_img = pygame.image.load("assets/images/btn_1.png").convert_alpha()
        self.kill_label = Label("", self.kills, (50, 50, 50), 40)
        self.sine_speed = 200.0
        self.sine_range = 10.0
        self.score_rect = pygame.Rect(255, sine(self.sine_speed, 1280, self.sine_range, 30), 200, 75)
        self.bullets = 10
        self.is_pause = False
        self.space_pressed = True
        self.enemy_generation_true = True
        self.health_green_width = 240
        self.transparent_bg = False
        self.revive_condition = False
        self.kill_count_for_nuke = 0
        self.controls = False
        self.explosion = pygame.mixer.Sound("assets/sounds/explosion.mp3")
        self.reload = pygame.mixer.Sound("assets/sounds/reload.mp3")

    def grid(self, surface):
        for i in range((self.grid_width//self.block_size) + 1):
            pygame.draw.line(surface, self.line_color, (i*self.block_size, 0), (i*self.block_size, self.grid_height), 5)

        for j in range((self.grid_height//self.block_size) + 1):
            pygame.draw.line(surface, self.line_color, (0, j*self.block_size), (self.grid_width, j*self.block_size), 5)

    def enemy_scope_collision(self):

        for enemy in self.enemy_list[:]:
            if check_collision(enemy, self.scope):
                enemy.visible = False
                self.score += 1
                self.kills += 1
                self.kill_count_for_nuke += 1
                
    def bullet_counter(self):

        for i in range(self.bullets):
            pygame.draw.circle(self.win, (200, 200, 200), (15 + (i * 25), 735), 10)

    def handle_pause(self):
        if self.is_pause:
            self.scope.speed = 0
            self.sine_range = 0
            self.space_pressed = False
            self.enemy_generation_true = False

            for enemy in self.enemy_list[:]:
                enemy.speed = 0
                enemy.to_animate = False

        else:
            self.scope.speed = self.block_size
            self.sine_range = 10.0
            self.space_pressed = True
            self.enemy_generation_true = True

            for enemy in self.enemy_list[:]:
                enemy.speed = 4
                enemy.to_animate = True
                
    def healthbar(self):
        pygame.draw.rect(self.win, (240, 0, 0), pygame.Rect(470, 725, 240, 20))
        pygame.draw.rect(self.win, (0, 240, 0), pygame.Rect(470, 725, self.health_green_width, 20))

        if len(self.enemy_list) > 10 and len(self.enemy_list) < 20:
            if self.health_green_width > 0:
                self.health_green_width -= 0.03

        if len(self.enemy_list) >= 20 and (len(self.enemy_list) < 25):
            if self.health_green_width > 0:
                self.health_green_width -= 0.3

        if len(self.enemy_list ) >= 25:
            if self.health_green_width > 0:
                self.health_green_width = 0

        if self.health_green_width <= 0:
            self.scope.visible = False
            self.bullets = 0
            self.transparent_bg = True
            self.enemy_generation_true = False

    def transparent(self):
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        surface.fill((100, 100, 100, 200))
        surface = surface.convert_alpha()

        score_label = Label("Score: ", self.score, (10, 10, 10), 40)

        revive_label = Label("PRESS CTRL AND A TO REVIVE", "", (10, 10, 10), 35)

        if self.transparent_bg:
            score_label.render(self.win, (360, sine(self.sine_speed, 1280, self.sine_range, 200)))
            revive_label.render(self.win, (360, sine(self.sine_speed, 1280, self.sine_range, 315)))
            self.win.blit(surface, (0, 0))

    def handle_nuking(self):

        nums = (self.kill_count_for_nuke//20)

        for i in range(nums):
            pygame.draw.circle(self.win, (240, 240, 10), (270 + (i * 25), 735), 10)

    def revive_handling(self):
        if self.revive_condition:
            self.transparent_bg = False
            self.scope.visible = True
            self.scope.x, self.scope.y = 48, 48
            self.score = 0
            self.kills = 0
            self.bullets = 10
            self.health_green_width = 240
            self.enemy_list.clear()
            self.time_difference = 3000
            self.revive_condition = False
            self.kill_count_for_nuke = 0

    def main(self):

        self.Running, self.controls = main_menu(self.win, self.width, self.height, self.color)

##--------Controls Screen--------##

        surface = pygame.Surface((self.width, self.height))

        font = pygame.font.SysFont("monospace", 16)
        font.set_bold(True)

        font_2 = pygame.font.SysFont("monospace", 19)
        font_2.set_bold(True)

        labels = [TypeWriter(get_text(i), 10, (120 + (i * 25)), (10, 10, 10), 20, font) for i in range(11)]

        game_label = TypeWriter(get_game_text(0), 10, 500, (10, 10, 10), 20, font_2)

        last_update = pygame.time.get_ticks()

        back_btn = Button(20, sine(self.sine_speed, 1280, self.sine_range, 670), pygame.image.load("assets/images/btn_5.png"))

        back_label = Label("BACK", "", (10, 10, 10), 40)
        control_label = Label("Controls", "!", (10, 10, 10), 40)

        while self.controls:

            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - last_update
       
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.controls = False

                if event.type == pygame.MOUSEBUTTONDOWN:

                    pos = pygame.mouse.get_pos()
                    if back_btn.rect.collidepoint(pos):
                        back_btn.clicked = True
                        self.Running, self.controls = main_menu(self.win, self.width, self.height, self.color)

                if event.type == pygame.MOUSEBUTTONUP:
                    back_btn.clicked = False

            surface.fill(self.color)

            back_btn.draw(surface)

            control_label.render(surface, (360, sine(self.sine_speed, 1280, self.sine_range, 50)))

            back_label.render(surface, (115, sine(self.sine_speed, 1280, self.sine_range, 695)))

            back_btn.y = sine(self.sine_speed, 1280, self.sine_range, 670)

            previous_complete = True

            for label in labels:
                if previous_complete and elapsed_time > (500 / label.speed):
                    label.update()
                    last_update = current_time
                    if label.speed > 4:
                        label.speed -= 0.05

                previous_complete = label.is_complete()

            if previous_complete and elapsed_time > (500 / game_label.speed):
                    game_label.update()
                    last_update = current_time

            for label in labels:
                label.draw(surface)

            game_label.draw(surface)

            self.win.blit(surface, (0, 0))

            pygame.display.update()
            self.clock.tick(self.FPS)

##--------Controls Screen--------##

        while self.Running:

            self.current_time = pygame.time.get_ticks()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.Running = False

                if event.type == pygame.KEYDOWN:
                    self.scope.moving = True

                    if self.space_pressed:
                        if event.key == pygame.K_SPACE:
                            if self.bullets > 0:
                                self.enemy_scope_collision()
                                self.screen_shake = 30
                                self.hit_sound.play()
                                self.bullet_fired = True
                                self.bullets -= 1

                    if event.key == pygame.K_r:
                        if self.bullets < 10:
                            self.bullets = 10
                            self.score -= 5
                            self.reload.play()

                    if event.key == pygame.K_a and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        self.revive_condition = True
                                                    
                    if event.key == pygame.K_n:
                        if self.kill_count_for_nuke >= 20:
                            self.enemy_list.clear()
                            self.screen_shake = 60
                            self.explosion.play()

                            self.kill_count_for_nuke -= 20

                    if event.key == pygame.K_p:
                        self.is_pause = not self.is_pause

                    if event.key == pygame.K_LEFT and self.scope.x > 0:
                        self.scope.x -= self.scope.speed
                        self.scope.scope_sound.play()
            
                    if event.key == pygame.K_RIGHT and self.scope.x < self.grid_width - self.scope.width:
                        self.scope.x += self.scope.speed
                        self.scope.scope_sound.play()

                    if event.key == pygame.K_UP and self.scope.y > 0:
                        self.scope.y -= self.scope.speed
                        self.scope.scope_sound.play()

                    if event.key == pygame.K_DOWN and self.scope.y < self.grid_height - self.scope.width:
                        self.scope.y += self.scope.speed
                        self.scope.scope_sound.play()

            self.surface.fill(self.color)

            self.win.fill((60, 60, 60))

            self.bullet_counter()
            self.handle_pause()
            self.healthbar()
            self.handle_nuking()
            self.revive_handling()

            self.grid(self.surface)

            pygame.draw.rect(self.surface, (0, 0, 0), pygame.Rect(255, sine(self.sine_speed, 1280, self.sine_range, 30), 200, 75), 5, 5, 5, 5)
            pygame.draw.rect(self.surface, (255, 255, 255), pygame.Rect(257.5, sine(self.sine_speed, 1280, self.sine_range, 32.5), 195, 70))

            self.kill_label.render(self.surface, (self.score_rect.center[0], sine(self.sine_speed, 1280, self.sine_range, 30 + 35)))
            self.kill_label.update(self.kills)

            if self.enemy_generation_true:
                if self.current_time - self.time_since_enemy_generation >= self.time_difference:
                    enemy = Enemy(random.randint(0, 14) * 48, random.randint(0, 14)*48, random.choice([self.enemy_one_img, self.enemy_two_img, self.enemy_three_img]))
                    self.enemy_list.append(enemy)
                    self.time_since_enemy_generation = self.current_time

                if self.time_difference > 1000:
                    self.time_difference -= 1 

            if (self.kills >= 15):
                if self.health_green_width < 240:
                    self.health_green_width += 0.02

            for enemy in self.enemy_list:
                enemy.animation(self.surface, (self.grid_width - enemy.width - 5), (0))

                if enemy.visible == False:
                    self.enemy_list.remove(enemy)

            if self.screen_shake > 0:
                self.screen_shake -= 1

            if self.screen_shake:
                self.offset[0] = random.randint(0, 6) - 3 
                self.offset[1] = random.randint(0, 6) - 3

            self.scope.draw(self.surface)

            self.win.blit(self.surface, (self.offset[0], self.offset[1]))

            self.transparent()

            pygame.display.update()
            self.clock.tick(self.FPS)

M = Main()
M.main()