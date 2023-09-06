# alien_invasion的开发流程

## 一：项目规划

## 二：安装pygame

python -m pip install --user pygame

## 三：开始游戏项目

### 1 创建pygame窗口以及响应用户的输入

创建一个游戏的类，创建空的pygame窗口

```python
import sys
import pygame


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏窗口和游戏资源"""
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            """侦听键盘和鼠标事件"""
            for event in pygame.event.get():
                if event.type == pygame.quit():
                    sys.exit()

            # 让最近绘制的屏幕可见
            pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例并运行
    ai = AlienInvasion()
    ai.run_game()

```

### 2 控制帧率

pygame 使用 clock控制帧率，如果这个循环的通过速度超过我们定义的帧率时，pygame会计算需要暂停多长时间，以便游戏运行的速度保持一致。

```python
# 我们在__init__()方法中定义这个时钟
def __init__(self):
    pygame.init()
    self.clock = pygame.time.Clock()
    
# 初始化pygame后，创建pygame.time模块中的Clock类的一个实例，然后在run_game()的while循环末尾让这个时钟# 进行计时
def run_game(self):
    while True:
        pygame.display.flip()
        self.clock.tick(60)
# tick()方法接受一个参数，是你想让游戏运行游戏的帧率
```

### 3 设置背景色

pygame默认创建一个黑色的北京，我们可以在__init__()方法将背景颜色设置为其他颜色

```python
def __init__(self):
    #跳过其他代码
    pygame.display.set_caption('星舰大战')
    
    #设置北京颜色
    self.bg_color = (230, 230, 230)
    
def run_game(self):
    
    #每次循环都重绘屏幕
    self.screen.fill(self.bg_color)
    pygame.display.flip()
    self.clock.tick(165)
```

### 4 创建setting类

每次给游戏添加新的功能时，我们都需要引入一些新的设置，下面来编写一个Setting模块，其中包含一个Setting类，用于储存设置，以免于在代码中到处添加其他的设置，看着简洁

```python
class Settings:
    """初始化游戏的设置"""
    def __init__(self):
        # 游戏窗口名字
        self.title = '星舰大战'
        # 窗口宽度
        self.screen_width = 1200
        # 窗口高度
        self.screen_height = 800
        # 窗口的背景颜色
        self.bg_color = (230, 230, 230)
        
# 我们在alien_invasion做以下修改
from settings import Settings
def __init__(self):
    self.settings = Settings()
    self.screen = 								pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
    
    
def run_game(self):
    self.screen.fill(self.settings.bg_color)
```

## 四：添加飞船图像

下面将飞船加入游戏，为了在屏幕上绘制飞船，需要先加载一个图像，使用pygame.blit()去绘制它

### 1 创建ship类

```python
import pygame


class Ship:
    """管理飞船的类"""

    def __init__(self, ai_game):
        """初始化飞船并设置它的初始位置"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('image/SpaceShip_0.png')
        self.rect = self.image.get_rect()

        # 每艘新飞船都放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

```

### 2 在屏幕上绘制飞船

```python
# 接下来更新alien_invasion.py,创建一艘飞船，并调用其方法blitme()

from settings import Settings
from ship import Ship

class AlienInvasion:
    def __init__(self):
        self.ship = Ship(self)
        
    def run_game(self):
        self.ship.blitem()
```

## 五：重构 \_check_event()方法和_update_screen()方法

在大型项目中，经常需要在添加新代码前重构既有的代码。重构旨在简化既有的代码的结构，使其更容易扩展。在本环节把越来越长的run_game()方法拆成两个辅助方法。辅助方法一般只在类中调用，不会在类外调用。在Python中，辅助方法使用单下划线打头。

### 1 \_check_event方法

```python
# 我们把管理事件的代码移动到_check_event()方法中，以简化run_game()方法并隔离时间循环。
def run_game(self):
    while True:
        self._check_event()
    
def _check_event(self):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
    	if event.type == pygame.QUIT:
    		sys.exit()
```

### 2 _update_screen方法

