
from ..config import *

# Rarirty:dict = {
#     "common":0,
#     "uncommon":1,
#     "rare":2,
#     "epic":3,
#     "legendary":4
# }

# rarity_color = {
#     "common":pge.Colors.GRAY,
#     "uncommon":pge.Colors.DARKGREEN,
#     "rare":pge.Colors.DARKORANGE,
#     "epic":pge.Colors.DARKPURPLE,
#     "legendary":pge.Colors.BLACK
# }

Rarirty = {
    "common":{
        "color":pge.Colors.GRAY,
        "chance":35 # In %
    },
    "uncommon":{
        "color":pge.Colors.DARKGREEN,
        "chance":20
    },
    "rare":{
        "color":pge.Colors.DARKORANGE,
        "chance":18
    },
    "epic":{
        "color":pge.Colors.DARKPURPLE,
        "chance":16
    },
    "legendary":{
        "color":pge.Colors.BLACK,
        "chance":10
    },
    "mythic":{
        "color":pge.Colors.RED,
        "chance":1
    }
}

Icons_spritesheet:spritesheet = pge.createSpritesheet(GAME_PATH_TEXTURES+"/CardsIcons.png")

class Card:
    cardname:str
    description:str
    rarity:str
    icon:pg.SurfaceType
    
    surface:pg.SurfaceType
    surface_rect:pg.rect.RectType
    
    rect:pg.Rect
    size:tuple[int,int] = (170,260)
    selected:bool = False
    
    
    
    tip:pw.Tip
    hover:bool = False
    
    CPS14 = pge.createFont(FONT_PIXELIFYSANS, 15)
    CPS18 = pge.createFont(FONT_PIXELIFYSANS, 17)
    CPS22 = pge.createFont(FONT_PIXELIFYSANS, 20)
    
    widgets = []
    def __init__(self, cardname, description, rarity, icon_rect:tuple[int,int,int,int]=None):
        self.cardname = cardname
        self.description = description
        self.rarity = rarity
        
        self.widgets = []
        
        self.surface = pg.Surface(self.size,pg.SRCALPHA)
        self.surface_rect = self.surface.get_rect()
        
        if icon_rect is not None:
            self.icon = Icons_spritesheet.image_at(pg.Rect(*icon_rect),-1)
            self.icon = pg.transform.scale(self.icon, (48,48))
        else:
            self.icon = None
        
        self.set_widgets()
        
        self.rect = self.surface.get_rect()
        
    def set_widgets(self):
        self.surface.fill(COLOR_DARK_ALMOND.rgb)
        
        self.tip = pw.Tip(pge, f'Name: {str(self.cardname).capitalize()}\nRarity: {str(self.rarity).capitalize()}', PS14)
        
        # Draw Title
        pge.draw_text((self.surface_rect.centerx,11), str(self.cardname).capitalize(), self.CPS22, Rarirty[self.rarity]['color'], surface=self.surface, root_point='center')
        
        # Draw Description
        pge.draw_rect((2,72), (self.surface.get_size()[0]-4, self.surface.get_size()[1]-74), pge.Colors.BROWN, surface=self.surface, root_point='topleft')
        
        # Draw Icon
        if self.icon is not None:
            self.surface.blit(self.icon, (66,22))
        
        lines = self.get_lines(self.description)
        y = 71
        for line in lines.values():
            pge.draw_text((5,y), line, self.CPS18, pge.Colors.WHITE, surface=self.surface)
            y += 15
    
    def on_hover(self):
        if self.rect.collidepoint(pge.mouse.pos): self.hover = True
        else: self.hover = False
    
    def on_select(self):
        pass
    
    def effect(self, player):
        pass
    
    def get_lines(self,text:str) -> dict:
        """
        Splits the text into lines based on the width of the text and the screen size.
        Returns a dictionary where the keys are the line numbers and the values are the lines of text.
        """
        lines = {}
        current_line = ''
        line_number = 1
        for word in text.replace('\n',' <BreakHere> ').split():
            if word in [' <BreakHere> ', '\n', '<BreakHere>']:
                lines[line_number] = current_line.strip()
                current_line = ''
                line_number += 1
            elif pg.font.Font.size(self.CPS14, current_line + ' ' + word)[0]+10 > (self.surface.get_size()[0]-50):
                lines[line_number] = current_line.strip()
                current_line = word
                line_number += 1
            else:
                if word != ' ':
                    current_line += ' ' + word
        if current_line:
            lines[line_number] = current_line.strip()
        return lines
    
    def draw(self, pos:tuple, surface:pg.SurfaceType = None):
        if surface is None:
            surface = pge.screen
        surface.blit(pg.transform.scale(self.surface, Position((170,260))*RATIO), pos)
        self.rect.topleft = pos
        
        self.on_hover()
        if self.hover:
            self.tip.draw()
            if pge.mouse.left:
                self.on_select()

