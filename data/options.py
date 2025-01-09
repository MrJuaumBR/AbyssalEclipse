from .config import *
# +++ OPTIONS MENU SCREEN +++ #
BackButtonOptions = pw.Button(pge, Position((15,55))*RATIO, PS16, "BACK",[COLOR_DARK_RED,COLOR_DARK_ALMOND])

# Screen Resolution
ScreenResSelect = pw.Select(pge, Position((50,90))*RATIO, PS18, [pge.Colors.DARKBROWN, pge.Colors.ALMOND, pge.Colors.BLACK], [str(i) for i in GAME_WINDOW_RESOLUTION_OPTIONS], CONFIG['window_resolution'], tip=("Window Resolution (Requires Restart)",PS14))
# Fullscreen, Checkbox
FullScreenCheck = pw.Checkbox(pge, Position((20,130))*RATIO, PS18, "FULLSCREEN", [pge.Colors.WHITE, pge.Colors.ALMOND, pge.Colors.BLACK, pge.Colors.DARKBROWN], tip=("Fullscreen (Requires Restart)",PS14))
# FPS Limit, Select
FPSLimitSelect = pw.Select(pge, Position((50,170))*RATIO, PS18, [pge.Colors.DARKBROWN, pge.Colors.ALMOND, pge.Colors.BLACK], [str(i) for i in GAME_FPS_OPTIONS], CONFIG['fps'], tip=("FPS Limit",PS14))
# Dynamic FPS, Checkbox
DynamicFPSCheck = pw.Checkbox(pge, Position((20,210))*RATIO, PS18, "DYNAMIC FPS", [pge.Colors.WHITE, pge.Colors.ALMOND, pge.Colors.BLACK, pge.Colors.DARKBROWN], tip=("Dynamic FPS (Make time pass more precise)",PS14))
# Show FPS, Checkbox
ShowFPSCheck = pw.Checkbox(pge, Position((20,250))*RATIO, PS18, "SHOW FPS", [pge.Colors.WHITE, pge.Colors.ALMOND, pge.Colors.BLACK, pge.Colors.DARKBROWN], tip=("Show FPS",PS14))
# Dynamic Mouse Wheel, Checkbox
DynMouseWhlCheck = pw.Checkbox(pge, Position((20,290))*RATIO, PS18, "DYNAMIC MOUSE WHEEL", [pge.Colors.WHITE, pge.Colors.ALMOND, pge.Colors.BLACK, pge.Colors.DARKBROWN], tip=("Dynamic Mouse Wheel (Make Mouse Wheel more smooth)",PS14))
# Use GPU, Checkbox
VsyncCheck = pw.Checkbox(pge, Position((20,330))*RATIO, PS18, "USE VSYNC", [pge.Colors.WHITE, pge.Colors.ALMOND, pge.Colors.BLACK, pge.Colors.DARKBROWN], tip=("Use Vertical Synchronization (Requires Restart)",PS14))
# Debug, Checkbox
DebugCheck = pw.Checkbox(pge, Position((20,370))*RATIO, PS18, "DEBUG", [pge.Colors.YELLOW, pge.Colors.ALMOND, pge.Colors.BLACK, pge.Colors.DARKBROWN], tip=("Debug (Requires Restart)",PS14))

# Measure Speed, Select
MeasureSpeedSelect = pw.Select(pge, Position((50,410))*RATIO, PS18, [pge.Colors.DARKBROWN, pge.Colors.ALMOND, pge.Colors.BLACK], [str(i) for i in GAME_SPEED_MEASURE_OPTIONS], CONFIG['speed_measure'], tip=("Measure Speed",PS14))

# Trail options
# Trail, Checkbox
TrailCheck = pw.Checkbox(pge, Position((20, 485))*RATIO, PS16, 'MOUSE TRAIL', [pge.Colors.YELLOW, pge.Colors.ALMOND, pge.Colors.BLACK, pge.Colors.DARKBROWN], tip=("Mouse Trail",PS14))
TrailColor = pw.Dropdown(pge, Position((200, 485))*RATIO, [pge.Colors.WHITE, (140,123,106), pge.Colors.BLACK], ['Red','Green','Blue','Yellow','Purple',"White","Random"], PS16, current_text=CONFIG['trail_color'])

