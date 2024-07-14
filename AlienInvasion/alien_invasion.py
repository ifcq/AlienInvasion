import sys
import pygame
from setting import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from stats import Stats
from time import sleep
from button import Button
from scoreboard import Scoreboard
from sounds import Sound
from texiao import Explosion


class AlienInvasion:
    def __init__(self):
        """Initialize alien invasion."""
        pygame.init()

        self.game_active = False

        self.sound = Sound()

        self.settings = Settings()
        """可以储存游戏数据的stats实例"""
        self.stats = Stats(self)
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        self.play_button = Button(self, 'Play')
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        """创建子弹组，在后面检测事件方法中才会调用，并将实例化的的子弹加入子弹组中，"""
        self.bullets = pygame.sprite.Group()
        """创建外星人组，在后面创建了一个生成外星人方法_creat_fleet将创建好的外星人加入到外星人组中"""
        self.aliens = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self._creat_fleet()

        self.clock = pygame.time.Clock()
        pygame.display.set_caption(self.settings.caption)

    def _check_event(self):
        """辅助方法，只会在类中调用，这个方法检查键盘事件并做出回应"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stats.save_highest_score(self.stats.high_score)
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                """鼠标按下事件"""
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)


    def _check_play_button(self, mouse_pos):
        """检查是否按下play按钮，如果按下，则修改game_active的状态"""
        if (self.play_button.rect.collidepoint(mouse_pos)) and (not self.game_active):
            """重置统计信息"""
            self.stats.reset_stats()
            self.game_active = True

            """清空子弹组和外星人组"""
            self.bullets.empty()
            self.aliens.empty()

            """创建新舰队，从次游戏走向循环"""
            self._creat_fleet()
            self.ship.moving_center()

            """画上剩余飞船数量"""
            self.sb.prep_ships()


    def _creat_fleet(self):
        """创建外星人组，并将其加入到外星人组中"""
        alien = Alien(self)
        #不断添加外星人知道窗口再也没有空间，为了避免拥挤，创建外星人的间距为一个外星人的宽度及以上
        self.aliens.add(alien)
        alien_width = alien.rect.width
        alien_height = alien.rect.height

        """两层循环，第一层选择y坐标，第二层选择x坐标并调用_creat_alien方法"""
        current_x = alien_width
        current_y = alien_height
        while current_y <= (self.settings.screen_height - 5 * alien_height):
            while current_x <= (self.settings.screen_width - alien_width * 3):
                self._create_alien(current_x, current_y)
                current_x += alien_width *2

            """第二层循环结束后得重置x的值并递增y的值"""
            current_x = alien_width
            current_y += alien_height

    def _create_alien(self, x_pos, y_pos):
        """嵌套在_creat_fleet中的辅助方法，可以折叠不用管
        给一个x坐标这个方法可以生成相应的外星人实例并加入到外星人组中"""
        new_alien = Alien(self)
        new_alien.x = x_pos
        new_alien.rect.x = x_pos
        new_alien.rect.y = y_pos
        self.aliens.add(new_alien)

    def _check_keydown_events(self, event):
        """检查键盘被摁下的事件"""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            # 向右移动飞船
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            # 向左移动飞船
            self.ship.moving_left = True
        elif event.key == pygame.K_ESCAPE:
            self.stats.save_highest_score(self.stats.high_score)
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组 bullet """
        if len(self.bullets) < self.settings.bullet_max:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.sound.fire.play()

    def _check_keyup_events(self, event):
        """检查键盘抬起"""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False

    def _update_bullets(self):
        """更新子弹的位置，还检查舰队是否为空，如果是，那就新建一个舰队"""

        self.bullets.update()

        # 删除超出窗口的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_collision()
        self._defeat_fleet()

    def _check_collision(self):
        """检查是否有子弹集中了外星人如果有，那就将那颗子弹删除, 还检查舰队是否为空，如果是，那就新建一个舰队 PS:还实现了记分功能"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        """这个第三方函数非常方便，第一个和第二个参数是要检测碰撞的组，后两个接受bool值，
        如果是true代表发生碰撞后，那个组中发生碰撞的元素会消失，两个bool值代表两个组"""

        if collisions:
            self.sound.blast.play()
            for alien in collisions.values():
                for i in alien:
                    position = (i.rect.x, i.rect.y)
                    explosion = Explosion(self, position)
                    self.explosions.add(explosion)

                self.stats.score += self.settings.alien_points * len(alien)
            self.sb.prep_score()

    def _defeat_fleet(self):
        """判断外星人组是不是空了，如果是，那就删除按现有的子弹并新建一个舰队组"""
        if not self.aliens:
            """判断外星人组是不是空了，如果是，那就删除按现有的子弹并新建一个舰队组"""
            self.bullets.empty()
            """empty方法请空组内的元素，下面在调用一次创建舰队方法"""
            self._creat_fleet()
            """节奏快起来"""
            self.settings.speed_up()
            """关卡加一"""
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """更新外星人组中外星人的位置，还会检测外星人与飞船的碰撞。"""
        """aliens 是个alien组，所我们其实是在对这个组调用了update方法，
        该方法会对组中的每个alien对象调用方法"""
        self._check_fleet_edges()
        self.aliens.update()
        self._check_ship_hit()
        self._check_fleet_bottom()

    def _check_ship_hit(self):
        """检查并在检查为真后成功实现功能"""
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
           self._ship_hitted()

    def _ship_hitted(self, words="SHIP HITTED"):
        """飞船被击中或者是外星人触底时调用,ship_left减一"""
        if self.stats.ship_left > 0:
            """还有命"""
            self.stats.ship_left -= 1
            self.sb.prep_ships()
            """清空子弹组和外星人组"""
            self.bullets.empty()
            self.aliens.empty()
            """再创建一个舰队"""
            self._creat_fleet()
            self.ship.moving_center()

            """播放被击中音效"""
            self.sound.hitted.play()

            print(words)
            print(f"We have {self.stats.ship_left} ships left.")

            """实现暂停效果"""
            sleep(2)

        else:
            """没命啦！"""
            self._defeated()

    def _defeated(self):
        """不做判断，记录游戏失败后发生什么"""
        self.game_active = False
        """速度回归正常"""
        self.settings.reset_speed()
        """得分归零，待会实现一个记录最高分功能"""
        self.sb.check_high_score()
        self.stats.score = 0
        self.sb.prep_score()
        self.stats.level = 0
        self.sb.prep_level()

    def _check_fleet_bottom(self):
        for alien in self.aliens:
            if alien.rect.bottom >= self.settings.screen_height:
                # 意味着有外星人碰到底了
                self._ship_hitted("Alien Hitted The Base ")



    def _update_screen(self):
        """又是一个辅助方法，用于更新屏幕,里面现在有
        1、背景
        2、子弹组
        3、飞船
        4、外星人组
        5、按钮（可能）
        6、计分板
        7、特效动画
        """
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.ship.blit_ship()
        self.aliens.draw(self.screen)
        self.explosions.update()
        self.explosions.draw(self.screen)


        """计分板"""
        self.sb.show_score()

        """如果有没开始那就画开始按钮"""
        if not self.game_active:
            self.play_button.draw_button()
        pygame.display.flip()


    def _check_fleet_edges(self):
        """检查舰队里的外星人是否有到达边缘的，如果有，整个舰队往下之后再改变整体方向"""

        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                """这里break 是因为我们要将整个舰队往下移动，所以只要任何一个外星人碰到边缘就会调用change，
                使整个舰队下移且改变舰队的direction,最后break"""
                break


    def change_fleet_direction(self):
        """组里每一个外星人的位置都要改变，所以用一个遍历"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        """ x*=-1 就是 x = x * -1"""
        self.settings.fleet_direction *= -1


    def run_game(self):
        """begin running game."""
        while True:
            # detect keyboard event
            self._check_event()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(self.settings.fps)



if __name__ == '__main__':
    ai = AlienInvasion()
    ai.sound.play_music()
    ai.run_game()