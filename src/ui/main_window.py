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

        self.main_container = tk.Frame(
            self.root,
            bg=BACKGROUND_COLOR
        )

        self.main_container.pack(
            fill="both",
            expand=True
        )

        # ===========================
        # Top Section
        # ===========================

        self.top_section = tk.Frame(
            self.main_container,
            bg=BACKGROUND_COLOR
        )

        self.top_section.pack(
            fill="both",
            expand=True
        )

        # ===========================
        # Navigation
        # ===========================

        self.navigation_frame = NavigationPanel(self.top_section)

        self.navigation_frame.pack(
        side="left",
        fill="y"
        )

        # ===========================
        # Cassette Area
        # ===========================

        self.cassette_frame = CassettePanel(
        self.top_section
        )

        self.cassette_frame.pack(
        side="left",
        fill="both",
        expand=True
        )

        # ===========================
        # Playlist
        # ===========================
        self.playlist_frame = PlaylistView(
        self.top_section,
        on_song_selected=self.handle_song_selection,
        )

        self.playlist_frame.pack(
        side="right",
        fill="y"
        )

        # ===========================
        # Bottom Controls
        # ===========================
        self.controls_frame = PlayerControls(
        self.main_container,
        on_play_pause=self.handle_play_pause,
        on_volume_change=self.handle_volume_change,
        )

        self.controls_frame.pack(
        side="bottom",
        fill="x"
        )
    def handle_song_selection(self, song):
        """Handle a song selected from the playlist."""
        # Update the Now Playing UI
        self.cassette_frame.update_song(song)

        # Load the selected song
        self.audio_service.load_song(song)

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

    def run(self):

        self.root.mainloop()
