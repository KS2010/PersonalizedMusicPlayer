"""
Playback controls for the music player.
"""

import tkinter as tk

from src.ui.theme import (
    CONTROLS_BG,
    ACCENT_COLOR,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TEXT_MUTED,
    SMALL_FONT,
)


class PlayerSlider(tk.Canvas):
    """Custom canvas-based horizontal slider."""

    def __init__(
        self,
        parent,
        minimum=0,
        maximum=100,
        value=0,
        command=None,
        on_press=None,
        on_release=None,
        height=22,
        **kwargs,
    ):
        super().__init__(
            parent,
            height=height,
            bg=CONTROLS_BG,
            highlightthickness=0,
            bd=0,
            relief="flat",
            cursor="hand2",
            **kwargs,
        )

        self.minimum = float(minimum)
        self.maximum = float(maximum)
        self.value = float(value)

        self.command = command
        self.on_press = on_press
        self.on_release = on_release

        # Visual appearance.
        self.track_height = 7
        self.knob_radius = 8

        self.is_dragging = False

        # Redraw when the widget changes size.
        self.bind(
            "<Configure>",
            self._redraw,
        )

        # Mouse interaction.
        self.bind(
            "<Button-1>",
            self._mouse_press,
        )

        self.bind(
            "<B1-Motion>",
            self._mouse_drag,
        )

        self.bind(
            "<ButtonRelease-1>",
            self._mouse_release,
        )

        self.after(
            10,
            self._redraw,
        )

    # =================================================
    # Drawing
    # =================================================

    def _redraw(self, event=None):
        """Redraw the slider."""

        self.delete("all")

        width = self.winfo_width()
        height = self.winfo_height()

        if width <= 2:
            return

        center_y = height / 2

        left = self.knob_radius
        right = width - self.knob_radius

        if right <= left:
            return

        # ==========================================
        # Background track
        # ==========================================

        self.create_rectangle(
            left,
            center_y - self.track_height / 2,
            right,
            center_y + self.track_height / 2,
            fill="#303038",
            outline="",
        )

        # ==========================================
        # Filled track
        # ==========================================

        ratio = self._value_ratio()

        fill_right = (
            left
            + (right - left) * ratio
        )

        if fill_right > left:

            self.create_rectangle(
                left,
                center_y - self.track_height / 2,
                fill_right,
                center_y + self.track_height / 2,
                fill=ACCENT_COLOR,
                outline="",
            )

        # ==========================================
        # Slider knob
        # ==========================================

        knob_x = fill_right

        self.create_oval(
            knob_x - self.knob_radius,
            center_y - self.knob_radius,
            knob_x + self.knob_radius,
            center_y + self.knob_radius,
            fill=ACCENT_COLOR,
            outline=ACCENT_COLOR,
        )

    # =================================================
    # Value Helpers
    # =================================================

    def _value_ratio(self):
        """Return current value as a 0-1 ratio."""

        if self.maximum <= self.minimum:
            return 0

        ratio = (
            self.value - self.minimum
        ) / (
            self.maximum - self.minimum
        )

        return max(
            0,
            min(1, ratio),
        )

    def _value_from_x(self, x):
        """Convert mouse X position into a slider value."""

        width = self.winfo_width()

        left = self.knob_radius
        right = width - self.knob_radius

        if right <= left:
            return self.minimum

        x = max(
            left,
            min(right, x),
        )

        ratio = (
            x - left
        ) / (
            right - left
        )

        return (
            self.minimum
            + ratio
            * (
                self.maximum
                - self.minimum
            )
        )

    # =================================================
    # Mouse Interaction
    # =================================================

    def _mouse_press(self, event):
        """Begin slider interaction."""

        self.is_dragging = True

        self.value = self._value_from_x(
            event.x
        )

        self._redraw()

        if self.on_press:
            self.on_press(event)

        if self.command:
            self.command(self.value)

    def _mouse_drag(self, event):
        """Update slider while dragging."""

        if not self.is_dragging:
            return

        self.value = self._value_from_x(
            event.x
        )

        self._redraw()

        if self.command:
            self.command(self.value)

    def _mouse_release(self, event):
        """Finish slider interaction."""

        if not self.is_dragging:
            return

        self.value = self._value_from_x(
            event.x
        )

        self._redraw()

        self.is_dragging = False

        if self.command:
            self.command(self.value)

        if self.on_release:
            self.on_release(event)

    # =================================================
    # Public API
    # =================================================

    def set(self, value):
        """Set the slider value."""

        try:
            value = float(value)

        except (
            TypeError,
            ValueError,
        ):
            value = self.minimum

        self.value = max(
            self.minimum,
            min(self.maximum, value),
        )

        self._redraw()

    def get(self):
        """Return the current slider value."""

        return self.value

    def set_range(self, maximum):
        """Set the maximum value of the slider."""

        try:
            maximum = float(maximum)

        except (
            TypeError,
            ValueError,
        ):
            maximum = 100

        self.maximum = max(
            self.minimum,
            maximum,
        )

        self.value = max(
            self.minimum,
            min(self.maximum, self.value),
        )

        self._redraw()


