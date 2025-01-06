# Importando as coisas de "..config"
from ..config import *

# Importando as bibliotecas necessárias
import pygame
from pygame.locals import *
from pygame.sprite import Group

# Classe World que herda de pg.sprite.Group
class World(Group):
    def __init__(self):
        super().__init__()
        # Carregando a imagem do chão
        self.floor_image = pygame.image.load('../assets/textures/floor.png')
        self.floor_rect = self.floor_image.get_rect()
        self.floor_rect.width = 128
        self.floor_rect.height = 64

        # Criando o mapa
        self.map_width = 2048
        self.map_height = 2048
        self.map_surface = pygame.Surface((self.map_width, self.map_height))
        self.map_surface.fill((255, 255, 255))

        # Repetindo o chão para criar o mapa
        for x in range(0, self.map_width, self.floor_rect.width):
            for y in range(0, self.map_height, self.floor_rect.height):
                self.map_surface.blit(self.floor_image, (x, y))

        # Criando a câmera
        self.camera = pygame.Rect(0, 0, 640, 480)  # ajuste os valores conforme necessário

    # Método para renderizar tudo
    def render(self, screen):
        # Preenchendo a tela com branco
        screen.fill((255, 255, 255))

        # Renderizando o mapa
        screen.blit(self.map_surface, (0, 0))

        # Renderizando todas as sprites
        for sprite in self.sprites():
            sprite.render(screen)

    # Método para atualizar a câmera
    def update(self):
        # Atualizando a câmera com base na posição do player
        # (vou criar o código para isso em player.py)
        pass