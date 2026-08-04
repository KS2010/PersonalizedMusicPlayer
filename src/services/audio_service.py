"""
Audio playback service.

Handles loading, playing, pausing, resuming,
stopping, and volume control for audio files.
"""

import pygame


class AudioService:
    """Controls audio playback using pygame."""

    def __init__(self):
        pygame.mixer.init()

        self.current_song = None
        self.is_playing = False
        self.is_paused = False

        # Default volume = 70%
        pygame.mixer.music.set_volume(0.7)

    def load_song(self, song):
        """Load a song into the audio player."""

        try:
            pygame.mixer.music.load(song.filepath)

            self.current_song = song
            self.is_playing = False
            self.is_paused = False

            return True

        except pygame.error as error:
            print(f"Could not load song: {error}")
            return False

    def play(self):
        """Play the currently loaded song."""

        if self.current_song is None:
            return

        pygame.mixer.music.play()

        self.is_playing = True
        self.is_paused = False

    def pause(self):
        """Pause playback."""

        if not self.is_playing:
            return

        pygame.mixer.music.pause()

        self.is_playing = False
        self.is_paused = True

    def resume(self):
        """Resume paused playback."""

        if not self.is_paused:
            return

        pygame.mixer.music.unpause()

        self.is_playing = True
        self.is_paused = False

    def stop(self):
        """Stop playback."""

        pygame.mixer.music.stop()

        self.is_playing = False
        self.is_paused = False

    def set_volume(self, volume):
        """Set playback volume using a perceptual curve."""

        volume = max(0, min(100, float(volume)))

        pygame_volume = (volume / 100) ** 2

        pygame.mixer.music.set_volume(pygame_volume)
