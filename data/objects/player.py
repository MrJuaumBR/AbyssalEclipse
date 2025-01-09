from ..config import *

from pygame.locals import *

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
    def __init__(self, world:pg.sprite.Group):
        super().__init__(world)
        self.world = world
        self.surface = pg.Surface((32,32))
        self.surface.fill((100,100,255))
    def input(self):
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