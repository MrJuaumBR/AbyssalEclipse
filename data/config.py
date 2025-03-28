# Imports
import pygameengine, os, random, datetime, JPyDB, typing, threading, sys, math, json
from pygameengine import pg
import pygameengine.widgets as pw
from pygameengine.objects import spritesheet
from pygameengine.objects import color as reqColor
from typing import Literal



GAME:dict = {
    'version':'0.0.1',
    'name':'Abyssal Eclipse',
    'game_news':b'aHR0cHM6Ly9tcmp1YXVtYnIuZ2l0aHViLmlvL2RhdGFiYXNlL2RhdGEvbmV3cy1hYnlzc2FsZWNsaXBzZS5qc29u'
}




# Paths
GAME_PATH_ROOT = './'
GAME_PATH_DATA = os.path.join(GAME_PATH_ROOT,'data')
GAME_PATH_SCREENS = os.path.join(GAME_PATH_DATA,'screens')
GAME_PATH_ASSETS = os.path.join(GAME_PATH_DATA,'assets')
GAME_PATH_LICENSES = os.path.join(GAME_PATH_ASSETS,'licenses')
GAME_PATH_FONTS = os.path.join(GAME_PATH_ASSETS,'fonts')
GAME_PATH_TEXTURES = os.path.join(GAME_PATH_ASSETS,'textures')
GAME_PATH_SOUNDS = os.path.join(GAME_PATH_ASSETS,'sounds')

# Fonts Paths
    # Rubik Italic, Rubik, Rubik Glitch
FONT_RUBIK_ITALIC = os.path.join(GAME_PATH_FONTS,'Rubik-Italic.ttf')
FONT_RUBIK = os.path.join(GAME_PATH_FONTS,'Rubik.ttf')
FONT_RUBIK_GLITCH = os.path.join(GAME_PATH_FONTS,'RubikGlitch.ttf')
    # Tiny5
FONT_TINY5 = os.path.join(GAME_PATH_FONTS,'Tiny5.ttf')
    # PixelifySans
FONT_PIXELIFYSANS = os.path.join(GAME_PATH_FONTS,'PixelifySans.ttf')









# Config
GAME_FPS_OPTIONS = [
    30,
    60,
    90,
    120
]

GAME_WINDOW_RESOLUTION_OPTIONS = [
    (640,480),
    (800,600),
    (1024,720),
    (1280,768),
    (1366,768),
    (1600,900),
    (1920,1080)
]

GAME_TRAIL_COLOR_OPTIONS = [
    (200,100,100), # Red
    (100,200,100), # Green
    (100,100,200), # Blue
    (200,200,100), # Yellow
    (200,100,200), # Purple
    (200,200,200), # White
    "Random"
]

GAME_SPEED_MEASURE_OPTIONS = [
    'px/s',
    'm/s',
    'km/h',
    'mph'
]

GAME_FLOOR_COLOR_OPTIONS = [
    'red',
    'green',
    'blue',
    'yellow',
    'purple',
    'orange'
]
GAME_LANGUAGE_OPTIONS = [
    'en-us',
    'pt-br'
]

# Game Difficulty

GAME_DIFFICULTY = {
    'easy':{
        'enemy_life':0.95,
        'enemy_speed':0.95,
        'enemy_damage':0.95,
        'start_enemy':7,
        'increase_enemy':4,
        'exp_drop_bonus':1,
    },
    'normal':{
        'enemy_life':1,
        'enemy_speed':1,
        'enemy_damage':1,
        'start_enemy':9,
        'increase_enemy':5,
        'exp_drop':1.025,
    },
    'hard':{
        'enemy_life':1.05,
        'enemy_speed':1.05,
        'enemy_damage':1.05,
        'start_enemy':11,
        'increase_enemy':6,
        'exp_drop':1.075,
    },
}

class GAME_DEFAULT_CFG_TYPE(typing.TypedDict):
    fullscreen:bool
    window_resolution:int
    fps:int
    show_fps:bool
    dynamic_fps:bool
    dynamic_mouse_wheel:bool
    debug:bool
    speed_measure:int
    vsync:bool
    mouse_trail:bool
    trail_color:int
    floor_color:int
    volume:float
    lang:Literal['en-us','pt-br']

