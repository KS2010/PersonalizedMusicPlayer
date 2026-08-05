"""
Main application window.
"""

from src.models import song
from src.ui.theme import (
    BACKGROUND_COLOR,
    NAVIGATION_WIDTH,
    PLAYLIST_WIDTH,
    CONTROLS_HEIGHT,
)

from src.ui.cassette import CassettePanel
import tkinter as tk
from src.ui.navigation import NavigationPanel
from src.ui.playlist_view import PlaylistView
from src.ui.player_controls import PlayerControls
from src.services.audio_service import AudioService


class MainWindow:
    """Main application window."""

    def __init__(self):

        self.root = tk.Tk()

        self.audio_service = AudioService()
        self.configure_window()

        self.create_frames()
        self.start_progress_updater()

    # -------------------------------------------------

    def configure_window(self):

        self.root.title("🎵 Personalized Music Player")

        self.root.geometry("1500x850")

        self.root.minsize(1200, 700)

        self.root.configure(bg=BACKGROUND_COLOR)

    # -------------------------------------------------

    def create_frames(self):

        # ===========================
        # Main Container
        # ===========================

        self.main_container = tk.Frame(self.root, bg=BACKGROUND_COLOR)

        self.main_container.pack(fill="both", expand=True)

        # ===========================
        # Top Section
        # ===========================

        self.top_section = tk.Frame(self.main_container, bg=BACKGROUND_COLOR)

        self.top_section.pack(fill="both", expand=True)

        # ===========================
        # Navigation
        # ===========================

        self.navigation_frame = NavigationPanel(self.top_section)

        self.navigation_frame.pack(side="left", fill="y")

        # ===========================
        # Cassette Area
        # ===========================

        self.cassette_frame = CassettePanel(self.top_section)

        self.cassette_frame.pack(side="left", fill="both", expand=True)

        # ===========================
        # Playlist
        # ===========================
        self.playlist_frame = PlaylistView(
            self.top_section,
            on_song_selected=self.handle_song_selection,
        )

        self.playlist_frame.pack(side="right", fill="y")

        # ===========================
        # Bottom Controls
        # ===========================
        self.controls_frame = PlayerControls(
            self.main_container,
            on_play_pause=self.handle_play_pause,
            on_volume_change=self.handle_volume_change,
            on_seek=self.handle_seek,
        )

        self.controls_frame.pack(side="bottom", fill="x")

    def handle_song_selection(self, song):
        """Handle a song selected from the playlist."""

        self.cassette_frame.update_song(song)

        self.audio_service.load_song(song)

        self.controls_frame.set_duration(song.duration)

        self.controls_frame.update_progress(0)

    # -------------------------------------------------
    def handle_play_pause(self):
        """Toggle between playing and paused states."""

        if self.audio_service.current_song is None:
            return

        if self.audio_service.is_paused:

            self.audio_service.resume()

            self.controls_frame.set_playing(True)

        elif self.audio_service.is_playing:

            self.audio_service.pause()

            self.controls_frame.set_playing(False)

        else:

            self.audio_service.play()

            self.controls_frame.set_playing(True)

    def handle_volume_change(self, value):
        """Change playback volume."""

        self.audio_service.set_volume(value)

    def start_progress_updater(self):
        """Start periodically updating playback progress."""

        self.update_playback_progress()

    def update_playback_progress(self):
        """Update the playback progress display."""

        if (
            self.audio_service.current_song is not None
            and self.audio_service.is_playing
        ):
            position = self.audio_service.get_position()

            self.controls_frame.update_progress(position)

        self.root.after(
            500,
            self.update_playback_progress,
        )

    def handle_seek(self, position):
      """Seek the current song to the selected position."""

      self.audio_service.seek(position)

      self.controls_frame.update_progress(position)

    def run(self):

        self.root.mainloop()
