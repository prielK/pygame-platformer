import pygame
import os


class SoundManager:
    def __init__(self):
        pygame.init()
        self.sfx_volume = 0.4
        self.music_volume = 0.2
        self.sfx = {
            "walk": pygame.mixer.Sound(
                os.path.join("Assets", "sounds", "SFX", "Footstep_Dirt_01.wav")
            ),
            "land": pygame.mixer.Sound(
                os.path.join("Assets", "sounds", "SFX", "Footstep_Dirt_09.wav")
            ),
            "gold": pygame.mixer.Sound(
                os.path.join("Assets", "sounds", "SFX", "Pickup_Gold_03.wav")
            ),
            "hp": pygame.mixer.Sound(
                os.path.join("Assets", "sounds", "SFX", "Footstep_Water_05.wav")
            ),
        }
        self.music = {
            "level_1": os.path.join(
                "Assets", "sounds", "music", "Ambience_Cave_00.ogg"
            ),
            "menu": os.path.join("Assets", "sounds", "music", "Menu_Music.ogg"),
        }
        self.curr_song = None

    def play_sfx(self, sound_name):
        self.sfx[sound_name].set_volume(self.sfx_volume)
        self.sfx[sound_name].play()

    def play_music(self, music_name):
        # If the same song is already playing dont play it from the beginning otherwise play new song
        if self.curr_song is not music_name or not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(self.music[music_name])
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(loops=-1, fade_ms=2500)
            self.curr_song = music_name

    def fade_music(self):
        pygame.mixer.music.fadeout(500)  # Fades out the music currently playing