```python
# 为了更进一步的简化run_game()方法，我们把更新屏幕的代码移动到_update_screen()方法中
def run_game(self):
    while True:
        self._check_event()
    	self._update_screen()
		self.clock.tick(165)
def _update_screen(self):
    # 让最近绘制的屏幕可见
            self.screen.fill(self.settings.bg_color)
            # 画出飞船
            self.ship.blitme()
            pygame.display.flip()
            
```

## 六：驾驶飞船

### 1 响应按键并允许持续向右移动

在pygame中，时间都是pygame.event.get()获取的，需要在\_check_event()中指定要检查事件的类型，没当用户按下一个键时，都会在pygame中产生一个keydown事件。

```python
    def _check_event(self):
        """侦听键盘和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    # 飞船向右移动
                    self.ship.rect.x += 10
                elif event.key == pygame.K_LEFT:
                    # 飞船向左移动
                    self.ship.rect.x -= 10
    # 但这样优缺点，我们需要按一次键，它移动一次，
    # 我们需要将它改动成，按下键不松开，他就一直移动
    # 这时候，我们需要使用keyup事件类型，并且，我们设置一个标志move_right为False,当move_right为false  	 # 时，飞船不会移动，当keydown时，move_right为True，飞船移动，当keyup时，move_right为False，飞船	  # 停止移动
```

### 2 左右移动

对ship类和update()方法进行修改

```python
def __init__(self):
    # 移动标志
    move_right = False
    move_left = False
    
update(self):
    if move_right:
        self.rect.x += 10
    if move_left:
        self.rect.x -= 10
```

还需要对\_check_event()进行修改

```python
def _check_event(self):
    """侦听键盘和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.ship.move_right = True
            elif event.key == pygame.K_LEFT:
                self.ship.move_left = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                self.ship.move_right = False
            elif event.key == pygame.K_LEFT:
                self.ship.move_left = False
```

### 3 调整飞船的速度

```python
# 我们可以在Settings类追溯添加属性ship_speed来控制飞船的速度
class Settings:
    def __init__(self):
        self.ship_speed = 5
        
class Ship:
    def __init__(self,ai_game):
        self.settings = ai_game.settings
        
        # 在飞船的属性x存储一个浮点数
        self.x = float(self.rect.x)
        
    def update(self):
        if self.move_right:
            self.x += self.settings.ship_speed
        if self.move_left:
            self.x -= self.settings.ship_speed
        # 根据self.x的值更新飞船的位置
```

### 4 限制飞船的活动范围

目前，当我们按住方向键足够长的时间，飞船就会飞到屏幕的外边，所以我们要修改ship类的update方法。

```python
    def update(self):
        """根据移动标志移动飞船"""
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.move_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        # 根据self.x的值更新飞船的位置
        self.rect.x = self.x
```

### 5 重构\_check_event()方法

随着游戏的开发，此函数又变得越来越长，因此，我们将keydown和keyup拆分成两个方法

```python
def _check_event(self):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            self._check_key_down(event)
        elif event.type == pygame.KEYUP:
            self._check_key_up(event)



def _check_key_down(self, event):
     if event.key == pygame.K_RIGHT:
           self.ship.move_right = True
     elif event.key == pygame.K_LEFT:
           self.ship.move_left = True

def _check_key_up(self, event):
     if event.key == pygame.K_RIGHT:
     	 self.ship.move_right = False
     elif event.key == pygame.K_LEFT:
         self.ship.move_left = False
```

### 6 按q键退出

```python
    def _check_key_down(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.move_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.move_left = True  
        elif event.key == pygame.K_q:
            sys.exit()
```

### 7 在全屏模式下运行游戏

```python
def __init__(self):
    self.settings = Settings()
    self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    self.settings.screen_width = self.screen.get_rect().width
    self.settings.screen_height = self.screen.get_rect().height
```

## 七：简单回顾

## 八：射击

接下来 添加射击子弹的功能，我们将编写在玩家按空格时发射子弹（用 小矩形表示）的代码，子弹将在屏幕中直线上升，并在屏幕到达边缘消失

### 1 添加子弹设置

首先，更新Settings类，在\__init__()方法末尾储存新类Bullet所需的值

```python
def __init__(self):
    # 子弹设置
    self.bullet_speed = 5.0
    self.bullet_width = 3
    self.bullet_height = 15
    self.bullet_color = (60, 60, 60)
```

### 2 创建Bullet类

