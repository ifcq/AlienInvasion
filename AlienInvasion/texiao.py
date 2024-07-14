import pygame
from pygame.sprite import Sprite

class Explosion(Sprite):
    def __init__(self, ai_game, position):
        super().__init__()
        self.screen = ai_game.screen
        self.explosion_frames = [pygame.image.load(f'texiao/explosion_{i}.png') for i in range(1, 10)]
        self.current_frame = 0
        self.image = self.explosion_frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.frame_count = len(self.explosion_frames)
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 10  # 毫秒


    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame += 1
            if self.current_frame >= self.frame_count:
                self.kill()
            else:
                self.image = self.explosion_frames[self.current_frame]
                self.rect = self.image.get_rect(center=self.rect.center)



    def draw(self):
        self.screen.blit(self.image, self.rect)
