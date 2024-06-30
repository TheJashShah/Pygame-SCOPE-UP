import pygame, time

from button import Button
from label import Label

from sine import sine

play_btn_sheet = pygame.image.load("assets/images/btn_2.png")

control_btn_sheet = pygame.image.load("assets/images/btn_6.png")

play_text = Label("PLAY", "!", (10, 10, 10), 40)

title_text = Label("SCOPE-UP", "!", (10, 10, 10), 60)

control_text = Label("CONTROLS", "", (10, 10, 10), 25)

def main_menu(win, width, height, color):

    play_btn = Button((width/2 - 96), sine(200.0, 1280, 20.0, (height/2 - 32)), play_btn_sheet)

    control_btn = Button((width/2 - 96), sine(200.0, 1280, 20.0, (height/2 - 32 + 100)), control_btn_sheet)

    running = True
    game_running = False
    controls = False

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                pos = pygame.mouse.get_pos()
                if play_btn.rect.collidepoint(pos):
                    play_btn.clicked = True
                    play_btn.hover = False
                    running = False

                    game_running = True
                    controls = False

                if control_btn.rect.collidepoint(pos):
                    control_btn.clicked = True
                    control_btn.hover = False
                    running = False

                    controls = True
                    game_running = False
                
            if event.type == pygame.MOUSEBUTTONUP:
                play_btn.clicked = False
                control_btn.clicked = False


        win.fill(color)

        play_btn.draw(win)

        control_btn.draw(win)

        title_text.render(win, (360, sine(200.0, 1280, 20.0, 100)))

        play_text.render(win, (width/2, sine(200.0, 1280, 20.0, height/2 - 8)))

        control_text.render(win, (width/2, sine(200.0, 1280, 20.0, height/2 - 8 + 100)))

        play_btn.y = sine(200.0, 1280, 20.0, (height/2 - 32))

        control_btn.y = sine(200.0, 1280, 20.0, (height/2 - 32 + 100))

        pygame.display.update()
        pygame.time.Clock().tick(60)

    return game_running, controls
