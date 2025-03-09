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

class Projectile(pg.sprite.Sprite):
    type:str = 'projectile'
    
    player:object
    surface:pg.SurfaceType
    
    damage:float = 10.0
    start_pos:pg.math.Vector2 = pg.math.Vector2(0,0)
    mouse_pos:pg.math.Vector2 = pg.math.Vector2(0,0)
    position:pg.math.Vector2 = pg.math.Vector2(0,0)
    rect:pg.Rect = pg.Rect(0,0,*(Position((16,16))*RATIO))
    start_time:datetime.timedelta = None
    lifetime:float = 10.0
    speed:float = 6.5
    hits:int = 1
    
    direction:pg.math.Vector2 = pg.math.Vector2(0,0)
    
    animation_frames:list[pg.SurfaceType,] = []
    frame:float = 0.0
    
    rep_color = (255,0,0)
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
        
        # Setup the weapon with the given attributes
        self.setup(attributes)
        
        self.position += self.player.world.offset
        
        # Set the time when the weapon was created
        self.start_time:datetime.timedelta = pge.delta_time.total_seconds()
        
        
    def setup(self, attributes:GAME_WEAPON_ATTRIBUTTES_TYPE):
        """
        Sets up the weapon with the given attributes.
        
        This function will set the direction of the weapon to the direction of the mouse from the start position of the weapon.
        It will also set the correct attributes of the weapon based on the given attributes.
        Lastly it will set up the spritesheet for the weapon.
        
        Args:
            attributes (GAME_WEAPON_ATTRIBUTTES_TYPE): The attributes of the weapon.
        """
        self.rep_color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
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
        self.frame = (self.frame+(0.3*(pge.getAvgFPS()/pge.fps)) * (60/pge.getAvgFPS())) % len(self.animation_frames)
        
        # Switch the animation frame by using the frame index as the index to the animation_frames list
        self.surface = self.animation_frames[int(self.frame)]
    
    def draw(self, world:object):
        """
        Draws the weapon on the screen.
        
        """
        # offset:pg.math.Vector2 = world.offset
        r = pg.rect.Rect(0,0, *Position((32,32))*RATIO)
        r.center = self.position.xy - world.offset
        world.surface.blit(self.surface, r)
        if CONFIG['debug']:
            pg.draw.rect(world.surface, self.rep_color, r, 1)
    
    def detect_collision(self):
        enemys:list[pg.sprite.Sprite,] = self.player.world.enemys
        
        my_rect:pg.rect.RectType = pg.Rect(*(self.position.copy() + self.player.world.offset),32,32)
        for enemy in enemys:
            e_rect:pg.rect.RectType = pg.Rect(*(enemy.position + self.player.world.offset),32,32)
            if my_rect.colliderect(e_rect): # Is colliding with this enemy?
                if self.hits > 0: # This projectile has hits left?
                    self.hits -= 1 # Remove a hit
                    if enemy.health > 0: # Is the enemy alive?
                        enemy.take_damage(self.damage)
                    
        if self.hits <= 0: # This projectile has no hits left?
            self.kill()
        
    
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
        
        self.detect_collision()

