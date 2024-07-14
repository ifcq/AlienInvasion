import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_game):
        """initialize your ship position here."""
        super().__init__()

        """get the screen and its rect"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = self.screen.get_rect()

        """load ship image to self.image and get its rect to self.rect"""
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        """every ship will on the bottom of the screen."""
        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)

        self.moving_right = False
        self.moving_left = False



    def update(self):
        """根据状态移动飞船位置"""
        if self.moving_right and (self.rect.right < self.screen_rect.right):
            self.x += self.settings.ship_speed
        if self.moving_left and (self.rect.left > 0):
            self.x -= self.settings.ship_speed

        # 更新ship 的 rect 的 x
        self.rect.x = self.x


    def blit_ship(self):
        """ blit your ship """
        self.screen.blit(self.image, self.rect)


    def moving_center(self):
        """飞船放在底部中间位置，在扣血时调用一次, 点击开始按钮也会调用一次"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
