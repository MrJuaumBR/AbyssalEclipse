from .config import *
# +++ LICENSES +++ #
BackButtonLicenses = pw.Button(pge, Position((15,55))*RATIO, PS16, "BACK (B)",[COLOR_LIGHT_REJECT, COLOR_DARK_BACKGROUND,COLOR_LIGHT_BORDER])

class Licenses(Screen):
    id:int = 0x3
    widgets:list[pw.Widget,] = []
    def __init__(self,SCH):
        super().__init__(SCH)
        self.widgets.append(BackButtonLicenses)
        
        self.license_text:str = ''
        
        self.set_license_text()
        
        # LicenseText = pw.Textarea(pge, (5*RATIO, 80*RATIO), [pge.Colors.ANTIFLASH, pge.Colors.ANTIFLASH, pge.Colors.BLACK], PS14, self.license_text)
        # LicenseText.editable = False
        LicenseText = pw.Longtext(pge, Position((5, 80))*RATIO, PS12, self.license_text, [pge.Colors.ANTIFLASH, COLOR_DARK_BACKGROUND, COLOR_LIGHT_BORDER])
        
        self.widgets.append(LicenseText)
        
    def set_license_text(self):
        for file in os.listdir(GAME_PATH_LICENSES):
            if file != 'readme.txt':
                license = f'LICENSE - {file.replace(".txt","")}\n'
                with open(os.path.join(GAME_PATH_LICENSES,file),'r+') as f:
                    data = f.readlines()
                    for line in data:
                        license += f'{line}\n'
                        
                self.license_text += license
    def _update(self):
        if abs(pge.mouse.scroll) > 0:
            LicenseText:pw.Longtext = self.widgets[1]
            LicenseText.rect.top += ((pge.mouse.scroll * 5)*RATIO.y)
        return super()._update()
    def draw(self):
        if BackButtonLicenses.value:
            self.SCH.changeScreen(0x0)
        
        # Draw Main Title
        pge.draw_text(Position((20,20))*RATIO,"Licenses",RBG24, (125,90,115), alpha=80)
        pge.draw_text(Position((10,10))*RATIO,"Licenses",RBG26, (255,255,255))
    