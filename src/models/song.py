"""
Song data model.
"""

from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song in the music library."""

    filepath: str
    title: str
    artist: str = "Unknown Artist"
    album: str = "Unknown Album"
    duration: float = 0.0

    @property
    def formatted_duration(self):
        """Return the song duration as MM:SS."""

        total_seconds = int(self.duration)

        minutes = total_seconds // 60
        seconds = total_seconds % 60

        return f"{minutes}:{seconds:02d}"
