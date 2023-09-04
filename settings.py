class Settings:
    """初始化游戏的设置"""
    def __init__(self):
        # 游戏窗口名字
        self.title = '外星人入侵'
        # 窗口宽度
        self.screen_width = 1200
        # 窗口高度
        self.screen_height = 800
        # 窗口的背景颜色
        self.bg_color = (230, 230, 230)
        # 控制飞船的速度
        self.ship_speed = 5