```python
import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """管理飞船所发射的子弹的类"""

    def __init__(self, ai_game):
        """在飞船的当前位置创建一个子弹对象"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = ai_game.settings.bullet_color

        # 在(0,0)处创建一个表示子弹的矩形
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # 储存用浮点数表示子弹的y值
        self.y = float(self.rect.y)

    def update(self):
        """向上移动子弹"""
        # 更新子弹的位置
        self.y -= self.settings.bullet_speed
        # 更新表示子弹位置
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)
```

### 3 将子弹存储到编组中

在定义好Bullet类和必要的设置后，便可以编写代码每一次按下空格发射一颗子弹了，我们将在Alien_invasion类中创建一个编组，来保存所有有效的子弹，一遍管理发射出去的所有的子弹。这个编组是一个Group类（来自pygame.Sprite模块)的一个实例。Group类似于列表，但是提供了有助于开发游戏的额外功能

首先，导入新的Bullet类

```python
from bullet import Bullet
```

接下来，在\__init__()中创建用于储存子弹的编组

```python
def __init__(self):
    self.ship = Ship(self)
    self.bullets = pygame.sprite.Group()
    
```

然后在while循环中更新子弹的位置

```python
def run_game(self):
    while True:
        self._check_event()
        self.ship.update()
        self.bullets.update()
        self._update_screen()
        self.clock.tick(165)
```

### 4 开火

在AlienInvasion中，需要修改\_check_key_down()，以便玩家按空格时发射一颗子弹，还需要修改\_update_screen()，确保在调用flip()前在屏幕上重绘子弹

为了发射子弹，需要做的工作不少，因此编写一个新方法\_fire_bullet()来完成这个任务

```python
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
    
    def _fire_bullet(self):
        """创建一颗子弹，并将它加入到bullets中"""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)
        
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
```

### 5 删除已经消失的子弹

虽然目前子弹会在屏幕边缘消失，但是，仅仅是因为子弹无法在pygame窗口外渲染，实际上子弹依然存在。

随着发射的子弹越来越多，占用系统的资源也越来越大，所以我们需要将小时的子弹删除，

很简单，当子弹的y=0时，删除

```python
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
```

### 6 限制子弹的数量

首先将允许的子弹的数量设置保存在Settings类中

```python
class Settings:
    def __init__(self):
        self.bullets_allow = 6
```

在Alien_invasion中的\_fire_bullet中检测当前屏幕的子弹数量，如果小于6个，再发射子弹

```python
    def _fire_bullet(self):
        """创建一颗子弹，并将它加入到bullets中"""
        if len(self.bullets) < self.settings.bullets_allow
        	new_bullet = Bullet(self)
        	self.bullets.add(new_bullet)
```

### 7 创建\_update_bullets()方法

编写并仔细检查子弹管理代码后，可以将这些代码移动台一个独立的方法中，以确保Alien_Invasion类整洁。

创建一个名为\_update_bullets的新方法，并放在\_update_screen方法之前。

```python
def _update_bullets(self):
    """更新子弹的位置，并删除已经消失的子弹的位置"""
    # 更新子弹的位置
    self.bullets.update()
    # 删除已经消失的子弹
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
```

## 九：创建第一个外星人

### 1 创建Alien类

```python
import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """表示单个外星人的类"""
    def __init__(self, ai_game):
        """初始化外星人，并设置起始位置"""
        super().__init__()
        self.screen = ai_game.screen

        # 加载外星人图像并设置其rect属性
        self.image = pygame.image.load('image/alien.png')
        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕的左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 储存外星人精确水平位置
        self.x = float(self.rect.x)

```

### 2 创建Alien实例

要想要第一个外星人出现在屏幕上，我们需要创建Alien实例，这属于初始化工作之一，因此需要将代码放在Alien_Invasion类的\__init__方法的末尾，我们最终会创建一个外星人舰队，设计的工作量不少，因此新建一个

\_create_fleet（）方法

```python
from alien import Alien

def __init__(self):
    self.aliens = pygame.sprite.Group()
    
    self._create_fleet()
    
    
def _create_fleet(self):
    """创建一个外星人舰队"""
    alien = Alien(self)
    self.aliens = add(alien)
```

