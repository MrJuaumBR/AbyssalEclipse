from .config import *

# +++ MAIN MENU SCREEN +++ #

PlayButton = pw.Button(pge, Position((15,120))*RATIO, PS36, "PLAY",[COLOR_DARK_GREEN,COLOR_DARK_ALMOND])
OptionsButton = pw.Button(pge, Position((15,175))*RATIO, PS36, "OPTIONS",[COLOR_DARK_BLUE,COLOR_DARK_ALMOND])
ExitButton = pw.Button(pge, Position((15,230))*RATIO, PS36, "EXIT",[COLOR_DARK_RED,COLOR_DARK_ALMOND])

# Triple Buttons = 3/ Area of the others
LicenseButton = pw.Button(pge, Position((15,560))*RATIO, PS16, "LICENSES",[pge.Colors.YELLOW,COLOR_DARK_ALMOND],tip=("Page for\nall the LICENSES",PS14))
DiscordButton = pw.Button(pge, Position((90,560))*RATIO, PS16, "DISCORD",[COLOR_DISCORD_BLUE,COLOR_DARK_ALMOND],tip=("Discord\nServer Link",PS14))
GitHubButton = pw.Button(pge, Position((165,560))*RATIO, PS16, "GITHUB",[pge.Colors.BLACK,COLOR_DARK_ALMOND],tip=("GitHub\nRepository",PS14))

News = LoadNews()

# NewsArea = pw.Textarea(pge, Position((600,320))*RATIO, [pge.Colors.ALMOND, pge.Colors.ALMOND, pge.Colors.BLACK], PS14, News, alpha=200)
NewsArea = pw.Longtext(pge, Position((600,320))*RATIO, PS14, News, [pge.Colors.BLACK, pge.Colors.ALMOND, pge.Colors.BLOODRED], alpha=200)

class Main_Menu(Screen):
    id:int = 0x0
    widgets:list[pw.Widget,] = []
    
    news_y:int = 320
    def __init__(self,SCH):
        super().__init__(SCH)
        self.widgets = [
            PlayButton,
            OptionsButton,
            ExitButton,
            LicenseButton,
            DiscordButton,
            GitHubButton,
            NewsArea
        ]
        
        self.version_text = pge.createSurface(len(GAME['version'])*(20*RATIO.med),len(GAME['version'])*(20*RATIO.med),pg.SRCALPHA)
        self.version_text_rect = self.version_text.get_rect()

        pge.draw_text((0,0),GAME['version'],PS20,pge.Colors.CYAN,self.version_text)
        self.version_text,self.version_text_rect = pge.rotate(self.version_text,self.version_text_rect,-45)
        self.version_text_rect.center = Position((435,80)) *RATIO
    
    def _update(self):
        if abs(pge.mouse.scroll) > 0 and NewsArea.rect.collidepoint(pge.mouse.pos):
            self.news_y += ((pge.mouse.scroll * 5)*RATIO.y)
        NewsArea.rect.y = self.news_y
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
        
        # Draw Main Title
        pge.draw_text(Position((20,20))*RATIO,"Abyssal Eclipse",RBG50, (125,90,115), alpha=80)
        pge.draw_text(Position((10,10))*RATIO,"Abyssal Eclipse",RBG52, (255,255,255))
        GAME_SCREEN.blit(self.version_text, self.version_text_rect)