class PlayerControls(tk.Frame):
    """Bottom playback control panel."""

    def __init__(
        self,
        parent,
        on_play_pause=None,
        on_volume_change=None,
        on_seek=None,
        on_previous=None,
        on_next=None,
    ):
        super().__init__(
            parent,
            bg=CONTROLS_BG,
            height=150,
        )

        self.on_play_pause = on_play_pause
        self.on_volume_change = on_volume_change
        self.on_seek = on_seek
        self.on_previous = on_previous
        self.on_next = on_next

        self.is_seeking = False

        # Prevent volume callbacks while loading
        # the saved volume.
        self.loading_volume = True

        self.pack_propagate(False)

        self.create_widgets()

        self.loading_volume = False

    # =================================================
    # Create Widgets
    # =================================================

    def create_widgets(self):
        """Create playback controls."""

        # ==========================================
        # Progress Section
        # ==========================================

        progress_frame = tk.Frame(
            self,
            bg=CONTROLS_BG,
        )

        progress_frame.pack(
            fill="x",
            padx=90,
            pady=(16, 8),
        )

        # ==========================================
        # Current Time
        # ==========================================

        self.current_time_label = tk.Label(
            progress_frame,
            text="0:00",
            font=SMALL_FONT,
            bg=CONTROLS_BG,
            fg=TEXT_MUTED,
            width=5,
            anchor="w",
        )

        self.current_time_label.pack(
            side="left",
        )

        # ==========================================
        # Progress Slider
        # ==========================================

        self.progress_bar = PlayerSlider(
            progress_frame,
            minimum=0,
            maximum=100,
            value=0,
            command=self.handle_progress_change,
            on_press=self.start_seek,
            on_release=self.finish_seek,
            height=22,
        )

        self.progress_bar.pack(
            side="left",
            fill="x",
            expand=True,
            padx=14,
        )

        # ==========================================
        # Duration
        # ==========================================

        self.duration_label = tk.Label(
            progress_frame,
            text="0:00",
            font=SMALL_FONT,
            bg=CONTROLS_BG,
            fg=TEXT_MUTED,
            width=5,
            anchor="e",
        )

        self.duration_label.pack(
            side="right",
        )

        # ==========================================
        # Main Controls Row
        # ==========================================

        controls_row = tk.Frame(
            self,
            bg=CONTROLS_BG,
        )

        controls_row.pack(
            fill="x",
            padx=70,
            pady=(0, 8),
        )

        # ==========================================
        # Left Spacer
        # ==========================================

        # Equal reserved space on the left and right
        # keeps the playback controls centered.

        left_section = tk.Frame(
            controls_row,
            bg=CONTROLS_BG,
            width=320,
        )

        left_section.pack(
            side="left",
        )

        left_section.pack_propagate(False)

        # ==========================================
        # Center Playback Controls
        # ==========================================

        button_frame = tk.Frame(
            controls_row,
            bg=CONTROLS_BG,
        )

        button_frame.pack(
            side="left",
            expand=True,
        )

        # ==========================================
        # Previous
        # ==========================================

        self.previous_button = self.create_icon_button(
            button_frame,
            icon_type="previous",
            command=self.handle_previous,
        )

        self.previous_button.pack(
            side="left",
            padx=8,
        )

        # ==========================================
        # Play / Pause
        # ==========================================

        self.play_button = self.create_play_button(
            button_frame,
        )

        self.play_button.pack(
            side="left",
            padx=10,
        )

        # ==========================================
        # Next
        # ==========================================

        self.next_button = self.create_icon_button(
            button_frame,
            icon_type="next",
            command=self.handle_next,
        )

        self.next_button.pack(
            side="left",
            padx=8,
        )

        # ==========================================
        # Volume Section
        # ==========================================

        # ==========================================
# Volume Section
# ==========================================

        volume_frame = tk.Frame(
        controls_row,
        bg=CONTROLS_BG,
        width=320,
        height=40,
        )

        volume_frame.pack(
    side="right",
    padx=(30, 0),
)

        volume_frame.pack_propagate(False)

# ==========================================
# Volume Icon
# ==========================================

        self.volume_icon = tk.Canvas(
    volume_frame,
    width=40,
    height=36,
    bg=CONTROLS_BG,
    highlightthickness=0,
    bd=0,
)

        self.volume_icon.pack(
    side="left",
    padx=(0, 8),
)

        self.draw_volume_icon()

