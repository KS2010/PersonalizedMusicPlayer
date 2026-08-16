"""
Statistics dashboard for the music player.
"""

import tkinter as tk

from src.ui.theme import (
    BACKGROUND_COLOR,
    ACCENT_COLOR,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BORDER_COLOR,
)


class StatisticsView(tk.Frame):
    """Displays listening statistics and music analytics."""

    def __init__(self, parent, database_service):
        super().__init__(
            parent,
            bg=BACKGROUND_COLOR,
        )

        self.database_service = database_service

        self.create_widgets()
        self.refresh_statistics()

    # =================================================
    # UI Creation
    # =================================================

    def create_widgets(self):
        """Create the statistics dashboard."""

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
            padx=50,
            pady=35,
        )

        # ==========================================
        # Header
        # ==========================================

        header_label = tk.Label(
            self.content_frame,
            text="STATISTICS",
            font=("Segoe UI", 22, "bold"),
            bg=BACKGROUND_COLOR,
            fg=TEXT_PRIMARY,
        )

        header_label.pack(
            anchor="w",
        )

        subtitle_label = tk.Label(
            self.content_frame,
            text="Your listening activity at a glance",
            font=("Segoe UI", 10),
            bg=BACKGROUND_COLOR,
            fg=TEXT_SECONDARY,
        )

        subtitle_label.pack(
            anchor="w",
            pady=(5, 25),
        )

        # ==========================================
        # Statistics cards container
        # ==========================================

        cards_frame = tk.Frame(
            self.content_frame,
            bg=BACKGROUND_COLOR,
        )

        cards_frame.pack(
            fill="x",
        )

        for column in range(4):
            cards_frame.grid_columnconfigure(
                column,
                weight=1,
            )

        # ==========================================
        # Total Songs
        # ==========================================

        self.total_songs_value = self.create_stat_card(
            cards_frame,
            column=0,
            icon="♫",
            title="TOTAL SONGS",
        )

        # ==========================================
        # Total Plays
        # ==========================================

        self.total_plays_value = self.create_stat_card(
            cards_frame,
            column=1,
            icon="▶",
            title="TOTAL PLAYS",
        )

        # ==========================================
        # Favorites
        # ==========================================

        self.favorite_count_value = self.create_stat_card(
            cards_frame,
            column=2,
            icon="♥",
            title="FAVORITES",
        )

        # ==========================================
        # Listening Time
        # ==========================================

        self.listening_time_value = self.create_stat_card(
            cards_frame,
            column=3,
            icon="◷",
            title="LISTENING TIME",
        )

        # ==========================================
        # Most Played Section
        # ==========================================

        most_played_container = tk.Frame(
            self.content_frame,
            bg="#1B1B1B",
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
        )

        most_played_container.pack(
            fill="both",
            expand=True,
            pady=(30, 0),
        )

        most_played_header = tk.Frame(
            most_played_container,
            bg="#1B1B1B",
        )

        most_played_header.pack(
            fill="x",
            padx=25,
            pady=(20, 15),
        )

        most_played_title = tk.Label(
            most_played_header,
            text="MOST PLAYED SONGS",
            font=("Segoe UI", 13, "bold"),
            bg="#1B1B1B",
            fg=TEXT_PRIMARY,
        )

        most_played_title.pack(
            side="left",
        )

        # ==========================================
        # Separator
        # ==========================================

        separator = tk.Frame(
            most_played_container,
            bg=BORDER_COLOR,
            height=1,
        )

        separator.pack(
            fill="x",
            padx=25,
        )

        # ==========================================
        # Most played song list
        # ==========================================

        self.most_played_frame = tk.Frame(
            most_played_container,
            bg="#1B1B1B",
        )

        self.most_played_frame.pack(
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
        """Create one statistics card."""

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

        # ==========================================
        # Icon
        # ==========================================

        icon_label = tk.Label(
            card,
            text=icon,
            font=("Segoe UI Symbol", 18),
            bg="#1B1B1B",
            fg=ACCENT_COLOR,
        )

        icon_label.pack(
            anchor="w",
            padx=18,
            pady=(15, 5),
        )

        # ==========================================
        # Value
        # ==========================================

        value_label = tk.Label(
            card,
            text="0",
            font=("Segoe UI", 22, "bold"),
            bg="#1B1B1B",
            fg=TEXT_PRIMARY,
        )

        value_label.pack(
            anchor="w",
            padx=18,
        )

        # ==========================================
        # Title
        # ==========================================

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
    # Refresh Statistics
    # =================================================

    def refresh_statistics(self):
        """Reload statistics from the database."""

        if self.database_service is None:
            return

        # ==========================================
        # Basic statistics
        # ==========================================

        total_songs = (
            self.database_service.get_total_songs()
        )

        total_plays = (
            self.database_service.get_total_plays()
        )

        favorite_count = (
            self.database_service.get_favorite_count()
        )

        listening_seconds = (
            self.database_service.get_total_listening_time()
        )

        # ==========================================
        # Update cards
        # ==========================================

        self.total_songs_value.config(
            text=str(total_songs)
        )

        self.total_plays_value.config(
            text=str(total_plays)
        )

        self.favorite_count_value.config(
            text=str(favorite_count)
        )

        self.listening_time_value.config(
            text=self.format_listening_time(
                listening_seconds
            )
        )

        # ==========================================
        # Most played songs
        # ==========================================

        self.refresh_most_played()

    # =================================================
    # Most Played
    # =================================================

    def refresh_most_played(self):
        """Display the most frequently played songs."""

        # Remove previous rows.
        for widget in self.most_played_frame.winfo_children():
            widget.destroy()

        most_played = (
            self.database_service.get_most_played_songs(
                limit=5
            )
        )

        # ==========================================
        # Empty state
        # ==========================================

        if not most_played:

            empty_label = tk.Label(
                self.most_played_frame,
                text="No listening data yet",
                font=("Segoe UI", 10),
                bg="#1B1B1B",
                fg=TEXT_SECONDARY,
            )

            empty_label.pack(
                pady=30,
            )

            return

        # ==========================================
        # Song rows
        # ==========================================

        for rank, item in enumerate(
            most_played,
            start=1,
        ):

            song = item["song"]
            play_count = item["play_count"]

            self.create_song_row(
                rank,
                song,
                play_count,
            )

    # =================================================
    # Most Played Song Row
    # =================================================

    def create_song_row(
        self,
        rank,
        song,
        play_count,
    ):
        """Create one most-played song row."""

        row = tk.Frame(
            self.most_played_frame,
            bg="#1B1B1B",
        )

        row.pack(
            fill="x",
            pady=7,
        )

        # ==========================================
        # Rank
        # ==========================================

        rank_label = tk.Label(
            row,
            text=f"{rank:02}",
            width=4,
            font=("Segoe UI", 10, "bold"),
            bg="#1B1B1B",
            fg=ACCENT_COLOR,
        )

        rank_label.pack(
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
            padx=(10, 10),
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
        # Play count
        # ==========================================

        play_text = (
            f"{play_count} play"
            if play_count == 1
            else f"{play_count} plays"
        )

        play_count_label = tk.Label(
            row,
            text=play_text,
            font=("Segoe UI", 9, "bold"),
            bg="#1B1B1B",
            fg=TEXT_SECONDARY,
        )

        play_count_label.pack(
            side="right",
            padx=10,
        )

    # =================================================
    # Listening Time Formatting
    # =================================================

    def format_listening_time(self, seconds):
        """Convert seconds into a readable duration."""

        seconds = int(seconds)

        hours = seconds // 3600

        minutes = (
            seconds % 3600
        ) // 60

        # Less than one minute.
        if hours == 0 and minutes == 0:
            return "<1 min" if seconds > 0 else "0 min"

        # Less than one hour.
        if hours == 0:
            return f"{minutes} min"

        # Whole number of hours.
        if minutes == 0:
            return f"{hours}h"

        return f"{hours}h {minutes}m"
    
