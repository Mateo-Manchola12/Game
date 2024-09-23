import pygame
import numpy as np
from perlin_noise import PerlinNoise
from constants import COLOR, SIZES
from libs.seedCreate import SEED
from data.blocks import BLOCKS, block

# Clase WORLD representa el mundo del juego
class WORLD:
    def __init__(self, size, resource_probabilities, seed=None):
        """
        Constructor para la clase WORLD. 
        Inicializa el mundo y sus chunks basado en las probabilidades de recursos y la semilla.
        
        :param size: Tamaño del mundo (número de chunks por lado)
        :param resource_probabilities: Array que representa la abundancia de cada recurso en el mundo (de 1 a 10)
        :param seed: Semilla para generar el ruido de Perlin. Si no se proporciona, se genera una automáticamente.
        """
        self.x = 0  # Coordenada x del jugador (o del foco de visualización)
        self.y = 0  # Coordenada y del jugador (o del foco de visualización)
        self.size = size  # Tamaño del mundo (en chunks)
        self.chunks = {}  # Diccionario para almacenar los chunks generados
        self.resource_probabilities = resource_probabilities  # Probabilidades de los recursos
        self.seed = seed if isinstance(seed, int) and len(str(seed)) == 6 else SEED(seed)  # Manejo de la semilla
        self.noise = PerlinNoise(octaves=24, seed=self.seed)  # Genera el ruido de Perlin basado en la semilla
        self.chunk_size = (SIZES.width // SIZES.gridSize, SIZES.height // SIZES.gridSize)  # Tamaño de cada chunk en bloques (grid size)

    def draw(self, screen):
        """
        Dibuja el mundo en la pantalla. Cada chunk se renderiza de manera individual.
        
        :param screen: Pantalla de Pygame donde se dibuja el mundo.
        """
        current_chunk = self.get_chunk(self.x, self.y)  # Obtiene el chunk actual basado en la posición del jugador
        dim0 = current_chunk.data[0]  # Dimensión 0 (suelo)
        dim1 = current_chunk.data[1]  # Dimensión 1 (objetos sobre el suelo)

        # Dibujar el suelo (dim0)
        for x in range(len(dim0)):
            for y in range(len(dim0[x])):
                block_type = BLOCKS[dim0[x, y].value]  # Obtener el tipo de bloque
                rect = pygame.Rect(x * SIZES.gridSize, y * SIZES.gridSize, SIZES.gridSize, SIZES.gridSize)
                pygame.draw.rect(screen, block_type.color, rect)  # Dibujar el bloque

        # Dibujar objetos encima del suelo (dim1)
        for x in range(len(dim1)):
            for y in range(len(dim1[x])):
                if BLOCKS[dim1[x, y].value].id != "air":  # Si el bloque no es "aire"
                    rect = pygame.Rect(x * SIZES.gridSize, y * SIZES.gridSize, SIZES.gridSize, SIZES.gridSize)
                    pygame.draw.rect(screen, BLOCKS[dim1[x, y].value].color, rect)

    def get_chunk(self, x, y):
        """
        Obtiene un chunk específico. Si no existe, lo genera automáticamente.
        Utiliza la posición global para extraer el trozo correcto del ruido global.

        :param x: Coordenada x del chunk
        :param y: Coordenada y del chunk
        :return: El chunk solicitado.
        """
        # Verificar si el chunk ya fue generado
        if (x, y) not in self.chunks and -self.size // 2 <= x <= self.size // 2 and -self.size // 2 <= y <= self.size // 2:
            # Generar el chunk si no está en caché
            self.chunks[(x, y)] = CHUNK(x, y, self.size, self.noise, self.resource_probabilities, self.chunk_size)
            
            # Si estamos en los bordes del mundo, agregar paredes
            if x == -(self.size // 2) or x == (self.size // 2) or y == -(self.size // 2) or y == (self.size // 2):
                print('3')
                self.chunks[(x, y)].add_walls()
        
        return self.chunks[(x, y)]  # Retornar el chunk

    def checkCollision(self, character, dx, dy):
        current_chunk = self.get_chunk(self.x, self.y)
        dim1 = current_chunk.data[1]
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
# Clase CHUNK representa un chunk del mundo (una pequeña porción de bloques)
# Clase CHUNK representa un chunk del mundo (una pequeña porción de bloques)
class CHUNK:
    def __init__(self, x, y, size, noise, resource_probabilities, chunk_size):
        """
        Constructor para un CHUNK del mundo.
        
        :param x: Coordenada x del chunk
        :param y: Coordenada y del chunk
        :param seed: Semilla del mundo (para consistencia en generación)
        :param noise: Mapa de ruido de Perlin (instancia ya inicializada para usar)
        :param resource_probabilities: Array de probabilidades de recursos
        :param chunk_size: Tamaño del chunk en bloques
        """
        self.x = x  # Coordenada x del chunk
        self.y = y  # Coordenada y del chunk
        self.size = size
        self.data = self.generate_chunk(noise, chunk_size, resource_probabilities, size)  # Generar los bloques del chunk

    def generate_chunk(self, noise, chunk_size, resource_probabilities, size):
        """
        Genera los bloques del chunk basado en el ruido de Perlin. El ruido es ajustado
        para que cada chunk se alinee con sus vecinos.

        :param noise: Instancia de PerlinNoise para generar el ruido
        :param chunk_size: Tamaño del chunk en bloques
        :param resource_probabilities: Array de probabilidades para los recursos
        :return: Datos del chunk (bloques generados)
        """
        chunk_data = np.empty((2, chunk_size[0], chunk_size[1]), dtype=object)  # Crear un array para almacenar los datos de los bloquesnp.empty((2, gridsInX, gridsInY), dtype=object)
        rect = None

        # Generar los bloques basados en el ruido de Perlin
        for i in range(chunk_size[0]):
            for j in range(chunk_size[1]):
                # Las coordenadas globales del bloque se basan en las coordenadas del chunk y el bloque dentro del chunk
                global_x = (self.x * chunk_size[0]) + i
                global_y = (self.y * chunk_size[1]) + j
                
                # Generar el valor del ruido usando las coordenadas globales normalizadas
                noise_value = noise([global_x / (chunk_size[0] * size), global_y / (chunk_size[1] * size)])
                
                # Tomar como semilla el valor del ruido conviertiendolo a un entero de 8 cifras
                np.random.seed(SEED(noise_value))
                
                # Primera capa: Suelo o Agua
                if noise_value < -0.25:  # Agua en ruidos bajos 
                    chunk_data[0, i, j] = block(5, rect)  # Agua en la primera capa
                else:
                    chunk_data[0, i, j] = block(2, rect)  # Suelo (hierba) en la primera capa
                
                # Segunda capa: Recursos como madera o piedra
                if noise_value > 0.2:  # Bosques de madera en ruido medio
                    chunk_data[1, i, j] = block(3, rect)  # Madera
                elif noise_value > 0 and np.random.random() < 0.05:  # Piedra aparece aleatoriamente
                    chunk_data[1, i, j] = block(4, rect)  # Piedra
                else:
                    chunk_data[1, i, j] = block(0, rect)  # Sin recurso




                # else:
                #     print(f'i{i} j{j}')
                #     chunk_data[1, i, j] = block(3, rect)

        return chunk_data

    def add_walls(self):
        """
        Agrega paredes alrededor del chunk si este está en el borde del mundo.
        Utiliza las coordenadas del chunk (self.x, self.y) para determinar si es un chunk de borde.
        """
        # Número de celdas en X y en Y en el chunk
        gridsInX = self.data.shape[1]
        gridsInY = self.data.shape[2]
        print('2')
        # Definir los bordes donde se agregarán las paredes
        if self.x == -(self.size // 2):
            # Agregar paredes en el borde izquierdo
            for y in range(gridsInY):
                self.data[1][0, y] = block(1, None)  # Pared en el borde izquierdo

        if self.x == (self.size // 2):
            # Agregar paredes en el borde derecho
            for y in range(gridsInY):
                self.data[1][-1, y] = block(1, None)  # Pared en el borde derecho

        if self.y == -(self.size // 2):
            print('1')
            # Agregar paredes en el borde inferior
            for x in range(gridsInX):
                self.data[1][x, 0] = block(1, None)  # Pared en el borde inferior

        if self.y == (self.size // 2):
            # Agregar paredes en el borde superior
            for x in range(gridsInX):
                self.data[1][x, -1] = block(1, None)  # Pared en el borde superior
