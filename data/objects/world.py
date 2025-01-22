from ..config import *

def LoadFloor() -> tuple[pg.SurfaceType, int, int]:
    """
    Loads a Floor spritesheet and creates a surface with the size of the screen + the width and height of the floor sprite.
    The surface is filled with a pattern of floor sprites, with the color chosen from the configuration.
    
    Returns:
        tuple[pg.SurfaceType, int, int]: The surface, width and height of the floor sprite.
    """
    # Load the floor spritesheet
    floor_spritesheet = pge.createSpritesheet(GAME_PATH_TEXTURES + '/floors.png')
    
    # Define the colors and their respective positions in the spritesheet
    floors_rects = {
        'red': (0, 0, 64, 64),
        'green': (64, 0, 64, 64),
        'blue': (128, 0, 64, 64),
        'yellow': (192, 0, 64, 64),
        'purple': (256, 0, 64, 64),
        'orange': (320, 0, 64, 64),
    }
    
    # Calculate the width and height of the floor sprite
    floor_width, floor_height = Position((64,64))*RATIO
    
    # Create the surface to draw the floor on
    floor_surface = pge.createSurface(GD.screen[0] + floor_width, GD.screen[1] + floor_height)
    
    # Get the color chosen from the configuration
    color = GAME_FLOOR_COLOR_OPTIONS[CONFIG['floor_color']]
    
    # Fill a surface with floor_img, for blit after
    # Calculate the number of tiles needed to fill the screen
    x_tiles = int(GD.screen[0]/floor_width)+1
    y_tiles = int(GD.screen[1]/floor_height)+1
    
    # Fill the surface with the floor sprite
    for x in range(x_tiles):
        for y in range(y_tiles):
            floor_img = pg.transform.scale(floor_spritesheet.image_at(pg.Rect(*floors_rects[color]),0), (floor_width, floor_height))
            floor_surface.blit(floor_img, (x * floor_width, y * floor_height))
            
    return floor_surface, floor_width, floor_height



from .player import Player

class World(pg.sprite.Group):
    surface:pg.SurfaceType = None
    surface_size:tuple[int,int] = (0,0)
    offset:pg.math.Vector2

    player:Player = None
    
    projectiles:list[pg.sprite.Sprite,] = []
    def __init__(self):
        """
        Initialize the World object.
        
        This method sets up the initial state of the World, including loading the floor,
        setting up the surface, and initializing various attributes.
        """
        super().__init__()
        
        # Load the floor and its dimensions
        global floor_surface, floor_width, floor_height
        floor_surface, floor_width, floor_height = LoadFloor()
        
        # Initialize offset for floor movement
        self.offset: pg.math.Vector2 = pg.Vector2(0, 0)
        
        # List to store projectiles in the world
        self.projectiles: list[pg.sprite.Sprite,] = []
        
        # Create a transparent surface for the world
        self.surface = pg.Surface(GD.screen, pg.SRCALPHA)
        self.surface_size = self.surface.get_size()
        
        # Initialize the player within the world
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
    
    def draw_projectiles(self):
        for proj in self.projectiles:
            proj:pg.sprite.Sprite
            proj.draw(self)
            if CONFIG['debug']:
                pg.draw.line(self.surface, pge.Colors.RED.rgb, end_pos=proj.start_pos-self.offset, start_pos=proj.rect.center-self.offset, width=int(2*RATIO.med))
            
    def add_projectile(self, projectile:pg.sprite.Sprite):
        self.projectiles.append(projectile)
        self.add(projectile)
        
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
        self.surface.fill(pge.Colors.DARKBLUE.rgb)

        # Extract the current offset for drawing the floor and sprites
        offset = self.offset

        # Draw the floor tiles based on the current offset
        self.draw_floor(offset.x, offset.y)
        
        # Iterate through all sprites and draw them onto the screen
        for sprite in self.sprites():
            if sprite.type != 'player' and sprite.type != 'bullet':  # Skip drawing the player sprite here
                sprite_rect = sprite.rect
                # Adjust the sprite position by the offset
                sprite_rect.topleft += offset
                # Blit the sprite onto the screen at the adjusted position
                self.surface.blit(sprite.surface, sprite_rect)
                
        self.draw_projectiles()
        
        # Get the rectangle of the screen and the world surface
        screen_rect = screen.get_rect()
        surface_rect = self.surface.get_rect()
        # Center the world surface on the screen
        surface_rect.center = screen_rect.center
        
        # Blit the world surface onto the screen at the centered position
        screen.blit(self.surface, surface_rect)
