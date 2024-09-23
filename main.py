import pygame
import sys

from constants import *
from components.character import *
from components.world import *

# Inicializar 
pygame.init()

screen = pygame.display.set_mode((SIZES.width, SIZES.height))
pygame.display.set_caption("Um filho da puta nu")

def main():
    resource_probabilities = [5, 5, 5]  # Ajustar abundancia de recursos
    clock = pygame.time.Clock()
    world = WORLD(9, resource_probabilities, seed=0)  # Crear mundo con seed 0
    character = CHARACTER(SIZES.width / 2, SIZES.height / 2)  # Inicializar personaje

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_RIGHT]:
            dx = 1
        if keys[pygame.K_UP]:
            dy = -1
        if keys[pygame.K_DOWN]:
            dy = 1

        # Mover al personaje y detectar colisiones
        if not world.checkCollision(character, dx, dy):
            character.move(dx, dy)

        # Dibujar el mundo y el personaje
        world.draw(screen)
        character.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