class Options(Screen):
    id:int = 0x1
    widgets:list[pw.Widget,] = []
    cfg:GAME_DEFAULT_CFG_TYPE = CONFIG
    
    frames_runned:int = 0
    def __init__(self,SCH):
        super().__init__(SCH)
        self.widgets.append(BackButtonOptions)
        self.widgets.append(ScreenResSelect)
        self.widgets.append(FullScreenCheck)
        self.widgets.append(FPSLimitSelect)
        self.widgets.append(DynamicFPSCheck)
        self.widgets.append(ShowFPSCheck)
        self.widgets.append(DynMouseWhlCheck)
        self.widgets.append(VsyncCheck)
        self.widgets.append(DebugCheck)
        self.widgets.append(MeasureSpeedSelect)
        self.widgets.append(TrailCheck)
        self.widgets.append(TrailColor)
    def draw(self):
        pge.draw_rect(Position((10,450))*RATIO,Position((300,80))*RATIO,COLOR_DARK_ALMOND,2,pge.Colors.GRAY,alpha=128)
        pge.draw_text(Position((15,455))*RATIO,'Trail Options', PS16,pge.Colors.WHITE)
        if self.frames_runned == 0:
            self.frames_runned = 1
            self.cfg = CONFIG
            
            ScreenResSelect.value = self.cfg['window_resolution']
            FullScreenCheck.value = self.cfg['fullscreen']
            FPSLimitSelect.value = self.cfg['fps']
            DynamicFPSCheck.value = self.cfg['dynamic_fps']
            ShowFPSCheck.value = self.cfg['show_fps']
            DynMouseWhlCheck.value = self.cfg['dynamic_mouse_wheel']
            VsyncCheck.value = self.cfg['vsync']
            DebugCheck.value = self.cfg['debug']
            MeasureSpeedSelect.value = self.cfg['speed_measure']
            TrailCheck.value = self.cfg['mouse_trail']
            TrailColor.current_text = self.cfg["trail_color"]
        if BackButtonOptions.value:
            self.SCH.changeScreen(0x0)
            self.exiting()
        
        self.cfg['window_resolution'] = ScreenResSelect.value
        self.cfg['fullscreen'] = FullScreenCheck.value
        self.cfg['fps'] = FPSLimitSelect.value
        self.cfg['dynamic_fps'] = DynamicFPSCheck.value
        self.cfg['show_fps'] = ShowFPSCheck.value
        self.cfg['dynamic_mouse_wheel'] = DynMouseWhlCheck.value
        self.cfg['vsync'] = VsyncCheck.value
        self.cfg['debug'] = DebugCheck.value
        self.cfg['speed_measure'] = MeasureSpeedSelect.value
        self.cfg['mouse_trail'] = TrailCheck.value
        self.cfg['trail_color'] = TrailColor.current_text
            
        # Draw Main Title
        pge.draw_text(Position((20,20))*RATIO,"Options",RBG24, (125,90,115), alpha=80)
        pge.draw_text(Position((10,10))*RATIO,"Options",RBG26, (255,255,255))
        
    def exiting(self):
        CONFIG['fullscreen'] = self.cfg['fullscreen']
        CONFIG['dynamic_fps'] = self.cfg['dynamic_fps']
        CONFIG['dynamic_mouse_wheel'] = self.cfg['dynamic_mouse_wheel']
        CONFIG['show_fps'] = self.cfg['show_fps']
        CONFIG['window_resolution'] = self.cfg['window_resolution']
        CONFIG['fps'] = self.cfg['fps']
        CONFIG['debug'] = self.cfg['debug']
        CONFIG['vsync'] = self.cfg['vsync']
        CONFIG['speed_measure'] = self.cfg['speed_measure']
        CONFIG['mouse_trail'] = self.cfg['mouse_trail']
        CONFIG['trail_color'] = self.cfg['trail_color']
        self.cfg = CONFIG
        self.frames_runned = 0
        pge.setFPS(GAME_FPS_OPTIONS[CONFIG['fps']])
        pge.enableFPS_unstable(CONFIG['dynamic_fps'])
        pge.mouse.mouse_trail_enabled = CONFIG['mouse_trail']
        if GAME_TRAIL_COLOR_OPTIONS[CONFIG['trail_color']] == 'Random':
            pge.mouse.trail_node_random_color = True
        else:
            pge.mouse.trail_node_random_color = False
            pge.mouse.trail_node_color = GAME_TRAIL_COLOR_OPTIONS[CONFIG['trail_color']]
        
        pge.mouse.smooth_scroll = CONFIG['dynamic_mouse_wheel']
        db.update_value('config', 'data', 0, CONFIG)
        db.save()