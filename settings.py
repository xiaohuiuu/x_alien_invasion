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

        # 子弹设置
        self.bullet_speed = 5.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allow = 3

        # 外星人相关设置
        self.alien_speed = 1.0
        # 外星人到达右边缘后向下移动的速度
        self.fleet_drop_speed = 4
        # 移动方向
        self.fleet_direction = 1
