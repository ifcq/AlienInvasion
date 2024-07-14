import random
import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    """这个不负责记录，只负责显示得分"""
    def __init__(self, ai_game):
        """"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        """字体设置"""
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        """自动调用生成score的image 和 rect"""
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """每次实例化自动运行，将字体渲染为图像"""
        score_str = str(self.stats.score)
        self.score_image = self.font.render(f"Score : {score_str}", True, (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200)), self.settings.bg_color)

        """控制位置在屏幕右上角"""
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 10
        self.score_rect.top = self.screen_rect.top


    def prep_high_score(self):
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"High Score : {high_score}"
        self.high_score_image = self.font.render(high_score_str, True, (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200)), self.settings.bg_color)

        """图片和矩形位置"""
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 0


    def show_score(self):
        """在屏幕上绘制，待会放在update里面"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.leverl_rect)
        """Group里的方法"""
        self.ships.draw(self.screen)


    def check_high_score(self):
        """检查是否是最高分，在defeated中调用"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()


    def prep_level(self):
        """渲染等级"""
        level_str = f"Level : {self.stats.level}"
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        """图片和矩形位置"""
        self.leverl_rect = self.level_image.get_rect()
        self.leverl_rect.right = self.screen_rect.right - 10
        self.leverl_rect.top = self.leverl_rect.top + 50



    def prep_ships(self):
        """显示剩下的飞船，以图像的方式显示在左上角"""
        self.ships = Group()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)