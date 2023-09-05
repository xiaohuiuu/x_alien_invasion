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

## 七 简单回顾

## 八 射击

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

## 九 创建第一个外星人

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

## 十 让外星舰队移动

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

