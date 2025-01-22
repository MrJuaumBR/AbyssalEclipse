from ..config import *

floor_img = pg.image.load(GAME_PATH_DATA + '/assets/textures/floor.png')
floor_width, floor_height = floor_img.get_width(), floor_img.get_height()
floor_surface = pg.Surface((GD.screen[0] + floor_width, GD.screen[1] + floor_height))

# Fill a surface with floor_img, for blit after
for x in range(0, int(GD.screen[0]//floor_width)+2):
    for y in range(0, int(GD.screen[1]//floor_height)+1):
        floor_surface.blit(floor_img, (x * floor_width, y * floor_height))



from .player import Player

class World(pg.sprite.Group):
    surface:pg.SurfaceType = None
    surface_size:tuple[int,int] = (0,0)
    offset:pg.math.Vector2 = pg.Vector2(0,0)

    player:Player = None
    def __init__(self):
        super().__init__()
        self.surface = pg.Surface(GD.screen,pg.SRCALPHA)
        self.surface_size = self.surface.get_size()
        
        self.player = Player(self)

        
    def draw_floor(self, offset_x, offset_y):
        """
        Draw the floor
        
        floor_surface will be blit into self.surface by using offset_x and offset_y for draw
        
        i want the floor to look like it is infinity
        """
        # Calculate the modulo of the offset to ensure it stays within the bounds of the floor surface
        mod_x = offset_x % floor_width
        mod_y = offset_y % floor_height

        # Draw the floor surface in a 2x2 grid to create the illusion of infinity
        self.surface.blit(floor_surface, (-mod_x, -mod_y))
        self.surface.blit(floor_surface, (-mod_x + floor_width, -mod_y))
        self.surface.blit(floor_surface, (-mod_x, -mod_y + floor_height))
        self.surface.blit(floor_surface, (-mod_x + floor_width, -mod_y + floor_height))
        
        
    def update(self):
        for sprite in self.sprites():
            sprite.update()
            
    def draw(self):
        screen = pge.screen
        screen.fill(pge.Colors.DARKBLUE.rgb)

        offset = self.offset

        self.draw_floor(offset.x, offset.y)
        for sprite in self.sprites():
            if sprite.type != 'player':
                sprite_rect = sprite.rect.move(offset)
                screen.blit(sprite.surface, sprite_rect)

        screen_rect = screen.get_rect()
        surface_rect = self.surface.get_rect()
        surface_rect.center = screen_rect.center
        
        screen.blit(self.surface, surface_rect)