# ==========================================
# VOL label
# ==========================================

        volume_label = tk.Label(
    volume_frame,
    text="VOL",
    font=(
        "Segoe UI",
        8,
        "bold",
    ),
    bg=CONTROLS_BG,
    fg=TEXT_MUTED,
)

        volume_label.pack(
    side="left",
    padx=(0, 10),
)

# ==========================================
# Volume slider
# ==========================================

        self.volume_slider = PlayerSlider(
    volume_frame,
    minimum=0,
    maximum=100,
    value=70,
    command=self.handle_volume_change,
    height=32,
)

        self.volume_slider.pack(
    side="left",
    fill="x",
    expand=True,
)

# ==========================================
# Volume percentage
# ==========================================

        self.volume_value_label = tk.Label(
    volume_frame,
    text="70%",
    font=(
        "Segoe UI",
        8,
        "bold",
    ),
    bg=CONTROLS_BG,
    fg=TEXT_SECONDARY,
    width=4,
    anchor="e",
)

        self.volume_value_label.pack(
    side="right",
    padx=(10, 0),
)

    # =================================================
    # Previous / Next Buttons
    # =================================================

    def create_icon_button(
        self,
        parent,
        icon_type,
        command=None,
    ):
        """Create a Canvas-based Previous/Next button."""

        button = tk.Canvas(
            parent,
            width=58,
            height=44,
            bg="#24242A",
            highlightthickness=0,
            bd=0,
            relief="flat",
            cursor="hand2",
        )

        self.draw_navigation_icon(
            button,
            icon_type,
        )

        if command is not None:

            button.bind(
                "<Button-1>",
                lambda event: command(),
            )

        button.bind(
            "<Enter>",
            lambda event:
            self.navigation_hover(
                button,
                icon_type,
                True,
            ),
        )

        button.bind(
            "<Leave>",
            lambda event:
            self.navigation_hover(
                button,
                icon_type,
                False,
            ),
        )

        return button

    def draw_navigation_icon(
        self,
        button,
        icon_type,
        color=None,
    ):
        """Draw a distinct Previous or Next icon."""

        button.delete("all")

        if color is None:
            color = TEXT_SECONDARY

        # ==========================================
        # Previous <<
        # ==========================================

        if icon_type == "previous":

            button.create_polygon(
                27,
                12,
                27,
                32,
                17,
                22,
                fill=color,
                outline="",
            )

            button.create_polygon(
                40,
                12,
                40,
                32,
                30,
                22,
                fill=color,
                outline="",
            )

        # ==========================================
        # Next >>
        # ==========================================

        else:

            button.create_polygon(
                18,
                12,
                18,
                32,
                28,
                22,
                fill=color,
                outline="",
            )

            button.create_polygon(
                31,
                12,
                31,
                32,
                41,
                22,
                fill=color,
                outline="",
            )

    def navigation_hover(
        self,
        button,
        icon_type,
        hovering,
    ):
        """Handle Previous/Next hover state."""

        if hovering:

            button.config(
                bg="#303038",
            )

            self.draw_navigation_icon(
                button,
                icon_type,
                ACCENT_COLOR,
            )

        else:

            button.config(
                bg="#24242A",
            )

            self.draw_navigation_icon(
                button,
                icon_type,
                TEXT_SECONDARY,
            )

    # =================================================
    # Play / Pause Button
    # =================================================

    def create_play_button(
        self,
        parent,
    ):
        """Create the central Canvas-based play button."""

        button = tk.Canvas(
            parent,
            width=72,
            height=52,
            bg=ACCENT_COLOR,
            highlightthickness=0,
            bd=0,
            relief="flat",
            cursor="hand2",
        )

        self.draw_play_icon(
            button,
        )

        button.bind(
            "<Button-1>",
            lambda event:
            self.handle_play_pause(),
        )

        button.bind(
            "<Enter>",
            lambda event:
            self.update_play_button_hover(
                True,
            ),
        )

        button.bind(
            "<Leave>",
            lambda event:
            self.update_play_button_hover(
                False,
            ),
        )

        return button

    def draw_play_icon(
        self,
        button,
    ):
        """Draw the play triangle."""

        button.delete("all")

        button.create_polygon(
            29,
            15,
            29,
            37,
            47,
            26,
            fill=TEXT_PRIMARY,
            outline="",
        )

    def draw_pause_icon(
        self,
        button,
    ):
        """Draw the pause bars."""

        button.delete("all")

        button.create_rectangle(
            27,
            15,
            33,
            37,
            fill=TEXT_PRIMARY,
            outline="",
        )

        button.create_rectangle(
            39,
            15,
            45,
            37,
            fill=TEXT_PRIMARY,
            outline="",
        )

    def update_play_button_hover(
        self,
        hovering,
    ):
        """Update central play button hover state."""

        if hovering:

            self.play_button.config(
                bg="#9B6BFF",
            )

        else:

            self.play_button.config(
                bg=ACCENT_COLOR,
            )

    # =================================================
    # Playback State
    # =================================================

    def set_playing(
        self,
        playing,
    ):
        """Update the central play/pause icon."""

        if playing:

            self.draw_pause_icon(
                self.play_button,
            )

        else:

            self.draw_play_icon(
                self.play_button,
            )

    # =================================================
    # Volume Icon
    # =================================================

    def draw_volume_icon(self):
        """Draw a large, clear speaker icon."""

        self.volume_icon.delete("all")

        icon_color = TEXT_SECONDARY

    # ==========================================
    # Speaker body
    # ==========================================

        self.volume_icon.create_rectangle(
        5,
        13,
        12,
        23,
        fill=icon_color,
        outline="",
    )

    # ==========================================
    # Speaker cone
    # ==========================================

        self.volume_icon.create_polygon(
        12,
        13,
        22,
        7,
        22,
        29,
        12,
        23,
        fill=icon_color,
        outline="",
    )

    # ==========================================
    # Sound wave - outer
    # ==========================================

        self.volume_icon.create_arc(
        17,
        5,
        36,
        31,
        start=-55,
        extent=110,
        style="arc",
        outline=icon_color,
        width=3,
    )
    # =================================================
    # Volume
    # =================================================

    def set_volume(
        self,
        value,
    ):
        """Update the volume slider visually."""

        try:

            value = float(value)

        except (
            TypeError,
            ValueError,
        ):

            value = 70

        value = max(
            0,
            min(100, value),
        )

        previous_state = (
            self.loading_volume
        )

        self.loading_volume = True

        self.volume_slider.set(
            value,
        )

        self.volume_value_label.config(
            text=f"{int(value)}%",
        )

        self.loading_volume = (
            previous_state
        )

    def handle_volume_change(
        self,
        value,
    ):
        """Notify MainWindow when volume changes."""

        if self.loading_volume:
            return

        try:

            volume = float(value)

        except (
            TypeError,
            ValueError,
        ):

            return

        volume = max(
            0,
            min(100, volume),
        )

        self.volume_value_label.config(
            text=f"{int(volume)}%",
        )

        if self.on_volume_change:

            self.on_volume_change(
                volume,
            )

    # =================================================
    # Progress
    # =================================================

    def handle_progress_change(
        self,
        value,
    ):
        """Update displayed time while seeking."""

        if not self.is_seeking:
            return

        try:

            position = float(value)

        except (
            TypeError,
            ValueError,
        ):

            return

        self.current_time_label.config(
            text=self.format_time(
                position,
            ),
        )

    def format_time(
        self,
        seconds,
    ):
        """Convert seconds into M:SS format."""

        seconds = max(
            0,
            int(seconds),
        )

        minutes = seconds // 60

        remaining_seconds = (
            seconds % 60
        )

        return (
            f"{minutes}:"
            f"{remaining_seconds:02d}"
        )

    def set_duration(
        self,
        duration,
    ):
        """Set the total duration."""

        self.progress_bar.set_range(
            max(
                duration,
                1,
            ),
        )

        self.duration_label.config(
            text=self.format_time(
                duration,
            ),
        )

    def update_progress(
        self,
        position,
    ):
        """Update playback position."""

        if self.is_seeking:
            return

        self.progress_bar.set(
            position,
        )

        self.current_time_label.config(
            text=self.format_time(
                position,
            ),
        )

    # =================================================
    # Seeking
    # =================================================

    def start_seek(
        self,
        event,
    ):
        """Begin seeking."""

        self.is_seeking = True

    def finish_seek(
        self,
        event,
    ):
        """Finish seeking."""

        position = self.progress_bar.get()

        self.is_seeking = False

        self.current_time_label.config(
            text=self.format_time(
                position,
            ),
        )

        if self.on_seek:

            self.on_seek(
                position,
            )

    # =================================================
    # Play / Pause
    # =================================================

    def handle_play_pause(self):
        """Notify MainWindow."""

        if self.on_play_pause:

            self.on_play_pause()

    # =================================================
    # Previous / Next
    # =================================================

    def handle_previous(self):
        """Notify MainWindow."""

        if self.on_previous:

            self.on_previous()

    def handle_next(self):
        """Notify MainWindow."""

        if self.on_next:

            self.on_next()
