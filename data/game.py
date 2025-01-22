from .config import *

from .objects.world import World

LifeBar = pw.Progressbar(pge, Position((5,555))*RATIO, Position((250,20))*RATIO, [pge.Colors.BLOODRED, pge.Colors.BLACK, pge.Colors.ALMOND, pge.Colors.WHITE], 1, "Health", PS16, tip=("Health", PS14))
ExpBar = pw.Progressbar(pge, Position((5,580))*RATIO, Position((790,15))*RATIO, [pge.Colors.BLUE,pge.Colors.BLACK, pge.Colors.ALMOND, pge.Colors.WHITE], 1, "Experience", PS14 , tip=("Experience", PS12))

# Pause Menu Widgets

ResumeButton = pw.Button(pge, Position((15,75))*RATIO, PS16, "RESUME", [pge.Colors.GREEN, COLOR_DARK_ALMOND, pge.Colors.BLACK])
ExitToMenuButton = pw.Button(pge, Position((15,115))*RATIO, PS16, "EXIT TO MENU", [pge.Colors.RED, COLOR_DARK_ALMOND, pge.Colors.BLACK],tip=("Exit to Menu",PS14))
ExitGame = pw.Button(pge, Position((15,155))*RATIO, PS16, "EXIT GAME", [pge.Colors.DARKRED, COLOR_DARK_ALMOND, pge.Colors.BLACK], tip=("Exit Game",PS14))

ResumeButton.enable = False
ExitToMenuButton.enable = False
ExitGame.enable = False

class Game(Screen):
    id:int = 0x4
    widgets:list[pw.Widget,] = []
    
    paused:bool = False
    
    world:World
    
    pause_timer:int = 0
    def __init__(self, SCH):
        super().__init__(SCH)
        
        self.widgets.append(LifeBar)
        self.widgets.append(ExpBar)
        
        self.widgets.append(ResumeButton)
        self.widgets.append(ExitToMenuButton)
        self.widgets.append(ExitGame)
        
        self.world:World = World()
    
    def _update(self):
        if (pge.hasKeyPressed(pg.K_ESCAPE) or pge.mouse.button_4 or (pge.joystick.main and pge.joystick.main.getButtonByString("start"))) and self.pause_timer <= 0:
            self.paused = not self.paused
            self.pause_timer = pge.TimeSys.s2f(0.32)
            
        if not self.paused:
            self.world.update()
            LifeBar.value = self.world.player.health / self.world.player.maxHealth
            ExpBar.value = self.world.player.experience / (self.world.player.level * 100)
            LifeBar.text = f"Health: {int(self.world.player.health)}/{int(self.world.player.maxHealth)} ({int(LifeBar.value*100)}%)"
            ExpBar.text = f"Level: {self.world.player.level} | Experience: {int(self.world.player.experience)}/{self.world.player.level*100} ({int(ExpBar.value*100)}%)"
            
        if self.pause_timer > 0: self.pause_timer -= 1
        
        if ResumeButton.value and self.pause_timer <= 0:
            self.paused = False
            self.pause_timer = pge.TimeSys.s2f(0.32)
        elif ExitToMenuButton.value and self.pause_timer <= 0:
            self.exiting()
            self.SCH.changeScreen(0x0)
        elif ExitGame.value and self.pause_timer <= 0:
            self.exiting()
            pge.exit()
        
        return super()._update()
    
    def draw(self):
        self.world.draw()
        self.world.player.draw()

        speed_measure = GAME_SPEED_MEASURE_OPTIONS[CONFIG["speed_measure"]]
        speed = round(self.world.player.register_speed[speed_measure], 2)
        pge.draw_text(Position((5, 15)) * RATIO, f'Speed: {speed} {speed_measure}', PS12, pge.Colors.WHITE)

        pause_elements = [ResumeButton, ExitToMenuButton, ExitGame]
        if self.paused:
            pge.draw_rect(Position((5, 5)) * RATIO, Position((390, 590)) * RATIO, COLOR_DARK_ALMOND, 3, pge.Colors.BLOODRED, alpha=180)
            pge.draw_text(Position((10, 10)) * RATIO, "MENU", PS20, pge.Colors.BLACK)
            pge.draw_text(Position((10, 40)) * RATIO, "PAUSED", PS16, pge.Colors.BLACK)
            for element in pause_elements:
                element.enable = True
        else:
            for element in pause_elements:
                element.enable = False
    
    def exiting(self):
        self.__dict__ = Game(self.SCH).__dict__