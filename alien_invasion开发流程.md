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

