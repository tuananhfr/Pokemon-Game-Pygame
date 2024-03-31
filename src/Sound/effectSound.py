import pygame
from Sound import Sound
class effectSound(Sound):
    def __init__(self, src):
        super().__init__(src) 
        self.effect_sound = pygame.mixer.Sound(self.src)
        self.effect_sound.set_volume(0.3)
    def play(self):
         # Play the background Sound
        
        self.effect_sound.play()
    def setVolume(self, volume):
        self.effect_sound.set_volume(volume)

