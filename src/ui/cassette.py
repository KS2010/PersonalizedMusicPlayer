"""
Cassette panel.

Design 3:
Minimal dark cassette with subtle purple neon accents.
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
    BODY_FONT,
)


class CassettePanel(tk.Frame):
    """Center Now Playing cassette panel."""

    # ---------------------------------------------------------
    # Layout constants
    # ---------------------------------------------------------

    TEXT_MAX_WIDTH = 760

    CASSETTE_WIDTH = 430
    CASSETTE_HEIGHT = 205

    def __init__(self, parent):
        super().__init__(
            parent,
            bg=CASSETTE_BG,
        )

        self.create_widgets()

    # =========================================================
    # Main UI
    # =========================================================

    def create_widgets(self):
        """Create the Now Playing interface."""

        # -----------------------------------------------------
        # NOW PLAYING
        # -----------------------------------------------------

        now_playing = tk.Label(
            self,
            text="NOW PLAYING",
            font=("Segoe UI", 11, "bold"),
            fg=ACCENT_COLOR,
            bg=CASSETTE_BG,
        )

        now_playing.pack(
            pady=(40, 18),
        )

        # -----------------------------------------------------
        # CASSETTE CONTAINER
        #
        # Fixed dimensions prevent the cassette itself from
        # affecting the center panel geometry.
        # -----------------------------------------------------

        cassette_container = tk.Frame(
            self,
            bg=CASSETTE_BG,
            width=self.CASSETTE_WIDTH + 80,
            height=self.CASSETTE_HEIGHT + 55,
        )

        cassette_container.pack(
            pady=(5, 15),
        )

        cassette_container.pack_propagate(False)

        self.create_cassette(
            cassette_container
        )

        # -----------------------------------------------------
        # SEPARATOR
        # -----------------------------------------------------

        separator = tk.Frame(
            self,
            bg=BORDER_COLOR,
            height=1,
        )

        separator.pack(
            fill="x",
            padx=40,
            pady=(15, 30),
        )

        # -----------------------------------------------------
        # SONG INFORMATION
        # -----------------------------------------------------

        self.create_song_information()

    # =========================================================
    # Cassette
    # =========================================================

    def create_cassette(self, parent):
        """Draw the stylized cassette."""

        self.cassette_canvas = tk.Canvas(
            parent,
            width=self.CASSETTE_WIDTH,
            height=self.CASSETTE_HEIGHT,
            bg=CASSETTE_BG,
            highlightthickness=0,
            bd=0,
        )

        self.cassette_canvas.pack(
            expand=True,
        )

        canvas = self.cassette_canvas

        # -----------------------------------------------------
        # Coordinates
        # -----------------------------------------------------

        left = 20
        top = 18
        right = self.CASSETTE_WIDTH - 20
        bottom = self.CASSETTE_HEIGHT - 18

        # -----------------------------------------------------
        # Shadow
        # -----------------------------------------------------

        canvas.create_rectangle(
            left + 5,
            top + 8,
            right + 5,
            bottom + 8,
            fill="#0D0D0F",
            outline="",
        )

        # -----------------------------------------------------
        # Outer cassette body
        # -----------------------------------------------------

        canvas.create_rectangle(
            left,
            top,
            right,
            bottom,
            fill="#1B1B1D",
            outline="#47474A",
            width=2,
        )

        # -----------------------------------------------------
        # Inner cassette surface
        # -----------------------------------------------------

        canvas.create_rectangle(
            left + 7,
            top + 7,
            right - 7,
            bottom - 7,
            fill="#202022",
            outline="#2E2E31",
            width=1,
        )

        # -----------------------------------------------------
        # Subtle top texture / lines
        # -----------------------------------------------------

        for y in range(
            top + 12,
            top + 43,
            4,
        ):
            canvas.create_line(
                left + 14,
                y,
                right - 14,
                y,
                fill="#242427",
                width=1,
            )

        # -----------------------------------------------------
        # Tape window frame
        # -----------------------------------------------------

        window_left = left + 75
        window_top = top + 24
        window_right = right - 75
        window_bottom = top + 62

        canvas.create_rectangle(
            window_left,
            window_top,
            window_right,
            window_bottom,
            fill="#101012",
            outline="#353539",
            width=1,
        )

        # -----------------------------------------------------
        # Tape inside window
        # -----------------------------------------------------

        canvas.create_rectangle(
            window_left + 18,
            window_top + 10,
            window_right - 18,
            window_bottom - 10,
            fill="#151517",
            outline="",
        )

        # Subtle tape lines

        for x in range(
            window_left + 24,
            window_right - 20,
            7,
        ):
            canvas.create_line(
                x,
                window_top + 12,
                x,
                window_bottom - 12,
                fill="#1D1D20",
                width=1,
            )

        # -----------------------------------------------------
        # Reels
        # -----------------------------------------------------

        self.draw_reel(
            canvas,
            left + 105,
            top + 103,
            37,
        )

        self.draw_reel(
            canvas,
            right - 105,
            top + 103,
            37,
        )

        # -----------------------------------------------------
        # Center label / window
        # -----------------------------------------------------

        label_left = 185
        label_top = 87
        label_right = 245
        label_bottom = 132

        canvas.create_rectangle(
            label_left,
            label_top,
            label_right,
            label_bottom,
            fill="#18181A",
            outline="#303034",
            width=1,
        )

        # Small purple accent line

        canvas.create_line(
            label_left + 7,
            label_top + 7,
            label_right - 7,
            label_top + 7,
            fill=ACCENT_COLOR,
            width=2,
        )

        # -----------------------------------------------------
        # Lower cassette panel
        # -----------------------------------------------------

        lower_top = bottom - 52

        canvas.create_polygon(
            left + 105,
            lower_top,
            right - 105,
            lower_top,
            right - 122,
            bottom - 9,
            left + 122,
            bottom - 9,
            fill="#19191B",
            outline=ACCENT_COLOR,
            width=1,
        )

        # -----------------------------------------------------
        # Lower panel holes
        # -----------------------------------------------------

        for x in (
            left + 155,
            left + 205,
            right - 205,
            right - 155,
        ):

            canvas.create_oval(
                x - 4,
                bottom - 25,
                x + 4,
                bottom - 17,
                fill="#09090A",
                outline="",
            )

        # Center lower hole

        center_x = self.CASSETTE_WIDTH // 2

        canvas.create_oval(
            center_x - 4,
            bottom - 25,
            center_x + 4,
            bottom - 17,
            fill="#09090A",
            outline="",
        )

        # -----------------------------------------------------
        # Corner screws
        # -----------------------------------------------------

        screw_positions = [
            (left + 15, top + 15),
            (right - 15, top + 15),
            (left + 15, bottom - 15),
            (right - 15, bottom - 15),
        ]

        for x, y in screw_positions:

            canvas.create_oval(
                x - 3,
                y - 3,
                x + 3,
                y + 3,
                fill="#505054",
                outline="#242427",
            )

            canvas.create_line(
                x - 2,
                y,
                x + 2,
                y,
                fill="#1D1D20",
                width=1,
            )

        # -----------------------------------------------------
        # Purple bottom highlight
        # -----------------------------------------------------

        canvas.create_line(
            left + 35,
            bottom - 2,
            right - 35,
            bottom - 2,
            fill="#333337",
            width=1,
        )

    # =========================================================
    # Reel
    # =========================================================

    def draw_reel(
        self,
        canvas,
        x,
        y,
        radius,
    ):
        """Draw a detailed cassette reel."""

        # Outer ring

        canvas.create_oval(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            fill="#101012",
            outline="#4B4B50",
            width=2,
        )

        # Inner ring

        inner = radius - 7

        canvas.create_oval(
            x - inner,
            y - inner,
            x + inner,
            y + inner,
            fill="#1D1D20",
            outline="#343438",
            width=2,
        )

        # Reel spokes

        spoke_length = radius - 12

        for angle in (
            0,
            60,
            120,
            180,
            240,
            300,
        ):

            import math

            radians = math.radians(angle)

            x2 = (
                x
                + math.cos(radians)
                * spoke_length
            )

            y2 = (
                y
                + math.sin(radians)
                * spoke_length
            )

            canvas.create_line(
                x,
                y,
                x2,
                y2,
                fill="#4A4A4E",
                width=3,
            )

        # Center hub

        canvas.create_oval(
            x - 8,
            y - 8,
            x + 8,
            y + 8,
            fill="#26262A",
            outline="#55555A",
            width=1,
        )

        # Purple center

        canvas.create_oval(
            x - 4,
            y - 4,
            x + 4,
            y + 4,
            fill=ACCENT_COLOR,
            outline="",
        )

    # =========================================================
    # Song Information
    # =========================================================

    def create_song_information(self):
        """Create the Now Playing metadata."""

        # -----------------------------------------------------
        # Title container
        #
        # Fixed horizontal boundaries prevent a long title
        # from changing the window geometry.
        # -----------------------------------------------------

        title_container = tk.Frame(
            self,
            bg=CASSETTE_BG,
            width=self.TEXT_MAX_WIDTH,
        )

        title_container.pack(
            fill="x",
            padx=50,
        )

        title_container.pack_propagate(False)

        # -----------------------------------------------------
        # Song title
        # -----------------------------------------------------

        self.song_title = tk.Label(
            title_container,
            text="No Song Playing",
            font=TITLE_FONT,
            bg=CASSETTE_BG,
            fg=TEXT_PRIMARY,
            anchor="center",
            justify="center",
            wraplength=self.TEXT_MAX_WIDTH,
        )

        self.song_title.pack(
            fill="x",
            pady=(0, 12),
        )

        # -----------------------------------------------------
        # Artist
        # -----------------------------------------------------

        self.artist_label = tk.Label(
            self,
            text="Unknown Artist",
            font=BODY_FONT,
            bg=CASSETTE_BG,
            fg=TEXT_SECONDARY,
            anchor="center",
            justify="center",
            wraplength=600,
        )

        self.artist_label.pack(
            fill="x",
            padx=50,
            pady=(0, 8),
        )

        # -----------------------------------------------------
        # Album
        # -----------------------------------------------------

        self.album_label = tk.Label(
            self,
            text="Album : --",
            font=BODY_FONT,
            bg=CASSETTE_BG,
            fg=TEXT_SECONDARY,
            anchor="center",
            justify="center",
            wraplength=600,
        )

        self.album_label.pack(
            fill="x",
            padx=50,
            pady=(0, 8),
        )

        # -----------------------------------------------------
        # Duration
        # -----------------------------------------------------

        self.duration_label = tk.Label(
            self,
            text="Duration : --:--",
            font=BODY_FONT,
            bg=CASSETTE_BG,
            fg=TEXT_SECONDARY,
        )

        self.duration_label.pack(
            pady=(5, 40),
        )

    # =========================================================
    # Text Helpers
    # =========================================================

    def truncate_text(
        self,
        text,
        max_chars=70,
    ):
        """
        Safely limit displayed metadata.

        The actual Song object/database value is never changed.
        """

        if text is None:
            return ""

        text = str(text)

        if len(text) <= max_chars:
            return text

        return (
            text[: max_chars - 3].rstrip()
            + "..."
        )

    # =========================================================
    # Update Song
    # =========================================================

    def update_song(self, song):
        """Update the Now Playing information."""

        self.song_title.config(
            text=self.truncate_text(
                song.title,
                max_chars=70,
            )
        )

        self.artist_label.config(
            text=self.truncate_text(
                song.artist,
                max_chars=55,
            )
        )

        self.album_label.config(
            text=(
                "Album : "
                + self.truncate_text(
                    song.album,
                    max_chars=50,
                )
            )
        )

        self.duration_label.config(
            text=(
                "Duration : "
                + song.formatted_duration
            )
        )
