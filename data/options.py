from .config import *
# +++ OPTIONS MENU SCREEN +++ #
BackButtonOptions = pw.Button(pge, Position((15,55))*RATIO, PS16, LGS.translate(5),[COLOR_LIGHT_REJECT,COLOR_DARK_BACKGROUND,COLOR_DARK_BORDER])

# Screen Resolution
ScreenResSelect = pw.Select(pge, Position((35,120))*RATIO, PS18, [pge.Colors.WHITE, COLOR_LIGHT_BACKGROUND, COLOR_DARK_BORDER], [str(i) for i in GAME_WINDOW_RESOLUTION_OPTIONS], CONFIG['window_resolution'], tip=(LGS.translate(6),PS14))
# Fullscreen, Checkbox
FullScreenCheck = pw.Checkbox(pge, Position((20,150))*RATIO, PS18, LGS.translate(9), [pge.Colors.WHITE, COLOR_LIGHT_ACCEPT, COLOR_LIGHT_REJECT, COLOR_DARK_BORDER], tip=(LGS.translate(8),PS14))
# FPS Limit, Select
FPSLimitSelect = pw.Select(pge, Position((35,180))*RATIO, PS18, [pge.Colors.WHITE, COLOR_LIGHT_BACKGROUND, COLOR_DARK_BORDER], [str(i) for i in GAME_FPS_OPTIONS], CONFIG['fps'], tip=(LGS.translate(10),PS14))
# Dynamic FPS, Checkbox
DynamicFPSCheck = pw.Checkbox(pge, Position((20,210))*RATIO, PS18, LGS.translate(12), [pge.Colors.WHITE, COLOR_LIGHT_ACCEPT, COLOR_LIGHT_REJECT, COLOR_DARK_BORDER], tip=(LGS.translate(11),PS14))
# Show FPS, Checkbox
ShowFPSCheck = pw.Checkbox(pge, Position((20, 240))*RATIO, PS18, LGS.translate(14), [pge.Colors.WHITE, COLOR_LIGHT_ACCEPT, COLOR_LIGHT_REJECT, COLOR_DARK_BORDER], tip=(LGS.translate(13),PS14))
# Dynamic Mouse Wheel, Checkbox
DynMouseWhlCheck = pw.Checkbox(pge, Position((20,270))*RATIO, PS18, LGS.translate(16), [pge.Colors.WHITE, COLOR_LIGHT_ACCEPT, COLOR_LIGHT_REJECT, COLOR_DARK_BORDER], tip=(LGS.translate(15),PS14))
# Use GPU, Checkbox
VsyncCheck = pw.Checkbox(pge, Position((20,300))*RATIO, PS18, LGS.translate(18), [pge.Colors.WHITE, COLOR_LIGHT_ACCEPT, COLOR_LIGHT_REJECT, COLOR_DARK_BORDER], tip=(LGS.translate(17),PS14))
# Debug, Checkbox
DebugCheck = pw.Checkbox(pge, Position((20,330))*RATIO, PS18, LGS.translate(20), [pge.Colors.WHITE, COLOR_LIGHT_ACCEPT, COLOR_LIGHT_REJECT, COLOR_DARK_BORDER], tip=(LGS.translate(19),PS14))

# Measure Speed, Select
MeasureSpeedSelect = pw.Select(pge, Position((35,360))*RATIO, PS18, [pge.Colors.WHITE, COLOR_LIGHT_BACKGROUND, COLOR_DARK_BORDER], [str(i) for i in GAME_SPEED_MEASURE_OPTIONS], CONFIG['speed_measure'], tip=(LGS.translate(21),PS14))

# Volume, Slider
VolumeSlider = pw.Slider(pge, Position((20,390))*RATIO, Position((260,18))*RATIO,[pge.Colors.WHITE, COLOR_LIGHT_ACCEPT, COLOR_LIGHT_REJECT, COLOR_DARK_BORDER], CONFIG['volume'], True, tip=(LGS.translate(22),PS14))

# Language, Dropdown
LanguageDropdown = pw.Dropdown(pge, Position((410, 120))*RATIO, [pge.Colors.WHITE, COLOR_LIGHT_BACKGROUND, COLOR_DARK_BORDER], GAME_LANGUAGE_OPTIONS, PS16, current_text=GAME_LANGUAGE_OPTIONS.index(CONFIG['lang']), tip=(LGS.translate(23),PS14))


