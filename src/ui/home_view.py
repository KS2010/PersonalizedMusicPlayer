"""
Home dashboard for the music player.
"""

import tkinter as tk

from src.ui.theme import (
    BACKGROUND_COLOR,
    ACCENT_COLOR,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BORDER_COLOR,
)


class HomeView(tk.Frame):
    """Main dashboard displayed on the Home page."""

    def __init__(
        self,
        parent,
        database_service,
        on_song_selected=None,
    ):
        super().__init__(
            parent,
            bg=BACKGROUND_COLOR,
        )

        self.database_service = database_service
        self.on_song_selected = on_song_selected

        self.create_widgets()
        self.refresh_home()

    # =================================================
    # UI Creation
    # =================================================

    def create_widgets(self):
        """Create the Home dashboard."""

        # ==========================================
        # Main container
        # ==========================================

        self.content_frame = tk.Frame(
            self,
            bg=BACKGROUND_COLOR,
        )

        self.content_frame.pack(
            fill="both",
            expand=True,
            padx=45,
            pady=35,
        )

        # ==========================================
        # Header
        # ==========================================

        header_frame = tk.Frame(
            self.content_frame,
            bg=BACKGROUND_COLOR,
        )

        header_frame.pack(
            fill="x",
        )

        self.greeting_label = tk.Label(
            header_frame,
            text="WELCOME BACK",
            font=("Segoe UI", 22, "bold"),
            bg=BACKGROUND_COLOR,
            fg=TEXT_PRIMARY,
        )

        self.greeting_label.pack(
            anchor="w",
        )

        subtitle_label = tk.Label(
            header_frame,
            text="Your music, your library, your listening journey.",
            font=("Segoe UI", 10),
            bg=BACKGROUND_COLOR,
            fg=TEXT_SECONDARY,
        )

        subtitle_label.pack(
            anchor="w",
            pady=(5, 25),
        )

        # ==========================================
        # Quick Statistics
        # ==========================================

        stats_frame = tk.Frame(
            self.content_frame,
            bg=BACKGROUND_COLOR,
        )

        stats_frame.pack(
            fill="x",
        )

        for column in range(3):
            stats_frame.grid_columnconfigure(
                column,
                weight=1,
            )

        self.total_songs_value = (
            self.create_stat_card(
                stats_frame,
                0,
                "♫",
                "TOTAL SONGS",
            )
        )

        self.favorite_count_value = (
            self.create_stat_card(
                stats_frame,
                1,
                "♥",
                "FAVORITES",
            )
        )

        self.total_plays_value = (
            self.create_stat_card(
                stats_frame,
                2,
                "▶",
                "TOTAL PLAYS",
            )
        )

        # ==========================================
        # Recently Played
        # ==========================================

        recent_section = tk.Frame(
            self.content_frame,
            bg="#1B1B1B",
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
        )

        recent_section.pack(
            fill="both",
            expand=True,
            pady=(30, 0),
        )

        recent_header = tk.Frame(
            recent_section,
            bg="#1B1B1B",
        )

        recent_header.pack(
            fill="x",
            padx=25,
            pady=(20, 15),
        )

        recent_title = tk.Label(
            recent_header,
            text="RECENTLY PLAYED",
            font=("Segoe UI", 13, "bold"),
            bg="#1B1B1B",
            fg=TEXT_PRIMARY,
        )

        recent_title.pack(
            side="left",
        )

        recent_subtitle = tk.Label(
            recent_header,
            text="Your latest listening activity",
            font=("Segoe UI", 9),
            bg="#1B1B1B",
            fg=TEXT_SECONDARY,
        )

        recent_subtitle.pack(
            side="right",
        )

        separator = tk.Frame(
            recent_section,
            bg=BORDER_COLOR,
            height=1,
        )

        separator.pack(
            fill="x",
            padx=25,
        )

        self.recent_songs_frame = tk.Frame(
            recent_section,
            bg="#1B1B1B",
        )

        self.recent_songs_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20,
        )

    # =================================================
    # Statistic Card
    # =================================================

    def create_stat_card(
        self,
        parent,
        column,
        icon,
        title,
    ):
        """Create a compact statistic card."""

        card = tk.Frame(
            parent,
            bg="#1B1B1B",
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=8,
        )

        icon_label = tk.Label(
            card,
            text=icon,
            font=("Segoe UI Symbol", 17),
            bg="#1B1B1B",
            fg=ACCENT_COLOR,
        )

        icon_label.pack(
            anchor="w",
            padx=18,
            pady=(15, 3),
        )

        value_label = tk.Label(
            card,
            text="0",
            font=("Segoe UI", 20, "bold"),
            bg="#1B1B1B",
            fg=TEXT_PRIMARY,
        )

        value_label.pack(
            anchor="w",
            padx=18,
        )

        title_label = tk.Label(
            card,
            text=title,
            font=("Segoe UI", 8, "bold"),
            bg="#1B1B1B",
            fg=TEXT_SECONDARY,
        )

        title_label.pack(
            anchor="w",
            padx=18,
            pady=(3, 15),
        )

        return value_label

    # =================================================
    # Refresh
    # =================================================

    def refresh_home(self):
        """Refresh Home dashboard data."""

        if self.database_service is None:
            return

        # ==========================================
        # Statistics
        # ==========================================

        total_songs = (
            self.database_service.get_total_songs()
        )

        favorite_count = (
            self.database_service.get_favorite_count()
        )

        total_plays = (
            self.database_service.get_total_plays()
        )

        self.total_songs_value.config(
            text=str(total_songs)
        )

        self.favorite_count_value.config(
            text=str(favorite_count)
        )

        self.total_plays_value.config(
            text=str(total_plays)
        )

        # ==========================================
        # Recent songs
        # ==========================================

        self.refresh_recent_songs()

    # =================================================
    # Recent Songs
    # =================================================

    def refresh_recent_songs(self):
        """Display recently played songs."""

        for widget in (
            self.recent_songs_frame.winfo_children()
        ):
            widget.destroy()

        recent_songs = (
            self.database_service.get_recent_songs(
                limit=5
            )
        )

        if not recent_songs:

            empty_label = tk.Label(
                self.recent_songs_frame,
                text="No recently played songs",
                font=("Segoe UI", 10),
                bg="#1B1B1B",
                fg=TEXT_SECONDARY,
            )

            empty_label.pack(
                pady=30,
            )

            return

        for index, song in enumerate(
            recent_songs
        ):

            self.create_recent_song_row(
                song,
                index,
            )

    # =================================================
    # Recent Song Row
    # =================================================

    def create_recent_song_row(
        self,
        song,
        index,
    ):
        """Create a clickable recent-song row."""

        row = tk.Frame(
            self.recent_songs_frame,
            bg="#1B1B1B",
            cursor="hand2",
        )

        row.pack(
            fill="x",
            pady=5,
        )

        # ==========================================
        # Number
        # ==========================================

        number_label = tk.Label(
            row,
            text=f"{index + 1:02}",
            width=4,
            font=("Segoe UI", 9, "bold"),
            bg="#1B1B1B",
            fg=ACCENT_COLOR,
        )

        number_label.pack(
            side="left",
        )

        # ==========================================
        # Song information
        # ==========================================

        info_frame = tk.Frame(
            row,
            bg="#1B1B1B",
        )

        info_frame.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10,
        )

        title_label = tk.Label(
            info_frame,
            text=song.title,
            font=("Segoe UI", 10, "bold"),
            bg="#1B1B1B",
            fg=TEXT_PRIMARY,
            anchor="w",
        )

        title_label.pack(
            fill="x",
        )

        artist_label = tk.Label(
            info_frame,
            text=song.artist,
            font=("Segoe UI", 9),
            bg="#1B1B1B",
            fg=TEXT_SECONDARY,
            anchor="w",
        )

        artist_label.pack(
            fill="x",
            pady=(2, 0),
        )

        # ==========================================
        # Duration
        # ==========================================

        duration_label = tk.Label(
            row,
            text=song.formatted_duration,
            font=("Segoe UI", 9),
            bg="#1B1B1B",
            fg=TEXT_SECONDARY,
        )

        duration_label.pack(
            side="right",
            padx=10,
        )

        # ==========================================
        # Click handling
        # ==========================================

        clickable_widgets = [
            row,
            number_label,
            info_frame,
            title_label,
            artist_label,
            duration_label,
        ]

        for widget in clickable_widgets:

            widget.bind(
                "<Button-1>",
                lambda event,
                selected_song=song:
                    self.select_song(
                        selected_song
                    ),
            )

    # =================================================
    # Song Selection
    # =================================================

    def select_song(self, song):
        """Play a selected song."""

        if self.on_song_selected:

            self.on_song_selected(
                song
            )
