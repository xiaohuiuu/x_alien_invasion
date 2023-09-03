import sys
import pygame

title = '星舰大战'


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏窗口和游戏资源"""
        pygame.init()

        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption(title)
        self.bg_color = (230, 230, 230)
        self.clock = pygame.time.Clock()

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            """侦听键盘和鼠标事件"""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # 让最近绘制的屏幕可见
            self.screen.fill(self.bg_color)
            pygame.display.flip()
            self.clock.tick(165)


if __name__ == '__main__':
    # 创建游戏实例并运行
    ai = AlienInvasion()
    ai.run_game()

print(f'当前文件名：{__name__}')
