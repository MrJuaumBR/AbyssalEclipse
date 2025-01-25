from ..config import *

from pygame.locals import *

Player_Frames_Positions = {
    'idle':[(0,0),(32,0),(64,0),(96,0),(128,0)],
    'top':[(0,32),(32,32),(64,32),(96,32),(128,32)],
    'left':[(0,64),(32,64),(64,64),(96,64),(128,64)],
    'bottom':[(0,96),(32,96),(64,96),(96,96),(128,96)],
    # 'right':[], => Just invert the left for right :)
}

Weapon_Frames_Positions = [
    (0,0),
    (32,0),
    (64,0),
    (96,0),
    (128,0)
]

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
    speed:float = 5.0
    hits:int = 1
    
    direction:pg.math.Vector2 = pg.math.Vector2(0,0)
    
    animation_frames:list[pg.SurfaceType,] = []
    frame:float = 0.0
    def __init__(self, player:object, attributes:GAME_WEAPON_ATTRIBUTTES_TYPE=GAME_DEFAULT_WEAPON_ATTRIBUTTES, center_of_screen:tuple[int,int]=(0,0)):
        """
        Creates a new weapon at the given position, with the given attributes and player.

        Args:
            player (object): The player that owns this weapon.
            attributes (GAME_WEAPON_ATTRIBUTTES_TYPE, optional): The attributes of the weapon. Defaults to GAME_DEFAULT_WEAPON_ATTRIBUTTES.
            center_of_screen (tuple[int,int], optional): The position of the weapon on the screen. Defaults to (0,0).
        """
        super().__init__()
        # print(f"Weapon Created at: {center_of_screen}, and is going to: {pge.mouse.pos}")
        self.player = player
        self.surface = pg.Surface(Position((16,16))*RATIO)
        
        # Set the start position of the weapon
        self.position = pg.math.Vector2(*center_of_screen)
        
        # Set the start position of the weapon
        self.start_pos = self.position
        # Set the position of the mouse
        self.mouse_pos = pg.math.Vector2(pge.mouse.pos)
        # Set the time when the weapon was created
        self.start_time:datetime.timedelta = pge.delta_time.total_seconds()
        
        
        # Setup the weapon with the given attributes
        self.setup(attributes)
        
    def setup(self, attributes:GAME_WEAPON_ATTRIBUTTES_TYPE):
        """
        Sets up the weapon with the given attributes.
        
        This function will set the direction of the weapon to the direction of the mouse from the start position of the weapon.
        It will also set the correct attributes of the weapon based on the given attributes.
        Lastly it will set up the spritesheet for the weapon.
        
        Args:
            attributes (GAME_WEAPON_ATTRIBUTTES_TYPE): The attributes of the weapon.
        """
        # Set the direction of the weapon to the direction of the mouse from the start position of the weapon
        self.direction = self.mouse_pos - self.start_pos
        
        # Create the spritesheet for the weapon
        ss = pge.createSpritesheet(GAME_PATH_TEXTURES+'/hatchet.png')
        
        # Set the correct attributes of the weapon based on the given attributes
        for key in attributes.keys():
            if key in self.__dict__.keys():
                self.__dict__[key] = attributes[key]
                
        # Add the sprites to the animation frames
        for frame in Weapon_Frames_Positions:
            s = ss.image_at(Rect(frame[0],frame[1],32,32),-1)
            s = pg.transform.scale(s, Position((32,32))*RATIO)
            self.animation_frames.append(s)
        
        # Normalize the direction of the weapon
        self.direction.normalize_ip()
    
    def animate(self):
        """
        Animates the weapon by switching between the sprites in the spritesheet.
        
        The animation is done by increasing the frame index by half the average framerate divided by the target framerate.
        The animation frames are then switched by using the frame index as the index to the animation_frames list.
        """
        # Framerate independant animation
        self.frame = (self.frame + 0.5 * (pge.getAvgFPS()/pge.fps)) % len(self.animation_frames)
        
        # Switch the animation frame by using the frame index as the index to the animation_frames list
        self.surface = self.animation_frames[int(self.frame)]
    
    def draw(self, world:object):
        """
        Draws the weapon on the screen.
        
        """
        offset:pg.math.Vector2 = world.offset
        world.surface.blit(self.surface, self.position - offset)
    
    def update(self):
        """
        Updates the weapon by animating it and by checking if its lifetime has expired.
        
        If the lifetime of the weapon has expired it will be removed from the projectiles list and it will be killed.
        
        The position of the weapon is updated by adding the direction of the weapon multiplied by the speed of the weapon and the medium ratio to the current position of the weapon.
        The center of the rect is then updated to the new position of the weapon.
        """
        self.animate()
        # Check if the lifetime of the weapon has expired
        if self.start_time + self.lifetime < pge.delta_time.total_seconds():
            # Remove the weapon from the projectiles list
            self.player.world.projectiles.remove(self)
            # Kill the weapon
            self.kill()
        
        # Update the position of the weapon
        self.position += (self.direction * self.speed)
        
        # Update the center of the rect to the new position of the weapon
        self.rect.center = self.position.xy

