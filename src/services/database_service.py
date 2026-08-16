"""
SQLite database service for the music player.
"""

import sqlite3
from pathlib import Path

from src.models.song import Song


class DatabaseService:
    """Handles persistent storage for the music library."""

    def __init__(self):
        """Initialize the database service."""

        # Find the project root based on this file's location.
        #
        # Project structure:
        #
        # Personalized-Music-Player/
        # ├── data/
        # │   └── music_player.db
        # └── src/
        #     └── services/
        #         └── database_service.py
        #
        # parents[0] -> services
        # parents[1] -> src
        # parents[2] -> project root

        project_root = Path(
            __file__
        ).resolve().parents[2]

        self.database_path = (
            project_root
            / "data"
            / "music_player.db"
        )

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.create_tables()

    # =================================================
    # Database Connection
    # =================================================

    def connect(self):
        """Create and return a database connection."""

        return sqlite3.connect(
            self.database_path
        )

    # =================================================
    # Database Setup
    # =================================================

    def create_tables(self):
        """Create required database tables."""

        with self.connect() as connection:

            # ==========================================
            # Songs table
            # ==========================================

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS songs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filepath TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    artist TEXT NOT NULL,
                    album TEXT,
                    duration REAL NOT NULL,
                    date_added
                        TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            # ==========================================
            # Favorites migration
            # ==========================================

            try:

                connection.execute(
                    """
                    ALTER TABLE songs
                    ADD COLUMN is_favorite
                        INTEGER DEFAULT 0
                    """
                )

            except sqlite3.OperationalError:
                # Column already exists.
                pass

            # ==========================================
            # Play history table
            # ==========================================

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS play_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    song_filepath TEXT NOT NULL,
                    played_at
                        TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            # ==========================================
            # Settings table
            # ==========================================

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
                """
            )

            connection.commit()

    # =================================================
    # Songs
    # =================================================

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

    # =================================================
    # Favorites
    # =================================================

    def set_favorite(
        self,
        filepath,
        is_favorite,
    ):
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

    # =================================================
    # Play History
    # =================================================

    def record_play(self, filepath):
        """Record a song playback event."""

        with self.connect() as connection:

            connection.execute(
                """
                INSERT INTO play_history (
                    song_filepath
                )
                VALUES (?)
                """,
                (filepath,),
            )

            connection.commit()

    def get_recent_songs(self, limit=20):
        """Return recently played songs."""

        with self.connect() as connection:

            cursor = connection.execute(
                """
                SELECT
                    songs.filepath,
                    songs.title,
                    songs.artist,
                    songs.album,
                    songs.duration,
                    songs.is_favorite
                FROM play_history
                INNER JOIN songs
                    ON play_history.song_filepath =
                       songs.filepath
                GROUP BY songs.filepath
                ORDER BY MAX(play_history.played_at) DESC
                LIMIT ?
                """,
                (limit,),
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

    # =================================================
    # Statistics
    # =================================================

    def get_total_songs(self):
        """Return the total number of songs."""

        with self.connect() as connection:

            cursor = connection.execute(
                """
                SELECT COUNT(*)
                FROM songs
                """
            )

            result = cursor.fetchone()

        return result[0]

    def get_favorite_count(self):
        """Return the number of favorite songs."""

        with self.connect() as connection:

            cursor = connection.execute(
                """
                SELECT COUNT(*)
                FROM songs
                WHERE is_favorite = 1
                """
            )

            result = cursor.fetchone()

        return result[0]

    def get_total_plays(self):
        """Return the total number of recorded plays."""

        with self.connect() as connection:

            cursor = connection.execute(
                """
                SELECT COUNT(*)
                FROM play_history
                """
            )

            result = cursor.fetchone()

        return result[0]

    def get_total_listening_time(self):
        """
        Return the total estimated listening time
        in seconds.
        """

        with self.connect() as connection:

            cursor = connection.execute(
                """
                SELECT COALESCE(
                    SUM(songs.duration),
                    0
                )
                FROM play_history
                INNER JOIN songs
                    ON play_history.song_filepath =
                       songs.filepath
                """
            )

            result = cursor.fetchone()

        return float(result[0])

    def get_most_played_songs(self, limit=5):
        """Return the most frequently played songs."""

        with self.connect() as connection:

            cursor = connection.execute(
                """
                SELECT
                    songs.filepath,
                    songs.title,
                    songs.artist,
                    songs.album,
                    songs.duration,
                    songs.is_favorite,
                    COUNT(play_history.id)
                        AS play_count
                FROM play_history
                INNER JOIN songs
                    ON play_history.song_filepath =
                       songs.filepath
                GROUP BY songs.filepath
                ORDER BY play_count DESC
                LIMIT ?
                """,
                (limit,),
            )

            rows = cursor.fetchall()

        return [
            {
                "song": Song(
                    filepath=row[0],
                    title=row[1],
                    artist=row[2],
                    album=row[3] or "Unknown Album",
                    duration=row[4],
                    is_favorite=bool(row[5]),
                ),
                "play_count": row[6],
            }
            for row in rows
        ]

    # =================================================
    # Settings
    # =================================================

    def set_setting(
        self,
        key,
        value,
    ):
        """Save or update an application setting."""

        with self.connect() as connection:

            connection.execute(
                """
                INSERT INTO settings (
                    key,
                    value
                )
                VALUES (?, ?)
                ON CONFLICT(key)
                DO UPDATE SET
                    value = excluded.value
                """,
                (
                    key,
                    str(value),
                ),
            )

            connection.commit()

    def get_setting(
        self,
        key,
        default=None,
    ):
        """Return a saved setting."""

        with self.connect() as connection:

            cursor = connection.execute(
                """
                SELECT value
                FROM settings
                WHERE key = ?
                """,
                (key,),
            )

            row = cursor.fetchone()

        if row is None:
            return default

        return row[0]

    def clear_settings(self):
        """Delete all saved application settings."""

        with self.connect() as connection:

            connection.execute(
                """
                DELETE FROM settings
                """
            )

            connection.commit()

    # =================================================
    # Data Management
    # =================================================

    def clear_play_history(self):
        """Delete all playback history."""

        with self.connect() as connection:

            connection.execute(
                """
                DELETE FROM play_history
                """
            )

            connection.commit()

    def clear_library(self):
        """Delete all songs and their playback history."""

        with self.connect() as connection:

            connection.execute(
                """
                DELETE FROM play_history
                """
            )

            connection.execute(
                """
                DELETE FROM songs
                """
            )

            connection.commit()
