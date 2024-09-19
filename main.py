import pygame
import sys

from constants import *
from components.character import *
from components.world import *

# Inicializar 
pygame.init()

screen = pygame.display.set_mode((SIZES.width, SIZES.height))
pygame.display.set_caption("um filho da puta nu")

def main():
    clock = pygame.time.Clock()
    world = WORLD(9, seed=0)
    character = CHARACTER(SIZES.width/2, SIZES.height/2)
    world.chunkGen()
    # world.chunks[0,0].generate()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if not world.checkColission(character, -1, 0):
                character.move(-1, 0)
        if keys[pygame.K_RIGHT]:
            if not world.checkColission(character, 1, 0):
                character.move(1, 0)
        if keys[pygame.K_UP]:
            if not world.checkColission(character, 0, -1):
                character.move(0, -1)
        if keys[pygame.K_DOWN]:
            if not world.checkColission(character, 0, 1):
                character.move(0, 1)

        world.draw(screen)
        character.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()