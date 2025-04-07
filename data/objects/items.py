from ..config import *

class Item(pg.sprite.Sprite):
    type:str = 'item'
    
    name:str = "BaseItem"
    position:pg.math.Vector2 = pg.math.Vector2(0,0)
    rect:pg.rect.RectType
    world:object
    
    surface:pg.surface.SurfaceType
    
    animation:list[pg.surface.SurfaceType,]=[]
    _frame:float = 0
    
    started:float
    @property
    def frame(self, value:float=None) -> float:
        if value is not None:
            self._frame = value
        return self._frame
    @frame.setter
    def frame(self, value:float=None) -> float:
        self._frame = value
        if self._frame >= len(self.animation):
            self._frame = 0
        elif self._frame < 0:
            self._frame = 0
    def __init__(self, position:list[int,int],*groups):
        super().__init__(*groups)
        
        self.started = pge.delta_time.total_seconds()
        self.position = pg.math.Vector2(*position)
        
        self.surface = pg.Surface(Position((32,32))*RATIO)
        
        self.rect = self.surface.get_rect()
        
        if len(self.groups()) > 0:
            self.world:object = self.groups()[0]
        
        self.setup_animation()
        
    def setup_animation(self):
        pass
    
    def action(self):
        pass
    
    def animate(self):
        self.frame = self.frame+(0.5*(pge.getAvgFPS()/pge.fps)*GD.fps_ratio) % len(self.animation)
        self.surface = self.animation[int(self.frame)]
        if self.frame >= len(self.animation):
            self.frame = 0
    
    def draw(self):
        r = pg.rect.Rect(0,0, *Position((16,16))*RATIO)
        r.topleft = self.position.xy - self.world.offset
        self.world.surface.blit(self.surface, r)
        if CONFIG['debug']:
            pg.draw.rect(self.world.surface, self.world.debug_item_color, r, 1)
    
    def collide(self):
        if self.world.player.rect.colliderect(self.rect):
            self.action()
            if GAME_MUSIC_CHANNEL2.get_sound() != GAME_SFX_PICKUP:
                GAME_MUSIC_CHANNEL2.play(GAME_SFX_PICKUP)
            self.kill()
        else:
            if pge.delta_time.total_seconds()-self.started > 3.5:
                direction = (self.world.player.position - self.position)
                self.position += direction.normalize() * (self.world.player.speed*1.25)
            
    
    def update(self):
        self.rect.topleft = self.position
        self.collide()
        self.animate()
        
class ExpCrystal(Item):
    name:str = "Exp Crystal"
    
    def action(self):
        player = self.world.player
        needed:float = (player.level*100)
        player.experience += needed*(random.uniform(0.02,0.1) * player.luck) #random.randint(player.level * 5, player.level * 20) * player.luck
    
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