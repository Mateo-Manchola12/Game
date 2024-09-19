import pygame
import numpy as np

from constants import COLOR, SIZES
from libs.seedCreate import SEED
from data.blocks import BLOCKS, block

class WORLD:
    def __init__(self, size, resource_probabilities, seed = None):
        self.x = 0
        self.y = 0
        self.size = size
        self.chunks = np.empty((self.size, self.size), dtype=object)
        if type(seed) == int and len(str(seed)) == 6:
            self.seed = seed
        elif type(seed) != int or len(str(seed)) != 6 and seed != None:
            self.seed = SEED(seed)
        else:
            self.seed = SEED()
        
    def draw(self, screen):
        dim0 = self.chunks[self.x,self.y].data[0]
        dim1 = self.chunks[self.x,self.y].data[1]
        for x in range(len(dim0)):
            for y in range(len(dim0[x])):
                self.chunks[self.x,self.y].data[0,x,y].rect = pygame.draw.rect(screen,BLOCKS[int(dim0[x,y].value)].color, rect=(x*SIZES.gridSize,y*SIZES.gridSize,SIZES.gridSize,SIZES.gridSize))
        for x in range(len(dim1)):
            for y in range(len(dim1[x])):
                if BLOCKS[int(dim1[x,y].value)].id != "air":
                    self.chunks[self.x,self.y].data[1,x,y].rect = pygame.draw.rect(screen,BLOCKS[int(dim1[x,y].value)].color, rect=(x*SIZES.gridSize,y*SIZES.gridSize,SIZES.gridSize,SIZES.gridSize))      

    def chunkGen(self):
        for x in range(len(self.chunks)):
            dx = int(x - np.trunc(self.size/2))
            for y in range(len(self.chunks[dx])):
                dy = int(y - np.trunc(self.size/2))
                self.chunks[dx,dy]=CHUNK(dx,dy,f'{self.seed}{x}{y}')
                if dx == -(self.size // 2) or dx == (self.size // 2) or dy == -(self.size // 2) or dy == (self.size // 2):
                    self.add_walls_to_chunk(self.chunks[dx, dy], dx, dy)
    def add_walls_to_chunk(self, chunk, dx, dy):
        gridsInX = chunk.data.shape[1]  # Número de celdas en X
        gridsInY = chunk.data.shape[2]  # Número de celdas en Y

        if dx == (self.size // 2):
            for y in range(gridsInY):
                chunk.data[1][-1, y] = block(1, None)  # Poner pared en el borde derecho

        # Si estamos en el borde izquierdo
        if dx == -(self.size // 2):
            for y in range(gridsInY):
                chunk.data[1][0, y] = block(1, None)  # Poner pared en el borde izquierdo

        # Si estamos en el borde inferior
        if dy == -(self.size // 2):
            for x in range(gridsInX):
                chunk.data[1][x, 0] = block(1, None)  # Poner pared en el borde inferior

        # Si estamos en el borde superior
        if dy == (self.size // 2):
            for x in range(gridsInX):
                chunk.data[1][x, -1] = block(1, None)  # Poner pared en el borde superior
    def checkColission(self, character, dx, dy):
        dim1 = self.chunks[self.x,self.y].data[1]
        if dx != 0:
            if character.x%SIZES.gridSize == 0:
                y1 = np.trunc(character.y/SIZES.gridSize)
                y2 = np.trunc((character.y+character.size-.1)/SIZES.gridSize)
                x = (character.x+character.size)/SIZES.gridSize if dx == 1 else (character.x/SIZES.gridSize)-1
                x = int(x)
                y1 = int(y1)
                y2 = int(y2)
                for y in range (y1,y2+1):
                    if 0 <= x < len(dim1) and 0 <= y < len(dim1[0]):
                        if BLOCKS[dim1[x,y].value].colissionable:
                            return True
                    elif x <= -1 or x >= len(dim1):
                        print(f'X:{self.x+dx} Y:{self.y+dy}')
                        if dx == 1:
                            character.x = 0
                        elif dx == -1:
                            character.x = (len(dim1)*SIZES.gridSize)-SIZES.gridSize
                        self.x +=dx
                        self.y +=dy
                        return True
        if dy != 0:
            if character.y%SIZES.gridSize == 0:
                x1 = np.trunc(character.x/SIZES.gridSize)
                x2 = np.trunc((character.x+character.size-.1)/SIZES.gridSize)
                y = (character.y+character.size)/SIZES.gridSize if dy == 1 else (character.y/SIZES.gridSize)-1
                y = int(y)
                x1 = int(x1)
                x2 = int(x2)
                for x in range (x1,x2+1):
                    if 0 <= x < len(dim1) and 0 <= y < len(dim1[0]):
                        if BLOCKS[dim1[x,y].value].colissionable:
                            return True
                    elif y <= -1 or y >= len(dim1[0]):
                        print(f'X:{self.x+dx} Y:{self.y+dy}')
                        if dy == 1:
                            character.y = 0
                        elif dy == -1:
                            character.y = (len(dim1[0])*SIZES.gridSize)-SIZES.gridSize
                        self.x +=dx
                        self.y +=dy
                        return True
        

class CHUNK:
    def __init__(self, x, y, seed, data=None):
        self.x = x
        self.y = y
        self.seed = int(seed)
        gridsInX = int(SIZES.width/SIZES.gridSize)
        gridsInY = int(SIZES.height/SIZES.gridSize)
        if data is None:
            self.data = np.empty((2, gridsInX, gridsInY), dtype=object)
            self.generate()
        else:
            self.data = data

    def generate(self):
        np.random.seed(self.seed)
        
        # Crear los valores aleatorios para la segunda dimensión
        random_values = np.random.choice([0, 3, 4], np.shape(self.data[1]), p=[.9, .05, .05])
        
        # Iterar sobre la matriz para crear los objetos 'block' con 'value' y 'rect'
        for x in range(self.data.shape[1]):  # gridsInX
            for y in range(self.data.shape[2]):  # gridsInY
                rect = None
                
                # Para el suelo (dim0) - todos los valores son 1
                self.data[0][x, y] = block(2, rect)  # Suelo con valor 1 (grass)
                
                # Para la segunda capa (dim1) - con valores aleatorios 0, 2, o 3
                self.data[1][x, y] = block(random_values[x, y], rect)