# Cards
    # Movement Speed
class MovSpeed1(Card):
    def __init__(self):
        super().__init__("Movement Speed", "This card gives you 2.5% more movement speed.", "common",(0,0,32,32))

class MovSpeed2(Card):
    def __init__(self):
        super().__init__("Movement Speed", "This card gives you 7% more movement speed.", "uncommon",(0,0,32,32))
        
class MovSpeed3(Card):
    def __init__(self):
        super().__init__("Movement Speed", "This card gives you 16% more movement speed.", "rare",(0,0,32,32))

class MovSpeed4(Card):
    def __init__(self):
        super().__init__("Movement Speed", "This card gives you 28% more movement speed.", "epic",(0,0,32,32))
    
    # Attack Damage
class AttDmg1(Card):
    def __init__(self):
        super().__init__("Attack Damage", "This card gives you 1% more attack damage.", "common",(32,0,32,32))

class AttDmg2(Card):
    def __init__(self):
        super().__init__("Attack Damage", "This card gives you 2% more attack damage.", "uncommon",(32,0,32,32))
        
class AttDmg3(Card):
    def __init__(self):
        super().__init__("Attack Damage", "This card gives you 4% more attack damage.", "rare",(32,0,32,32))

class AttDmg4(Card):
    def __init__(self):
        super().__init__("Attack Damage", "This card gives you 8% more attack damage.", "epic",(32,0,32,32))
        
    # Reload Speed
class RelSpd1(Card):
    def __init__(self):
        super().__init__("Reload Speed", "This card gives you 0.5% minus reload speed.", "common",(64,0,32,32))
        
class RelSpd2(Card):
    def __init__(self):
        super().__init__("Reload Speed", "This card gives you 1% minus reload speed.", "uncommon",(64,0,32,32))
        
class RelSpd3(Card):
    def __init__(self):
        super().__init__("Reload Speed", "This card gives you 2% minus reload speed.", "rare",(64,0,32,32))
        
class RelSpd4(Card):
    def __init__(self):
        super().__init__("Reload Speed", "This card gives you 4% minus reload speed.", "epic",(64,0,32,32))
        
class RelSpd5(Card):
    def __init__(self):
        super().__init__("Reload Speed", "This card gives you 25% minus reload speed.\n\n Are you a speedrunner?!", "legendary",(64,0,32,32))

    # Health
class Health1(Card):
    def __init__(self):
        super().__init__("Health", "This card gives you 10+ more health.", "common",(96,0,32,32))

class Health2(Card):
    def __init__(self):
        super().__init__("Health", "This card gives you 20+ more health.", "uncommon",(96,0,32,32))
        
class Health3(Card):
    def __init__(self):
        super().__init__("Health", "This card gives you 40+ more health.", "rare",(96,0,32,32))        
        
class Health4(Card):
    def __init__(self):
        super().__init__("Health", "This card gives you 80+ more health.", "epic",(96,0,32,32))
        
class Health5(Card):
    def __init__(self):
        super().__init__("Health", "This card gives you 250+ more health.\n\n Yooo! a bodybuilder damn.", "legendary",(96,0,32,32))
        
    # Luck
class Luck1(Card):
    def __init__(self):    
        super().__init__("Luck", "This card gives you 2% more luck.", "common",(128,0,32,32))

class Luck2(Card):
    def __init__(self):
        super().__init__("Luck", "This card gives you 4% more luck.", "uncommon",(128,0,32,32))
        
class Luck3(Card):
    def __init__(self):
        super().__init__("Luck", "This card gives you 8% more luck.", "rare",(128,0,32,32))
        
class Luck4(Card):
    def __init__(self):
        super().__init__("Luck", "This card gives you 16% more luck.", "epic",(128,0,32,32))
        
class Luck5(Card):
    def __init__(self):
        super().__init__("Luck", "This card gives you 50% more luck.\n\n Miss Murphy? Where are you?", "legendary",(128,0,32,32))

# Abilities
class Shield(Card):
    def __init__(self):
        super().__init__("Shield", "shield with the ability to negate damage of 20% of your HP, after being destroyed it recovers in 10s.\n\n Scaredy cat!", "uncommon",(128,32,32,32))

class GrownManTear(Card):
    def __init__(self):
        super().__init__("Grown Man Tear", "Negates all damage for 5s after losing 15% health with a 30s cooldown.\n\n Men don't cry, but when necessary, the suitcase is already out.","legendary",(64,32,32,32))

class MermaidTear(Card):
    def __init__(self):
        super().__init__("Mermaid Tear", "When your health is below 60%, your regeneration is increased by 15%.\n\n You made a mermaid cry...","legendary",(96,32,32,32))