GAME_DEFAULT_CFG:GAME_DEFAULT_CFG_TYPE = {
    "fullscreen":True,
    "window_resolution":1,
    "fps":1,
    "show_fps":False,
    "dynamic_fps":True,
    "dynamic_mouse_wheel":True,
    "debug":False,
    "vsync":False,
    "mouse_trail":True,
    "trail_color":1,
    'speed_measure':0,
    'floor_color':0,
    'volume':0.8,
    'lang':'en-us'
}

class GAME_WEAPON_ATTRIBUTTES_TYPE(typing.TypedDict):
    damage:float
    speed:float
    lifetime:float
    hits:int

GAME_DEFAULT_WEAPON_ATTRIBUTTES:GAME_WEAPON_ATTRIBUTTES_TYPE = {
    "damage":5.0,
    "speed":5.0,
    "lifetime":1.0,
    "hits":1
}

CONFIG:GAME_DEFAULT_CFG_TYPE = GAME_DEFAULT_CFG



# Game Engine
pge = pygameengine.PyGameEngine()
CURRENT_WINDOW_SIZE = pg.display.Info()


# Setup Database
pyd = JPyDB.pyDatabase(f"{GAME_PATH_DATA}/data",'pydb')
db = pyd.database

if not ('config' in db.tables.keys()):
    db.create_table('config', [('data',dict)])
    nearest_resolution = min(GAME_WINDOW_RESOLUTION_OPTIONS, key=lambda x: abs(x[0] - CURRENT_WINDOW_SIZE.current_w) + abs(x[1] - CURRENT_WINDOW_SIZE.current_h))
    nearest_resolution = GAME_WINDOW_RESOLUTION_OPTIONS.index(nearest_resolution)
    GAME_DEFAULT_CFG['window_resolution'] = nearest_resolution
    db.add_value('config','data',0,GAME_DEFAULT_CFG)
else:
    CONFIG = db.get_value('config','data',0)
    
if not ('leaderboard' in db.tables.keys()):
    db.create_table('leaderboard', [('data',dict)])
    db.add_value('leaderboard','data',0,{})

# Update CURRENT_WINDOW_SIZE
CURRENT_WINDOW_SIZE:tuple[int,int] = GAME_WINDOW_RESOLUTION_OPTIONS[CONFIG['window_resolution']]

# Game Handling
class _GameData:
    _current_screen = 0x0
    _old_cs = 0x0
    screen = GAME_WINDOW_RESOLUTION_OPTIONS[CONFIG['window_resolution']]
    fps = GAME_FPS_OPTIONS[CONFIG['fps']]
    username:str = f'User{random.randint(10000,99999)}'
    difficulty:str = 'normal'
    taskquery:list[object,] = []
    fps_ratio:float = 1.0
    def new_task(self, task:object, args:tuple[object,] = ()): self.taskquery.append((task, args))



    
GD = _GameData()


GAME_SCREEN = pge.createScreen(*GD.screen, pg.FULLSCREEN|pg.SCALED if CONFIG['fullscreen'] else pg.HWSURFACE,VSync=CONFIG['vsync'])
pge.setScreenTitle(GAME['name'])
pge.setScreenIcon(pge.loadImage(f"{GAME_PATH_TEXTURES}/icon.png"))

GAME_MENU_BACKGROUND = pg.transform.scale(pge.loadImage(f"{GAME_PATH_TEXTURES}/menubg.png"), GD.screen)
GAME_MENU_BACKGROUND.set_alpha(80)

def BackgroundThread():
    c = pg.time.Clock()
    print(f'Thread started pid: ({os.getpid()})')
    while pge.is_running:
        for (task, args) in GD.taskquery:
            if callable(task):
                try:
                    task(*args)
                    GD.taskquery.remove((task, args))
                except Exception as e:
                    print(f'Error in thread: {e}')
        c.tick(int(GD.fps-1))

_BackgroundThread = threading.Thread(target=BackgroundThread,name='BackgroundThread')
_BackgroundThread.start()

    
# Fast Fix for new Config
for key in GAME_DEFAULT_CFG.keys():
    if key not in CONFIG.keys():
        CONFIG[key] = GAME_DEFAULT_CFG[key]
        
db.save()

