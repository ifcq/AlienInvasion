import pygame

class Sound:
    def __init__(self):
        pygame.mixer.init()
        self.blast = pygame.mixer.Sound('sounds/blast.wav')
        self.blast.set_volume(0.8)
        self.fire = pygame.mixer.Sound('sounds/fire.wav')
        self.fire.set_volume(0.3)
        self.hitted = pygame.mixer.Sound('sounds/hitted.wav')
        self.hitted.set_volume(1)
        self.music = pygame.mixer.Sound('sounds/music.ogg')



    def play_music(self):
        self.music.play(-1)