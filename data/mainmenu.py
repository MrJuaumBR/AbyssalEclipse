from .config import *

# +++ MAIN MENU SCREEN +++ #

PlayButton = pw.Button(pge, Position((15,120))*RATIO, PS36, LGS.translate(0),[COLOR_LIGHT_ACCEPT,COLOR_DARK_BACKGROUND])
OptionsButton = pw.Button(pge, Position((15,175))*RATIO, PS36, LGS.translate(1),[COLOR_LIGHT_BLUE,COLOR_DARK_BACKGROUND])
ExitButton = pw.Button(pge, Position((15,230))*RATIO, PS36, LGS.translate(2),[COLOR_LIGHT_REJECT,COLOR_DARK_BACKGROUND])

# Triple Buttons = 3/ Area of the others
LicenseButton = pw.Button(pge, Position((15,560))*RATIO, PS16, LGS.translate(3),[pge.Colors.YELLOW,COLOR_DARK_BACKGROUND],tip=(LGS.translate(29),PS14))
DiscordButton = pw.Button(pge, Position((90,560))*RATIO, PS16, "DISCORD",[COLOR_DISCORD_BLUE,COLOR_DARK_BACKGROUND],tip=(LGS.translate(30),PS14))
GitHubButton = pw.Button(pge, Position((165,560))*RATIO, PS16, "GITHUB",[pge.Colors.WHITE,COLOR_DARK_BACKGROUND],tip=(LGS.translate(31),PS14))
CreditsButton = pw.Button(pge, Position((240,560))*RATIO, PS16, LGS.translate(4),[pge.Colors.CYAN,COLOR_DARK_BACKGROUND],tip=(LGS.translate(32),PS14))

class Main_Menu(Screen):
    id:int = 0x0
    widgets:list[pw.Widget,] = []
    
    title_animation:list[float, int] = [0.0, 1]
    def __init__(self,SCH):
        super().__init__(SCH)
        self.widgets = [
            PlayButton,
            OptionsButton,
            ExitButton,
            LicenseButton,
            DiscordButton,
            GitHubButton,
            CreditsButton,
        ]
    
    
    def opened(self):
        if GAME_MUSIC_CHANNEL0.get_sound() != GAME_MUSIC_OST2:
            GAME_MUSIC_CHANNEL0.play(GAME_MUSIC_OST2,-1,fade_ms=500)
            print("Volume: ", round(CONFIG['volume'],2))
            GAME_MUSIC_CHANNEL0.set_volume(round(CONFIG['volume'],2))
    
    def _update(self):
        self.title_animation[0] += (0.7 * (60/(pge.getAvgFPS() or pge.fps)))*self.title_animation[1]
        if self.title_animation[0] >= 20 or self.title_animation[0] <= 0:
            self.title_animation[1] *= -1
        return super()._update()
    
    def draw(self):
        if PlayButton.value:
            self.SCH.changeScreen(0x2)
        elif OptionsButton.value:
            self.SCH.changeScreen(0x1)
        elif LicenseButton.value:
            self.SCH.changeScreen(0x3)
        elif ExitButton.value:
            self.exiting()
            pge.exit()
        elif CreditsButton.value:
            self.SCH.changeScreen(0x5)
        
        # Draw Main Title
        pge.draw_text(Position((20+(self.title_animation[0]*0.8),20+(self.title_animation[0]*1.2)))*RATIO,"Abyssal Eclipse",RBG50, (125,90,115), alpha=80)
        pge.draw_text(Position((10,10+self.title_animation[0]))*RATIO,"Abyssal Eclipse",RBG52, (255,255,255))
        pge.draw_text(Position((360,75+self.title_animation[0]))*RATIO,GAME['version'],PS20,pge.Colors.LIGHTGRAY)