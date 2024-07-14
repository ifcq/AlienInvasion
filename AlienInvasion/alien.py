import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """表示外星人的类，继承自pygame.sprite的Sprite类"""
    def __init__(self, ai_game):
        super().__init__()
        """来自主文件的screen和setting的setting"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        """先定义好alien类的图像和矩形"""
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        """每次生成外星人实例都在屏幕的左上角，为了美观把高和宽设为了矩形的x和y"""
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        """存储精确位置"""
        self.x = float(self.rect.x)



    def update(self):
        """变成了x坐标乘以fleet_direction，"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        """这里大费周章同样还是因为rect（）方法不能自增浮点数，于是用self.x接受rect的x为浮点数，
        在加上同样为浮点数的alien_speed最后再传入到rect中"""
        self.rect.x = self.x



    def check_edges(self):
        """如果外星人到达了窗口边缘，就返回true"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)






