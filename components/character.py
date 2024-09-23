import pygame
from constants import COLOR, PHYSICS
class CHARACTER:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20
        self.speed = PHYSICS.speed

    def draw(self, screen):
        self.rect = pygame.draw.rect(screen, COLOR.black, rect=(self.x, self.y, self.size, self.size))

    def move(self, dx, dy):
        self.x += dx*self.speed;
        self.y += dy*self.speed;