class Player(pg.sprite.Sprite):
    type:str = 'player'
    
    world:object
    surface:pg.SurfaceType
    
    maxHealth:float=100.0
    health:float=100.0
    level:int = 1
    experience:float = 0.0
    reload_time:float = 1.0
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
        """
        Creates a player sprite.
        
        It will be added to the given world group and will be initialized with the
        default values of the player class.
        """
        super().__init__(world)
        self.world = world
        self.surface = pge.createSurface(*Position((64,64))*RATIO)
        self.surface.fill((100,100,255))
        
        self.max_speed = self.speed*100 # the maximum speed in px/s
        
        self.last_reload_time = pge.delta_time.total_seconds() # the time when the player last reloaded
        
        self.setup_animations() # sets up the animations for the player
        
    def setup_animations(self) -> None:
        """
        Sets up the animations for the player.

        It will load all the possible animations for the player and will store them in the
        animations dict.

        The animations are loaded from a spritesheet and are stored in the animations dict.
        The key of the dict is the name of the animation and the value is a list of frames that
        represent the animation.

        The frames are loaded from the spritesheet and are resized to fit the size of the player.
        The frames are also flipped horizontally if the animation is for the right direction.

        The animations are stored in the following order:

        - top
        - left
        - right
        - bottom
        - idle
        """
        # load the spritesheet
        ss = pge.createSpritesheet(GAME_PATH_TEXTURES+'/player.png')
        # loop through all the animations and load their frames
        for key in ['top','left','right','bottom','idle']:
            self.animations[key] = []
            for frame in Player_Frames_Positions[(key if key != 'right' else 'left')]:
                # get the frame from the spritesheet
                s = ss.image_at(Rect(frame[0],frame[1],32,32),255)
                # resize the frame to fit the size of the player
                s = pg.transform.scale(s, Position((64,64))*RATIO)
                # flip the frame horizontally if the animation is for the right direction
                if key == 'right':
                    s = pg.transform.flip(s, True, False)
                # add the frame to the list of frames for the animation
                self.animations[key].append(s)

    def shoot(self) -> None:
        """
        Shoots a bullet from the player to the mouse position.

        This method is called when the player is shooting and the player is not
        reloading.

        It will create a new bullet at the current position of the player and
        will add it to the world.

        :return: None
        """
        if pge.mouse.left and pge.delta_time.total_seconds()-self.last_reload_time > self.reload_time:
            # get the center of the screen
            # create a new bullet at the current position of the player
            w = Weapon(self, center_of_screen=GAME_CENTER_OF_SCREEN)
            # add the bullet to the world
            self.world.add_projectile(w)
            # update the last reload time
            self.last_reload_time = pge.delta_time.total_seconds()
        
        
    
    def input(self):
        """
        This method is called every frame and is responsible for
        handling the player input.
        
        It will detect if the player is using a controller or not.
        If the player is using a controller, it will get the axis
        values of the left analog stick and add them to the player's
        movement vector. If the player is not using a controller,
        it will check if the player is pressing the arrow keys or
        the WASD keys and add the corresponding direction to the
        player's movement vector.
        
        The player's movement vector is then normalized to prevent
        the player from moving too fast.
        
        The player's position is then updated by adding the normalized
        movement vector to the player's current position.
        
        The player's speed is also updated by setting the speed
        attribute to the length of the normalized movement vector.
        """
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
            self.shoot()
            
            if UP: self.movement_vector.y -= self.speed
            elif DOWN: self.movement_vector.y += self.speed
            if LEFT: self.movement_vector.x -= self.speed
            elif RIGHT: self.movement_vector.x += self.speed
            
            # Reload TIme is time delta
            # Reload Time is stored in reload_time
            
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
        """
        Updates the player's animation.

        Detects the current state of the player (left, right, top, bottom, idle)
        and updates the current frame of the animation accordingly.
        """
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
        self.current_frame = (self.current_frame + 0.2 * (pge.getAvgFPS()/pge.fps)) % len(self.animations[self.current_state])
        
        self.surface = self.animations[self.current_state][int(self.current_frame)]
    
    def reset_vector(self) -> None:
        """
        Resets the player's movement vector to (0, 0).

        This is used to reset the player's movement when the player releases all
        movement keys.
        """
        self.movement_vector.x = 0
        self.movement_vector.y = 0

    def get_speed(self, measure_type: Literal['px/s', 'm/s', 'km/h', 'mph'] = 'px/s', mov_vector: pg.Vector2 = None) -> float:
        """
        Returns the speed of the player in the given measure type.

        Args:
            measure_type (str, optional): The unit of measurement to use. Defaults to 'px/s'.
            mov_vector (pg.Vector2, optional): The movement vector to use. Defaults to the player's current movement vector.

        Returns:
            float: The speed of the player in the given measure type.

        Raises:
            ValueError: If the measure type is not one of the options.
        """
        if measure_type not in ["px/s", "m/s", "km/h", "mph"]:
            raise ValueError(
                "Invalid measure type. Use one of these options:\n'"
                "px/s', 'm/s', 'km/h', 'mph'."
            )

        # Get the actual speed of the player in pixels per second
        actual_speed = (mov_vector or self.movement_vector).length() * int(pge.getAvgFPS())

        # Convert the speed to the desired unit of measurement
        conversion_factors = {'px/s': 1, 'm/s': 0.01, 'km/h': 0.036, 'mph': 0.0223694}
        return actual_speed * conversion_factors.get(measure_type, 1)
    
    def update(self) -> None:
        """
        Updates the player object.

        This function will call the input function to update the player's movement vector,
        then call the animation update function to update the player's animation,
        and finally reset the player's movement vector to (0, 0).
        """
        self.input()
        self.animation_update()
        self.reset_vector()
        
    def draw(self):
        """
        Draw the player's surface centered on the screen.

        If debug mode is enabled, additional debug information is displayed.
        """
        if self.surface:
            # Get the rectangle for the player's surface centered on the screen
            rect = self.surface.get_rect(center=pge.screen.get_rect().center)

            # Blit the player's surface onto the screen at the calculated rectangle position
            pge.screen.blit(self.surface, rect)

            if CONFIG['debug']:
                # Debug: Draw a line from the player's center to the mouse position
                if pge.mouse.pos:
                    mouse_pos = (pge.mouse.pos[0] + 5, pge.mouse.pos[1] + 5)
                    pg.draw.line(pge.screen, pge.Colors.LIGHTGREEN.rgb, rect.center, mouse_pos, int(1 * RATIO.med))
