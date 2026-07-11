"""
Main application window.
"""

import tkinter as tk
from src.ui.navigation import NavigationPanel


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

        self.root.configure(bg="#121212")

    # -------------------------------------------------

    def create_frames(self):

        # ===========================
        # Main Container
        # ===========================

        self.main_container = tk.Frame(
            self.root,
            bg="#121212"
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
            bg="#121212"
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

        self.cassette_frame = tk.Frame(
            self.top_section,
            bg="#222222"
        )

        self.cassette_frame.pack(
            side="left",
            fill="both",
            expand=True
        )

        # ===========================
        # Playlist
        # ===========================

        self.playlist_frame = tk.Frame(
            self.top_section,
            bg="#191919",
            width=300
        )

        self.playlist_frame.pack(
            side="right",
            fill="y"
        )

        self.playlist_frame.pack_propagate(False)

        # ===========================
        # Bottom Controls
        # ===========================

        self.controls_frame = tk.Frame(
            self.main_container,
            bg="#181818",
            height=120
        )

        self.controls_frame.pack(
            side="bottom",
            fill="x"
        )

        self.controls_frame.pack_propagate(False)

    # -------------------------------------------------

    def run(self):

        self.root.mainloop()