class Nuketown(Card):
    def __init__(self):
        super().__init__("Nuke Town", "This card gives you a nuke. That happens every 30 seconds.\n\n We are not in CoD.", "mythic",(160,0,32,32))
        
class Repeater(Card):
    def __init__(self):
        super().__init__("Repeater", "This card makes you shoot +1 shoot per reload.\n\n That's a lot of shots damn it.", "mythic",(192,0,32,32))
        
class Berserker(Card):
    def __init__(self):
        super().__init__("Berserker", "every 10 points of health lost is equal to 1% more damage.(Limit is 50% and ends after 10 seconds)\nYou're a warrior aren't you?", "mythic",(224,0,32,32))

class Vampire(Card):
    def __init__(self):
        super().__init__("Vampire", "every 10% of damage given heals 1% of health.\n\n Serious? Do you lack creativity?", "mythic",(256,0,32,32))
        
class Ninja(Card):
    def __init__(self):
        super().__init__("Ninja", "Every 5 points of health lost is equal to 1% more movement speed.\n\n You're a ninja aren't you?", "mythic",(288,0,32,32))
        
class Assasin(Card):
    def __init__(self):
        super().__init__("Assasin", "Every 5 points of health lost is equal to 1% more attack speed.\n\n You're going to join the vampire, aren't you?", "mythic",(320,0,32,32))
        
class Statsless(Card):
    def __init__(self):
        super().__init__("Statsless", "+10% in all stats\n\n Huh? Looks like you aren't mastering nothing? ", "mythic",(352,0,32,32))

class MasterOfGravity(Card):
    def __init__(self):
        super().__init__("Master of Gravity", "You become the Master of Gravity, increasing your speed by 5% and decreasing that of enemies by 10%.\n\n Already controls part of space, and now, time?","mythic",(0,32,32,32))
        
class Bloodlust(Card):
    def __init__(self):
        super().__init__("Bloodlust", "You will scare enemies around you every 15s, paralyzing them for 3s.\n\n It seems to me that you are a little angry?", "mythic",(32,32,32,32))

class CardHandler:
    def __init__(self):
        self.cards = [cls() for cls in Card.__subclasses__()]
    
    def cards_by_rarity(self):
        """
        A way to randomize cards by rarity
        
        common = 35%
        uncommon = 20%
        rare = 18%
        epic = 16%
        legendary = 10%
        mythic = 1%
        
        Total = 100
        """
        
        rarities = []
        for r in Rarirty.keys():
            for i in range(Rarirty[r]['chance']):
                rarities.append(r)
        return random.choice(rarities)
    
    def only_cards_of_rarity(self, rarity):
        return [c for c in self.cards if c.rarity == rarity]
    
    def random_card(self) -> Card:
        cards = self.only_cards_of_rarity(self.cards_by_rarity())
        if len(cards) == 0: return self.random_card()
        return random.choice(cards)
        
    def random_cards(self, times:int=3) -> list[Card,]:
        x = []
        for i in range(times):
            x.append(self.random_card())
        return x
                       
# Test
def CardTest():
    pge.setScreenTitle('Abyssal Eclipse - Card Test')
    
    CDH = CardHandler()
    
    widgets:list[pw.Widget,] = []
    
    x = 10
    for key in Rarirty.keys():
        dp = pw.Dropdown(pge, Position((x,32))*RATIO, [COLOR_DARK_BLUE,COLOR_DARK_ALMOND, COLOR_WHITE], [card.cardname.capitalize() for card in CDH.only_cards_of_rarity(key)], PS14, current_text=1, tip=(f"Rarity: {key.capitalize()}",PS14))
        dp.rarity = key
        widgets.append(dp)
        x += 135
    
    cards:list[Card,] = []
    
    for wd in widgets:
        index = wd.current_text
        rarity = wd.rarity
        
        card = CDH.only_cards_of_rarity(rarity)[index]
        cards.append(card)

    while True:
        pge.draw_text(Position((2,2))*RATIO,"Card Test",PS20,pge.Colors.WHITE)
        
        x,y = 25,60
        for card in cards:
            card.draw(Position((x,y))*RATIO)
            x += 205
            if x*RATIO.x <= 625*RATIO.x:
                pass
            else:
                x = 25
                y += 275
        pge.draw_widgets(widgets)
        for event in pge.events:
            if event.type == pg.QUIT:
                pge.exit()
                
        cards.clear()
        for wd in widgets:
            index = wd.current_text
            rarity = wd.rarity
            
            card = CDH.only_cards_of_rarity(rarity)[index]
            cards.append(card)
                
        if pge.hasKeyPressed(pg.K_F1):
            for wd in widgets:
                rarity = wd.rarity
                cards = CDH.only_cards_of_rarity(rarity)
                wd.current_text = random.randint(0,len(cards)-1)
        
        pge.update()
        pge.screen.fill((0,0,0))
        pge.fpsw()