from .config import *

from .objects.world import World, Card

LifeBar = pw.Progressbar(pge, Position((5,545))*RATIO, Position((250,20))*RATIO, [pge.Colors.BLOODRED, pge.Colors.BLACK, pge.Colors.ALMOND, pge.Colors.WHITE], 1, "Health", PS16, tip=("Health", PS14))
ExpBar = pw.Progressbar(pge, Position((5,570))*RATIO, Position((790,15))*RATIO, [pge.Colors.BLUE,pge.Colors.BLACK, pge.Colors.ALMOND, pge.Colors.WHITE], 1, "Experience", PS14 , tip=("Experience", PS12))

# Pause Menu Widgets

ResumeButton = pw.Button(pge, Position((15,75))*RATIO, PS16, "RESUME", [COLOR_LIGHT_ACCEPT, COLOR_DARK_BACKGROUND, COLOR_LIGHT_BORDER])
ExitToMenuButton = pw.Button(pge, Position((15,115))*RATIO, PS16, "EXIT TO MENU", [COLOR_LIGHT_REJECT, COLOR_DARK_BACKGROUND, COLOR_LIGHT_BORDER])
ExitGame = pw.Button(pge, Position((15,155))*RATIO, PS16, "EXIT GAME", [COLOR_REJECT, COLOR_DARK_BACKGROUND, COLOR_LIGHT_BORDER])

ResumeButton.enable = False
ExitToMenuButton.enable = False
ExitGame.enable = False



class Game(Screen):
    id:int = 0x4
    widgets:list[pw.Widget,] = []
    content_offset:pg.math.Vector2 = pg.math.Vector2(0,0)
    increase_offset:pg.math.Vector2 = pg.math.Vector2(1,1)
    paused:int = 0x0
    
    world:World
    
    pause_timer:int = 0
    def __init__(self, SCH):
        super().__init__(SCH)
        
        self.widgets.append(LifeBar)
        self.widgets.append(ExpBar)
        
        self.widgets.append(ResumeButton)
        self.widgets.append(ExitToMenuButton)
        self.widgets.append(ExitGame)
        
        self.world:World = World(GD.difficulty,self.level_up)
    
    def level_up(self):
        self.paused:int = 0x2
    
    def _update(self):
        if ((pge.hasKeyPressed(pg.K_ESCAPE) or pge.mouse.button_4) or (pge.joystick.main and pge.joystick.main.getButtonByString("start"))) and self.pause_timer <= 0 and not self.paused == 0x2:
            self.paused = 0x0 if self.paused == 0x1 else 0x1
            self.pause_timer = pge.TimeSys.s2f(0.32)
            
        if self.paused == 0x0: # Not Paused
            self.world.update()
            LifeBar.value = self.world.player.health / self.world.player.maxHealth
            ExpBar.value = self.world.player.experience / (self.world.player.level * 100)
            LifeBar.text = f"Health: {int(self.world.player.health)}/{int(self.world.player.maxHealth)} ({int(LifeBar.value*100)}%)"
            ExpBar.text = f"Level: {self.world.player.level} | Experience: {int(self.world.player.experience)}/{self.world.player.level*100} ({int(ExpBar.value*100)}%)"
        elif self.paused == 0x1: # Paused
            if ResumeButton.value and self.pause_timer <= 0:
                self.paused = False
                self.pause_timer = pge.TimeSys.s2f(0.32)
            elif ExitToMenuButton.value and self.pause_timer <= 0:
                print("Exit to Menu")
                self.exiting()
                self.SCH.changeScreen(0x0)
            elif ExitGame.value and self.pause_timer <= 0:
                self.exiting()
                pge.exit()
        elif self.paused == 0x2: # Leveled Up
            self.content_offset.y += self.increase_offset.y * (0.025 * (60/pge.getAvgFPS()))
            if self.content_offset.y >= 1 or self.content_offset.y <= 0:
                self.increase_offset.y *= -1
            
        if self.pause_timer > 0: self.pause_timer -= 1
        
        
        return super()._update()
    
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
    
    def draw(self):
        self.world.draw()
        self.world.player.draw()
        # self.world.draw_projectiles()
        speed_measure = GAME_SPEED_MEASURE_OPTIONS[CONFIG["speed_measure"]]
        pge.draw_text(Position((5, 15)) * RATIO, f'Speed: {round(self.world.player.register_speed[speed_measure], 2)} {speed_measure}', PS12, pge.Colors.WHITE)
        pge.draw_text(Position((5, 30)) * RATIO, f'Projectiles: {len(self.world.projectiles)}', PS12, pge.Colors.WHITE)
        pge.draw_text(Position((5, 45)) * RATIO, f'Offset: {self.world.offset.xy}', PS12, pge.Colors.WHITE)
        
        pge.draw_text((GAME_CENTER_OF_SCREEN[0],15*RATIO.y), f"{self.time_fix()}", PS16, pge.Colors.WHITE,root_point="center")

        pause_elements = [ResumeButton, ExitToMenuButton, ExitGame]
        if self.paused == 0x1:
            pge.draw_rect(Position((5, 5)) * RATIO, Position((390, 590)) * RATIO, COLOR_DARK_BACKGROUND, 3, COLOR_LIGHT_BORDER, alpha=180)
            pge.draw_text(Position((10, 10)) * RATIO, "MENU", PS16, pge.Colors.WHITE)
            pge.draw_text(Position((10, 40)) * RATIO, "PAUSED", PS16, pge.Colors.WHITE)
            for element in pause_elements:
                element.enable = True
        elif self.paused == 0x0:
            pge.draw_text(Position((400,550))*RATIO,'Enemies Left: '+str(len(self.world.enemys)),PS16,pge.Colors.WHITE,surface=pge.screen,root_point='center')
            for element in pause_elements:
                element.enable = False
        elif self.paused == 0x2:
            pge.draw_text(Position((400,50+(self.content_offset.y*5)))*RATIO, f"Level Up to {self.world.player.level}!", PS32, pge.Colors.WHITE, surface=pge.screen, root_point='center')
    
    def exiting(self):
        # self.world:World = World(GD.difficulty,self.level_up)
        self.__dict__ = Game(self.SCH).__dict__