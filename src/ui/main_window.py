"""
Main application window.
"""
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

class MainWindow:
    """Main application window."""

    def __init__(self):

        self.root = tk.Tk()

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
        self.top_section
        )

        self.playlist_frame.pack(
        side="right",
        fill="y"
        )

        # ===========================
        # Bottom Controls
        # ===========================
        self.controls_frame = PlayerControls(
        self.main_container
        )

        self.controls_frame.pack(
        side="bottom",
        fill="x"
        )

    # -------------------------------------------------

    def run(self):

        self.root.mainloop()