要想外星人现身，需要在\_update_screen()方法中draw

```python
def _update_screen(self):
    self.aliens.draw(self.screen)
```

### 3 创建一个外星人舰队

```python
def _create_fleet(self):
    """创建一个外星人舰队"""
    # 外星人的间距为外星人的宽度
    alien = Alien(self)
    alien_width = alien.rect.width
    
    current_x = alien_width
    while current_x < (self.settings.screen_width -2 * alien_width):
        new_alien = Alien(self)
        new_alien.x = current_x
        new_alien.rect.x = current_x
        self.aliens.add(new_alien)
        current_x += 2 * alien_width
```

### 4 重构\_create_fleet()

```python
def _create_fleet(self):
    while current_x < (self.setting.screen_width -2 * alien_width):
        self._create_alien(current_x)
        current_x += 2 * alien_width

def _create_alien(self, x_position):
    """创建一个外星人并放在当前行中"""
    new_alien = Alien(self)
    new_alien.rect.x = x_position
    self.aliens.add(new_alien)
```

### 5 添加多行外星人

 ```python
 def _create_fleet(self):
     alien = Alien(self)
     alien_width, alien_height = alien.rect.size
     current_x, current_y = alien_width, alien_height
     while current_y < (self.settings.screen_height -3 * alien_height):
         while current_x < (self.settings.screen_width -2 * alien_width):
             self._create_alien(current_x, current_y)
             current_x += 2 * alien_width
         
         # 添加一行外星人后，重置x值并递增y值
         current_x = alien_width
         current_y += 2 * alien_height
 ```

修改\_create_alien()，以正确的设置外星人的垂直位置

```python
def _create_alien(self, x_position, y_position):
    new_alien = Alien(self)
    new_alien.x = x_position
    new_alien.rect.x = x_position
    new_alien.rect.y = y_position
    self.aliens.add(new_alien)
```

## 十 ：让外星舰队移动

### 1 向右移动外星舰队

移动外星舰队需要使用alien.py中的update()方法，对于外星舰队中的每个外星人都需要调用方法，首先添加一个控制外星人速度的设置

```python
def __init__(self):
    self.alien_speed = 1.0
```

然后在alien.py中实现update()

```python
def update(self):
    """向右移动外星人"""
    self.x += self.settings.alien_speed
    self.rect.x = self.x
```

### 2 创建表示外星人移动方向的设置

下面创建表示外星人到达屏幕右边缘后，向下移动，再向左移动。实现这种行为的代码

```python
# 外星人到达右边缘后向下移动的速度
        self.fleet_drop_speed = 4
        # 移动方向
        self.fleet_direction = 1
```

实现fleet_direction可以实用文本，例如，left和right，但是这样需要使用if语句来实现外星人的移动，所以我们使用1和-1来表示方向

### 3 检查外星人是否到达了屏幕边缘

现在需要些一个方法来判断外星人是否到达了屏幕边缘，还需要修改update()来外星人沿着正确的方向移动

```python
def check_edges(self):
    """如果外星人到达了屏幕边缘，返回TRUE"""
    screen_rect = self.screen.get_rect()
    return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
```

修改update()

```python
def update(self):
    """向右或向左移动外星人"""
    self.x += self.settings.alien_speed * self.settings.fleet_direction
    self.rect.x = self.x
```

### 4 向下移动外星舰队并改变移动方向

当有外星人到达左右边缘时，需要整个外星人舰队向下移动并改变他们的移动方向

需要在Alien_Invasion中添加两个方法，\_check_fleet_edges()和\_change_fleet_direction()，并修改\_update_alien()

```python
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
```

对update_alien()的修改

```python
def update_alien(self):
    """更新外星人位置的方法"""
    self._check_fleet_edges()
    self.aliens.update()
```

## 十一：击落外星人

### 1 检查子弹和外星人的碰撞

为了让子弹能够击落外星人，我们将使用sprite.groupcollide()检测两个编组成员之间的碰撞

当子弹击中外星人后，我们需要马上知道，一遍在碰撞发生之后让子弹立即消失。为此。。将在更新所有子弹的位置后（绘制子弹前）立即检查碰撞。

sprite.groupcollide()函数将一个编组中的每一个rect元素与另一个编组的所有的rect元素进行比较，并返回一个字典，其中包含了发生碰撞的子弹和外星人

