import pygame.font

class Button:
    """游戏的按钮类"""
    def __init__(self, ai_game, msg):
        """将主文件里的实例化了的ai类的screen属性赋值到这里来"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        """导入setting类"""
        self.settings = ai_game.settings

        """设置按钮的尺寸和其他属性，哦不，都在设置类里了,字体名字None让程序使用默认字体"""
        self.font = pygame.font.SysFont(None, 48)

        """创建按钮的rect对象并居中"""
        self.rect = pygame.Rect(0, 0, self.settings.button_width, self.settings.button_height)
        self.rect.center = self.screen_rect.center

        """msg 就是massage，会打印在按钮上的, 放在这里，在每次实例化的时候都会调用"""
        self.prep_msg(msg)




    def prep_msg(self, msg):
        """不用担心，实例化的时候会自动调用，将输入的文字对象转化为图像并放在按钮上"""
        self.msg_image = self.font.render(msg, True, self.settings.button_text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """先用颜色填充按钮在绘制文字图像"""
        self.screen.fill(self.settings.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)



