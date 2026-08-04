"""
Playlist panel for displaying and searching songs.
"""

import tkinter as tk

from src.ui.theme import (
    PLAYLIST_BG,
    BORDER_COLOR,
    ACCENT_COLOR,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TEXT_MUTED,
    BODY_FONT,
    SMALL_FONT,
)


class PlaylistView(tk.Frame):
    """Right-side panel containing the user's playlist."""

    def __init__(self, parent):
        super().__init__(
            parent,
            bg=PLAYLIST_BG,
            width=300,
        )

        self.pack_propagate(False)
        self.create_widgets()

    def create_widgets(self):
        """Create playlist interface elements."""

        # Playlist heading
        heading = tk.Label(
            self,
            text="YOUR PLAYLIST",
            font=("Segoe UI", 14, "bold"),
            bg=PLAYLIST_BG,
            fg=TEXT_PRIMARY,
        )

        heading.pack(
            anchor="w",
            padx=20,
            pady=(30, 2),
        )

        # Song counter
        self.song_count_label = tk.Label(
            self,
            text="0 songs",
            font=SMALL_FONT,
            bg=PLAYLIST_BG,
            fg=TEXT_MUTED,
        )

        self.song_count_label.pack(
            anchor="w",
            padx=20,
            pady=(0, 20),
        )

        # Search box
        self.search_entry = tk.Entry(
            self,
            font=BODY_FONT,
            bg="#242424",
            fg=TEXT_PRIMARY,
            insertbackground=TEXT_PRIMARY,
            relief="flat",
            bd=0,
        )

        self.search_entry.insert(
            0,
            "Search songs..."
        )

        self.search_entry.pack(
            fill="x",
            padx=20,
            ipady=8,
        )

        # Divider
        divider = tk.Frame(
            self,
            bg=BORDER_COLOR,
            height=1,
        )

        divider.pack(
            fill="x",
            padx=20,
            pady=20,
        )

        # Empty playlist message
        self.empty_title = tk.Label(
            self,
            text="No songs yet",
            font=("Segoe UI", 12, "bold"),
            bg=PLAYLIST_BG,
            fg=TEXT_SECONDARY,
        )

        self.empty_title.pack(
            pady=(100, 5)
        )

        self.empty_message = tk.Label(
            self,
            text="Add music to your library",
            font=SMALL_FONT,
            bg=PLAYLIST_BG,
            fg=TEXT_MUTED,
        )

        self.empty_message.pack()
