from .config import *
# +++ Leaderboard +++ #

BackButtonLeaderboard = pw.Button(pge, Position((15,55))*RATIO, PS16, "BACK",[COLOR_DARK_RED, COLOR_DARK_ALMOND])
OrderDropdown = pw.Dropdown(pge, Position((65,55))*RATIO, [COLOR_DARK_BLUE,COLOR_DARK_ALMOND, COLOR_WHITE], ['By Score','By Date','By Username'], PS16, current_text=1, tip=("Order By",PS14))
StartNewRunButton = pw.Button(pge, Position((15,550))*RATIO, PS16, "START NEW RUN",[pge.Colors.GREEN,COLOR_DARK_ALMOND])
UsernameTextbox = pw.Textbox(pge, Position((145,550))*RATIO, 25*RATIO.y, colors=[COLOR_DARK_ALMOND,pge.Colors.ALMOND,pge.Colors.BLACK, pge.Colors.WHITE], font=PS16, text=f"{GD.username}", tip=("Username that will save score",PS14), placeholder="Enter your username...")

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
        
        self.order()
        
        OrderDropdown.on_change = self.order
        
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
            self.SCH.changeScreen(0x4)

        # Draw Main Title
        pge.draw_text(Position((20, 20)) * RATIO, "Leaderboard", RBG24, (125, 90, 115), alpha=80)
        pge.draw_text(Position((10, 10)) * RATIO, "Leaderboard", RBG26, (255, 255, 255))
        
        x, y = 15, 90
        for score in self.board.values():
            pge.draw_rect(Position((x, y)) * RATIO, Position((250, 100)) * RATIO, pge.Colors.ALMOND, 2, pge.Colors.BLOODRED, alpha=230)
            pge.draw_text(Position((x + 10, y + 10)) * RATIO, f'Username: {score["username"]}', PS16, pge.Colors.BLACK)
            pge.draw_text(Position((x + 10, y + 40)) * RATIO, f'Score: {score["score"]}', PS16, pge.Colors.BLACK)
            pge.draw_text(Position((x + 10, y + 70)) * RATIO, f'Date: {score["date"]}', PS16, pge.Colors.BLACK)
            if x * RATIO.x <= 535 * RATIO.x:
                x += 265  # Adjusted for spacing
            else:
                y += 115
                x = 15