DEFAULT_WINDOW_SIZE = (800,600) # Default screen size is 800x600
RATIO_WIDTH = CURRENT_WINDOW_SIZE[0] / DEFAULT_WINDOW_SIZE[0]
RATIO_HEIGHT = CURRENT_WINDOW_SIZE[1] / DEFAULT_WINDOW_SIZE[1]
SRATIO = (RATIO_WIDTH, RATIO_HEIGHT) 



# Activate Controller Support
pge.setMouseEmulation(True)

class RatioType():
    def __init__(self, ratio_vector:tuple[int,int]) -> None:
        self.ratio_vector = ratio_vector
        self.x,self.y = ratio_vector
        self.med = (self.x + self.y) / 2
        
RATIO = RatioType(SRATIO)

GAME_CENTER_OF_SCREEN:tuple[int,int] = GAME_SCREEN.get_rect().center
GAME_ENEMY_SPAWN_RANGE:tuple[int,int] = (256,768)

# Music
Music = pg.mixer.music
Music.load(f"{GAME_PATH_SOUNDS}/music.mp3")

# Colors

COLOR_LIGHT_GREEN = reqColor(100,190,100)
COLOR_DARK_GREEN = reqColor(50,150,50)
COLOR_LIGHT_BLUE = reqColor(100,100,190)
COLOR_DARK_BLUE = reqColor(50,50,150)
COLOR_LIGHT_RED = reqColor(190,100,100)
COLOR_DARK_RED = reqColor(150,50,50)
COLOR_LIGHT_YELLOW = reqColor(190,190,100)
COLOR_DARK_YELLOW = reqColor(150,150,50)
COLOR_WHITE = reqColor(255,255,255)
COLOR_DARK_ALMOND = reqColor(180, 163, 146)

COLOR_DARK_BACKGROUND = reqColor(25,25,25)
COLOR_LIGHT_BACKGROUND = reqColor(150,150,150)
COLOR_DARK_BORDER = reqColor(75,75,75)
COLOR_LIGHT_BORDER = reqColor(200,200,200)
COLOR_LIGHT_REJECT = reqColor(255,170,190)
COLOR_REJECT = reqColor(255,0,0)
COLOR_LIGHT_ACCEPT = reqColor(190,255,170)

COLOR_DARK_UNACTIVE = reqColor(50,50,50)
COLOR_DARK_ACTIVE = reqColor(75,120,80)

COLOR_DISCORD_BLUE = reqColor(88,101,242)


COLOR_EXPLOSION_RED = reqColor(255,0,0)
COLOR_EXPLOSION_DARKRED = reqColor(150,0,0)
COLOR_EXPLOSION_YELLOW = reqColor(255,255,0)
COLOR_EXPLOSION_DARKYELLOW = reqColor(150,150,0)
COLOR_EXPLOSION_ORANGE = reqColor(255,128,0)
COLOR_EXPLOSION_DARKORANGE = reqColor(150,75,0)


pge.cfgtips.background_color = COLOR_LIGHT_BACKGROUND
pge.cfgtips.border_color = COLOR_DARK_BORDER
pge.cfgtips.text_color = pge.Colors.BLACK
pge.setFPS(GAME_FPS_OPTIONS[CONFIG['fps']])
pge.enableFPS_unstable(CONFIG['dynamic_fps'])
pge.mouse.mouse_trail_enabled = CONFIG['mouse_trail']
if GAME_TRAIL_COLOR_OPTIONS[CONFIG['trail_color']] == 'Random':
    pge.mouse.trail_node_random_color = True
else:
    pge.mouse.trail_node_color = GAME_TRAIL_COLOR_OPTIONS[CONFIG['trail_color']]
pge.widget_limits = 50


# Fonts
# All the fonts are from 8 to 36px
    # Rubik Italic(RBI), Rubik(RB), Rubik Glitch(RBG)