在\_update_bullets()方法末尾，添加如下检查子弹和外星人碰撞的代码

```python
def _update_bullets(self):
    """更新子弹的位置，并删除已经消失的子弹"""
    
    # 检查是否有子弹击中了外星人
    # 如果是，就删除响应的子弹和外星人
    collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
```

### 2 生成新的外星人舰队

这个游戏的特点是，当一个外星人舰队别完全消灭后，又出现新的外星人舰队

检查aliens编组是否为空，如果为空，调用\_create_fleet()，我们将在\_update_bullets()末尾执行这项任务，，因为外星人都是在这里击落的。

```python
def _update_bullets(self):
    """删除现有的子弹，并创建新的外星人舰队"""
    if not self.aliens:
        self.bullets.empty()
        self._create_fleet()
```

### 3 重构\_update_bullets()

可以将子弹和外星人碰撞的代码移动到新的方法中

```python
    def _update_bullets(self):
        """更新子弹的位置，并删除已经消失的子弹的位置"""
        # 更新子弹的位置
        self.bullets.update()
        # 删除已经消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # 检查是否有子弹击中了外星人
        # 如果是，就删除响应的子弹和外星人
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """响应外星人和子弹的碰撞"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        # 删除现有的子弹，并创建新的外星人舰队
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
```

## 十二：结束游戏

如果玩家没有在足够短的时间内击败所有的外星人，导致有外星人撞到了飞船或到达了屏幕的下边缘，飞船将被摧毁，与此同时，我们会限制飞船的数量，在玩家用光所有的飞船后，游戏将结束。

### 1 检查外星人和飞船的碰撞

```python
def _update_alien(self):
    
    # 检测外星人和飞船的碰撞
    if pygame.sprite.spritecollideany(self.ship, self.aliens):
        print('ship hit')
```

### 2 响应外星人和飞船的碰撞

我们需要确定，当外星人和飞船发生碰撞后，该做些什么，我们不是销毁ship实例再创建，而是跟踪游戏的统计信息来几率飞船碰撞了几次

下面来编写用于统计游戏信息的新类GameStats,保存为game_stats.py

```python
class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_game):
        """初始化信息"""
        self.settings = ai_game.settings
        self.ships_left = 0
        self.reset_stats()

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.settings.ship_limit
```

AlienInvasion也需要实例化这个类

```python
from time import sleep
from game_stats import GameStats
class AlienInvasion:
    def __init__(self):
        # 实例化gamestats
        self.stats = GameStats(self)
        
```

当外星人撞到飞船后，将剩余飞船数量-1，并创建一个新的外星舰队，并将飞船重新放在底部中间，并让游戏暂停一会，让玩家意识到撞到了飞船，并在创建新的外星舰队前重整旗鼓

```python
def _ship_hit(self):
    """响应飞船和外星人的碰撞"""
    # 将ship_left -1
    self.stats.ships_left -= 1
    # 清空外星人列表和子弹列表
    self.bullets.empty()
    self.aliens.empty()
    # 创建一个新的外星人舰队,并将飞船放在屏幕底部的中央
    self._create_alien()
    self.ship.center_ship()
    # 暂停
    sleep(0.5)
```

在\_update_aliens()中，当有外星人撞到飞船使，使用\_ship_hit()函数

```python
def update_alien(self):
    """更新外星人位置的方法"""
    self._check_fleet_edges()
    self.aliens.update()

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(self.ship, self.aliens):
        self._ship_hit()
```

将center_ship(self)添加到ship类中

```python
def center_ship(self):
    """将飞船放在屏幕底部中央"""
    self.rect.midbottom = self.screen_rect.midbottom
    self.x = float(self.rect.x)
```

### 3 有外星人达到屏幕的下边缘

为了检测这种情况，我们在alien_invasion添加新的方法

```python
def _check_aliens_bottom(self):
    """检查是否有外星人到达了屏幕底部"""
    for alien in self.aliens.sprites():
        if alien.rect.bottom >= self.settings.screen_height:
            # 和外星人碰撞到飞船一样的处理
            self._ship_hit()
            break
```

在update_aliens()中调用\_check_aliens_bottom()

