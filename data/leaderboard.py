from .config import *
# +++ Leaderboard +++ #

BackButtonLeaderboard = pw.Button(pge, Position((15,55))*RATIO, PS16, LGS.translate(5),[COLOR_LIGHT_REJECT, COLOR_DARK_BACKGROUND,COLOR_LIGHT_BORDER])
OrderDropdown = pw.Dropdown(pge, Position((85,55))*RATIO, [pge.Colors.WHITE, COLOR_DARK_BACKGROUND, COLOR_LIGHT_BORDER], LGS.translate_list('list3'), PS16, current_text=1, tip=(LGS.translate(36),PS14))
StartNewRunButton = pw.Button(pge, Position((15,550))*RATIO, PS16, LGS.translate(37),[COLOR_LIGHT_ACCEPT, COLOR_DARK_BACKGROUND])
UsernameTextbox = pw.Textbox(pge, Position((220,550))*RATIO, 25*RATIO.y, colors=[COLOR_DARK_UNACTIVE,COLOR_DARK_ACTIVE, pge.Colors.WHITE, COLOR_LIGHT_BORDER], font=PS16, text=f"{GD.username}", tip=(LGS.translate(38),PS14), placeholder=LGS.translate(39))
DifficultyDropdown = pw.Dropdown(pge, Position((145,550))*RATIO, [pge.Colors.WHITE, COLOR_DARK_BACKGROUND, COLOR_LIGHT_BORDER], LGS.translate_list('list4'), PS16, current_text=1, tip=(LGS.translate(40),PS14))

class Leaderboard(Screen):
    id:int = 0x2
    widgets:list[pw.Widget,] = []
    
    board:dict = {}
    
    def __init__(self,SCH):
        super().__init__(SCH)
        self.widgets.append(BackButtonLeaderboard)
        self.widgets.append(OrderDropdown)
        self.widgets.append(StartNewRunButton)
        self.widgets.append(UsernameTextbox)
        self.widgets.append(DifficultyDropdown)
        
        self.board = db.get_value('leaderboard', 'data', 0).copy()
        
        self.order()
        
        OrderDropdown.on_change = self.order
    
    def opened(self):
        self.board = db.get_value('leaderboard', 'data', 0).copy()
    
    def order(self,__=None):
        self.board = db.get_value('leaderboard', 'data', 0).copy()
        order_key = 'score' if OrderDropdown.current_text == 0 else ('date' if OrderDropdown.current_text == 1 else 'username')
        self.board = dict(sorted(self.board.items(), key=lambda item: item[1][order_key], reverse=True))
        
        
    def draw(self):
        if BackButtonLeaderboard.value:
            self.SCH.changeScreen(0x0)
            self.exiting()
        elif StartNewRunButton.value:
            GD.username = UsernameTextbox.text
            GD.difficulty = str(DifficultyDropdown.text).lower()
            self.SCH.changeScreen(0x4)

        # Draw Main Title
        pge.draw_text(Position((20, 20)) * RATIO, LGS.translate(41), RBG24, (125, 90, 115), alpha=80)
        pge.draw_text(Position((10, 10)) * RATIO, LGS.translate(41), RBG26, (255, 255, 255))
        
        x, y = 15, 90
        for score in self.board.values():
            COLOR = COLOR_WHITE
            if score['difficulty'] == 'easy': COLOR = COLOR_GREEN
            elif score['difficulty'] == 'medium': COLOR = COLOR_YELLOW
            elif score['difficulty'] == 'hard': COLOR = COLOR_RED
            pge.draw_rect(Position((x, y)) * RATIO, Position((250, 100)) * RATIO, COLOR_DARK_BACKGROUND, 2, COLOR_LIGHT_BORDER, alpha=230)
            pge.draw_text(Position((x + 10, y + 10)) * RATIO, LGS.translate(42).format(score["username"]), PS16, COLOR)
            pge.draw_text(Position((x + 10, y + 40)) * RATIO, LGS.translate(43).format(score["score"]), PS16, COLOR)
            pge.draw_text(Position((x + 10, y + 70)) * RATIO, LGS.translate(44).format(score["date"]), PS16, COLOR)
            if score['debug'] == 'True': pge.draw_text(Position((x + 10, y + 100)) * RATIO, "* Debug Game", PS16, COLOR, alpha=230)
            if x * RATIO.x <= 535 * RATIO.x:
                x += 265  # Adjusted for spacing
            else:
                y += 115
                x = 15
