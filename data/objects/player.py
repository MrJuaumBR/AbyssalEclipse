# Importando as coisas de "..config"
from ..config import *

# Importando as bibliotecas necessárias
import pygame
from pygame.locals import *
from pygame.sprite import Sprite

# Classe Bullet que herda de pg.sprite.Sprite
class Bullet(Sprite):
    def __init__(self, x, y, target):
        super().__init__()
        # Carregando a imagem da bala
        self.image = pygame.Surface((6, 12))  # tamanho da bala
        self.image.fill((255, 255, 0))  # cor da bala (amarelo)

        # Criando o retângulo da bala
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        # Calculando a direção da bala
        dx = target[0] - x
        dy = target[1] - y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        self.direction = (dx / distance, dy / distance)

        # Lifetime da bala
        self.lifetime = pge.TimeSys.s2f(2)

    # Método para atualizar a bala
    def update(self):
        # Movendo a bala
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

        # Rotacionando a bala
        angle = math.atan2(self.direction[1], self.direction[0])
        self.image = pygame.transform.rotate(self.image, math.degrees(angle))

        # Diminuindo o lifetime
        self.lifetime -= 1

    # Método para renderizar a bala
    def render(self, screen):
        # Renderizando a bala
        screen.blit(self.image, self.rect)

        # Verificando se a bala deve ser removida
        if self.lifetime <= 0:
            self.kill()

# Classe Player que herda de pg.sprite.Sprite
class Player(Sprite):
    def __init__(self):
        super().__init__()
        # Carregando a imagem do player
        self.image = pygame.Surface((32, 32))  # tamanho do player
        self.image.fill((255, 0, 0))  # cor do player (vermelho)

        # Criando o retângulo do player
        self.rect = self.image.get_rect()
        self.rect.centerx = 320  # posição inicial do player
        self.rect.centery = 240

        # Velocidade do player
        self.speed = 5

        # Lista de balas
        self.bullets = []

    # Método para atualizar o player
    def update(self):
        # Movendo o player
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x -= self.speed
        if keys[K_RIGHT]:
            self.rect.x += self.speed
        if keys[K_UP]:
            self.rect.y -= self.speed
        if keys[K_DOWN]:
            self.rect.y += self.speed

        # Atirando bala
        if keys[K_SPACE]:
            self.shoot()

    # Método para atirar bala
    def shoot(self):
        # Obtendo a posição do mouse
        mouse_pos = pygame.mouse.get_pos()

        # Criando uma nova bala
        bullet = Bullet(self.rect.centerx, self.rect.centery, mouse_pos)

        # Adicionando a bala à lista de balas
        self.bullets.append(bullet)

    # Método para renderizar o player
    def render(self, screen):
        # Renderizando o player
        screen.blit(self.image, self.rect)