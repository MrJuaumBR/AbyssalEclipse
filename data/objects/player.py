from ..config import *

from pygame.locals import *

Frames_Positions = {
    'idle':[(0,0),(32,0),(64,0),(96,0),(128,0)],
    'top':[(0,32),(32,32),(64,32),(96,32),(128,32)],
    'left':[(0,64),(32,64),(64,64),(96,64),(128,64)],
    'bottom':[(0,96),(32,96),(64,96),(96,96),(128,96)],
    # 'right':[], => Just invert the left for right :)
}

class Player(pg.sprite.Sprite):
    type:str = 'player'
    
    world:object
    surface:pg.SurfaceType
    
    maxHealth:float=100.0
    health:float=100.0
    level:int = 1
    experience:float = 0.0
    
    speed:float = 3.0
    
    movement_vector:pg.math.Vector2 = pg.math.Vector2(0,0)
    
    register_speed = {
        'px/s':0.0,
        'm/s':0.0
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
        self.surface = pg.Surface((32,32))
        self.surface.fill((100,100,255))
        
        self.setup_animations()
        
    def setup_animations(self):
        ss = pge.createSpritesheet(GAME_PATH_TEXTURES+'/player.png')
        for key in ['top','left','right','bottom','idle']:
            self.animations[key] = []
            for frame in Frames_Positions[(key if key != 'right' else 'left')]:
                s = ss.image_at(Rect(frame[0],frame[1],32,32),-1)
                s = pg.transform.scale(s, Position((32,32))*RATIO)
                if key == 'right':
                    s = pg.transform.flip(s, True, False)
                self.animations[key].append(s)

    
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
            
            if UP: self.movement_vector.y -= self.speed
            elif DOWN: self.movement_vector.y += self.speed
            if LEFT: self.movement_vector.x -= self.speed
            elif RIGHT: self.movement_vector.x += self.speed
        
        magnitude = math.sqrt(self.movement_vector.x**2 + self.movement_vector.y**2)
        
        if magnitude > 0:
            self.movement_vector.x /= magnitude
            self.movement_vector.y /= magnitude
            
        # Now you can scale the normalized vector by the desired speed
        self.movement_vector.x *= self.speed
        self.movement_vector.y *= self.speed
        
        self.world.offset += self.movement_vector
        
        self.register_speed['px/s'] = self.get_speed('px/s')
        self.register_speed['m/s'] = self.get_speed('m/s')
    
    def animation_update(self):
        Vector_X:float = self.movement_vector.x
        Vector_Y:float = self.movement_vector.y
        
        # Detect Current State
        # Left, Right, Top, Bottom, Idle
        last_state = self.current_state
        if abs(Vector_X) > 0.1:
            self.current_state = 'left' if Vector_X < 0 else 'right'
        elif abs(Vector_Y) > 0.1:
            self.current_state = 'top' if Vector_Y < 0 else 'bottom'
        else:
            self.current_state = 'idle'
            
        if last_state != self.current_state: # Change
            self.current_frame = 0
        
        # Update Current Frame
        self.current_frame += 0.1
        if self.current_frame > len(self.animations[self.current_state]):
            self.current_frame = 0
        
        self.surface = self.animations[self.current_state][int(self.current_frame)]
    
    def reset_vector(self):
        self.movement_vector.x = 0
        self.movement_vector.y = 0

    def get_speed(self, measure_type):
            if measure_type not in ["px/s", "m/s"]:
                raise ValueError("Invalid measure type. Use 'px/s' or 'm/s'.")

            actual_speed = self.movement_vector.length()

            if measure_type == "px/s":
                return actual_speed * 60
            elif measure_type == "m/s":
                return actual_speed * 60 / 100
    
    def update(self):
        self.input()
        self.animation_update()
        self.reset_vector()
        
    def draw(self):
        if self.surface:
            r = self.surface.get_rect()
            r.center = pge.screen.get_rect().center
            pge.screen.blit(self.surface, r)