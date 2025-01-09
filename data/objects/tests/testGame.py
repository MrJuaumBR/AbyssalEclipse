"""
A Massive Shooter game, based in Relic Dudes, Brotato and Vampire Survivors

Classes:
Player - Will be the player sprite that will have the shoot trigger
World - Will draw all sprites on the screen and will handle with the Camera
Bullet - Is what the player will launch, need to have a 1.25 Lifetime and to shoot go point into mouse Direction, will have a trail
Enemy - The enemy that will flash in white 3 times when player gives damage to it, and when die becames into the state "died" that will not collide
"""
import pygame as pg
from pygame.locals import *
import sys,random

pg.init()

sw,sh = 1024,720

screen = pg.display.set_mode((sw,sh),0)
pg.display.set_caption("Massive Shooter Test")

clock = pg.time.Clock()

font = pg.font.SysFont("arial",14)
def render_text(position,text,color):
    f = font.render(text, True, color)
    r = f.get_rect()
    r.topleft = position
    screen.blit(f,r)

class _Bullet(pg.sprite.Sprite):
    type="bullet"
    trail_nodes:list = []
    
    position:pg.math.Vector2 = pg.math.Vector2(0,0)
    
    direction:pg.math.Vector2
    
    life_time:int = 90
    
    world:pg.sprite.Group
    def __init__(self, position:tuple[int,int],target_pos:tuple[int,int],*groups):
        super().__init__(*groups)
        self.position.x = position[0]-8
        self.position.y = position[1]-8
        self.surface = pg.Surface((16,16),SRCALPHA)
        pg.draw.circle(self.surface, (255,100,100), (8,8), 3,16)
        
        self.world = self.groups()[0]
        
        self.direction = (pg.Vector2(*target_pos)+self.world.shift) - self.position
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()
            
            
    def render_trail(self):
        if len(self.trail_nodes) >= 6:
            self.trail_nodes.pop(len(self.trail_nodes)-1)
        trail = (self.position,(6-len(self.trail_nodes))/6)
        self.trail_nodes.append(trail)
        
    def update(self):
        self.render_trail()
        self.position += self.direction * 5
        self.life_time -= 1
        if self.life_time <= 0:
            if self.world.player.bullets.index(self):
                # Stays alive???
                self.world.player.bullets.pop(self.world.player.bullets.index(self))
            self.kill()
        
        


class _Player(pg.sprite.Sprite):
    type='player'
    bullets:list = []
    velocity:float = 5
    
    rect:pg.rect.RectType= pg.rect.Rect(0,0,32,32)
    
    bullet_delay = 0
    
    world:pg.sprite.Group
    def __init__(self, *groups):
        super().__init__(*groups)
        self.surface = pg.Surface((32,32))
        self.surface.fill((100,100,255))
        
        self.rect.center = screen.get_rect().center
        
        self.detect_world()
     
    def player_shoot(self):
        if len(self.bullets) >= 6:
            for index,bullet in enumerate(self.bullets):
                if bullet.life_time <= 15:
                    self.bullets.pop(index)
        if self.bullet_delay <= 0 and pg.mouse.get_pressed(3)[0]:
            b = _Bullet(self.rect.center+self.world.shift,pg.mouse.get_pos(),self.world)
            self.bullets.append(b)
            self.bullet_delay = 30
        
    def detect_world(self):
        self.world = self.groups()[0]
        
    def update(self):
        self.player_shoot()
        if self.bullet_delay > 0: self.bullet_delay -= 1

