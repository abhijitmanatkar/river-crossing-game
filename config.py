import pygame

""" All constants used within the game are defined here.
Also includes fonts, RGB values of colors and sound effects.
"""

# constants
WIDTH = 1200
HEIGHT = 800
LAND_HEIGHT = 40
LAND_DIFF = (HEIGHT - 6*LAND_HEIGHT)/5 + LAND_HEIGHT
WATER_HEIGHT = (HEIGHT - 6*LAND_HEIGHT)/5
LAND_SPEED = 3
WATER_SPEED = 1
ENEMY_SPEED = 4

# colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
LAND_COLOR = (0, 128, 30)
RIVER_BLUE = (42, 180, 255)

# fonts
pygame.font.init()
font = pygame.font.Font('CodaCaption-ExtraBold.ttf', 25)
title_font = pygame.font.Font('CodaCaption-ExtraBold.ttf', 100)
mid_font = pygame.font.Font('CodaCaption-ExtraBold.ttf', 50)

# sound effect
pygame.mixer.init()
exp = pygame.mixer.Sound("ded.wav")
