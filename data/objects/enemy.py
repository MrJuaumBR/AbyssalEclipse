from ..config import *

class _Enemy(pg.sprite.Sprite):
    type:str = "enemy"
    
    position:pg.math.Vector2 = pg.math.Vector2(0,0)
    rect:pg.rect.RectType
    
    world:object
    
    health:int = 40
    max_health:int = 40
    speed:float = 4.5
    
    blinking:bool = False
    dying:bool = False
    at_distance:bool = False
    blink_time:float = 0
    fade_time:float = 0
    last_blink_time = pg.time.get_ticks()
    last_fade_time = pg.time.get_ticks()
    
    moving_right:bool = False
    animation = []
    frame = 0
    def __init__(self, position:list[int,int],level:int=1,*groups):
        super().__init__(*groups)
        self.blinking = False
        self.dying = False
        self.at_distance = False
        self.blink_time = 0
        self.fade_time = 0
        self.last_blink_time = pg.time.get_ticks()
        self.last_fade_time = pg.time.get_ticks()
        
        self.position = pg.math.Vector2(*position)
        
        self.surface = pg.Surface(Position((32,32))*RATIO)
        self.surface.fill((190,190,50))
        
        self.rect = self.surface.get_rect()
        
        if len(self.groups()) > 0:
            self.world:object = self.groups()[0]
            
        self.setup_animation()
    
    def setup_animation(self):
        pass
    
    def animate(self):
        pass
    
    def enemy_moveset(self):
        pass
    
    def take_damage(self, amount:int):
        self.health -= amount
        knockback_direction = (self.position - self.world.player.position).normalize()
        self.position += knockback_direction * (5 * RATIO.med)
        
        if self.health <= 0:
                self.dying = True
        else:
            self.blinking = True
            self.blink_time = pg.time.get_ticks()

    def draw(self):
        r = pg.rect.Rect(0,0, *Position((48,48))*RATIO)
        r.topleft = self.position.xy - self.world.offset
        self.world.surface.blit(self.surface, r)
        if CONFIG['debug']:
            pg.draw.rect(self.world.surface, self.world.debug_enemy_color, r, 1)
            
    def blink_sequence(self):
        if self.blinking:
            current_time = pg.time.get_ticks()
            if current_time - self.blink_time < 350:  # milliseconds
                self.surface.set_alpha(100 if self.surface.get_alpha() == 255 else 255)
            else:
                self.surface.set_alpha(255)
                self.blinking = False
        
    def kill_sequence(self):
        if self.dying:
            current_time = pg.time.get_ticks()
            if current_time - self.fade_time < 1000:  # milliseconds
                self.alpha -= 0.01
                if self.alpha < 0:
                    self.alpha = 0
                self.surface.set_alpha(self.alpha)
            else:
                self.world.add_item(self.position, random.choice(['ExpShard','Coin']))
                self.kill()
                self.dying = False
            
    def update(self):
        self.enemy_moveset()
        self.animate()
        self.blink_sequence()
        self.kill_sequence()

class BloodyEye(_Enemy):
    def setup_animation(self):
        spritesheet = pge.createSpritesheet(GAME_PATH_TEXTURES+'/enemys.png')
        frame_size = Position((48,48)) * RATIO
        self.animation = [
            pg.transform.scale(spritesheet.image_at(pg.Rect(x, 0, 32, 32), 0), frame_size)
            for x in range(0, 160, 32)
        ]
        self.rect = self.animation[0].get_rect()
        
    def enemy_moveset(self):
        player = self.world.player
        direction = (player.position - self.position)
        distance = direction.length()

        if distance < 280 * RATIO.med:
            self.at_distance = False
            direction = direction.normalize() * -1  # move away from the player
            self.position += direction * self.speed
            self.moving_right = direction.x > 0
        elif distance > 470 * RATIO.med:
            self.at_distance = False
            direction = direction.normalize()  # move towards the player
            self.position += direction * self.speed
            self.moving_right = direction.x > 0
        else:
            self.at_distance = True
            # stop moving when at distance
            self.position = self.position
            # you can add other behavior here, like shooting at the player
            for rect in self.rect.collidelistall([i.rect for i in self.world.enemys]):
                dx,dy = (self.rect.centerx - self.world.enemys[rect].rect.centerx), (self.rect.centery - self.world.enemys[rect].rect.centery)
                distance = math.hypot(dx, dy)
                if distance < (32*RATIO.med) and distance > 0:
                    self.position += pg.math.Vector2(dx/distance, dy/distance) * 2
            
    def animate(self):
        self.frame = (self.frame + 0.5 * (pge.getAvgFPS()/pge.fps)) % len(self.animation)
        self.surface = self.animation[int(self.frame)]
        if self.moving_right:
            self.surface = pg.transform.flip(self.surface, True, False)

class NightmareImp(_Enemy):
    def setup_animation(self):
        s = pge.createSpritesheet(GAME_PATH_TEXTURES+'/enemys.png')
        self.animation = []
        
        x = 0
        for _ in range(5):
            i = s.image_at(pg.Rect(x,32,32,32),0)
            i = pg.transform.scale(i, Position((48,48))*RATIO)
            self.animation.append(i)
            x += 32
            
        self.rect = self.animation[0].get_rect()
        self.rect.topleft = self.position
    
    def enemy_moveset(self):
        
        direction = (GAME_CENTER_OF_SCREEN+self.world.offset) - self.position
        if direction.length() > 0:
            self.position += direction.normalize() * self.speed
            self.rect.topleft = self.position
            for rect in self.rect.collidelistall([i.rect for i in self.world.enemys]):
                dx,dy = (self.rect.centerx - self.world.enemys[rect].rect.centerx), (self.rect.centery - self.world.enemys[rect].rect.centery)
                distance = math.hypot(dx, dy)
                if distance < (32*RATIO.med) and distance > 0:
                    self.position += pg.math.Vector2(dx/distance, dy/distance) * 2
    
    def animate(self):
        self.frame = (self.frame + 0.5 * (pge.getAvgFPS()/pge.fps)) % len(self.animation)
        self.surface = self.animation[int(self.frame)]
        if self.moving_right:
            self.surface = pg.transform.flip(self.surface, True, False)
            