RBI8 = pge.createFont(FONT_RUBIK_ITALIC, int(8*RATIO.med))
RB8 = pge.createFont(FONT_RUBIK, int(8*RATIO.med))
RBG8 = pge.createFont(FONT_RUBIK_GLITCH, int(8*RATIO.med))
RBI10 = pge.createFont(FONT_RUBIK_ITALIC, int(10*RATIO.med))
RB10 = pge.createFont(FONT_RUBIK, int(10*RATIO.med))
RBG10 = pge.createFont(FONT_RUBIK_GLITCH, int(10*RATIO.med))
RBI12 = pge.createFont(FONT_RUBIK_ITALIC, int(12*RATIO.med))
RB12 = pge.createFont(FONT_RUBIK, int(12*RATIO.med))
RBG12 = pge.createFont(FONT_RUBIK_GLITCH, int(12*RATIO.med))
RBI14 = pge.createFont(FONT_RUBIK_ITALIC, int(14*RATIO.med))
RB14 = pge.createFont(FONT_RUBIK, int(14*RATIO.med))
RBG14 = pge.createFont(FONT_RUBIK_GLITCH, int(14*RATIO.med))
RBI16 = pge.createFont(FONT_RUBIK_ITALIC, int(16*RATIO.med))
RB16 = pge.createFont(FONT_RUBIK, int(16*RATIO.med))
RBG16 = pge.createFont(FONT_RUBIK_GLITCH, int(16*RATIO.med))
RBI18 = pge.createFont(FONT_RUBIK_ITALIC, int(18*RATIO.med))
RB18 = pge.createFont(FONT_RUBIK, int(18*RATIO.med))
RBG18 = pge.createFont(FONT_RUBIK_GLITCH, int(18*RATIO.med))
RBI20 = pge.createFont(FONT_RUBIK_ITALIC, int(20*RATIO.med))
RB20 = pge.createFont(FONT_RUBIK, int(20*RATIO.med))
RBG20 = pge.createFont(FONT_RUBIK_GLITCH, int(20*RATIO.med))
RBI22 = pge.createFont(FONT_RUBIK_ITALIC, int(22*RATIO.med))
RB22 = pge.createFont(FONT_RUBIK, int(22*RATIO.med))
RBG22 = pge.createFont(FONT_RUBIK_GLITCH, int(22*RATIO.med))
RBI24 = pge.createFont(FONT_RUBIK_ITALIC, int(24*RATIO.med))
RB24 = pge.createFont(FONT_RUBIK, int(24*RATIO.med))
RBG24 = pge.createFont(FONT_RUBIK_GLITCH, int(24*RATIO.med))
RBI26 = pge.createFont(FONT_RUBIK_ITALIC, int(26*RATIO.med))
RB26 = pge.createFont(FONT_RUBIK, int(26*RATIO.med))
RBG26 = pge.createFont(FONT_RUBIK_GLITCH, int(26*RATIO.med))
RBI28 = pge.createFont(FONT_RUBIK_ITALIC, int(28*RATIO.med))
RB28 = pge.createFont(FONT_RUBIK, int(28*RATIO.med))
RBG28 = pge.createFont(FONT_RUBIK_GLITCH, int(28*RATIO.med))
RBI30 = pge.createFont(FONT_RUBIK_ITALIC, int(30*RATIO.med))
RB30 = pge.createFont(FONT_RUBIK, int(30*RATIO.med))
RBG30 = pge.createFont(FONT_RUBIK_GLITCH, int(30*RATIO.med))
RBI32 = pge.createFont(FONT_RUBIK_ITALIC, int(32*RATIO.med))
RB32 = pge.createFont(FONT_RUBIK, int(32*RATIO.med))
RBG32 = pge.createFont(FONT_RUBIK_GLITCH, int(32*RATIO.med))
RBI36 = pge.createFont(FONT_RUBIK_ITALIC, int(36*RATIO.med))
RB36 = pge.createFont(FONT_RUBIK, int(36*RATIO.med))
RBG36 = pge.createFont(FONT_RUBIK_GLITCH, int(36*RATIO.med))

RBG50 = pge.createFont(FONT_RUBIK_GLITCH, int(50*RATIO.med))
RBG52 = pge.createFont(FONT_RUBIK_GLITCH, int(52*RATIO.med))

    # Tiny5(T5)
