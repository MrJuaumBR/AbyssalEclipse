from ..config import *

def LoadFloor():
    floor_spritesheet = pge.createSpritesheet(GAME_PATH_TEXTURES + '/floors.png')
    floors_rects = {
        'red': (0, 0, 64, 64),
        'green': (64, 0, 64, 64),
        'blue': (128, 0, 64, 64),
        'yellow': (192, 0, 64, 64),
        'purple': (256, 0, 64, 64),
        'orange': (320, 0, 64, 64),
    }
    floor_width, floor_height = Position((64,64))*RATIO
    floor_surface = pge.createSurface(GD.screen[0] + floor_width, GD.screen[1] + floor_height)

    color:str = GAME_FLOOR_COLOR_OPTIONS[CONFIG['floor_color']]

    # Fill a surface with floor_img, for blit after
    for x in range(0, int(GD.screen[0]//floor_width)+2):
        for y in range(0, int(GD.screen[1]//floor_height)+1):
            floor_img = pg.transform.scale(floor_spritesheet.image_at(pg.Rect(*floors_rects[color]),0), (floor_width, floor_height))
            floor_surface.blit(floor_img, (x * floor_width, y * floor_height))
            
    return floor_surface, floor_width, floor_height



from .player import Player

class World(pg.sprite.Group):
    surface:pg.SurfaceType = None
    surface_size:tuple[int,int] = (0,0)
    offset:pg.math.Vector2 = pg.Vector2(0,0)

    player:Player = None
    def __init__(self):
        super().__init__()
        global floor_surface, floor_width, floor_height
        floor_surface, floor_width, floor_height = LoadFloor()
        
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
        """
        Draw the world including the floor and all sprites onto the screen.
        """
        # Get the main screen surface from the engine
        screen = pge.screen
        # Fill the screen with a dark blue color as the background
        screen.fill(pge.Colors.DARKBLUE.rgb)

        # Extract the current offset for drawing the floor and sprites
        offset = self.offset

        # Draw the floor tiles based on the current offset
        self.draw_floor(offset.x, offset.y)
        
        # Iterate through all sprites and draw them onto the screen
        for sprite in self.sprites():
            if sprite.type != 'player':  # Skip drawing the player sprite here
                sprite_rect = sprite.rect
                # Adjust the sprite position by the offset
                sprite_rect.topleft += offset
                # Blit the sprite onto the screen at the adjusted position
                screen.blit(sprite.surface, sprite_rect)

        # Get the rectangle of the screen and the world surface
        screen_rect = screen.get_rect()
        surface_rect = self.surface.get_rect()
        # Center the world surface on the screen
        surface_rect.center = screen_rect.center
        
        # Blit the world surface onto the screen at the centered position
        screen.blit(self.surface, surface_rect)
