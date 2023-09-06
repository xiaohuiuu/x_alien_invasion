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

    # 为了将要显示的文本转换为图像，调用一下函数
    def prep_score(self):
        """渲染为图像"""
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # 在屏幕的右上角显示得分
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
