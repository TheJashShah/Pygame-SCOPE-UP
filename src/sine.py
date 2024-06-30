import pygame, math

def sine(speed, time, how_far, y):
    t = pygame.time.get_ticks() / 1.5 % time
    y_ = math.sin(t / speed) * how_far + y
    return(y_)
# Copied