"""
Cassette panel.
"""

import tkinter as tk

from src.ui.theme import (
    BORDER_COLOR,
    CASSETTE_BG,
    CARD_BG,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    ACCENT_COLOR,
    TITLE_FONT,
    SUBTITLE_FONT,
    BODY_FONT,
)


class CassettePanel(tk.Frame):
    """Center cassette panel."""

    def __init__(self, parent):
        super().__init__(
            parent,
            bg=CASSETTE_BG
        )

        self.create_widgets()

    def create_widgets(self):

        now_playing = tk.Label(
        self,
        text="NOW PLAYING",
        font=("Segoe UI", 11, "bold"),
        fg=ACCENT_COLOR,
        bg=CASSETTE_BG
        )

        now_playing.pack(
        pady=(40, 15)
        )
        # Cassette Placeholder

        cassette = tk.Label(
            self,
            text="📼",
            font=("Segoe UI Emoji", 72),
            bg=CARD_BG,
            fg=ACCENT_COLOR
        )

        cassette.pack(pady=(40, 20))

        separator = tk.Frame(
            self,
            bg=BORDER_COLOR,
            height=1
        )
        separator.pack(
            fill="x",
            padx=40,
            pady=30
        )

        self.song_title = tk.Label(
            self,
            text="No Song Playing",
            font=TITLE_FONT,
            bg=CASSETTE_BG,
            fg=TEXT_PRIMARY
            )

        self.song_title.pack()



        self.artist_label = tk.Label(
            self,
            text="Unknown Artist",
            font=BODY_FONT,
            bg=CASSETTE_BG,
            fg=TEXT_SECONDARY
        )

        self.artist_label.pack(
        pady=5
        )

        self.album_label = tk.Label(
            self,
            text="Album : --",
            font=BODY_FONT,
            bg=CASSETTE_BG,
            fg=TEXT_SECONDARY
            )

        self.album_label.pack()


        self.duration_label = tk.Label(
        self,
        text="Duration : --:--",
        font=BODY_FONT,
        bg=CASSETTE_BG,
        fg=TEXT_SECONDARY
        )

        self.duration_label.pack(
        pady=(5, 40)
        )
def update_song(self, title, artist, album, duration):
    """Update the song information displayed."""

    self.song_title.config(text=title)
    self.artist_label.config(text=artist)
    self.album_label.config(text=f"Album : {album}")
    self.duration_label.config(text=f"Duration : {duration}")
