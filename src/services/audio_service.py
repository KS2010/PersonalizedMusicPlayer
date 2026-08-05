"""
Audio playback service.

Handles loading, playing, pausing, resuming,
stopping, and volume control for audio files.
"""

from turtle import position

import pygame


class AudioService:
    """Controls audio playback using pygame."""

    def __init__(self):
        pygame.mixer.init()

        self.current_song = None
        self.is_playing = False
        self.is_paused = False
        self.seek_offset = 0.0
        # Default volume = 70%
        pygame.mixer.music.set_volume(0.7)

    def load_song(self, song):
        """Load a song into the audio player."""

        try:
            pygame.mixer.music.load(song.filepath)

            self.current_song = song
            self.seek_offset = 0.0
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

    def get_position(self):
        """Return the current playback position in seconds."""

        if self.current_song is None:
            return 0.0

        position_ms = pygame.mixer.music.get_pos()

        if position_ms < 0:
            return self.seek_offset

        return self.seek_offset + (position_ms / 1000)

    def seek(self, position):
        """Seek to a specific position in the current song."""

        if self.current_song is None:
         return

        position = float(position)

        position = max(
        0.0,
        min(position, self.current_song.duration),
        )

        was_paused = self.is_paused

        try:
            pygame.mixer.music.play(
            start=position
        )

            self.seek_offset = position
            self.is_playing = True
            self.is_paused = False

            if was_paused:
                pygame.mixer.music.pause()

            self.is_playing = False
            self.is_paused = True

        except pygame.error as error:
            print(f"Could not seek song: {pygame.error}")
