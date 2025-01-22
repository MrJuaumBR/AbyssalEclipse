from ..config import *

from pygame.locals import *

Frames_Positions = {
    'idle':[(0,0),(32,0),(64,0),(96,0),(128,0)],
    'top':[(0,32),(32,32),(64,32),(96,32),(128,32)],
    'left':[(0,64),(32,64),(64,64),(96,64),(128,64)],
    'bottom':[(0,96),(32,96),(64,96),(96,96),(128,96)],
    # 'right':[], => Just invert the left for right :)
}

class Weapon(pg.sprite.Sprite):
    type:str = 'weapon'
    
    player:object
    surface:pg.SurfaceType
    
    damage:float = 10.0
    start_pos:pg.math.Vector2 = pg.math.Vector2(0,0)
    mouse_pos:pg.math.Vector2 = pg.math.Vector2(0,0)
    position:pg.math.Vector2 = pg.math.Vector2(0,0)
    rect:pg.Rect = pg.Rect(0,0,*(Position((16,16))*RATIO))
    start_time:datetime.timedelta = None
    lifetime:float = 10.0
    
    direction:pg.math.Vector2 = pg.math.Vector2(0,0)
    def __init__(self, player:object, center_of_screen:tuple[int,int]=(0,0)):
        super().__init__()
        print(f"Weapon Created at: {center_of_screen}, and is going to: {pge.mouse.pos}")
        self.player = player
        self.surface = pg.Surface(Position((16,16))*RATIO)
        self.surface.fill((255,0,0))
        
        self.position = pg.math.Vector2(*center_of_screen)
        
        self.start_pos = pg.math.Vector2(*center_of_screen)
        self.mouse_pos = pg.math.Vector2(pge.mouse.pos)
        self.start_time:datetime.timedelta = pge.delta_time.total_seconds()
        
        self.setup()
        
    def setup(self):
        self.direction = self.mouse_pos - self.start_pos
        
        
        
        self.direction.normalize_ip()
        print(f"Weapon Direction: {self.direction}")
    
    def update(self):
        if self.start_time + self.lifetime < pge.delta_time.total_seconds():
            print("Delete weapon")
            self.kill()
        
        # self.position += self.direction * 3
        self.rect.center = self.position.xy

