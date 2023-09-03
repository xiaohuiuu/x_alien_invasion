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

