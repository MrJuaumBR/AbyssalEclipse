from .config import *

# +++ MAIN MENU SCREEN +++ #

PlayButton = pw.Button(pge, Position((15,120))*RATIO, PS36, "PLAY",[COLOR_LIGHT_ACCEPT,COLOR_DARK_BACKGROUND])
OptionsButton = pw.Button(pge, Position((15,175))*RATIO, PS36, "OPTIONS",[COLOR_LIGHT_BLUE,COLOR_DARK_BACKGROUND])
ExitButton = pw.Button(pge, Position((15,230))*RATIO, PS36, "EXIT",[COLOR_LIGHT_REJECT,COLOR_DARK_BACKGROUND])

# Triple Buttons = 3/ Area of the others
LicenseButton = pw.Button(pge, Position((15,560))*RATIO, PS16, "LICENSES",[pge.Colors.YELLOW,COLOR_DARK_BACKGROUND],tip=("Page for\nall the LICENSES",PS14))
DiscordButton = pw.Button(pge, Position((90,560))*RATIO, PS16, "DISCORD",[COLOR_DISCORD_BLUE,COLOR_DARK_BACKGROUND],tip=("Discord\nServer Link",PS14))
GitHubButton = pw.Button(pge, Position((165,560))*RATIO, PS16, "GITHUB",[pge.Colors.WHITE,COLOR_DARK_BACKGROUND],tip=("GitHub\nRepository",PS14))
CreditsButton = pw.Button(pge, Position((240,560))*RATIO, PS16, "CREDITS",[pge.Colors.CYAN,COLOR_DARK_BACKGROUND],tip=("Page for\nall the CREDITS",PS14))



class Main_Menu(Screen):
    id:int = 0x0
    widgets:list[pw.Widget,] = []
    
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
    
    
    def _update(self):
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
        pge.draw_text(Position((20,20))*RATIO,"Abyssal Eclipse",RBG50, (125,90,115), alpha=80)
        pge.draw_text(Position((10,10))*RATIO,"Abyssal Eclipse",RBG52, (255,255,255))
        pge.draw_text(Position((360,75))*RATIO,GAME['version'],PS20,pge.Colors.LIGHTGRAY)