class Player(pg.sprite.Sprite):
    type:str = 'player'
    
    world:object
    surface:pg.SurfaceType
    
    maxHealth:float=100.0
    health:float=100.0
    level:int = 1
    experience:float = 0.0
    reload_time:float = 2.0
    last_reload_time:datetime.timedelta = pge.delta_time.total_seconds()
    
    speed:float = 1.5
    max_speed:float = 0.0
    
    movement_vector:pg.math.Vector2 = pg.math.Vector2(0,0)
    
    register_speed = {
        'px/s':0.0,
        'm/s':0.0,
        'km/h':0.0,
        'mph':0.0
    }
    
    animations = {
        'top':[],
        'left':[],
        'right':[],
        'bottom':[],
        'idle':[]
    }
    current_state:Literal['top','left','right','bottom','idle'] = 'idle'
    current_frame:int = 0
    def __init__(self, world:pg.sprite.Group):
        super().__init__(world)
        self.world = world
        self.surface = pge.createSurface(*Position((32,32))*RATIO)
        self.surface.fill((100,100,255))
        
        self.max_speed = self.speed*100
        
        self.setup_animations()
        
    def setup_animations(self):
        ss = pge.createSpritesheet(GAME_PATH_TEXTURES+'/player.png')
        for key in ['top','left','right','bottom','idle']:
            self.animations[key] = []
            for frame in Frames_Positions[(key if key != 'right' else 'left')]:
                s = ss.image_at(Rect(frame[0],frame[1],32,32),255)
                s = pg.transform.scale(s, Position((32,32))*RATIO)
                if key == 'right':
                    s = pg.transform.flip(s, True, False)
                self.animations[key].append(s)

    def shoot(self):
        center_of_screen = pge.screen.get_rect().center
        w = Weapon(self,center_of_screen)
        self.world.add(w)
        
    
    def input(self):
        if pge.joystick.main: # Has a controller/joystick
            x,y = pge.joystick.main.getAxisByString('left')
            if abs(x) > 0.2:
                self.movement_vector.x += x * self.speed
            if abs(y) > 0.2:
                self.movement_vector.y += y * self.speed
        else:
            UP = pge.hasKeyPressed(K_w) or pge.hasKeyPressed(K_UP)
            DOWN = pge.hasKeyPressed(K_s) or pge.hasKeyPressed(K_DOWN)
            LEFT = pge.hasKeyPressed(K_a) or pge.hasKeyPressed(K_LEFT)
            RIGHT = pge.hasKeyPressed(K_d) or pge.hasKeyPressed(K_RIGHT)
            CLICK = pge.mouse.left
            
            if UP: self.movement_vector.y -= self.speed
            elif DOWN: self.movement_vector.y += self.speed
            if LEFT: self.movement_vector.x -= self.speed
            elif RIGHT: self.movement_vector.x += self.speed
            
            # Reload TIme is time delta
            # Reload Time is stored in reload_time
            if CLICK and self.last_reload_time + self.reload_time < pge.delta_time.total_seconds():
                self.shoot()
                self.last_reload_time = pge.delta_time.total_seconds()
        
        # Normalize vectors
        magnitude = math.sqrt(self.movement_vector.x**2 + self.movement_vector.y**2)
            
        if magnitude > 0: # Prevent division by zero    
            
            # Detect if the speed is going to pass the speed limit
                # Simulate the movement vector with the speed
            _mov_vector = self.movement_vector
            _mov_vector /= magnitude
            _mov_vector *= self.speed
            _speed = self.get_speed('px/s', mov_vector=_mov_vector) # Gets the current speed
            
            if _speed > self.max_speed: # Speed Limit Reached
                # Rescale Magnitude to not pass the speed limit
                magnitude = (_speed / self.max_speed) * self.speed # (Actual Speed / Max Speed) * Speed
                
            # Normalize the vector
            self.movement_vector.x /= magnitude
            self.movement_vector.y /= magnitude
            
        # Now you can scale the normalized vector by the desired speed
        self.movement_vector.x *= self.speed
        self.movement_vector.y *= self.speed
        
        # Update world offset
        self.world.offset += self.movement_vector
        
        # Update Speed Measures
        self.register_speed['px/s'] = self.get_speed('px/s')
        self.register_speed['m/s'] = self.get_speed('m/s')
        self.register_speed['km/h'] = self.get_speed('km/h')
        self.register_speed['mph'] = self.get_speed('mph')
    
    def animation_update(self):
        # Detect Current State
        # Left, Right, Top, Bottom, Idle
        Vector_X, Vector_Y = self.movement_vector.xy
        self.current_state = (
            'left' if Vector_X < 0 else
            'right' if Vector_X > 0 else
            'top' if Vector_Y < 0 else
            'bottom' if Vector_Y > 0 else
            'idle'
        )
        
        # Update Current Frame
        # Animation Needs to be framerate independent
        self.current_frame = (self.current_frame + 0.07 * (pge.getAvgFPS()/pge.fps)) % len(self.animations[self.current_state])
        
        self.surface = self.animations[self.current_state][int(self.current_frame)]
    
    def reset_vector(self):
        self.movement_vector.x = 0
        self.movement_vector.y = 0

    def get_speed(self, measure_type: Literal['px/s', 'm/s', 'km/h', 'mph'] = 'px/s', mov_vector: pg.Vector2 = None) -> float:
        if measure_type not in ["px/s", "m/s", "km/h", "mph"]:
            raise ValueError("Invalid measure type. Use one of these options:\n'px/s', 'm/s', 'km/h', 'mph'.")

        actual_speed = (mov_vector or self.movement_vector).length() * int(pge.getAvgFPS())

        conversion_factors = {'px/s': 1, 'm/s': 0.01, 'km/h': 0.036, 'mph': 0.0223694}
        
        return actual_speed * conversion_factors.get(measure_type, 1)
    
    def update(self):
        self.input()
        self.animation_update()
        self.reset_vector()
        
    def draw(self):
        if self.surface:
            r = self.surface.get_rect(center=pge.screen.get_rect().center)

            if pge.mouse.pos :
                pg.draw.line(pge.screen, pge.Colors.LIGHTGREEN.rgb, r.center, pge.mouse.pos, int(1*RATIO.med))

            pge.screen.blit(self.surface, r)

            if CONFIG['debug']:
                pge.draw_text(Position((10,30))*RATIO,
                              'Position: {}, Offset: {}, Offset Position: {}'.format(
                                  r.center, self.world.offset, r.center - self.world.offset),
                              PS16, pge.Colors.WHITE.rgb)
