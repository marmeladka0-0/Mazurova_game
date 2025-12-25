import pygame
import os

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        
        self.bg_music = os.path.join('audio', 'Floating Dream.ogg')
        
        #dictionary
        self.sounds = {
            'bump': pygame.mixer.Sound(os.path.join('audio', 'Bump.wav')),
            'cancel': pygame.mixer.Sound(os.path.join('audio', 'Cancel.wav')),
            'click': pygame.mixer.Sound(os.path.join('audio', 'Click.wav')),
            'explosion': pygame.mixer.Sound(os.path.join('audio', 'Explosion.wav')),
            'jump': pygame.mixer.Sound(os.path.join('audio', 'Jump.wav')),
            'pause': pygame.mixer.Sound(os.path.join('audio', 'Pause.wav')),
            'meow': pygame.mixer.Sound(os.path.join('audio', 'Cat_Meow.wav')),
        }

        self.sound_volume = 0.3
        self.music_volume = 0.2

    def play_music(self):
        pygame.mixer.music.load(self.bg_music)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1) #-1 = loop

    def play_sound(self, name):
        sound = self.sounds.get(name)
        if sound:
            sound.set_volume(self.sound_volume)
            sound.play()

    def stop_music(self):
        pygame.mixer.music.stop()

    def set_music_volume(self, volume):
        self.music_volume = volume
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sounds_volume(self, volume):
        self.sound_volume = volume

audio_manager = AudioManager()