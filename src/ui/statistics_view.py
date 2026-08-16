"""
Statistics dashboard for the music player.
"""

import tkinter as tk

from src.ui.theme import (
    BACKGROUND_COLOR,
    CARD_BG,
    CARD_BG_HOVER,
    SURFACE_BG,
    BORDER_COLOR,
    ACCENT_COLOR,
    ACCENT_MUTED,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TEXT_MUTED,
    PAGE_TITLE_FONT,
    SECTION_TITLE_FONT,
    BODY_FONT,
    BODY_BOLD_FONT,
    SMALL_FONT,
    SMALL_BOLD_FONT,
    STAT_VALUE_FONT,
    STAT_LABEL_FONT,
    CARD_GAP,
    DASHBOARD_PADDING_X,
    DASHBOARD_PADDING_Y,
)


class StatisticsView(tk.Frame):
    """Displays listening statistics and music analytics."""

    def __init__(
        self,
        parent,
        database_service,
    ):
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
            padx=DASHBOARD_PADDING_X,
            pady=DASHBOARD_PADDING_Y,
        )

        # ==========================================
        # Header
        # ==========================================

        self.create_header()

        # ==========================================
        # KPI cards
        # ==========================================

        self.create_kpi_section()

        # ==========================================
        # Most played section
        # ==========================================

        self.create_most_played_section()

    # =================================================
    # Header
    # =================================================

    def create_header(self):
        """Create the Statistics page header."""

        self.header_frame = tk.Frame(
            self.content_frame,
            bg=BACKGROUND_COLOR,
        )

        self.header_frame.pack(
            fill="x",
            pady=(0, 22),
        )

        # Small page indicator

        page_indicator = tk.Label(
            self.header_frame,
            text="INSIGHTS",
            font=SMALL_BOLD_FONT,
            bg=BACKGROUND_COLOR,
            fg=ACCENT_COLOR,
        )

        page_indicator.pack(
            anchor="w",
            pady=(0, 5),
        )

        # Main title

        title_label = tk.Label(
            self.header_frame,
            text="STATISTICS",
            font=PAGE_TITLE_FONT,
            bg=BACKGROUND_COLOR,
            fg=TEXT_PRIMARY,
        )

        title_label.pack(
            anchor="w",
        )

        # Subtitle

        subtitle_label = tk.Label(
            self.header_frame,
            text="Your listening activity at a glance",
            font=BODY_FONT,
            bg=BACKGROUND_COLOR,
            fg=TEXT_SECONDARY,
        )

        subtitle_label.pack(
            anchor="w",
            pady=(6, 0),
        )

    # =================================================
    # KPI Section
    # =================================================

    def create_kpi_section(self):
        """Create the four statistics KPI cards."""

        self.kpi_frame = tk.Frame(
            self.content_frame,
            bg=BACKGROUND_COLOR,
        )

        self.kpi_frame.pack(
            fill="x",
            pady=(0, 26),
        )

        # Four equal columns.

        for column in range(4):

            self.kpi_frame.grid_columnconfigure(
                column,
                weight=1,
                uniform="statistics_kpi",
            )

        # ==========================================
        # Total songs
        # ==========================================

        self.total_songs_value = self.create_stat_card(
            self.kpi_frame,
            column=0,
            icon="♫",
            title="TOTAL SONGS",
        )

        # ==========================================
        # Total plays
        # ==========================================

        self.total_plays_value = self.create_stat_card(
            self.kpi_frame,
            column=1,
            icon="▶",
            title="TOTAL PLAYS",
        )

        # ==========================================
        # Favorites
        # ==========================================

        self.favorite_count_value = self.create_stat_card(
            self.kpi_frame,
            column=2,
            icon="♥",
            title="FAVORITES",
        )

        # ==========================================
        # Listening time
        # ==========================================

        self.listening_time_value = self.create_stat_card(
            self.kpi_frame,
            column=3,
            icon="◷",
            title="LISTENING TIME",
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
        """Create one polished statistics KPI card."""

        card = tk.Frame(
            parent,
            bg=CARD_BG,
            height=112,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=(
                0 if column == 0 else CARD_GAP // 2,
                0 if column == 3 else CARD_GAP // 2,
            ),
        )

        card.grid_propagate(False)

        # ==========================================
        # Main content
        # ==========================================

        content = tk.Frame(
            card,
            bg=CARD_BG,
        )

        content.pack(
            fill="both",
            expand=True,
            padx=16,
            pady=13,
        )

        # ==========================================
        # Icon
        # ==========================================

        icon_frame = tk.Frame(
            content,
            bg=ACCENT_MUTED,
            width=42,
            height=42,
        )

        icon_frame.pack(
            side="left",
            padx=(0, 13),
            anchor="center",
        )

        icon_frame.pack_propagate(False)

        icon_label = tk.Label(
            icon_frame,
            text=icon,
            font=(
                "Segoe UI Symbol",
                18,
            ),
            bg=ACCENT_MUTED,
            fg=ACCENT_COLOR,
        )

        icon_label.pack(
            expand=True,
        )

        # ==========================================
        # Text area
        # ==========================================

        text_frame = tk.Frame(
            content,
            bg=CARD_BG,
        )

        text_frame.pack(
            side="left",
            fill="both",
            expand=True,
        )

        # ==========================================
        # Value
        # ==========================================

        value_label = tk.Label(
            text_frame,
            text="0",
            font=STAT_VALUE_FONT,
            bg=CARD_BG,
            fg=TEXT_PRIMARY,
            anchor="w",
        )

        value_label.pack(
            anchor="w",
            pady=(0, 1),
        )

        # ==========================================
        # Title
        # ==========================================

        title_label = tk.Label(
            text_frame,
            text=title,
            font=STAT_LABEL_FONT,
            bg=CARD_BG,
            fg=TEXT_MUTED,
            anchor="w",
        )

        title_label.pack(
            anchor="w",
        )

        # ==========================================
        # Hover widgets
        # ==========================================

        hover_widgets = [
            card,
            content,
            icon_frame,
            icon_label,
            text_frame,
            value_label,
            title_label,
        ]

        for widget in hover_widgets:

            widget.bind(
                "<Enter>",
                lambda event,
                widgets=hover_widgets,
                icon_box=icon_frame,
                icon_widget=icon_label,
                value_widget=value_label,
                title_widget=title_label:
                self.set_card_hover(
                    widgets,
                    icon_box,
                    icon_widget,
                    value_widget,
                    title_widget,
                    True,
                ),
            )

            widget.bind(
                "<Leave>",
                lambda event,
                widgets=hover_widgets,
                icon_box=icon_frame,
                icon_widget=icon_label,
                value_widget=value_label,
                title_widget=title_label:
                self.set_card_hover(
                    widgets,
                    icon_box,
                    icon_widget,
                    value_widget,
                    title_widget,
                    False,
                ),
            )

        return value_label

    # =================================================
    # KPI Hover
    # =================================================

    def set_card_hover(
        self,
        widgets,
        icon_box,
        icon_widget,
        value_widget,
        title_widget,
        hovering,
    ):
        """Apply the KPI card hover state."""

        if hovering:

            background = CARD_BG_HOVER
            title_color = TEXT_SECONDARY

        else:

            background = CARD_BG
            title_color = TEXT_MUTED

        for widget in widgets:

            try:

                widget.configure(
                    bg=background,
                )

            except tk.TclError:

                pass

        try:

            icon_box.configure(
                bg=ACCENT_MUTED,
            )

            icon_widget.configure(
                bg=ACCENT_MUTED,
                fg=ACCENT_COLOR,
            )

            value_widget.configure(
                bg=background,
                fg=TEXT_PRIMARY,
            )

            title_widget.configure(
                bg=background,
                fg=title_color,
            )

        except tk.TclError:

            pass

    # =================================================
    # Most Played Section
    # =================================================

    def create_most_played_section(self):
        """Create the most played songs section."""

        self.most_played_container = tk.Frame(
            self.content_frame,
            bg=SURFACE_BG,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
        )

        self.most_played_container.pack(
            fill="both",
            expand=True,
        )

        # ==========================================
        # Header
        # ==========================================

        header_frame = tk.Frame(
            self.most_played_container,
            bg=SURFACE_BG,
        )

        header_frame.pack(
            fill="x",
            padx=22,
            pady=(18, 14),
        )

        # Header title

        title_label = tk.Label(
            header_frame,
            text="LISTENING LEADERS",
            font=SECTION_TITLE_FONT,
            bg=SURFACE_BG,
            fg=TEXT_PRIMARY,
        )

        title_label.pack(
            side="left",
        )

        # Header subtitle

        subtitle_label = tk.Label(
            header_frame,
            text="Your most played tracks",
            font=SMALL_FONT,
            bg=SURFACE_BG,
            fg=TEXT_MUTED,
        )

        subtitle_label.pack(
            side="left",
            padx=10,
        )

        # ==========================================
        # Header separator
        # ==========================================

        separator = tk.Frame(
            self.most_played_container,
            bg=BORDER_COLOR,
            height=1,
        )

        separator.pack(
            fill="x",
            padx=22,
        )

        # ==========================================
        # Column header
        # ==========================================

        self.create_table_header()

        # ==========================================
        # Song list
        # ==========================================

        self.most_played_frame = tk.Frame(
            self.most_played_container,
            bg=SURFACE_BG,
        )

        self.most_played_frame.pack(
            fill="both",
            expand=True,
            padx=22,
            pady=(0, 12),
        )

    # =================================================
    # Table Header
    # =================================================

    def create_table_header(self):
        """Create the most-played table header."""

        header = tk.Frame(
            self.most_played_container,
            bg="#202126",
            height=36,
        )

        header.pack(
            fill="x",
            padx=1,
            pady=(10, 0),
        )

        header.pack_propagate(False)

        # ==========================================
        # Rank
        # ==========================================

        rank_label = tk.Label(
            header,
            text="#",
            font=SMALL_BOLD_FONT,
            bg="#202126",
            fg=TEXT_MUTED,
            width=5,
            anchor="center",
        )

        rank_label.pack(
            side="left",
            padx=(14, 0),
        )

        # ==========================================
        # Track
        # ==========================================

        track_label = tk.Label(
            header,
            text="TRACK",
            font=SMALL_BOLD_FONT,
            bg="#202126",
            fg=TEXT_MUTED,
            anchor="w",
        )

        track_label.pack(
            side="left",
            padx=(10, 0),
        )

        # ==========================================
        # Plays
        # ==========================================

        plays_label = tk.Label(
            header,
            text="PLAYS",
            font=SMALL_BOLD_FONT,
            bg="#202126",
            fg=TEXT_MUTED,
            width=12,
            anchor="e",
        )

        plays_label.pack(
            side="right",
            padx=(0, 18),
        )

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
        # Update KPI cards
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
        # Refresh most played
        # ==========================================

        self.refresh_most_played()

    # =================================================
    # Most Played
    # =================================================

    def refresh_most_played(self):
        """Display the most frequently played songs."""

        # Remove existing rows.

        for widget in (
            self.most_played_frame.winfo_children()
        ):
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

            self.create_empty_state()

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
        """Create one polished most-played song row."""

        row = tk.Frame(
            self.most_played_frame,
            bg=SURFACE_BG,
            height=64,
            cursor="hand2",
        )

        row.pack(
            fill="x",
        )

        row.pack_propagate(False)

        # ==========================================
        # Rank
        # ==========================================

        rank_label = tk.Label(
            row,
            text=f"{rank:02d}",
            font=SMALL_BOLD_FONT,
            bg=SURFACE_BG,
            fg=ACCENT_COLOR,
            width=5,
            anchor="center",
        )

        rank_label.pack(
            side="left",
            padx=(0, 8),
        )

        # ==========================================
        # Music icon
        # ==========================================

        icon_frame = tk.Frame(
            row,
            bg=ACCENT_MUTED,
            width=38,
            height=38,
        )

        icon_frame.pack(
            side="left",
            padx=(2, 12),
        )

        icon_frame.pack_propagate(False)

        icon_label = tk.Label(
            icon_frame,
            text="♫",
            font=(
                "Segoe UI Symbol",
                15,
            ),
            bg=ACCENT_MUTED,
            fg=ACCENT_COLOR,
        )

        icon_label.pack(
            expand=True,
        )

        # ==========================================
        # Song information
        # ==========================================

        info_frame = tk.Frame(
            row,
            bg=SURFACE_BG,
        )

        info_frame.pack(
            side="left",
            fill="both",
            expand=True,
            pady=8,
        )

        # ==========================================
        # Song title
        # ==========================================

        title_label = tk.Label(
            info_frame,
            text=self.truncate_text(
                song.title,
                60,
            ),
            font=BODY_BOLD_FONT,
            bg=SURFACE_BG,
            fg=TEXT_PRIMARY,
            anchor="w",
        )

        title_label.pack(
            fill="x",
        )

        # ==========================================
        # Artist
        # ==========================================

        artist_label = tk.Label(
            info_frame,
            text=self.truncate_text(
                song.artist,
                40,
            ),
            font=SMALL_FONT,
            bg=SURFACE_BG,
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
            font=SMALL_BOLD_FONT,
            bg=SURFACE_BG,
            fg=TEXT_SECONDARY,
            width=12,
            anchor="e",
        )

        play_count_label.pack(
            side="right",
            padx=(10, 18),
        )

        # ==========================================
        # Separator
        # ==========================================

        separator = tk.Frame(
            self.most_played_frame,
            bg=BORDER_COLOR,
            height=1,
        )

        separator.pack(
            fill="x",
        )

        # ==========================================
        # Hover behavior
        # ==========================================

        widgets = [
            row,
            rank_label,
            icon_frame,
            icon_label,
            info_frame,
            title_label,
            artist_label,
            play_count_label,
        ]

        for widget in widgets:

            widget.bind(
                "<Enter>",
                lambda event,
                items=widgets,
                icon=icon_frame,
                plays=play_count_label:
                self.set_song_row_hover(
                    items,
                    icon,
                    plays,
                    True,
                ),
            )

            widget.bind(
                "<Leave>",
                lambda event,
                items=widgets,
                icon=icon_frame,
                plays=play_count_label:
                self.set_song_row_hover(
                    items,
                    icon,
                    plays,
                    False,
                ),
            )

    # =================================================
    # Song Row Hover
    # =================================================

    def set_song_row_hover(
        self,
        widgets,
        icon_frame,
        plays_label,
        hovering,
    ):
        """Apply hover styling to a most-played row."""

        background = (
            CARD_BG_HOVER
            if hovering
            else SURFACE_BG
        )

        play_color = (
            ACCENT_COLOR
            if hovering
            else TEXT_SECONDARY
        )

        for widget in widgets:

            try:

                widget.configure(
                    bg=background,
                )

            except tk.TclError:

                pass

        try:

            icon_frame.configure(
                bg=ACCENT_MUTED,
            )

        except tk.TclError:

            pass

        try:

            plays_label.configure(
                bg=background,
                fg=play_color,
            )

        except tk.TclError:

            pass

    # =================================================
    # Empty State
    # =================================================

    def create_empty_state(self):
        """Create a polished empty listening state."""

        empty_frame = tk.Frame(
            self.most_played_frame,
            bg=SURFACE_BG,
        )

        empty_frame.pack(
            fill="both",
            expand=True,
        )

        # ==========================================
        # Icon
        # ==========================================

        icon_frame = tk.Frame(
            empty_frame,
            bg=ACCENT_MUTED,
            width=48,
            height=48,
        )

        icon_frame.pack(
            pady=(30, 8),
        )

        icon_frame.pack_propagate(False)

        icon_label = tk.Label(
            icon_frame,
            text="♫",
            font=(
                "Segoe UI Symbol",
                22,
            ),
            bg=ACCENT_MUTED,
            fg=ACCENT_COLOR,
        )

        icon_label.pack(
            expand=True,
        )

        # ==========================================
        # Title
        # ==========================================

        title_label = tk.Label(
            empty_frame,
            text="No listening data yet",
            font=BODY_BOLD_FONT,
            bg=SURFACE_BG,
            fg=TEXT_PRIMARY,
        )

        title_label.pack()

        # ==========================================
        # Subtitle
        # ==========================================

        subtitle_label = tk.Label(
            empty_frame,
            text=(
                "Play some music to build your listening history."
            ),
            font=SMALL_FONT,
            bg=SURFACE_BG,
            fg=TEXT_MUTED,
        )

        subtitle_label.pack(
            pady=(5, 0),
        )

    # =================================================
    # Text Utilities
    # =================================================

    def truncate_text(
        self,
        text,
        max_length,
    ):
        """Safely truncate long text."""

        if text is None:
            return ""

        text = str(text)

        if len(text) <= max_length:
            return text

        return (
            text[: max_length - 3]
            + "..."
        )

    # =================================================
    # Listening Time Formatting
    # =================================================

    def format_listening_time(
        self,
        seconds,
    ):
        """Convert seconds into a readable duration."""

        try:

            seconds = int(seconds)

        except (
            TypeError,
            ValueError,
        ):

            return "0 min"

        hours = seconds // 3600

        minutes = (
            seconds % 3600
        ) // 60

        # ==========================================
        # Less than one minute
        # ==========================================

        if hours == 0 and minutes == 0:

            if seconds > 0:
                return "<1 min"

            return "0 min"

        # ==========================================
        # Less than one hour
        # ==========================================

        if hours == 0:

            return f"{minutes} min"

        # ==========================================
        # Whole hours
        # ==========================================

        if minutes == 0:

            return f"{hours}h"

        # ==========================================
        # Hours + minutes
        # ==========================================

        return f"{hours}h {minutes}m"
