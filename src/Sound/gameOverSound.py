import pygame
from Sound import Sound
class gameOverSound(Sound):
    def __init__(self, src):
        super().__init__(src) 
        self.game_over_sound = pygame.mixer.Sound(self.src)
        self.game_over_sound.set_volume(0.2)
        
    def play(self):
         # Play the background Sound
        
        self.game_over_sound.play()
        pygame.mixer.music.pause()
    def setVolume(self, volume):
        self.game_over_sound.set_volume(volume)

