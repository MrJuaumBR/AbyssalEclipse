from ..config import *

class _Enemy(pg.sprite.Sprite):
    type:str = "enemy"
    
    position:pg.math.Vector2 = pg.math.Vector2(0,0)
    rect:pg.rect.RectType
    
    world:object
    
    _health:int = 20
    max_health:int = 20
    speed:float = 3.6
    damage:float = 2.0
    attack_delay:float = 1.2
    
    blinking:bool = False
    dying:bool = False
    at_distance:bool = False
    blink_time:float = 0
    fade_time:float = 0
    last_blink_time = pg.time.get_ticks()
    last_fade_time = pg.time.get_ticks()
    last_attack:float = 0
    
    moving_right:bool = False
    animation = []
    distance = [128,256, 32]
    _frame = 0
    
    started:pygameengine.timedelta = None
    time_until_move:float = 0
    @property
    def health(self, value:int) -> int:
        self._health = value
    
    @health.setter
    def health(self, value:int) -> int:
        self._health = value
        if self._health > self.max_health:
            self._health = self.max_health
        elif self._health < 0:
            self._health = 0
    def __init__(self, position:list[int,int],level:int=1,*groups):
        super().__init__(*groups)
        self.started = pge.delta_time.total_seconds()
        self.blinking = False
        self.dying = False
        self.at_distance = False
        self.blink_time = 0
        self.fade_time = 0
        self.last_blink_time = pg.time.get_ticks()
        self.last_fade_time = pg.time.get_ticks()
        
        self.position = pg.math.Vector2(*position)
        
        self.surface = pg.Surface(Position((32,32))*RATIO)
        
        self.rect = self.surface.get_rect()
        
        if len(self.groups()) > 0:
            self.world:object = self.groups()[0]
            
        self.setup_animation()
    
    @property
    def frame(self):
        return self._frame
    
    @frame.setter
    def frame(self, value):
        self._frame = value
        if self._frame >= len(self.animation):
            self._frame = 0
        elif self._frame < 0:
            self._frame = 0
    
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
        self.world.surface.blit(self.surface, r.copy())
        if CONFIG['debug']:
            pg.draw.rect(self.world.surface, self.world.debug_enemy_color, r, 1)
            
    def blink_sequence(self):
        """
        On player attack, the enemy blinks
        
        """
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
                self.world.add_item(self.position, random.choice(['ExpShard','ExpShard','ExpShard','ExpShard','ExpShard','Coin']))
                self.kill()
                self.dying = False
    
    def collision(self):
        if self.world.player.rect.colliderect(self.rect):
            if pge.delta_time.total_seconds()-self.last_attack > self.attack_delay: #seconds-self.last_attack
                self.world.player.take_damage(self.damage)
                self.last_attack = pge.delta_time.total_seconds()
    
    def update(self):
        if pge.delta_time.total_seconds()-self.started > self.time_until_move:
            self.enemy_moveset()
            self.collision()
        self.animate()
        self.blink_sequence()
        self.kill_sequence()

class BloodyEye(_Enemy):
    time_until_move:float = 1.2
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
        if distance < self.distance[0] * RATIO.med:
            self.at_distance = False
            direction = direction.normalize() * -1  # move away from the player
            self.position += direction * (self.speed * GD.fps_ratio)
            self.moving_right = direction.x > 0
            GD.new_task(self.avoid_enemies, ())
        elif distance > self.distance[1] * RATIO.med:
            self.at_distance = False
            direction = direction.normalize()  # move towards the player
            self.position += direction * (self.speed * GD.fps_ratio)
            self.moving_right = direction.x > 0
            GD.new_task(self.avoid_enemies, ())
        else:
            self.at_distance = True
            # stop moving when at distance
            self.position = self.position
            GD.new_task(self.avoid_enemies, ())
    def avoid_enemies(self):
        """
        Avoid enemies by moving away from them if they are too close.

        This function is used to prevent enemies from entering each other.
        It calculates the distance between the current enemy and other enemies,
        and if the distance is too small, it moves the current enemy away from the other enemy.

        :return: None
        """
        for rect in self.rect.collidelistall([i.rect for i in self.world.enemys]):
            dx,dy = (self.rect.centerx - self.world.enemys[rect].rect.centerx), (self.rect.centery - self.world.enemys[rect].rect.centery)
            distance = math.hypot(dx, dy)
            if distance < (self.distance[2]*RATIO.med) and distance > 0:
                self.position += pg.math.Vector2(dx/distance, dy/distance) * 2
            
    def animate(self):
        self.frame = (self.frame+(0.3*(pge.getAvgFPS()/pge.fps)) * GD.fps_ratio) % len(self.animation)
        self.surface = self.animation[int(self.frame)]
        if self.moving_right:
            self.surface = pg.transform.flip(self.surface, True, False)

class NightmareImp(_Enemy):
    time_until_move:float = 1.75
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
    
    def avoid_enemies(self):
        """
        Avoid enemies by moving away from them if they are too close.

        This function is used to prevent enemies from entering each other.
        It calculates the distance between the current enemy and other enemies,
        and if the distance is too small, it moves the current enemy away from the other enemy.

        :return: None
        """
        for rect in self.rect.collidelistall([i.rect for i in self.world.enemys]):
            dx,dy = (self.rect.centerx - self.world.enemys[rect].rect.centerx), (self.rect.centery - self.world.enemys[rect].rect.centery)
            distance = math.hypot(dx, dy)
            if distance < (self.distance[2]*RATIO.med):
                self.position += pg.math.Vector2(dx/(distance or 1), dy/(distance or 1)) * 2
    
    def enemy_moveset(self):
        
        direction = self.world.player.rect.center - self.position
        if direction.length() > 0:
            self.position += direction.normalize() * (1+(self.speed * GD.fps_ratio))
            self.rect.topleft = self.position
            GD.new_task(self.avoid_enemies, ())
    
    def animate(self):
        self.frame = (self.frame+(0.3*(pge.getAvgFPS()/pge.fps)) * GD.fps_ratio) % len(self.animation)
        self.surface = self.animation[int(self.frame)]
        if self.moving_right:
            self.surface = pg.transform.flip(self.surface, True, False)
            