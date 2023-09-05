import pygame


class Ship:
    """管理飞船的类"""

    def __init__(self, ai_game):
        """初始化飞船并设置它的初始位置"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        self.settings = ai_game.settings

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('image/SpaceShip_0.png')
        self.rect = self.image.get_rect()

        # 每艘新飞船都放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom

        # 判断飞船是否移动的标志
        self.move_right = False
        self.move_left = False

        self.x = float(self.rect.x)

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """根据移动标志移动飞船"""
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.move_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        # 根据self.x的值更新飞船的位置
        self.rect.x = self.x

    def center_ship(self):
        """将飞船放在屏幕底部中央"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