```python
def update_aliens(self):
    self._check_aliens_bottom()
```

### 4 游戏结束

现在游戏看起来完整了，但永远不会结束

我们需要在飞船用完之后游戏结束

我们需要在alien_invasion中设置game_active属性来控制游戏

```python
def __init__(self):
    self.game_active = True
```



接下来在\_ship_hit()中添加代码，在玩家的飞船用完之后，将game_active设置为False

```python
def _ship_hit(self):
    """响应飞船和外星人的碰撞"""
    if self.stats.ships_left > 0:
        # 将ship_left -1
        self.stats.ships_left -= 1
        # 清空外星人列表和子弹列表
        self.bullets.empty()
        self.aliens.empty()
        # 创建一个新的外星人舰队,并将飞船放在屏幕底部的中央
        self._create_fleet()
        self.ship.center_ship()
        # 暂停
        sleep(0.5)
    else:
        self.game_active = False
```

### 5 确定应运行游戏的哪些部分

我们需要确定哪些部分是在游戏处于活跃状态下才运行

```python
def run_game(self):
    """开始游戏的主循环"""
    while True:
        self._check_event()
        if self.game_active:
            self.ship.update()
            self.update_alien()
            self._update_bullets()
            self._update_screen()
            self.clock.tick(165)
```

## 十三：计分，添加play按钮

本节添加一个play按钮，它在游戏开始前和游戏结束后出现，让玩家能够开始新的游戏

 当前这个游戏在玩家运行alien_invasion..py是就开始了，下面让游戏在一开始处于非活跃状态，并提示玩家点击开始游戏，修改AlienInvasion类的\__init__()方法

```python
def __init__(self):
    self.game_active = False
```

### 1 创建button类

pygame没有内置的创建按钮的方法，我们将编写一个button类，用于创建一个带标签的实心矩形

```python
import pygame.font


class Button:
    """微游戏创建按钮的类"""

    def __init__(self, ai_game, msg):
        """初始化按钮属性"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # 设置按钮的尺寸和其他属性
        self.width, self.height = 200, 50
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 244)
        self.font = pygame.font.SysFont(None, 48)

        # 创建按钮的rect对象，并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 按钮标签只需要创建一次
        self._prep_msg(msg)
        
        def _prep_msg(self, msg):
    		"""将msg渲染为图像，并使其在按钮上居中"""
    		self.msg_image = self.font.render(msg, True, self.text_color, 		self.button_color)
    		self.msg_image_rect = self.msg_image.get_rect()
    		self.msg_image_rect.center = self.rect.center
```

创建\_prep_msg

```python
def _prep_msg(self, msg):
    """将msg渲染为图像，并使其在按钮上居中"""
    self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
    self.msg_image_rect = self.msg_image.get_rect()
    self.msg_image_rect.center = self.rect.center
```

最后，创建draw_button()方法

```python
def draw_button(self):
    """绘制一个用颜色填充的按钮，再绘制文本"""
    self.screen.fill(self.button_color,self.rect)
    self.screen.blit(self.msg_image, self.msg_image_rect)
```

### 2 在屏幕上绘制按钮

在类AlienInvasion中使用Button类创建一个按钮

```python
from button import Button

class AlienInvasion:
    def __init__(self):
        self.play_button = Button(self, 'play')
```

要想显示按钮，我们需要在\_update_screen中钓友draw_button（）方法

```python
def _update_screen(self):
    # 如果游戏处于非活跃状态（game_active = False)，绘制play按钮
    if not self.game_active:
        self.play_button.draw_button()
```

### 3 开始游戏

为了实现点击play按钮开始游戏，在_check_event()末尾添加一下elif代码块，以监视与这个按钮相关的鼠标事件

```python
def _check_event(self):
    """侦听键盘和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            self._check_key_down(event)
        elif event.type == pygame.KEYUP:
            self._check_key_up(event)
        # 添加检测鼠标相关事件
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            self._check_play_button(mouse_pos)
```

\_check_play_button()的代码如下

```python
def _check_play_button(self, mouse_pos):
    """在玩家点击play后开始游戏"""
    if self.play_button.rect.collidepoint(mouse_pos):
        self.game_active = True
```

### 4 重置游戏