class _World(pg.sprite.Group):
    shift:pg.math.Vector2 = pg.math.Vector2(0,0)
    player:_Player = None
    trail_render:list=[]
    def __init__(self, *sprites):
        super().__init__(*sprites)
        
    def input(self):
        keys = pg.key.get_pressed()
        UP = keys[K_UP] or keys[K_w]
        DOWN = keys[K_DOWN] or keys[K_s]
        LEFT = keys[K_LEFT] or keys[K_a]
        RIGHT = keys[K_RIGHT] or keys[K_d]
        if self.player:
            if UP:
                self.shift.y += -self.player.velocity
            elif DOWN:
                self.shift.y += self.player.velocity
                
            if LEFT:
                self.shift.x += -self.player.velocity
            elif RIGHT:
                self.shift.x += self.player.velocity
        
    def detect_player(self):
        if not self.player:
            for sprite in self.sprites():
                if sprite.type == 'player':
                    self.player = sprite
    
    def draw(self):
        for sprite in self.sprites():
            if sprite.type != 'player':
                pos:pg.math.Vector2 = sprite.position
                r = pos.copy() - self.shift
                screen.blit(sprite.surface, r)
                if sprite.type == 'enemy':
                    # print(r, sprite.position, pos)
                    # print('Enemy')
                    render_text((sprite.position-self.shift)-pg.Vector2(20,20),f'Enemy ({sprite.uniqueId})',(255,255,255))
            else:
                screen.blit(sprite.surface, sprite.rect)
        
        for trail in self.trail_render:
            pg.draw.rect(*trail)
        
        self.trail_render.clear()
    
    def enemysCount(self):
        x = 0
        for sp in self.sprites():
            if sp.type == 'enemy': x += 1
        return x
    
    def update(self, *args, **kwargs):
        self.detect_player()
        self.input()
        return super().update(*args, **kwargs)
        
        
   
class _Enemy(pg.sprite.Sprite):
    uniqueId:str
    type='enemy'
    position:pg.math.Vector2 = pg.math.Vector2(0,0)
    
    world:_World = None
    
    life:int = 3
    
    flash_count:int = 0
    def __init__(self, position:list[int,int],*groups):
        super().__init__(*groups)
        self.uniqueId:str = f'enemy-{random.randint(1000,9999)}'
        self.position = pg.math.Vector2(*position)
        
        self.surface = pg.Surface((32,32))
        self.surface.fill((190,190,50))
        
        if len(self.groups()) > 0:
            self.world:_World = self.groups()[0]
        
    def update(self):
        if self.world == None:
            self.world:_World = self.groups()[0]
        if self.flash_count > 0:
            self.surface.fill((200,200,200))
            self.flash_count -= 1
            if self.flash_count <= 0:
                self.flash_count = 0
                self.surface.fill((190,190,50))
        
        for sprite in self.world.sprites():
            if sprite.type == 'bullet':
                my_rect:pg.rect.RectType = pg.Rect(*(self.position.copy() + self.world.shift),32,32)
                b_rect:pg.rect.RectType = pg.Rect(*(sprite.position + self.world.shift),16,16)
                screen.blit(self.surface,my_rect)
                if my_rect.colliderect(b_rect) and sprite.life_time >= 1:
                    self.flash_count = 10
                    sprite.life_time = 0
                    self.life -= 1
                    if self.life <= 0:
                        ex,ey = random.choice([-15,-10,-5,5,10,15]),random.choice([-15,-10,-5,5,10,15])
                        ex *= random.randint(5,10)
                        ey *= random.randint(5,10)
                        ex = self.world.player.rect.centerx + ex
                        ey = self.world.player.rect.centery + ey
                        pos:tuple[int,int] = (ex,ey)
                        e = _Enemy(pos)
                        self.world.add(e)
                        self.kill()
        
    
World:_World = _World()
Player:_Player = _Player(World)

print("Generating Enemys...")
print("\tINDEX | X AXIS | Y AXIS")
for i in range(random.randint(5,10)):
    ex,ey = random.choice([-15,-10,-5,5,10,15]),random.choice([-15,-10,-5,5,10,15])
    ex *= random.randint(5,10)
    ey *= random.randint(5,10)
    ex = Player.rect.centerx + ex
    ey = Player.rect.centery + ey
    pos:tuple[int,int] = (ex,ey)
    e = _Enemy(pos)
    World.add(e)
    print(f'\t {i} | {ex} | {ey}')

def run():
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_F1:
                    for enemy in World.sprites():
                        if enemy.type == 'enemy':
                            enemy:_Enemy
                            print(enemy.position)
                
        
        screen.fill((0,0,0))
        World.draw()
        render_text((5,5),f'Nº Of Bullets: {len(Player.bullets or [])}      Nº Of Enemys:{World.enemysCount()}      Shift(X,Y):{World.shift.xy}',(255,255,255))
        clock.tick(60)
        pg.display.flip()
        World.update()