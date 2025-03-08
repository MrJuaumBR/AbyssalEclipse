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



from .player import Player, Projectile
from .enemy import _Enemy,NightmareImp, BloodyEye
from .items import Item,ExpCrystal,Coin
from .cards import Card

class World(pg.sprite.Group):
    surface:pg.SurfaceType = None
    surface_size:tuple[int,int] = (0,0)
    offset:pg.math.Vector2

    player:Player = None
    
    start_time:float = 0
    elapsed_time:float = 0
    
    enemy_to_be_spawned:int = 7
    enemy_multiplier:int = 1.3 # + 30%
    
    enemys:list[_Enemy,] = []
    projectiles:list[Projectile,] = []
    items:list[Item,] = []
    
    
    debug_proj_color:tuple[int,int,int] = (0,255,0)
    debug_enemy_color:tuple[int,int,int] = (255,0,0)
    debug_item_color:tuple[int,int,int] = (0,0,255)
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
        
        # Set the start time of the world
        self.start_time = pge.delta_time.total_seconds()
        
        self.particles = []
        
        for i in range(self.enemy_to_be_spawned):
            self.spawn_enemy()


    
    def clear_killed_sprites(self):
        s = self.sprites()
        for enemy in self.enemys:
            if not (enemy in s):
                self.enemys.remove(enemy)

        for projectile in self.projectiles:
            if not (projectile in s):
                self.projectiles.remove(projectile)
            
    
    def spawn_enemy(self):
        EnemyX:int = random.randint(GAME_ENEMY_SPAWN_RANGE[0], GAME_ENEMY_SPAWN_RANGE[1]) * random.choice([-1,1])
        EnemyY:int = random.randint(GAME_ENEMY_SPAWN_RANGE[0], GAME_ENEMY_SPAWN_RANGE[1]) * random.choice([-1,1])
        EnemyX += GAME_CENTER_OF_SCREEN[0]
        EnemyY += GAME_CENTER_OF_SCREEN[1]
        Enemy:_Enemy = random.choice([NightmareImp, BloodyEye])
        self.enemys.append(Enemy((EnemyX, EnemyY),1,self))
        
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
            proj:Projectile
            proj.draw(self)
            if CONFIG['debug']:
                # Connect Player and Projectile with a line
                pg.draw.line(self.surface, self.debug_proj_color, GAME_CENTER_OF_SCREEN, proj.rect.center-self.offset, int(2*RATIO.med))
                
    def draw_enemys(self):
        for enemy in self.enemys:
            enemy.draw()
            if CONFIG['debug']:
                # Connect Player and Enemy with a line
                pg.draw.line(self.surface, self.debug_enemy_color, GAME_CENTER_OF_SCREEN, enemy.rect.center-self.offset, int(2*RATIO.med))
    
    def draw_items(self):
        for item in self.items:
            item.draw()
            
    
    def add_projectile(self, projectile:pg.sprite.Sprite):
        self.projectiles.append(projectile)
        self.add(projectile)
    
    def add_item(self, position:pg.math.Vector2,itemName:Literal['ExpShard','Coin']='ExpShard'):
        if itemName == 'ExpShard':
            x = ExpCrystal(position,self)
            self.items.append(x)
            self.add(x)
        elif itemName == 'Coin':
            x = Coin(position,self)
            self.items.append(x)
            self.add(x)
    
    def update(self):
        self.clear_killed_sprites()
        self.elapsed_time = pge.delta_time.total_seconds() - self.start_time
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
        
        # Draw Player Rect in self.surface using offset
        if CONFIG['debug']:
            r = pg.Rect(0,0,*Position((64,64))*RATIO)
            r.center = GAME_CENTER_OF_SCREEN
            pg.draw.rect(self.surface, pge.Colors.RED.rgb,r, int(3*RATIO.med))
        
        self.draw_enemys()     
        self.draw_items()   
        self.draw_projectiles()
        
        # Get the rectangle of the screen and the world surface
        screen_rect = screen.get_rect()
        surface_rect = self.surface.get_rect()
        # Center the world surface on the screen
        surface_rect.center = screen_rect.center
        
        # Blit the world surface onto the screen at the centered position
        screen.blit(self.surface, surface_rect)