前面编写的代码只处理了第一次开始游戏的情况，并没有处理游戏结束的情况，

为了每次玩家点击play都重置游戏，需要重置统计信息，删除现有的外星人和子弹，创建一个新的外星舰队并让飞机居中。

```python
def _check_play_button(self, mouse_pos):
    """在玩家点击play后开始游戏"""
    if self.play_button.rect.collidepoint(mouse_pos):
        # 重置游戏的统计信息
        self.stats.reset_stats()
        self.game_active = True

        # 清空外星人列表和子弹
        self.bullets.empty()
        self.aliens.empty()

        # 创建一个新的外星人舰队，并放在底部中央
        self._create_fleet()
        self.ship.center_ship()

```

### 5 将play按钮切换到非活跃状态

当前存在一个问题，在游戏进行的过程中，即使pygame为渲染play按钮，但不小心鼠标点到之前按钮渲染的位置，游戏将重新开始

为了修复这个问题，我们仅在game_active = False时才开始

```python
def _check_play_button(self, mouse_pos):
    """在玩家点击play后开始游戏"""
    button_clilked = self.play_button.rect.collidepoint(mouse_pos)
    if button_clilked and not self.game_active:
        # 重置游戏的统计信息
        self.stats.reset_stats()
        self.game_active = True

        # 清空外星人列表和子弹
        self.bullets.empty()
        self.aliens.empty()

        # 创建一个新的外星人舰队，并放在底部中央
        self._create_fleet()
        self.ship.center_ship()
```

### 6 隐藏光标

当游戏处于非活跃状态时，我们让光标处于可见，当游戏开始时，隐藏光标

```python
# 在_check_play_button中添加一下代码
pygame.mouse.set_visible(False)
```

游戏结束后，将重新展示光标

在\_ship_hit()中添加一下代码

```python
# 展示光标
     pygame.mouse.set_visible(True)
```

## 十四：提高难度

### 1 修改速度设置

首先重新组织Settings类，将游戏设置分为两组，动态和静态的，随着游戏进行而变化的设置，还要确保开始游戏时重置。settings.py的\__init__()方法如下

```python
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
        self.bullets_allow = 3

        # 外星人相关设置
        self.alien_speed = 1.0
        # 外星人到达右边缘后向下移动的速度
        self.fleet_drop_speed = 20
        # 移动方向
        self.fleet_direction = 1

        # 以什么速度加快游戏的节奏
        self.speedup_scale = 1.1
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
        

```

在\_check_bullet_alien_alien_collisions(self)中，在整个外星舰队被击落时调用increase_speed()来加快节奏

```python
def _check_bullet_alien_collisions(self):
    self.settings.increase_speed()
```

### 2 重置速度

每当玩家开始新的游戏时，需要将变化的设置还原为初始值

```python
def _check_play_button(self):
    # 还原游戏设置
    self.settings.initialize_dynamic_settings()
```

## 十五：计分

下面实现计分系统，实施的跟踪玩家的得分，并显示最高分，等级和剩下的飞船数。

GameStats

```python
class GameStats:
    def reset_stats(self):
        self.score = 0
```

### 1 显示得分

为了屏幕上显示得分，首先创建一个新类ScoreBoard，这个类只显示当前得分，但后面也将显示最高分，等级和剩下的飞船数量，

```python
import pygame.font


class ScoreBoard:
    """显示得分信息的类"""

    def __init__(self, ai_game):
        """初始化得分相关的属性"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # 现实得分信息使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # 准备初始化图像
        self.prep_score()
```

为了将要显示的文本转换为图像，调用一下函数

```python
def prep_score(self):
    """渲染为图像"""
    score_str = str(self.stats.score)
    self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

    # 在屏幕的右上角显示得分
    self.score_rect = self.score_image.get_rect()
    self.score_rect.right = self.screec_rect.right - 20
    self.score_rect.top = 20
```

接下来创建show_score()方法

```python
    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
```

### 2 创建记分牌

为了显示得分，在AlienInvasion中创建一个ScoreBoard实例，

然后在update_screen中调用

```python
class AlienInvasion:
    def __init__(self):
        self.sb = ScoreBoard(self)
        
        
    def _update_screen(self):
        self.sb.show_score()
```