T5_8 = pge.createFont(FONT_TINY5, int(8*RATIO.med))
T5_10 = pge.createFont(FONT_TINY5, int(10*RATIO.med))
T5_12 = pge.createFont(FONT_TINY5, int(12*RATIO.med))
T5_14 = pge.createFont(FONT_TINY5, int(14*RATIO.med))
T5_16 = pge.createFont(FONT_TINY5, int(16*RATIO.med))
T5_18 = pge.createFont(FONT_TINY5, int(18*RATIO.med))
T5_20 = pge.createFont(FONT_TINY5, int(20*RATIO.med))
T5_22 = pge.createFont(FONT_TINY5, int(22*RATIO.med))
T5_24 = pge.createFont(FONT_TINY5, int(24*RATIO.med))
T5_26 = pge.createFont(FONT_TINY5, int(26*RATIO.med))
T5_28 = pge.createFont(FONT_TINY5, int(28*RATIO.med))
T5_30 = pge.createFont(FONT_TINY5, int(30*RATIO.med))
T5_32 = pge.createFont(FONT_TINY5, int(32*RATIO.med))
T5_36 = pge.createFont(FONT_TINY5, int(36*RATIO.med))
    # PixelifySans(PS)
PS8 = pge.createFont(FONT_PIXELIFYSANS, int(8*RATIO.med))
PS10 = pge.createFont(FONT_PIXELIFYSANS, int(10*RATIO.med))
PS12 = pge.createFont(FONT_PIXELIFYSANS, int(12*RATIO.med))
PS14 = pge.createFont(FONT_PIXELIFYSANS, int(14*RATIO.med))
PS16 = pge.createFont(FONT_PIXELIFYSANS, int(16*RATIO.med))
PS18 = pge.createFont(FONT_PIXELIFYSANS, int(18*RATIO.med))
PS20 = pge.createFont(FONT_PIXELIFYSANS, int(20*RATIO.med))
PS22 = pge.createFont(FONT_PIXELIFYSANS, int(22*RATIO.med))
PS24 = pge.createFont(FONT_PIXELIFYSANS, int(24*RATIO.med))
PS26 = pge.createFont(FONT_PIXELIFYSANS, int(26*RATIO.med))
PS28 = pge.createFont(FONT_PIXELIFYSANS, int(28*RATIO.med))
PS30 = pge.createFont(FONT_PIXELIFYSANS, int(30*RATIO.med))
PS32 = pge.createFont(FONT_PIXELIFYSANS, int(32*RATIO.med))
PS36 = pge.createFont(FONT_PIXELIFYSANS, int(36*RATIO.med))

# Objects
class Position(tuple):
    """
    Position Object Based on Tuple
    
    Adds a way to multiply tuples
    """
    x:int
    y:int
    def __init__(self, xy:tuple[int,int], *args, **kwargs):
        super().__init__()
        self.x,self.y = xy
    
    def __mul__(self, other):
        if isinstance(other, (tuple, list, Position)):
            return tuple(x * y for x, y in zip(self, other))
        elif isinstance(other, (int, float)):
            return tuple(x * other for x in self)
        elif isinstance(other, RatioType):
            return tuple(x * y for x, y in zip(self, other.ratio_vector))
        
    

# Testing
# print(Position((1,2)) * 2)
# print(Position((2,2)) * (3,3))
# print(Position((2,2)) * Position((2,2)))

# Screen Handler
class Screen(object):
    """
    # Base Screen object.
    """
    id:int = 0x0
    widgets:list[pw.Widget,] = []
    disable_widget:bool = False
    blacklist:list[int,] = [0x0,0x4]
    SCH:object
    def __init__(self,SCH) -> None:
        """
        # Initializes the screen
        
        Here will go:
        * Initialize widgets;
        * Add widgets to the screen;
        * Defines required variables;
        * ...
        """
        self.SCH = SCH
        pass
    def draw(self):
        """
        # Draw the screen
        
        This function will have all necessaire things that needs to be draw
        """
        pass
    
    def exiting(self):
        """
        # Contains exiting functions
        
        Like:
        * Save data;
        * ...
        """
        pass
    
    def _update(self):
        """
        # Contains update functions
        
        This function will have all necessaire things that needs to be updated like:
        * Back Button 4;
        * Escape Key;
        * ...
        """
        if not (GD._current_screen in self.blacklist):
            if pge.mouse.button_4 or pge.hasKeyPressed(pg.K_ESCAPE) or (pge.joystick.main and pge.joystick.main.getButtonByString("b")):
                self.SCH.changeScreen(GD._old_cs)
                self.exiting()
        GD.new_task(self.SCH.updateWidgets, (self,))# Fix for glitch
                