class Player(pg.sprite.Sprite):
    type:str = 'player'
    
    world:object
    surface:pg.SurfaceType
    rect:pg.rect.RectType
    
    maxHealth:float=100.0
    _health:float=100.0
    _level:int = 1
    _experience:float = 0.0
    resistance:float = 0.0
    luck:float = 1.0
    reload_time:float = 1.0
    last_reload_time:datetime.timedelta = pge.delta_time.total_seconds()
    last_damage_taken:float = 0
    
    money:int = 0
    
    speed:float = 5.0
    
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
    
    sprite_size:int = 64
    
    state:Literal['top','left','right','bottom','idle'] = 'idle'
    _frame:int = 0
    @property
    def frame(self, value:int=None) -> int:
        if value is not None:
            self._frame = value
        return self._frame
    
    @frame.setter
    def frame(self, value:int):
        self._frame = value
        if self._frame >= len(self.animations[self.state]):
            self._frame = len(self.animations[self.state]) - 1
        elif self._frame < 0:
            self._frame = 0
    
    @property
    def health(self, value:float=None) -> float:
        if value is not None:
            self._health = value
        return self._health
    
    @health.setter
    def health(self, value:float):
        h = self._health
        self._health = value
        if self._health < h:
            self.last_damage_taken = pge.delta_time.total_seconds()
        if self._health > self.maxHealth:
            self._health = self.maxHealth
        elif self._health < 0:
            self._health = 0
    
    position:pg.Vector2 = pg.Vector2(0,0)
    def __init__(self, world:pg.sprite.Group):
        """
        Creates a player sprite.
        
        It will be added to the given world group and will be initialized with the
        default values of the player class.
        """
        super().__init__(world)
        self.world = world
        self.surface = pge.createSurface(*Position((self.sprite_size,self.sprite_size))*RATIO)
        self.surface.fill((100,100,255))
        
        self.last_reload_time = pge.delta_time.total_seconds() # the time when the player last reloaded
        
        self.setup_animations() # sets up the animations for the player
        
        self.rect = self.surface.get_rect()
        
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
                s = pg.transform.scale(s, Position((self.sprite_size,self.sprite_size))*RATIO)
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
            # add the bullet to the world
            self.world.add_projectile(Projectile(self, center_of_screen=GAME_CENTER_OF_SCREEN))
            # update the last reload time
            self.last_reload_time = pge.delta_time.total_seconds()
        
    @property
    def experience(self, value:float=None) -> float:
        if value is not None:
            self._experience = value
        return self._experience
    
    @experience.setter
    def experience(self, value:float):
        self._experience = value
        if self._experience >= self._level * 100:
            self._experience -= self._level * 100
            self.level += 1
            
    @property
    def level(self, value:int=None) -> int:
        if value is not None:
            self._level = value
        return self._level
    
    @level.setter
    def level(self, value:int):
        if value > self._level:
            self._level = value
            self.world.level_up_function()
    
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
            
            # if pge.hasKeyPressed(K_LCTRL) and UP: self.experience += 5
            
            if UP: self.movement_vector.y -= self.speed
            elif DOWN: self.movement_vector.y += self.speed
            if LEFT: self.movement_vector.x -= self.speed
            elif RIGHT: self.movement_vector.x += self.speed
            
            
            
            # Reload TIme is time delta
            # Reload Time is stored in reload_time
            
        # Normalize vectors
        self.magnitude = math.sqrt(self.movement_vector.x**2 + self.movement_vector.y**2)
            
        if self.magnitude > 0: # Prevent division by zero    
            # Normalize the vector
            self.movement_vector.x /= self.magnitude
            self.movement_vector.y /= self.magnitude
            
            # Now you can scale the normalized vector by the desired speed
            # Movement Vector gonna be on center, but i need on topleft
            self.movement_vector.x *= self.speed
            self.movement_vector.y *= self.speed
            
        r = pg.Rect(0,0,*(Position((self.sprite_size,self.sprite_size))*RATIO))
        r.topleft = self.movement_vector + self.world.offset
        
        # Update world offset
        self.world.offset.xy = r.topleft
        
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
        self.state = (
            'left' if Vector_X < 0 else
            'right' if Vector_X > 0 else
            'top' if Vector_Y < 0 else
            'bottom' if Vector_Y > 0 else
            'idle'
        )
        
        # Update Current Frame
        # Animation Needs to be framerate independent also consideer player speed from register_speed['px/s']
        # self.frame = (self.frame + (min(0.1,self.magnitude*0.2) if self.state != 'idle' else 0.07) * (pge.getAvgFPS()/pge.fps)) % len(self.animations[self.state])
        self.frame = (self.frame+((0.3 if self.state != 'idle' else 0.07)*(pge.getAvgFPS()/pge.fps)) * (60/pge.getAvgFPS())) % len(self.animations[self.state])
        
        
        self.surface = self.animations[self.state][int(self.frame)]
    
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
    
    def take_damage(self, amount:float):
        self.health -= amount*(1-self.resistance)
        
    def heal(self, amount:float):
        self.health += amount
    def life_manager(self):
        if self.health < self.maxHealth:
            if pge.delta_time.total_seconds()-self.last_damage_taken > 3:
                self.last_damage_taken = pge.delta_time.total_seconds() - 2.9
                self.health += (self.health/self.maxHealth)*(60/pge.getAvgFPS())
    
    def update(self) -> None:
        """
        Updates the player object.

        This function will call the input function to update the player's movement vector,
        then call the animation update function to update the player's animation,
        and finally reset the player's movement vector to (0, 0).
        """
        self.input()
        self.animation_update()
        self.life_manager()
        # Reset the movement vector
        self.reset_vector()
        
        self.position = GAME_CENTER_OF_SCREEN+self.world.offset
        self.rect.topleft = self.position
        
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
