# wrapper for sound playing functions
# in case they're complicated or i need to swap libraries (again)

import pygame

def init():
    pygame.mixer.init()

class Sound():
    def __init__(self, path):
        self.snd_obj = pygame.mixer.Sound(path)

    def play(self):
        self.snd_obj.play()

    def stop(self):
        self.snd_obj.stop()