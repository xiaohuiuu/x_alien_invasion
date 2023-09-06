class Settings:
    """初始化游戏的设置"""

    def __init__(self):
        # 屏幕设置
        # 游戏窗口名字
        self.title = '外星人入侵'
        # 窗口宽度
        self.screen_width = 1200
        # 窗口高度
        self.screen_height = 800
        # 窗口的背景颜色
        self.bg_color = (230, 230, 230)

        # 控制飞船的
        self.ship_speed = 5
        self.ship_limit = 3

        # 子弹设置
        self.bullet_speed = 5.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allow = 6

        # 外星人相关设置
        self.alien_speed = 1.0
        # 外星人到达右边缘后向下移动的速度
        self.fleet_drop_speed = 4
        # 移动方向
        self.fleet_direction = 1

        # 以什么速度加快游戏的节奏
        self.speedup_scale = 1.5
        # 表示玩家每升级一个等级，游戏节奏翻一倍
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随着游戏进行而变化的设置"""
        self.ship_speed = 5.0
        self.bullet_speed = 5.0
        self.alien_speed = 1.0

        # fleed_direction为1表示方向向右，-1方向向左
        self.fleet_direction = 1

    def increase_speed(self):
        """提高速度设置的值"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

