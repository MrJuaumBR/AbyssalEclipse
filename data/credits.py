
from .config import *

BackButtonCredits = pw.Button(pge, Position((15,55))*RATIO, PS16, LGS.translate(5), [COLOR_LIGHT_REJECT, COLOR_DARK_BACKGROUND, COLOR_DARK_BORDER])

News = LoadNews()
NewsArea = pw.Longtext(pge, Position((600,320))*RATIO, PS14, News, [pge.Colors.BLACK, COLOR_LIGHT_BACKGROUND, COLOR_DARK_BACKGROUND], alpha=200)

_credits:list[dict,] = [
    {
        'name':'João Pedro',
        'alias':'MrJuaum',
        'role':'Programmer, Arts e etc.',
    },
    {
        'name':'Anderson',
        'alias':'vendramin',
        'role':'Programmer, Tester',
    },
    {
        'name':'Rafael/Cambé Boys',
        'alias':'Rael/Cambé Boys',
        'role':'Musician',
    }
]

class Credits(Screen):
    id:int = 0x5
    widgets:list[pw.Widget,] = []
    
    news_y:int = 320
    
    texts:list[str,] = []
    def __init__(self,SCH):
        super().__init__(SCH)
        
        self.widgets.append(BackButtonCredits)
        self.widgets.append(NewsArea)
        
        self.texts = []
        for item in _credits:
            self.texts.append(f"{item['name']} ({item['alias']}) - {item['role']}")
        
    
    def _update(self):
        if abs(pge.mouse.scroll) > 0 and NewsArea.rect.collidepoint(pge.mouse.pos):
            self.news_y += ((pge.mouse.scroll * 5)*RATIO.y)
        NewsArea.rect.y = self.news_y
        return super()._update()
    
    def draw(self):
        if BackButtonCredits.value:
            self.SCH.changeScreen(0x0)
            
        # Draw Main Title
        pge.draw_text(Position((20,20))*RATIO,LGS.translate(34),RBG24, (125,90,115), alpha=80)
        pge.draw_text(Position((10,10))*RATIO,LGS.translate(34),RBG26, (255,255,255))
        
        # Draw Credits
        for index, item in enumerate(self.texts):
            pge.draw_rect(Position((10, 80 + (index * 40) + 5))*RATIO, Position((380, 30)) * RATIO, COLOR_DARK_BACKGROUND, 2, COLOR_DARK_BORDER, alpha=230)
            pge.draw_text(Position((20, 80 + (index * 40) + 10))*RATIO, item, PS16, pge.Colors.WHITE)