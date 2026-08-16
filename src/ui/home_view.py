"""
Home dashboard for the music player.
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
    TITLE_FONT,
    PAGE_TITLE_FONT,
    SECTION_TITLE_FONT,
    BODY_FONT,
    BODY_BOLD_FONT,
    SMALL_FONT,
    SMALL_BOLD_FONT,
    SONG_TITLE_FONT,
    SONG_ARTIST_FONT,
    STAT_VALUE_FONT,
    STAT_LABEL_FONT,
    DASHBOARD_PADDING_X,
    DASHBOARD_PADDING_Y,
    SECTION_GAP,
    CARD_GAP,
    PADDING_XL,
    HOME_HERO_BG,
    HOME_HERO_ACCENT,
)


class HomeView(tk.Frame):
    """Music-focused home dashboard."""

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
    # Main UI
    # =================================================

    def create_widgets(self):
        """Create the Home dashboard."""

        # ==========================================
        # Scrollable content area
        # ==========================================

        self.canvas = tk.Canvas(
            self,
            bg=BACKGROUND_COLOR,
            highlightthickness=0,
            bd=0,
        )

        self.scrollbar = tk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview,
            width=8,
            troughcolor=BACKGROUND_COLOR,
            bg="#2A2A2A",
            activebackground="#3A3A3A",
            relief="flat",
            bd=0,
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set,
        )

        self.scrollbar.pack(
            side="right",
            fill="y",
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True,
        )

        self.content_frame = tk.Frame(
            self.canvas,
            bg=BACKGROUND_COLOR,
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.content_frame,
            anchor="nw",
        )

        self.content_frame.bind(
            "<Configure>",
            self.update_scroll_region,
        )

        self.canvas.bind(
            "<Configure>",
            self.resize_content,
        )

        # Mouse-wheel scrolling.
        self.canvas.bind_all(
            "<MouseWheel>",
            self.handle_mousewheel,
        )

        # Linux mouse-wheel support.
        self.canvas.bind_all(
            "<Button-4>",
            self.handle_mousewheel_linux_up,
        )

        self.canvas.bind_all(
            "<Button-5>",
            self.handle_mousewheel_linux_down,
        )

        # ==========================================
        # Header
        # ==========================================

        self.create_header()

        # ==========================================
        # Hero section
        # ==========================================

        self.create_hero_section()

        # ==========================================
        # Library snapshot
        # ==========================================

        self.create_library_snapshot()

        # ==========================================
        # Recently played
        # ==========================================

        self.create_recent_section()

    # =================================================
    # Header
    # =================================================

    def create_header(self):
        """Create the Home page header."""

        self.header_frame = tk.Frame(
            self.content_frame,
            bg=BACKGROUND_COLOR,
        )

        self.header_frame.pack(
            fill="x",
            padx=DASHBOARD_PADDING_X,
            pady=(
                DASHBOARD_PADDING_Y,
                10,
            ),
        )

        # ==========================================
        # Small page indicator
        # ==========================================

        self.page_indicator = tk.Label(
            self.header_frame,
            text="MUSIC PLAYER",
            font=SMALL_BOLD_FONT,
            bg=BACKGROUND_COLOR,
            fg=ACCENT_COLOR,
        )

        self.page_indicator.pack(
            anchor="w",
            pady=(0, 5),
        )

        # ==========================================
        # Main title
        # ==========================================

        self.title_label = tk.Label(
            self.header_frame,
            text="WELCOME BACK",
            font=PAGE_TITLE_FONT,
            bg=BACKGROUND_COLOR,
            fg=TEXT_PRIMARY,
        )

        self.title_label.pack(
            anchor="w",
        )

        # ==========================================
        # Subtitle
        # ==========================================

        self.subtitle_label = tk.Label(
            self.header_frame,
            text=(
                "Your music, your library, "
                "your listening space."
            ),
            font=BODY_FONT,
            bg=BACKGROUND_COLOR,
            fg=TEXT_SECONDARY,
        )

        self.subtitle_label.pack(
            anchor="w",
            pady=(6, 0),
        )

    # =================================================
    # Hero Section
    # =================================================

    def create_hero_section(self):
        """Create the main music-focused hero section."""

        self.hero_frame = tk.Frame(
            self.content_frame,
            bg=HOME_HERO_BG,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
        )

        self.hero_frame.pack(
            fill="x",
            padx=DASHBOARD_PADDING_X,
            pady=(
                15,
                SECTION_GAP,
            ),
        )

        # ==========================================
        # Left visual block
        # ==========================================

        self.hero_visual = tk.Frame(
            self.hero_frame,
            bg=ACCENT_MUTED,
            width=150,
            height=150,
        )

        self.hero_visual.pack(
            side="left",
            padx=PADDING_XL,
            pady=PADDING_XL,
        )

        self.hero_visual.pack_propagate(False)

        # ==========================================
        # Decorative inner border
        # ==========================================

        self.hero_visual_border = tk.Frame(
            self.hero_visual,
            bg=HOME_HERO_BG,
            width=118,
            height=118,
            highlightbackground=HOME_HERO_ACCENT,
            highlightthickness=1,
        )

        self.hero_visual_border.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
        )

        self.hero_visual_border.pack_propagate(False)

        self.hero_icon = tk.Label(
            self.hero_visual_border,
            text="♫",
            font=(
                "Segoe UI Symbol",
                54,
            ),
            bg=HOME_HERO_BG,
            fg=HOME_HERO_ACCENT,
        )

        self.hero_icon.pack(
            expand=True,
        )

        # ==========================================
        # Right content
        # ==========================================

        self.hero_content = tk.Frame(
            self.hero_frame,
            bg=HOME_HERO_BG,
        )

        self.hero_content.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(
                0,
                PADDING_XL,
            ),
            pady=PADDING_XL,
        )

        # ==========================================
        # Tag
        # ==========================================

        hero_tag_frame = tk.Frame(
            self.hero_content,
            bg=HOME_HERO_BG,
        )

        hero_tag_frame.pack(
            anchor="w",
        )

        hero_tag_indicator = tk.Frame(
            hero_tag_frame,
            bg=ACCENT_COLOR,
            width=5,
            height=15,
        )

        hero_tag_indicator.pack(
            side="left",
            padx=(0, 8),
        )

        hero_tag_indicator.pack_propagate(
            False
        )

        hero_tag = tk.Label(
            hero_tag_frame,
            text="YOUR MUSIC LIBRARY",
            font=SMALL_BOLD_FONT,
            bg=HOME_HERO_BG,
            fg=ACCENT_COLOR,
        )

        hero_tag.pack(
            side="left",
        )

        # ==========================================
        # Hero title
        # ==========================================

        self.hero_title = tk.Label(
            self.hero_content,
            text="Ready to listen?",
            font=TITLE_FONT,
            bg=HOME_HERO_BG,
            fg=TEXT_PRIMARY,
        )

        self.hero_title.pack(
            anchor="w",
            pady=(9, 4),
        )

        # ==========================================
        # Hero description
        # ==========================================

        self.hero_description = tk.Label(
            self.hero_content,
            text=(
                "Pick something from your recent "
                "listening history or explore your library."
            ),
            font=BODY_FONT,
            bg=HOME_HERO_BG,
            fg=TEXT_SECONDARY,
            justify="left",
            wraplength=650,
        )

        self.hero_description.pack(
            anchor="w",
        )

        # ==========================================
        # Hero footer
        # ==========================================

        hero_footer = tk.Frame(
            self.hero_content,
            bg=HOME_HERO_BG,
        )

        hero_footer.pack(
            anchor="w",
            pady=(18, 0),
        )

        footer_dot = tk.Frame(
            hero_footer,
            bg=ACCENT_COLOR,
            width=7,
            height=7,
        )

        footer_dot.pack(
            side="left",
            padx=(0, 7),
            pady=3,
        )

        footer_dot.pack_propagate(
            False
        )

        footer_label = tk.Label(
            hero_footer,
            text="Your personal listening space",
            font=SMALL_FONT,
            bg=HOME_HERO_BG,
            fg=TEXT_MUTED,
        )

        footer_label.pack(
            side="left",
        )

    # =================================================
    # Library Snapshot
    # =================================================

    def create_library_snapshot(self):
        """Create a compact library snapshot."""

        section_header = tk.Frame(
            self.content_frame,
            bg=BACKGROUND_COLOR,
        )

        section_header.pack(
            fill="x",
            padx=DASHBOARD_PADDING_X,
            pady=(0, 10),
        )

        # ==========================================
        # Section title
        # ==========================================

        section_title = tk.Label(
            section_header,
            text="YOUR MUSIC",
            font=SECTION_TITLE_FONT,
            bg=BACKGROUND_COLOR,
            fg=TEXT_PRIMARY,
        )

        section_title.pack(
            side="left",
        )

        # ==========================================
        # Section subtitle
        # ==========================================

        section_subtitle = tk.Label(
            section_header,
            text="A quick look at your library",
            font=SMALL_FONT,
            bg=BACKGROUND_COLOR,
            fg=TEXT_MUTED,
        )

        section_subtitle.pack(
            side="left",
            padx=10,
        )

        # ==========================================
        # Cards
        # ==========================================

        self.snapshot_frame = tk.Frame(
            self.content_frame,
            bg=BACKGROUND_COLOR,
        )

        self.snapshot_frame.pack(
            fill="x",
            padx=DASHBOARD_PADDING_X,
            pady=(0, SECTION_GAP),
        )

        (
            self.total_songs_card,
            self.total_songs_value,
        ) = self.create_snapshot_card(
            self.snapshot_frame,
            "0",
            "SONGS",
            "♫",
        )

        self.total_songs_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, CARD_GAP),
        )

        (
            self.favorite_card,
            self.favorite_value,
        ) = self.create_snapshot_card(
            self.snapshot_frame,
            "0",
            "FAVORITES",
            "♥",
        )

        self.favorite_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(
                CARD_GAP,
                CARD_GAP,
            ),
        )

        (
            self.recent_card,
            self.recent_value,
        ) = self.create_snapshot_card(
            self.snapshot_frame,
            "0",
            "RECENT",
            "↻",
        )

        self.recent_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(CARD_GAP, 0),
        )

    # =================================================
    # Snapshot Card
    # =================================================

    def create_snapshot_card(
        self,
        parent,
        value,
        label,
        icon,
    ):
        """Create a polished Home KPI card."""

        # ==========================================
        # Card
        # ==========================================

        card = tk.Frame(
            parent,
            bg=CARD_BG,
            height=112,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
            cursor="hand2",
        )

        # Keep all three cards the same height.
        card.pack_propagate(False)

        # ==========================================
        # Inner container
        # ==========================================

        inner_frame = tk.Frame(
            card,
            bg=CARD_BG,
        )

        inner_frame.pack(
            fill="both",
            expand=True,
            padx=16,
            pady=13,
        )

        # ==========================================
        # Icon container
        # ==========================================

        icon_frame = tk.Frame(
            inner_frame,
            bg=ACCENT_MUTED,
            width=42,
            height=42,
        )

        icon_frame.pack(
            side="left",
            padx=(0, 13),
        )

        icon_frame.pack_propagate(
            False
        )

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
        # Text container
        # ==========================================

        text_frame = tk.Frame(
            inner_frame,
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
            text=value,
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
        # Label
        # ==========================================

        label_widget = tk.Label(
            text_frame,
            text=label,
            font=STAT_LABEL_FONT,
            bg=CARD_BG,
            fg=TEXT_MUTED,
            anchor="w",
        )

        label_widget.pack(
            anchor="w",
        )

        # ==========================================
        # Bottom accent
        # ==========================================

        accent_line = tk.Frame(
            card,
            bg=ACCENT_COLOR,
            height=2,
        )

        accent_line.place(
            relx=0,
            rely=1,
            relwidth=0,
            anchor="sw",
        )

        # ==========================================
        # Hover behavior
        # ==========================================

        hover_widgets = [
            card,
            inner_frame,
            icon_frame,
            icon_label,
            text_frame,
            value_label,
            label_widget,
        ]

        for widget in hover_widgets:

            widget.bind(
                "<Enter>",
                lambda event,
                widgets=hover_widgets,
                icon_container=icon_frame,
                icon_widget=icon_label,
                value_widget=value_label,
                label_item=label_widget,
                line=accent_line:
                self.set_snapshot_card_hover(
                    widgets,
                    icon_container,
                    icon_widget,
                    value_widget,
                    label_item,
                    line,
                    True,
                ),
            )

            widget.bind(
                "<Leave>",
                lambda event,
                widgets=hover_widgets,
                icon_container=icon_frame,
                icon_widget=icon_label,
                value_widget=value_label,
                label_item=label_widget,
                line=accent_line:
                self.set_snapshot_card_hover(
                    widgets,
                    icon_container,
                    icon_widget,
                    value_widget,
                    label_item,
                    line,
                    False,
                ),
            )

        return card, value_label

    # =================================================
    # Snapshot Card Hover
    # =================================================

    def set_snapshot_card_hover(
        self,
        widgets,
        icon_frame,
        icon_label,
        value_label,
        label_widget,
        accent_line,
        hovering,
    ):
        """Apply or remove the KPI card hover state."""

        if hovering:

            background = CARD_BG_HOVER
            icon_background = ACCENT_MUTED
            value_color = TEXT_PRIMARY
            label_color = TEXT_SECONDARY
            icon_color = ACCENT_COLOR
            line_width = 1

        else:

            background = CARD_BG
            icon_background = ACCENT_MUTED
            value_color = TEXT_PRIMARY
            label_color = TEXT_MUTED
            icon_color = ACCENT_COLOR
            line_width = 0

        # ==========================================
        # Background
        # ==========================================

        for widget in widgets:

            try:

                widget.configure(
                    bg=background,
                )

            except tk.TclError:

                pass

        # ==========================================
        # Icon
        # ==========================================

        try:

            icon_frame.configure(
                bg=icon_background,
            )

        except tk.TclError:

            pass

        try:

            icon_label.configure(
                bg=icon_background,
                fg=icon_color,
            )

        except tk.TclError:

            pass

        # ==========================================
        # Text
        # ==========================================

        try:

            value_label.configure(
                bg=background,
                fg=value_color,
            )

        except tk.TclError:

            pass

        try:

            label_widget.configure(
                bg=background,
                fg=label_color,
            )

        except tk.TclError:

            pass

        # ==========================================
        # Accent line
        # ==========================================

        try:

            accent_line.place_configure(
                relwidth=line_width,
            )

        except tk.TclError:

            pass

    # =================================================
    # Recently Played Section
    # =================================================

    def create_recent_section(self):
        """Create the recently played section."""

        # ==========================================
        # Section header
        # ==========================================

        header_frame = tk.Frame(
            self.content_frame,
            bg=BACKGROUND_COLOR,
        )

        header_frame.pack(
            fill="x",
            padx=DASHBOARD_PADDING_X,
            pady=(0, 10),
        )

        recent_title = tk.Label(
            header_frame,
            text="RECENTLY PLAYED",
            font=SECTION_TITLE_FONT,
            bg=BACKGROUND_COLOR,
            fg=TEXT_PRIMARY,
        )

        recent_title.pack(
            side="left",
        )

        recent_subtitle = tk.Label(
            header_frame,
            text="Continue where you left off",
            font=SMALL_FONT,
            bg=BACKGROUND_COLOR,
            fg=TEXT_MUTED,
        )

        recent_subtitle.pack(
            side="left",
            padx=10,
        )

        # ==========================================
        # Recent list container
        # ==========================================

        self.recent_frame = tk.Frame(
            self.content_frame,
            bg=SURFACE_BG,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
        )

        self.recent_frame.pack(
            fill="x",
            padx=DASHBOARD_PADDING_X,
            pady=(0, DASHBOARD_PADDING_Y),
        )

    # =================================================
    # Refresh Home
    # =================================================

    def refresh_home(self):
        """Refresh all Home dashboard information."""

        if self.database_service is None:
            return

        self.refresh_library_snapshot()
        self.refresh_recent_songs()

        # Make sure the scroll area starts at the top
        # after a complete Home refresh.
        self.after_idle(
            lambda: self.canvas.yview_moveto(0)
        )

    # =================================================
    # Library Snapshot Refresh
    # =================================================

    def refresh_library_snapshot(self):
        """Refresh the library summary."""

        total_songs = (
            self.database_service.get_total_songs()
        )

        favorite_count = (
            self.database_service.get_favorite_count()
        )

        recent_songs = (
            self.database_service.get_recent_songs(
                limit=20
            )
        )

        self.total_songs_value.config(
            text=str(total_songs)
        )

        self.favorite_value.config(
            text=str(favorite_count)
        )

        self.recent_value.config(
            text=str(len(recent_songs))
        )

    # =================================================
    # Recent Songs Refresh
    # =================================================

    def refresh_recent_songs(self):
        """Refresh the recently played list."""

        for widget in (
            self.recent_frame.winfo_children()
        ):
            widget.destroy()

        recent_songs = (
            self.database_service.get_recent_songs(
                limit=6
            )
        )

        if not recent_songs:

            self.show_recent_empty_state()

            return

        # ==========================================
        # Table header
        # ==========================================

        self.create_recent_table_header()

        # ==========================================
        # Song rows
        # ==========================================

        for index, song in enumerate(
            recent_songs
        ):

            self.create_recent_song_row(
                song,
                index,
            )

    # =================================================
    # Recent Table Header
    # =================================================

    def create_recent_table_header(self):
        """Create the header row for recently played."""

        header = tk.Frame(
            self.recent_frame,
            bg="#202126",
            height=38,
        )

        header.pack(
            fill="x",
        )

        header.pack_propagate(False)

        # ==========================================
        # Number
        # ==========================================

        number_label = tk.Label(
            header,
            text="#",
            font=SMALL_BOLD_FONT,
            bg="#202126",
            fg=TEXT_MUTED,
            width=5,
            anchor="center",
        )

        number_label.pack(
            side="left",
            padx=(10, 0),
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
            padx=(8, 0),
        )

        # ==========================================
        # Duration
        # ==========================================

        duration_label = tk.Label(
            header,
            text="TIME",
            font=SMALL_BOLD_FONT,
            bg="#202126",
            fg=TEXT_MUTED,
            width=9,
            anchor="e",
        )

        duration_label.pack(
            side="right",
            padx=(0, 15),
        )

        # ==========================================
        # Separator
        # ==========================================

        separator = tk.Frame(
            self.recent_frame,
            bg=BORDER_COLOR,
            height=1,
        )

        separator.pack(
            fill="x",
        )

    # =================================================
    # Recent Song Row
    # =================================================

    def create_recent_song_row(
        self,
        song,
        index,
    ):
        """Create a polished clickable recently played row."""

        row_bg = SURFACE_BG

        row = tk.Frame(
            self.recent_frame,
            bg=row_bg,
            cursor="hand2",
            height=64,
        )

        row.pack(
            fill="x",
        )

        row.pack_propagate(False)

        # ==========================================
        # Track number
        # ==========================================

        number_label = tk.Label(
            row,
            text=f"{index + 1:02d}",
            font=SMALL_BOLD_FONT,
            bg=row_bg,
            fg=TEXT_MUTED,
            width=5,
            anchor="center",
        )

        number_label.pack(
            side="left",
            padx=(10, 0),
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
            padx=(5, 12),
        )

        icon_frame.pack_propagate(False)

        icon_label = tk.Label(
            icon_frame,
            text="♫",
            font=(
                "Segoe UI Symbol",
                16,
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
            bg=row_bg,
        )

        info_frame.pack(
            side="left",
            fill="both",
            expand=True,
            pady=8,
        )

        # ==========================================
        # Title
        # ==========================================

        title_text = self.truncate_text(
            song.title,
            48,
        )

        title_label = tk.Label(
            info_frame,
            text=title_text,
            font=SONG_TITLE_FONT,
            bg=row_bg,
            fg=TEXT_PRIMARY,
            anchor="w",
        )

        title_label.pack(
            fill="x",
        )

        # ==========================================
        # Artist
        # ==========================================

        artist_text = self.truncate_text(
            song.artist,
            38,
        )

        artist_label = tk.Label(
            info_frame,
            text=artist_text,
            font=SONG_ARTIST_FONT,
            bg=row_bg,
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
            font=SMALL_FONT,
            bg=row_bg,
            fg=TEXT_MUTED,
            width=9,
            anchor="e",
        )

        duration_label.pack(
            side="right",
            padx=(8, 15),
        )

        # ==========================================
        # Play indicator
        # ==========================================

        play_label = tk.Label(
            row,
            text="▶",
            font=(
                "Segoe UI Symbol",
                11,
            ),
            bg=row_bg,
            fg=TEXT_MUTED,
            width=3,
            anchor="center",
        )

        play_label.pack(
            side="right",
            padx=(2, 2),
        )

        # ==========================================
        # Row separator
        # ==========================================

        separator = tk.Frame(
            self.recent_frame,
            bg=BORDER_COLOR,
            height=1,
        )

        separator.pack(
            fill="x",
        )

        # ==========================================
        # Click handling
        # ==========================================

        clickable_widgets = [
            row,
            number_label,
            icon_frame,
            icon_label,
            info_frame,
            title_label,
            artist_label,
            duration_label,
            play_label,
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

        # ==========================================
        # Hover handling
        # ==========================================

        for widget in clickable_widgets:

            widget.bind(
                "<Enter>",
                lambda event,
                widgets=clickable_widgets,
                icon=icon_frame,
                play=play_label:
                self.set_row_hover(
                    widgets,
                    icon,
                    play,
                    True,
                ),
            )

            widget.bind(
                "<Leave>",
                lambda event,
                widgets=clickable_widgets,
                icon=icon_frame,
                play=play_label:
                self.set_row_hover(
                    widgets,
                    icon,
                    play,
                    False,
                ),
            )

    # =================================================
    # Text Utilities
    # =================================================

    def truncate_text(
        self,
        text,
        max_length,
    ):
        """Safely truncate long UI text."""

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
    # Row Hover
    # =================================================

    def set_row_hover(
        self,
        widgets,
        icon_frame,
        play_label,
        hovering,
    ):
        """Apply a polished hover state to a recent song row."""

        background = (
            CARD_BG_HOVER
            if hovering
            else SURFACE_BG
        )

        play_color = (
            ACCENT_COLOR
            if hovering
            else TEXT_MUTED
        )

        number_color = (
            ACCENT_COLOR
            if hovering
            else TEXT_MUTED
        )

        # ==========================================
        # Row background
        # ==========================================

        for widget in widgets:

            try:

                widget.configure(
                    bg=background,
                )

            except tk.TclError:

                pass

        # ==========================================
        # Icon
        # ==========================================

        try:

            icon_frame.configure(
                bg=ACCENT_MUTED,
            )

        except tk.TclError:

            pass

        # ==========================================
        # Number
        # ==========================================

        try:

            widgets[1].configure(
                fg=number_color,
            )

        except (
            tk.TclError,
            IndexError,
        ):

            pass

        # ==========================================
        # Play indicator
        # ==========================================

        try:

            play_label.configure(
                bg=background,
                fg=play_color,
            )

        except tk.TclError:

            pass

    # =================================================
    # Empty Recent State
    # =================================================

    def show_recent_empty_state(self):
        """Display an empty recently played state."""

        empty_frame = tk.Frame(
            self.recent_frame,
            bg=SURFACE_BG,
            height=165,
        )

        empty_frame.pack(
            fill="x",
        )

        empty_frame.pack_propagate(
            False,
        )

        # ==========================================
        # Icon
        # ==========================================

        icon_container = tk.Frame(
            empty_frame,
            bg=ACCENT_MUTED,
            width=46,
            height=46,
        )

        icon_container.pack(
            pady=(23, 6),
        )

        icon_container.pack_propagate(
            False,
        )

        icon_label = tk.Label(
            icon_container,
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
            text="Nothing played yet",
            font=BODY_BOLD_FONT,
            bg=SURFACE_BG,
            fg=TEXT_PRIMARY,
        )

        title_label.pack()

        # ==========================================
        # Description
        # ==========================================

        subtitle_label = tk.Label(
            empty_frame,
            text=(
                "Start listening and your recent tracks "
                "will appear here."
            ),
            font=SMALL_FONT,
            bg=SURFACE_BG,
            fg=TEXT_MUTED,
        )

        subtitle_label.pack(
            pady=(4, 0),
        )

    # =================================================
    # Song Selection
    # =================================================

    def select_song(
        self,
        song,
    ):
        """Send the selected song to MainWindow."""

        if self.on_song_selected:

            self.on_song_selected(
                song
            )

    # =================================================
    # Scrolling
    # =================================================

    def update_scroll_region(
        self,
        event=None,
    ):
        """Update the scrollable region."""

        self.canvas.configure(
            scrollregion=self.canvas.bbox(
                "all"
            )
        )

    def resize_content(
        self,
        event,
    ):
        """Resize the inner frame to match the canvas."""

        self.canvas.itemconfigure(
            self.canvas_window,
            width=event.width,
        )

    def handle_mousewheel(
        self,
        event,
    ):
        """Handle Windows/macOS mouse-wheel scrolling."""

        try:

            if event.delta == 0:
                return

            self.canvas.yview_scroll(
                int(
                    -1
                    * (
                        event.delta
                        / 120
                    )
                ),
                "units",
            )

        except tk.TclError:

            pass

    def handle_mousewheel_linux_up(
        self,
        event,
    ):
        """Handle Linux scroll-up events."""

        try:

            self.canvas.yview_scroll(
                -3,
                "units",
            )

        except tk.TclError:

            pass

    def handle_mousewheel_linux_down(
        self,
        event,
    ):
        """Handle Linux scroll-down events."""

        try:

            self.canvas.yview_scroll(
                3,
                "units",
            )

        except tk.TclError:

            pass
