import sys
import pygame
from settings import Settings

title = '星舰大战'


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏窗口和游戏资源"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(self.settings.title)
        self.clock = pygame.time.Clock()

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            """侦听键盘和鼠标事件"""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # 让最近绘制的屏幕可见
            self.screen.fill(self.settings.bg_color)
            pygame.display.flip()
            self.clock.tick(165)


if __name__ == '__main__':
    # 创建游戏实例并运行
    ai = AlienInvasion()
    ai.run_game()

print(f'当前文件名：{__name__}')
