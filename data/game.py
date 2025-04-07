from .config import *

from .objects.world import World
from .objects.cards import Card, CardHandler

LifeBar = pw.Progressbar(pge, Position((5,545))*RATIO, Position((250,20))*RATIO, [pge.Colors.BLOODRED, pge.Colors.BLACK, pge.Colors.ALMOND, pge.Colors.WHITE], 1, LGS.translate(46), PS16, tip=(LGS.translate(46), PS14))
ExpBar = pw.Progressbar(pge, Position((5,570))*RATIO, Position((790,15))*RATIO, [pge.Colors.BLUE,pge.Colors.BLACK, pge.Colors.ALMOND, pge.Colors.WHITE], 1, LGS.translate(47), PS14 , tip=(LGS.translate(47), PS12))

# Pause Menu Widgets

ResumeButton = pw.Button(pge, Position((15,75))*RATIO, PS16, LGS.translate(48), [COLOR_LIGHT_ACCEPT, COLOR_DARK_BACKGROUND, COLOR_LIGHT_BORDER])
ExitToMenuButton = pw.Button(pge, Position((15,115))*RATIO, PS16, LGS.translate(49), [COLOR_LIGHT_REJECT, COLOR_DARK_BACKGROUND, COLOR_LIGHT_BORDER])
ExitGame = pw.Button(pge, Position((15,155))*RATIO, PS16, LGS.translate(50), [COLOR_REJECT, COLOR_DARK_BACKGROUND, COLOR_LIGHT_BORDER])

ResumeButton.enable = False
ResumeButton.click_time = 0.01
ExitToMenuButton.enable = False
ExitToMenuButton.click_time = 0.01
ExitGame.enable = False
ExitGame.click_time = 0.01


pause_elements = [ResumeButton, ExitToMenuButton, ExitGame]
game_elements = [LifeBar, ExpBar]

