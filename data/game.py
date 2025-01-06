# Importando as coisas de "..config"
from .config import *

# Importando as bibliotecas necessárias
import pygame
from pygame.locals import *
from pygame.sprite import Group

# Importando as classes do world.py e player.py
from .objects.world import World
from .objects.player import Player

# Classe Game que herda de Screen
class Game(Screen):
    def __init__(self):
        super().__init__()

        # Criando o grupo de sprites
        self.all_sprites = Group()

        # Criando o mundo
        self.world = World()

        # Criando o player
        self.player = Player()

        # Adicionando o player ao mundo
        self.world.add(self.player)

        # Adicionando o mundo ao grupo de sprites
        self.all_sprites.add(self.world)

    # Método para atualizar o jogo
    def update(self):
        # Atualizando todos os sprites
        self.all_sprites.update()

    # Método para renderizar o jogo
    def render(self):
        # Preenchendo a tela com branco
        self.screen.fill((255, 255, 255))

        # Renderizando todos os sprites
        self.all_sprites.render(self.screen)

    # Método para rodar o jogo
    def run(self):
        # Loop principal
        running = True
        while running:
            # Tratando eventos
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            # Atualizando o jogo
            self.update()

            # Renderizando o jogo
            self.render()