def LoadNews() -> str:
    """
    A new is:
    {
        "news": [
            {
                "title": "Title of the news",
                "date": "Date of the news", # YYYY/MM/DD
                "content": "Content of the news"
            }
        ]
    }
    """
    import base64, urllib.request, json
    url = base64.b64decode(GAME['game_news']).decode('utf-8')
    with urllib.request.urlopen(url) as response:
        data:dict = response.read().decode()
    data = json.loads(data)['news']
    
    # Sort the news by date
    data.sort(key=lambda x: x['date'], reverse=True)
    
    news:str = '+++++ NEWS +++++\n\n'
    
    
    for new in data:
        news += f"--------------------------------------------\n:: {new['title']} ::\n> Posted in: {new['date']}\n\n{new['content']}\n--------------------------------------------\n"
    return news

class TranslationSystem:
    lang:str = 'en-us'
    
    aliases:dict = {
        'en-us':['english', 'en'],
        'pt-br':['portuguese', 'pt'],
    }
    
    files:dict = {}
    def __init__(self, lang: str = Literal['en-us','pt-br']) -> None:
        for dir in os.listdir(GAME_PATH_ASSETS + '/translation/'):
            self.files[str(dir.split('.')[0])] = (json.loads(open(GAME_PATH_ASSETS + '/translation/' + dir, 'rb').read()))
        self.lang = str(lang).lower()
        
    def translate(self, text_id:any, language:str=None) -> str:
        if language is None: language = self.lang
        try:
            return str(self.files[str(language).lower()][str(text_id)])
        except:
            return self.translate(text_id, 'en-us')
        return 'Not Found Translation'
    
    def translate_list(self, list_id:any, language:str=None) -> list[str,]:
        if language is None: language = self.lang
        try:
            return list(self.files[str(language).lower()][str(list_id)])
        except:
            return self.translate_list(list_id, 'en-us')
        return ['Not Found Translation']
        
LGS = TranslationSystem(CONFIG['lang'])

DEBUG_CreateScoreButton = pw.Button(pge, Position((20,50))*RATIO, PS16, "Create Score", [COLOR_DARK_GREEN, pge.Colors.ALMOND])
DEBUG_ClearScoreButton = pw.Button(pge, Position((20,80))*RATIO, PS16, "Clear Score", [COLOR_DARK_GREEN, pge.Colors.ALMOND])

DEBUG_WIDGETS:list[pw.Widget,] = [
    DEBUG_CreateScoreButton,
    DEBUG_ClearScoreButton
]


from . import mainmenu, options, leaderboard, licenses, game, credits

