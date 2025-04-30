
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
        "chance":37 # In %
    },
    "uncommon":{
        "color":pge.Colors.DARKGREEN,
        "chance":23
    },
    "rare":{
        "color":pge.Colors.DARKORANGE,
        "chance":18
    },
    "epic":{
        "color":pge.Colors.DARKPURPLE,
        "chance":14
    },
    "legendary":{
        "color":pge.Colors.BLACK,
        "chance":7
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
    value:float
    
    surface:pg.SurfaceType
    surface_rect:pg.rect.RectType
    
    rect:pg.Rect
    size:tuple[int,int] = (150,260)
    selected:bool = False
    
    looped_action:bool = False
    one_pick:bool = False
    
    tip:pw.Tip
    hover:bool = False

    
    widgets = []
    def __init__(self, cardname, description, rarity, icon_rect:tuple[int,int,int,int]=None, value:float=1.0):
        self.cardname = cardname
        self.description = description
        self.rarity = rarity
        
        self.widgets = []
        
        self.surface = pg.Surface(Position(self.size)*RATIO,pg.SRCALPHA)
        self.surface_rect = self.surface.get_rect()
        
        if icon_rect is not None:
            self.icon = Icons_spritesheet.image_at(pg.Rect(*icon_rect),-1)
            self.icon = pg.transform.scale(self.icon, Position((48,48))*RATIO)
        else:
            self.icon = None
        
        self.set_widgets()
        
        self.rect = self.surface.get_rect()
        
        self.value = value
        
    def set_widgets(self):
        self.surface.fill(COLOR_DARK_ALMOND.rgb)
        
        self.tip = pw.Tip(pge, f'Name: {str(self.cardname).capitalize()}\nRarity: {str(self.rarity).capitalize()}', PS14)
        
        # Draw Title
        pge.draw_text((self.surface_rect.centerx,11), str(self.cardname).capitalize()[:13], PS22, Rarirty[self.rarity]['color'], surface=self.surface, root_point='center')
        
        # Draw Description
        pge.draw_rect((2,72), (self.surface.get_size()[0]-4, self.surface.get_size()[1]-74), pge.Colors.BROWN, surface=self.surface, root_point='topleft')
        
        # Draw Icon
        if self.icon is not None:
            r = self.icon.get_rect()
            r.center = (self.surface_rect.centerx, 60)
            self.surface.blit(self.icon, r)
        
        lines = self.get_lines(self.description)
        y = 71
        for line in lines.values():
            pge.draw_text(Position((5,y))*RATIO, line, PS14, pge.Colors.WHITE, surface=self.surface)
            y += 20
    
    def on_hover(self):
        if self.rect.collidepoint(pge.mouse.pos): self.hover = True
        else: self.hover = False
    
    def on_select(self):
        pass
    
    def action(self, attributes:dict):
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
            elif (pg.font.Font.size(PS14, current_line + ' ' + word)[0]) * RATIO.x > (self.surface.get_size()[0]-10)*RATIO.x:
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
        surface.blit(self.surface, pos)
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
        super().__init__("Movement Speed", "This card gives you 1% more movement speed.", "common",(0,0,32,32)) # Base: 2.5%
        
    def action(self, attributes:dict):
        try:
            player = attributes['player']
            player.speed += player.speed * (0.01*self.value)
        except Exception as e:
            print(f'Error in action: {e}')

class MovSpeed2(MovSpeed1):
    def __init__(self):
        super().__init__("Movement Speed", "This card gives you 3.2% more movement speed.", "uncommon",(0,0,32,32),value=3.2) # To calculate the value get the initial value and get the % of difference
        # Base: 1%
        # This: 3.2%
        # value = Base/This
        
class MovSpeed3(MovSpeed2):
    def __init__(self):
        super().__init__("Movement Speed", "This card gives you 6.25% more movement speed.", "rare",(0,0,32,32), value=6.25)

class MovSpeed4(MovSpeed3):
    def __init__(self):
        super().__init__("Movement Speed", "This card gives you 10% more movement speed.", "epic",(0,0,32,32), value=10.0)
    
    # Attack Damage
class AttDmg1(Card):
    def __init__(self):
        super().__init__("Attack Damage", "This card gives you 1% more attack damage.", "common",(32,0,32,32))
        
    def action(self, attributes:dict):
        try:
            player = attributes['player']
            player.projectile_attr['damage'] += player.projectile_attr['damage'] * (0.01*self.value)
        except Exception as e:
            print(f'Error in action: {e}')

class AttDmg2(Card):
    def __init__(self):
        super().__init__("Attack Damage", "This card gives you 2% more attack damage.", "uncommon",(32,0,32,32),value=2.0)
        
class AttDmg3(Card):
    def __init__(self):
        super().__init__("Attack Damage", "This card gives you 4% more attack damage.", "rare",(32,0,32,32),value=4.0)

class AttDmg4(Card):
    def __init__(self):
        super().__init__("Attack Damage", "This card gives you 8% more attack damage.", "epic",(32,0,32,32),value=8.0)
        
    # Reload Speed
class RelSpd1(Card):
    def __init__(self):
        super().__init__("Reload Speed", "This card gives you 0.5% minus reload speed.", "common",(64,0,32,32))
        
    def action(self, attributes:dict):
        try:
            player = attributes['player']
            player.reload_time -= 0.005 * self.value
        except Exception as e:
            print(f'Error in action: {e}')
            
        
class RelSpd2(Card):
    def __init__(self):
        super().__init__("Reload Speed", "This card gives you 1% minus reload speed.", "uncommon",(64,0,32,32), value=2)
        
class RelSpd3(Card):
    def __init__(self):
        super().__init__("Reload Speed", "This card gives you 2% minus reload speed.", "rare",(64,0,32,32), value=4)
        
class RelSpd4(Card):
    def __init__(self):
        super().__init__("Reload Speed", "This card gives you 4% minus reload speed.", "epic",(64,0,32,32), value=8)
        
class RelSpd5(Card):
    def __init__(self):
        super().__init__("Reload Speed", "This card gives you 12% minus reload speed.\n\n Are you a speedrunner?!", "legendary",(64,0,32,32), value=24)

    # Health
class Health1(Card):
    def __init__(self):
        super().__init__("Health", "This card gives you 10+ more health.", "common",(96,0,32,32))
        
    def action(self, attributes:dict):
        try:
            player = attributes['player']
            mh = player.maxHealth
            player.maxHealth = mh + (10*self.value)
            player.health *= player.maxHealth/mh
        except Exception as e:
            print(f'Error in action: {e}')

class Health2(Health1):
    def __init__(self):
        super().__init__("Health", "This card gives you 20+ more health.", "uncommon",(96,0,32,32),value=2.0)
        
class Health3(Health2):
    def __init__(self):
        super().__init__("Health", "This card gives you 40+ more health.", "rare",(96,0,32,32),value=4.0)        
        
class Health4(Health3):
    def __init__(self):
        super().__init__("Health", "This card gives you 80+ more health.", "epic",(96,0,32,32),value=8.0)
        
class Health5(Health4):
    def __init__(self):
        super().__init__("Health", "This card gives you 250+ more health.\n\n Yooo! a bodybuilder damn.", "legendary",(96,0,32,32),value=25.0)

    # Perfuration
class Perf1(Card):
    def __init__(self):
        super().__init__("Perfuration", "This card make your projectile hit +1 target.", "rare",(160,32,32,32))
        
    def action(self, attributes:dict):
        try:
            player = attributes['player']
            player.projectile_attr += 1 * int(self.value)
        except Exception as e:
            print(f'Error in action: {e}')
            
class Perf2(Perf1):
    def __init__(self):
        super().__init__("Perfuration", "This card make your projectile hit +2 target.", "epic",(160,32,32,32),value=2.0)
        
    # Projectile Speed
class ProjSpd1(Card):
    def __init__(self):
        super().__init__("Projectile Speed", "This card gives you 5% more projectile speed.", "common",(192,32,32,32))
        
    def action(self, attributes:dict):
        try:
            player = attributes['player']
            player.projectile_attr['speed'] += player.projectile_attr['speed'] * (0.05*self.value)
        except Exception as e:
            print(f'Error in action: {e}')
            
class ProjSpd2(ProjSpd1):
    def __init__(self):
        super().__init__("Projectile Speed", "This card gives you 10% more projectile speed.", "uncommon",(192,32,32,32),value=2.0)
        
class ProjSpd3(ProjSpd2):
    def __init__(self):
        super().__init__("Projectile Speed", "This card gives you 20% more projectile speed.", "rare",(192,32,32,32),value=4.0)


    # Luck
class Luck1(Card):
    def __init__(self):    
        super().__init__("Luck", "This card gives you 2% more luck.", "common",(128,0,32,32))
        
    def action(self, attributes:dict):
        try:
            player = attributes['player']
            player.luck += player.luck * (0.02*self.value)
        except Exception as e:
            print(f'Error in action: {e}')

class Luck2(Luck1):
    def __init__(self):
        super().__init__("Luck", "This card gives you 4% more luck.", "uncommon",(128,0,32,32), value=2.0)
        
class Luck3(Luck2):
    def __init__(self):
        super().__init__("Luck", "This card gives you 8% more luck.", "rare",(128,0,32,32), value=4.0)
        
class Luck4(Luck3):
    def __init__(self):
        super().__init__("Luck", "This card gives you 16% more luck.", "epic",(128,0,32,32), value=8.0)
        
class Luck5(Luck4):
    def __init__(self):
        super().__init__("Luck", "This card gives you 50% more luck.\n\n Miss Murphy? Where are you?", "legendary",(128,0,32,32), value=25.0)

# Abilities
class Shield(Card):
    one_pick:bool = True
    
    total_health:int = 0
    recover_time:int = 0
    
    looped_action:bool = True
    setuped:bool = False
    def __init__(self):
        super().__init__("Shield", "shield with the ability to negate damage of 20% of your HP, after being destroyed it recovers in 10s.\n\n Scaredy cat!", "uncommon",(128,32,32,32))
        
    def action(self, attributes):
        player = attributes['player']
        if not self.setuped:
            GAME_MUSIC_CHANNEL1.play(GAME_SFX_SHIELD_ON)
            self.total_health = player.maxHealth * 0.2
            self.setuped = True
            
        if player.health < player.maxHealth and self.total_health > 0:
            GAME_MUSIC_CHANNEL1.play(GAME_SFX_SHIELD_OFF)
            try:
                player.health += self.total_health
            except Exception as e:
                print(f'Error in action: {e}')
            self.total_health = 0
            self.recover_time = pge.delta_time
            
        if self.total_health <= 0 and self.recover_time.total_seconds() + 1 < pge.delta_time.total_seconds():
            self.setuped = False
            
            
        
        

class GrownManTear(Card):
    one_pick:bool = True
    def __init__(self):
        super().__init__("Grown Man Tear", "Negates all damage for 5s after losing 15% health with a 30s cooldown.\n\n Men don't cry, but when necessary, the suitcase is already out.","legendary",(64,32,32,32))

class MermaidTear(Card):
    one_pick:bool = True
    def __init__(self):
        super().__init__("Mermaid Tear", "When your health is below 60%, your regeneration is increased by 15%.\n\n You made a mermaid cry...","legendary",(96,32,32,32))

class Nuketown(Card):
    looped_action = True
    one_pick:bool = True
    # Individual Variables
    time_to_next_nuke = 30
    last_nuke = 0
    def __init__(self):
        super().__init__("Nuke Town", "This card gives you a nuke. That happens every 30 seconds.\n\n We are not in Fallout.", "mythic",(160,0,32,32))
        self.last_nuke = pge.delta_time
    
    def nuke(self, world:object):
        for enemy in world.enemys:
            if enemy.health > 0:
                enemy.health -= random.uniform(0.8,0.95) * enemy.health
    
    def action(self, attributes:dict):
        player= attributes['player']
        world= attributes['world']
        if pge.delta_time.total_seconds() - self.last_nuke.total_seconds() > self.time_to_next_nuke:
            GAME_MUSIC_CHANNEL1.play(GAME_SFX_NUKE)
            GD.new_task(self.nuke, (world,))
            self.last_nuke = pge.delta_time
        
class Repeater(Card):
    def __init__(self):
        super().__init__("Repeater", "This card makes you shoot +1 shoot per reload.\n\n That's a lot of shots damn it.", "mythic",(192,0,32,32))
        
class Berserker(Card):
    one_pick:bool = True
    def __init__(self):
        super().__init__("Berserker", "every 10 points of health lost is equal to 1% more damage.(Limit is 50% and ends after 10 seconds)\nYou're a warrior aren't you?", "mythic",(224,0,32,32))

class Vampire(Card):
    one_pick:bool = True
    def __init__(self):
        super().__init__("Vampire", "every 10% of damage given heals 1% of health.\n\n Serious? Do you lack creativity?", "mythic",(256,0,32,32))
        
class Ninja(Card):
    one_pick:bool = True
    def __init__(self):
        super().__init__("Ninja", "Every 5 points of health lost is equal to 1% more movement speed.\n\n You're a ninja aren't you?", "mythic",(288,0,32,32))
        
class Assasin(Card):
    one_pick:bool = True
    def __init__(self):
        super().__init__("Assasin", "Every 5 points of health lost is equal to 1% more attack speed.\n\n You're going to join the vampire, aren't you?", "mythic",(320,0,32,32))
        
class Statsless(Card):
    def __init__(self):
        super().__init__("Statsless", "+10% in all stats\n\n Huh? Looks like you aren't mastering nothing? ", "mythic",(352,0,32,32))
        
    def action(self, attributes:dict):
        try:
            player = attributes['player']
            stats:list[str,] = [
                'speed',
                'luck',
                'health',
                'maxHealth',
            ]
            for stat in stats:
                if stat in ['reload_time']:
                    player.__dict__[stat] -= player.__dict__[stat] * 0.1
                elif stat in ['resistance']:
                    if player.__dict__[stat] > 0:
                        player.__dict__[stat] += player.__dict__[stat] * 0.1
                    else:
                        player.__dict__[stat] = 1
                else:
                    player.__dict__[stat] *= 1.1
        except Exception as e:
            print(f'Error in action: {e}')

class MasterOfGravity(Card):
    def __init__(self):
        super().__init__("Master of Gravity", "You become the Master of Gravity, increasing your speed by 5% and decreasing that of enemies by 10%.\n\n Already controls part of space, and now, time?","mythic",(0,32,32,32))
        
class Bloodlust(Card):
    def __init__(self):
        super().__init__("Bloodlust", "You will scare enemies around you every 15s, paralyzing them for 3s.\n\n It seems to me that you are a little angry?", "mythic",(32,32,32,32))

class CardHandler:
    def __init__(self):
        self.cards = [cls() for cls in Card.__subclasses__()]
    
    def random_rarity(self, luck:float=1.0):
        return random.choices(list(Rarirty.keys()), weights=[(Rarirty[r]['chance']/100) * luck for r in Rarirty.keys()])[0]
    
    def random_rarities(self, times:int=3, luck:float=1.0):
        return [self.random_rarity(luck=luck) for i in range(times)]
    
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
    
    def only_cards_of_rarity(self, rarity, exclusion:list[Card,]=[]):
        exclusion_names:list[str,] = [str(n.cardname) for n in exclusion]
        cards:list[Card,] = []
        for c in self.cards:
            if c.rarity != rarity:
                if c.one_pick:
                    if not c.cardname in exclusion_names:
                        cards.append(c)
                    
                else:
                    cards.append(c)
                
        return cards
    
    def random_card(self, luck:float=1.0, exclusion:list[Card,]=[]) -> Card:
        cards = self.only_cards_of_rarity(self.random_rarity(luck=luck),exclusion)
        
        if len(cards) == 0: return self.random_card()
        return random.choice(cards)
        
    def random_cards(self, times:int=3, luck:float=1.0, can_repeat:bool=False, already_chosen:list[Card,]=[]) -> list[Card,]:
        x = []
        print(already_chosen)
        for i in range(times):
            card:Card = self.random_card(luck=luck)
            if not can_repeat:
                while (card in x):
                    card = self.random_card(luck=luck,exclusion=already_chosen)
            x.append(card)
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
