from ..config import *

class Item(pg.sprite.Sprite):
    type:str = 'item'
    
    name:str = "BaseItem"
    position:pg.math.Vector2 = pg.math.Vector2(0,0)
    rect:pg.rect.RectType
    world:object
    
    surface:pg.surface.SurfaceType
    
    animation:list[pg.surface.SurfaceType,]=[]
    frame:float = 0
    def __init__(self, position:list[int,int],*groups):
        super().__init__(*groups)
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
        self.frame = (self.frame + 0.5 * (pge.getAvgFPS()/pge.fps)) % len(self.animation)
        self.surface = self.animation[int(self.frame)]
    
    def draw(self):
        r = pg.rect.Rect(0,0, *Position((16,16))*RATIO)
        r.topleft = self.position.xy - self.world.offset
        self.world.surface.blit(self.surface, r)
        if CONFIG['debug']:
            pg.draw.rect(self.world.surface, self.world.debug_item_color, r, 1)
    
    def update(self):
        self.animate()
        
class ExpCrystal(Item):
    name:str = "Exp Crystal"
        
    def setup_animation(self):
        s = pge.createSpritesheet(GAME_PATH_TEXTURES+'/items.png')
        self.animation = []
        
        x = 0
        for _ in range(5):
            i = s.image_at(pg.Rect(x,32,32,32),0)
            i = pg.transform.scale(i, Position((16,16))*RATIO)
            self.animation.append(i)
            x += 32
            
class Coin(Item):
    name:str = "Coin"
        
    def setup_animation(self):
        s = pge.createSpritesheet(GAME_PATH_TEXTURES+'/items.png')
        self.animation = []
        
        x = 0
        for _ in range(5):
            i = s.image_at(pg.Rect(x,0,32,32),0)
            i = pg.transform.scale(i, Position((16,16))*RATIO)
            self.animation.append(i)
            x += 32