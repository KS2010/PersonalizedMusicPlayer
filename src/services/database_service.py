"""
SQLite database service for the music player.
"""

from multiprocessing import connection
import sqlite3
from pathlib import Path
from src.models.song import Song

class DatabaseService:
    """Handles persistent storage for the music library."""

    def __init__(self):
        self.database_path = Path("data/music_player.db")

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.create_tables()

    def connect(self):
        """Create and return a database connection."""

        return sqlite3.connect(self.database_path)

    def create_tables(self):
        """Create required database tables."""

        with self.connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS songs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filepath TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    artist TEXT NOT NULL,
                    album TEXT,
                    duration REAL NOT NULL,
                    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            try:
                connection.execute(
                """
                ALTER TABLE songs
                ADD COLUMN is_favorite INTEGER DEFAULT 0
                """
            )
            except sqlite3.OperationalError:
                # Column already exists.
                pass

            connection.commit()

    def add_song(self, song):
        """Add a song to the persistent library."""

        with self.connect() as connection:
            connection.execute(
            """
            INSERT OR IGNORE INTO songs (
                filepath,
                title,
                artist,
                album,
                duration
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                song.filepath,
                song.title,
                song.artist,
                song.album,
                song.duration,
            ),
        )

        connection.commit()

    def get_all_songs(self):
        """Return all songs stored in the library."""

        with self.connect() as connection:
            cursor = connection.execute(
            """
            SELECT
                filepath,
                title,
                artist,
                album,
                duration,
                is_favorite
            FROM songs
            ORDER BY date_added ASC
            """
        )

        rows = cursor.fetchall()

        return [
        Song(
            filepath=row[0],
            title=row[1],
            artist=row[2],
            album=row[3] or "Unknown Album",
            duration=row[4],
            is_favorite=bool(row[5]),
        )
        for row in rows
    ]

    def set_favorite(self, filepath, is_favorite):
        """Update a song's favorite status."""

        with self.connect() as connection:
            connection.execute(
                """
                UPDATE songs
                SET is_favorite = ?
                WHERE filepath = ?
                """,
                (
                int(is_favorite),
                filepath,
                ),
            )

        connection.commit()
