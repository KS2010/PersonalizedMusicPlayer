"""
Playback controls for the music player.
"""

import tkinter as tk
from tkinter import ttk
from turtle import position



from src.ui.theme import (
    CONTROLS_BG,
    ACCENT_COLOR,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    BODY_FONT,
    SMALL_FONT,
)


class PlayerControls(tk.Frame):
    """Bottom playback control panel."""

    def __init__(self, parent, on_play_pause=None, on_volume_change=None,on_seek=None,on_previous=None,on_next=None,):
        super().__init__(
            parent,
            bg=CONTROLS_BG,
            height=140,
        )
        self.on_play_pause = on_play_pause
        self.on_volume_change = on_volume_change
        self.on_seek = on_seek
        self.on_previous = on_previous
        self.on_next = on_next

        self.is_seeking = False
        self.pack_propagate(False)

        self.configure_styles()
        self.create_widgets()

    def configure_styles(self):
        """Configure custom styles for playback sliders."""

        style = ttk.Style(self)

        style.configure(
            "Player.Horizontal.TScale",
            background=CONTROLS_BG,
            troughcolor="#2A2A2A",
        )

    def create_widgets(self):
        """Create playback controls."""

        # ==========================================
        # Progress section
        # ==========================================

        progress_frame = tk.Frame(
            self,
            bg=CONTROLS_BG,
        )

        progress_frame.pack(
            fill="x",
            padx=100,
            pady=(20, 10),
        )

        self.current_time_label = tk.Label(
            progress_frame,
            text="0:00",
            font=SMALL_FONT,
            bg=CONTROLS_BG,
            fg=TEXT_SECONDARY,
        )

        self.current_time_label.pack(side="left")

        self.progress_bar = ttk.Scale(
            progress_frame,
            from_=0,
            to=100,
            orient="horizontal",
            style="Player.Horizontal.TScale",
        )
        self.progress_bar.pack(
            side="left",
            fill="x",
            expand=True,
            padx=15,
        )
        self.progress_bar.bind(
            "<ButtonPress-1>",
            self.start_seek,
            )

        self.progress_bar.bind(
            "<ButtonRelease-1>",
            self.finish_seek,
            )

        self.duration_label = tk.Label(
            progress_frame,
            text="0:00",
            font=SMALL_FONT,
            bg=CONTROLS_BG,
            fg=TEXT_SECONDARY,
        )

        self.duration_label.pack(side="right")
        self.progress_bar.set(0)
        # ==========================================
        # Control buttons
        # ==========================================

        controls_row = tk.Frame(
            self,
            bg=CONTROLS_BG,
        )

        controls_row.pack(
            fill="x",
            padx=80,
        )

        # Left spacer keeps controls centered.
        left_section = tk.Frame(
            controls_row,
            bg=CONTROLS_BG,
            width=200,
        )

        left_section.pack(side="left")
        left_section.pack_propagate(False)

        # Center playback buttons.
        button_frame = tk.Frame(
            controls_row,
            bg=CONTROLS_BG,
        )

        button_frame.pack(
            side="left",
            expand=True,
        )

        self.previous_button = self.create_button(
            button_frame,
            "⏮",
            command=self.handle_previous,
        )

        self.previous_button.pack(
            side="left",
            padx=10,
        )

        self.play_button = self.create_button(
            button_frame,
            "▶",
            accent=True,
            command=self.handle_play_pause,
        )

        self.play_button.pack(
            side="left",
            padx=12,
            ipady=3,
        )

        self.next_button = self.create_button(
            button_frame,
            "⏭",
            command=self.handle_next,
        )

        self.next_button.pack(
            side="left",
            padx=10,
        )

        # ==========================================
        # Volume
        # ==========================================

        volume_frame = tk.Frame(
            controls_row,
            bg=CONTROLS_BG,
            width=200,
        )

        volume_frame.pack(
            side="right",
        )

        volume_label = tk.Label(
            volume_frame,
            text="VOL",
            font=("Segoe UI", 9, "bold"),
            bg=CONTROLS_BG,
            fg=TEXT_SECONDARY,
        )

        volume_label.pack(
            side="left",
            padx=(0, 10),
        )

        self.volume_slider = ttk.Scale(
            volume_frame,
            from_=0,
            to=100,
            orient="horizontal",
            style="Player.Horizontal.TScale",
            command=self.handle_volume_change,
        )

        self.volume_slider.set(70)

        self.volume_slider.pack(
            side="left",
            fill="x",
            expand=True,
        )

    def create_button(
    self,
    parent,
    text,
    accent=False,
    command=None,
):
     """Create a playback button."""

     button = tk.Button(
        parent,
        text=text,
        font=(
            "Segoe UI Symbol",
            17 if accent else 14,
        ),
        bg=ACCENT_COLOR if accent else CONTROLS_BG,
        fg=TEXT_PRIMARY,
        activebackground=ACCENT_COLOR,
        activeforeground=TEXT_PRIMARY,
        relief="flat",
        bd=0,
        cursor="hand2",
        width=3,
    )

     if command is not None:
        button.config(command=command)

     return button

    def set_playing(self, playing):
        """Update the Play/Pause button icon."""

        if playing:
            self.play_button.config(text="⏸")
        else:
            self.play_button.config(text="▶")

    def handle_play_pause(self):
        """Notify MainWindow that Play/Pause was pressed."""

        if self.on_play_pause:
            self.on_play_pause()

    def handle_volume_change(self, value):
        """Notify MainWindow when volume changes."""

        if self.on_volume_change:
            self.on_volume_change(value)

    def format_time(self, seconds):
        """Convert seconds into M:SS format."""

        seconds = max(0, int(seconds))

        minutes = seconds // 60
        remaining_seconds = seconds % 60

        return f"{minutes}:{remaining_seconds:02d}"

    def set_duration(self, duration):
        """Set the total duration displayed by the controls."""

        self.progress_bar.config(
            to=max(duration, 1)
        )

        self.duration_label.config(
            text=self.format_time(duration)
        )

    def update_progress(self, position):
        """Update playback time and progress slider."""

        if self.is_seeking:
            return

        self.progress_bar.set(position)

        self.current_time_label.config(
            text=self.format_time(position)
        )

    def start_seek(self, event):
        """Pause automatic progress updates while dragging."""

        self.is_seeking = True

    def finish_seek(self, event):
        """Seek playback when the progress slider is released."""

        position = self.progress_bar.get()

        self.is_seeking = False

        self.current_time_label.config(
        text=self.format_time(position)
        )

        if self.on_seek:
            self.on_seek(position)

    def handle_previous(self):
        """Notify MainWindow that Previous was pressed."""

        if self.on_previous:
            self.on_previous()


    def handle_next(self):
        """Notify MainWindow that Next was pressed."""

        if self.on_next:
            self.on_next()