# Visual Options
# Trail, Checkbox
TrailCheck = pw.Checkbox(pge, Position((20, 485))*RATIO, PS16, LGS.translate(25), [pge.Colors.WHITE, COLOR_LIGHT_ACCEPT, COLOR_LIGHT_REJECT, COLOR_DARK_BORDER], tip=(LGS.translate(24),PS14))
# Trail Color, Dropdown
TrailColor = pw.Dropdown(pge, Position((200, 485))*RATIO, [pge.Colors.WHITE, COLOR_LIGHT_BACKGROUND, COLOR_DARK_BORDER], LGS.translate_list('list1'), PS16, current_text=CONFIG['trail_color'], tip=(LGS.translate(26),PS14))
# Floor Color, Dropdown
FloorColorDropwdown = pw.Dropdown(pge, Position((20, 515))*RATIO, [pge.Colors.WHITE, COLOR_LIGHT_BACKGROUND, COLOR_DARK_BORDER], LGS.translate_list('list2'), PS16, current_text=CONFIG['floor_color'], tip=(LGS.translate(27),PS14))

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
        self.widgets.append(VolumeSlider)
        self.widgets.append(TrailCheck)
        self.widgets.append(TrailColor)
        self.widgets.append(FloorColorDropwdown)
        self.widgets.append(LanguageDropdown)
        
        VolumeSlider._on_change = self.VolumeSliderChange
    def VolumeSliderChange(self,_):
        GAME_MUSIC_CHANNEL0.set_volume(round(VolumeSlider.value,2))
        GAME_MUSIC_CHANNEL1.set_volume(round(VolumeSlider.value*0.8,2))
        GAME_MUSIC_CHANNEL2.set_volume(round(VolumeSlider.value*0.8,2))
    def update_cfg(self):
        self.cfg['window_resolution'] = ScreenResSelect.value
        self.cfg['fullscreen'] = FullScreenCheck.value
        self.cfg['fps'] = FPSLimitSelect.value
        self.cfg['dynamic_fps'] = DynamicFPSCheck.value
        self.cfg['show_fps'] = ShowFPSCheck.value
        self.cfg['dynamic_mouse_wheel'] = DynMouseWhlCheck.value
        self.cfg['vsync'] = VsyncCheck.value
        self.cfg['debug'] = DebugCheck.value
        self.cfg['speed_measure'] = MeasureSpeedSelect.value
        self.cfg['volume'] = VolumeSlider.value
        self.cfg['mouse_trail'] = TrailCheck.value
        self.cfg['trail_color'] = TrailColor.current_text
        self.cfg['floor_color'] = FloorColorDropwdown.current_text
        self.cfg['lang'] = GAME_LANGUAGE_OPTIONS[LanguageDropdown.current_text]
    
    
    def draw(self):
        # Normal Options
        pge.draw_rect(Position((10,90))*RATIO,Position((380,335))*RATIO,COLOR_DARK_BACKGROUND,2,COLOR_LIGHT_BORDER,alpha=230)
        pge.draw_rect(Position((400,90))*RATIO,Position((380,335))*RATIO,COLOR_DARK_BACKGROUND,2,COLOR_LIGHT_BORDER,alpha=230)
        pge.draw_text(Position((15,95))*RATIO,LGS.translate(7), PS16,pge.Colors.WHITE)
        
        # Visual Options
        pge.draw_rect(Position((10,450))*RATIO,Position((300,120))*RATIO,COLOR_DARK_BACKGROUND,2,COLOR_LIGHT_BORDER,alpha=230)
        pge.draw_text(Position((15,455))*RATIO,LGS.translate(28), PS16,pge.Colors.WHITE)
        
        
        
            
        # Draw Main Title
        pge.draw_text(Position((20,20))*RATIO,LGS.translate(45),RBG24, (125,90,115), alpha=80)
        pge.draw_text(Position((10,10))*RATIO,LGS.translate(45),RBG26, (255,255,255))
    def _update(self):
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
            VolumeSlider.value = self.cfg['volume']
            TrailCheck.value = self.cfg['mouse_trail']
            TrailColor.current_text = self.cfg["trail_color"]
            FloorColorDropwdown.current_text = self.cfg["floor_color"]
            LanguageDropdown.current_text = GAME_LANGUAGE_OPTIONS.index(self.cfg['lang'])
        GD.new_task(self.update_cfg, ())
        
        if BackButtonOptions.value:
            self.SCH.changeScreen(0x0)
            self.exiting()
        return super()._update()
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
        CONFIG['volume'] = self.cfg['volume']
        CONFIG['mouse_trail'] = self.cfg['mouse_trail']
        CONFIG['trail_color'] = self.cfg['trail_color']
        CONFIG['floor_color'] = self.cfg['floor_color']
        CONFIG['lang'] = self.cfg['lang']
        self.SCH.findScreen(0x4).exiting() # Resets the game :)
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