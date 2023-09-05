import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

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
        # 外星人舰队
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def _check_event(self):
        """侦听键盘和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_key_down(event)
            elif event.type == pygame.KEYUP:
                self._check_key_up(event)

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

    def _update_bullets(self):
        """更新子弹的位置，并删除已经消失的子弹的位置"""
        # 更新子弹的位置
        self.bullets.update()
        # 删除已经消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _create_fleet(self):
        """创建一个外星人舰队"""
        # 外星人的间距为外星人的宽度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # 添加一行外星人后，重置x值并递增y值
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _change_fleet_direction(self):
        """将整个外星人舰队向下移动，并修改移动方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_fleet_edges(self):
        """在有外星人到达屏幕边缘后需要做的事"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def update_alien(self):
        """更新外星人位置的方法"""
        self._check_fleet_edges()
        self.aliens.update()

    def _update_screen(self):
        """更新屏幕"""
        # 让最近绘制的屏幕可见
        self.screen.fill(self.settings.bg_color)
        # 画出子弹
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # 画出飞船
        self.aliens.draw(self.screen)
        self.ship.blitme()
        pygame.display.flip()

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_event()
            self.ship.update()
            self.update_alien()
            self._update_bullets()
            self._update_screen()
            self.clock.tick(165)


print(f'当前文件名：{__name__}')
if __name__ == '__main__':
    # 创建游戏实例并运行
    ai = AlienInvasion()
    ai.run_game()
