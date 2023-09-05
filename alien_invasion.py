import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet

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
        # 实例化飞船
        self.ship = Ship(self)
        # 子弹
        self.bullets = pygame.sprite.Group()

    def _check_event(self):
        """侦听键盘和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_key_down(event)
            elif event.type == pygame.KEYUP:
                self._check_key_up(event)

    def _update_screen(self):
        """更新屏幕"""
        # 让最近绘制的屏幕可见
        self.screen.fill(self.settings.bg_color)
        # 画出子弹
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # 画出飞船
        self.ship.blitme()
        pygame.display.flip()

    def _check_key_down(self, event):
        """检测键盘按下事件"""
        if event.key == pygame.K_RIGHT:
            self.ship.move_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.move_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        # 按q键退出
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_key_up(self, event):
        """检测键盘按下松开事件"""
        if event.key == pygame.K_RIGHT:
            self.ship.move_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.move_left = False

    def _fire_bullet(self):
        """创建一颗子弹，并将它加入到bullets中"""
        if len(self.bullets) < self.settings.bullets_allow:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_event()
            self.ship.update()
            self.bullets.update()
            # 删除已经消失的子弹
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
            self._update_screen()
            self.clock.tick(165)


print(f'当前文件名：{__name__}')
if __name__ == '__main__':
    # 创建游戏实例并运行
    ai = AlienInvasion()
    ai.run_game()