SCREEN_IDS = {
    0x0: mainmenu.Main_Menu,
    0x1: options.Options,
    0x2: leaderboard.Leaderboard,
    0x3: licenses.Licenses,
    0x4: game.Game,
    0x5: credits.Credits
}
class ScreenHandler(object):    
    SCREENS_RELATIONS:list[Screen,] = []
    _current_screen:int = None
    screen:Screen = None
    debug_menu:bool = False
    
    wait_debug_menu_open:int = 0
    reset_when_change_screen:list[int,] = [0x4,]
    def __init__(self) -> None:
        
        self.SCREENS_RELATIONS.append(mainmenu.Main_Menu(self))
        self.SCREENS_RELATIONS.append(options.Options(self))
        self.SCREENS_RELATIONS.append(leaderboard.Leaderboard(self))
        self.SCREENS_RELATIONS.append(licenses.Licenses(self))
        self.SCREENS_RELATIONS.append(game.Game(self))
        self.SCREENS_RELATIONS.append(credits.Credits(self))
        
        self.current_screen = 0x0
        self.disableAutoUpdate()
        
    def disableAutoUpdate(self):
        sc = self.SCREENS_RELATIONS
        for screen in sc:
            for wd in screen.widgets:
                wd:pw.Widget
                wd._UpdateWhenDraw = False
    
    def updateWidgets(self, screen:Screen):
        for wd in screen.widgets:
            wd:pw.Widget
            wd.update()
    
    @property
    def current_screen(self):
        return self._current_screen
    
    @current_screen.setter
    def current_screen(self, value:int):
        GD._old_cs = self._current_screen
        GD._current_screen = value
        self._current_screen = value
        self.screen = self.findScreen(value)
    
    def exiting(self):
        if self.screen != None:
            self.screen.exiting()

    def changeScreen(self, screen_id:int):
        """
        This function is used to change the screens
        """
        screen = self.findScreen(screen_id)
        if screen is not None:
            if screen_id <= self.current_screen:
                GD.new_task(self.updateWidgets, (screen,))# Fix for glitch
            if screen_id in self.reset_when_change_screen:
                # Pop from self.SCREENS_RELATIONS
                self.SCREENS_RELATIONS.pop(self.SCREENS_RELATIONS.index(screen))
                # Reset
                self.SCREENS_RELATIONS.append(SCREEN_IDS[screen_id](self))
            if screen_id in [0x0,]:
                self.current_screen = screen_id
                GD._old_cs = screen_id
            else:
                self.current_screen = screen_id
        else:
            print(f"Screen {screen_id} not found")
            self.current_screen = 0x0

    
    def findScreen(self,screen_id) -> Screen:
        for screen in self.SCREENS_RELATIONS:
            if screen_id == screen.id:
                return screen
        return None
    
    def drawScreen(self):
        if self.screen.id in [0x0,0x1,0x2]:
            pge.screen.blit(GAME_MENU_BACKGROUND, (0,0))
        if self.screen != None:
            self.screen._update()
            self.screen.draw()
            if not self.screen.disable_widget: pge.draw_widgets(self.screen.widgets)
            
        if CONFIG['show_fps']:
            Critical:bool = False
            FPS = int(pge.getAvgFPS())
            Limit = GAME_FPS_OPTIONS[CONFIG['fps']]
            if FPS >= Limit * 0.8:
                Color = pge.Colors.LIGHTGREEN
            elif FPS >= Limit * 0.6:
                Color = pge.Colors.LIGHTYELLOW
            elif FPS >= Limit * 0.4:
                Critical = True
                Color = pge.Colors.YELLOW
            elif FPS >= Limit * 0.2:
                Critical = True
                Color = pge.Colors.ORANGE
            else:
                Critical = True
                Color = pge.Colors.RED
            pge.draw_text(Position((730,10))*RATIO,LGS.translate(33).format('(!) ' if Critical else '', FPS),PS14, Color)
        GD.fps_ratio = 60/(pge.getAvgFPS() or 60)
        if CONFIG['debug']:
            # Text
            Text = f"Screen(Id, Old): {self.current_screen, GD._old_cs}"
            
            pge.draw_text(Position((2,2))*RATIO,Text,PS14,Color)
            if self.wait_debug_menu_open > 0: self.wait_debug_menu_open -= 1
            if pge.hasKeyPressed(pg.K_F1) and self.wait_debug_menu_open <= 0:
                self.debug_menu = not self.debug_menu
                self.wait_debug_menu_open = pge.TimeSys.s2f(0.3)
                
            if self.debug_menu:
                pge.draw_rect(Position((5,5))*RATIO, Position((395,595))*RATIO, COLOR_DARK_BACKGROUND, 2, COLOR_LIGHT_BORDER, alpha=230)
                pge.draw_widgets(DEBUG_WIDGETS)
                
                if DEBUG_CreateScoreButton.value:
                    ldb:dict = db.get_value('leaderboard','data',0)
                    ldb[f'{len(ldb.keys())+1}'] = {
                        'score': random.randint(0, 10000),
                        'username': f'Juaum{len(ldb.keys())+1}',
                        'date': datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),#datetime.datetime().strftime("%Y/%m/%d %H:%M:%S", datetime.datetime.now()),
                    }
                    
                    db.update_value('leaderboard','data',0,ldb)
                    db.save()
                    DEBUG_CreateScoreButton.value = False # Makesure to disable
                elif DEBUG_ClearScoreButton.value:
                    ldb:dict = db.get_value('leaderboard','data',0)
                    ldb.clear()
                    db.update_value('leaderboard','data',0,ldb)
                    db.save()
                    DEBUG_ClearScoreButton.value = False
                
                
            
            
        
SCH = ScreenHandler()