"""
Service for reading metadata from audio files.
"""

from pathlib import Path

from mutagen import File

from src.models.song import Song


def load_song_metadata(filepath):
    """Read an audio file and return a Song object."""

    path = Path(filepath)

    title = path.stem
    artist = "Unknown Artist"
    album = "Unknown Album"
    duration = 0.0

    try:
        audio = File(filepath, easy=True)

        if audio is not None:
            if audio.tags:
                title = audio.tags.get("title", [title])[0]
                artist = audio.tags.get("artist", [artist])[0]
                album = audio.tags.get("album", [album])[0]

            if audio.info:
                duration = audio.info.length

    except Exception as error:
        print(f"Could not read metadata for {filepath}: {error}")

    return Song(
        filepath=str(path),
        title=title,
        artist=artist,
        album=album,
        duration=duration,
    )
