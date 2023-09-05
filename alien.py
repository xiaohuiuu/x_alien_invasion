import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """表示单个外星人的类"""

    def __init__(self, ai_game):
        """初始化外星人，并设置起始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # 加载外星人图像并设置其rect属性
        self.image = pygame.image.load('image/alienn.png')
        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕的左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 储存外星人精确水平位置
        self.x = float(self.rect.x)

    def update(self):
        """向右或向左移动外星人"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        """如果外星人到达了屏幕边缘，返回TRUE"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