class Game(Screen):
    id:int = 0x4
    widgets:list[pw.Widget,] = []
    content_offset:pg.math.Vector2 = pg.math.Vector2(0,0)
    increase_offset:pg.math.Vector2 = pg.math.Vector2(1,1)
    paused:int = 0x0
    
    world:World
    
    pause_timer:any
    CHR:CardHandler
    current_cards:list[Card, ] = []
    def __init__(self, SCH):
        super().__init__(SCH)
        self.CHR = CardHandler()
        self.widgets.append(LifeBar)
        self.widgets.append(ExpBar)
        
        self.widgets.append(ResumeButton)
        self.widgets.append(ExitToMenuButton)
        self.widgets.append(ExitGame)
        
        self.world:World = World(GD.difficulty,self.level_up)
        self.pause_timer = pge.delta_time
    
    def opened(self):
        if GAME_MUSIC_CHANNEL0.get_sound() != GAME_MUSIC_OST1:
            GAME_MUSIC_CHANNEL0.stop()
            GAME_MUSIC_CHANNEL0.play(GAME_MUSIC_OST1,-1)
            GAME_MUSIC_CHANNEL0.set_volume(round(CONFIG['volume'],2))
    
    def level_up(self):
        self.paused:int = 0x2
        self.current_cards = self.CHR.random_cards(5,1.0, can_repeat=False)
        if GAME_MUSIC_CHANNEL1.get_sound() != GAME_SFX_LEVELUP:
            GAME_MUSIC_CHANNEL1.play(GAME_SFX_LEVELUP)
    
    def UpdateUItext(self):
        if self.paused == 0x0:
            LifeBar.text = LGS.translate(51).format(int(self.world.player.health),int(self.world.player.maxHealth),int(LifeBar.value*100))
            ExpBar.text = LGS.translate(52).format(self.world.player.level,int(self.world.player.experience),int(self.world.player.level*100),int(ExpBar.value*100))
    
    def _update(self):
        if ((pge.hasKeyPressed(pg.K_ESCAPE) or pge.mouse.button_4) or (pge.joystick.main and pge.joystick.main.getButtonByString("start"))) and (self.pause_timer - pge.delta_time).total_seconds() <= 1:
            self.paused = 0x0 if self.paused == 0x1 else 0x1
            self.pause_timer = pge.delta_time
            
        if self.paused == 0x0: # Not Paused
            self.world.update()
            LifeBar.value = self.world.player.health / self.world.player.maxHealth
            ExpBar.value = self.world.player.experience / (self.world.player.level * 100)
            GD.new_task(self.UpdateUItext,())
        elif self.paused == 0x1: # Paused
            
            if ResumeButton.value and (self.pause_timer - pge.delta_time).total_seconds() <= 1:
                self.paused = 0x0
                self.pause_timer = pge.delta_time
            elif ExitToMenuButton.value and (self.pause_timer - pge.delta_time).total_seconds() <= 0.3:
                self.exiting()
                self.SCH.changeScreen(0x0)
            elif ExitGame.value and (self.pause_timer - pge.delta_time).total_seconds() <= 0.3:
                self.exiting()
                pge.exit()
        elif self.paused == 0x2: # Leveled Up
            self.content_offset.y += self.increase_offset.y * (0.025 * GD.fps_ratio)
            if self.content_offset.y >= 1 or self.content_offset.y <= 0:
                self.increase_offset.y *= -1
                
            if pge.hasKeyPressed(pg.K_1):
                self.SelectCard(0)
            elif pge.hasKeyPressed(pg.K_2):
                self.SelectCard(1)
            elif pge.hasKeyPressed(pg.K_3):
                self.SelectCard(2)
            elif pge.hasKeyPressed(pg.K_4):
                self.SelectCard(3)
            elif pge.hasKeyPressed(pg.K_5):
                self.SelectCard(4)
        
        
        return super()._update()
    
    def SelectCard(self, index:int):
        self.paused = 0x0
        GD.new_task(self.world.player.cardInsert, (self.current_cards[index],))
        if GAME_MUSIC_CHANNEL1.get_sound() != GAME_SFX_POWERUP:
            GAME_MUSIC_CHANNEL1.play(GAME_SFX_POWERUP)
    
    def time_fix(self) -> str:
        elapsed_time = self.world.elapsed_time
        humanized:dict = pygameengine.objects.humanize_seconds(elapsed_time)
        x = ''
        cc = {
            'days':'d',
            'hours':'h',
            'minutes':'m',
            'seconds':'s'
        }
        for key, value in humanized.items():
            if value > 0 and key != 'milliseconds':
                x += f"{value}{cc[key]}, "
        return x[:-2]
    
    def turnElements(self, element:Literal['Game','Pause'], state:bool):
        if element == 'Game':
            if game_elements[0].enable != state:
                for element in game_elements:
                    element.enable = state
                for element in pause_elements:
                    element.enable = not state
        elif element == 'Pause':
            if pause_elements[0].enable != state:
                for element in game_elements:
                    element.enable = not state
                for element in pause_elements:
                    element.enable = state
    
    def draw(self):
        self.world.draw()
        self.world.player.draw()
        # self.world.draw_projectiles()
        speed_measure = GAME_SPEED_MEASURE_OPTIONS[CONFIG["speed_measure"]]
        pge.draw_text(Position((5, 15)) * RATIO, LGS.translate(53).format(round(self.world.player.register_speed[speed_measure], 2), speed_measure), PS12, pge.Colors.WHITE)
        pge.draw_text(Position((5, 30)) * RATIO, LGS.translate(54).format(len(self.world.projectiles)), PS12, pge.Colors.WHITE)
        pge.draw_text(Position((5, 45)) * RATIO, LGS.translate(55).format(self.world.offset.xy), PS12, pge.Colors.WHITE)
        
        pge.draw_text((GAME_CENTER_OF_SCREEN[0],15*RATIO.y), f"{self.time_fix()}", PS16, pge.Colors.WHITE,root_point="center")

        
        if self.paused == 0x1:
            pge.draw_rect(Position((5, 5)) * RATIO, Position((390, 590)) * RATIO, COLOR_DARK_BACKGROUND, 3, COLOR_LIGHT_BORDER, alpha=180)
            pge.draw_text(Position((10, 10)) * RATIO, LGS.translate(56), PS18, pge.Colors.WHITE)
            GD.new_task(self.turnElements, ('Game', False))
        elif self.paused == 0x0:
            pge.draw_text(Position((400,550))*RATIO, LGS.translate(58).format(str(len(self.world.enemys))),PS16,pge.Colors.WHITE,surface=pge.screen,root_point='center')
            GAME_SCREEN.blit(self.world.player.cards_surface, Position((5, 530-self.world.player.cards_surface.get_height())) * RATIO)
            
            GD.new_task(self.turnElements, ('Game', True))
        elif self.paused == 0x2:
            pge.draw_text(Position((400,50+(self.content_offset.y*3)))*RATIO, LGS.translate(59).format(self.world.player.level), PS32, pge.Colors.WHITE, surface=pge.screen, root_point='center')
            for index, card in enumerate(self.current_cards):
                x = 5+(160*index)
                y = 250+(self.content_offset.y*5)
                pge.draw_text(Position((x-2, y-24))*RATIO, f'({index+1})', PS18, pge.Colors.WHITE, surface=pge.screen)
                card.draw(Position((x,250+(self.content_offset.y*5)))*RATIO, pge.screen)
    
    def exiting(self):
        # self.world:World = World(GD.difficulty,self.level_up)
        self.__dict__ = Game(self.SCH).__dict__
        GAME_MUSIC_CHANNEL0.stop()
        GAME_MUSIC_CHANNEL0.play(GAME_MUSIC_OST2,-1)
