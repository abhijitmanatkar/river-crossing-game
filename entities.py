import pygame
from config import *

"Class definitions for Player, Obstacle and Enemy classes."


class Player(pygame.sprite.Sprite):
    "Class for the Player object"

    def __init__(self, pos, play_id):
        super().__init__()
        self.image = pygame.image.load("player.png")
        # set image rotatiion based on player id
        self.image = pygame.transform.rotate(self.image, (play_id - 1)*180)
        self.rect = self.image.get_rect()
        self.height = self.image.get_width()
        self.width = self.image.get_height()
        self.rect.center = pos
        self.speed = LAND_SPEED

    def update(self):
        # set speed based on if player is in land or water
        self.speed = WATER_SPEED
        for i in range(6):
            if i*LAND_DIFF <= self.rect.centery <= i*LAND_DIFF + 60:
                self.speed = LAND_SPEED

        # confine player to screen bounds
        if self.rect.y <= 0:
            self.rect.y = 0
        if self.rect.y + self.height >= HEIGHT:
            self.rect.y = HEIGHT - self.height
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.x + self.width >= WIDTH:
            self.rect.x = WIDTH - self.width


class Obstacle(pygame.sprite.Sprite):
    "Class for fixed obstacles"

    def __init__(self, pos):
        super().__init__()
        self.crossed = [False, False, False]
        self.image = pygame.image.load("obs.png")
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.center = pos


class Enemy(pygame.sprite.Sprite):
    "Class for moving enemies"

    def __init__(self, pos, speed):
        super().__init__()
        self.speed = speed
        self.crossed = [False, False, False]
        self.image = pygame.image.load("enemy_red.png")
        self.rect = self.image.get_rect().inflate(-30, -20)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.center = pos

    def update(self):
        # change direction if edge of screen is reached
        if self.rect.x <= 0 or self.rect.x + self.width >= WIDTH:
            self.speed *= -1
            self.image = pygame.transform.flip(self.image, 1, 0)
        self.rect.x += self.speed
