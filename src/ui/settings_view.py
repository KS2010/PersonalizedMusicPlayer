"""
Settings dashboard for the music player.
"""

import tkinter as tk
from tkinter import messagebox

from src.ui.theme import (
    BACKGROUND_COLOR,
    ACCENT_COLOR,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TEXT_MUTED,
    BORDER_COLOR,
)


class SettingsView(tk.Frame):
    """Application settings dashboard."""

    def __init__(
        self,
        parent,
        database_service,
        audio_service=None,
        on_settings_reset=None,
        on_volume_change=None,
    ):
        super().__init__(
            parent,
            bg=BACKGROUND_COLOR,
        )

        self.database_service = database_service
        self.audio_service = audio_service
        self.on_settings_reset = on_settings_reset
        self.on_volume_change = on_volume_change

        # Prevent callbacks while loading settings.
        self.loading_settings = True

        self.create_widgets()
        self.load_settings()

        self.loading_settings = False

    # =================================================
    # UI
    # =================================================

    def create_widgets(self):
        """Create settings interface."""

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

        title_label = tk.Label(
            self.content_frame,
            text="SETTINGS",
            font=(
                "Segoe UI",
                22,
                "bold",
            ),
            bg=BACKGROUND_COLOR,
            fg=TEXT_PRIMARY,
        )

        title_label.pack(
            anchor="w",
        )

        subtitle_label = tk.Label(
            self.content_frame,
            text="Customize your music player",
            font=(
                "Segoe UI",
                10,
            ),
            bg=BACKGROUND_COLOR,
            fg=TEXT_SECONDARY,
        )

        subtitle_label.pack(
            anchor="w",
            pady=(5, 25),
        )

        # ==========================================
        # Playback
        # ==========================================

        self.create_section_title(
            "PLAYBACK"
        )

        playback_frame = self.create_section()

        self.create_setting_label(
            playback_frame,
            "Default Volume",
            "Volume used when the application starts.",
        )

        volume_control_frame = tk.Frame(
            playback_frame,
            bg="#1B1B1B",
        )

        volume_control_frame.pack(
            fill="x",
            padx=20,
            pady=(14, 20),
        )

        # ==========================================
        # Volume icon
        # ==========================================

        volume_icon = tk.Canvas(
            volume_control_frame,
            width=30,
            height=30,
            bg="#1B1B1B",
            highlightthickness=0,
            bd=0,
        )

        volume_icon.pack(
            side="left",
            padx=(0, 10),
        )

        self.draw_volume_icon(
            volume_icon
        )

        # ==========================================
        # Slider
        # ==========================================

        self.volume_slider = tk.Scale(
            volume_control_frame,
            from_=0,
            to=100,
            orient="horizontal",
            showvalue=False,
            resolution=1,
            bg="#1B1B1B",
            fg=TEXT_PRIMARY,
            troughcolor="#2A2A2A",
            highlightthickness=0,
            bd=0,
            activebackground=ACCENT_COLOR,
            command=self.handle_volume_change,
        )

        self.volume_slider.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 15),
        )

        # ==========================================
        # Percentage
        # ==========================================

        self.volume_value_label = tk.Label(
            volume_control_frame,
            text="70%",
            font=(
                "Segoe UI",
                10,
                "bold",
            ),
            bg="#1B1B1B",
            fg=ACCENT_COLOR,
            width=5,
            anchor="e",
        )

        self.volume_value_label.pack(
            side="right",
        )

        # ==========================================
        # History
        # ==========================================

        self.create_section_title(
            "HISTORY"
        )

        history_frame = self.create_section()

        self.create_setting_label(
            history_frame,
            "Recently Played",
            "Remove all recorded playback history.",
        )

        clear_history_button = self.create_action_button(
            history_frame,
            "CLEAR HISTORY",
            self.clear_history,
        )

        clear_history_button.pack(
            anchor="w",
            padx=20,
            pady=(12, 20),
            ipadx=10,
            ipady=5,
        )

        # ==========================================
        # Library
        # ==========================================

        self.create_section_title(
            "LIBRARY"
        )

        library_frame = self.create_section()

        self.create_setting_label(
            library_frame,
            "Music Library",
            "Remove all songs from the local library.",
        )

        clear_library_button = self.create_action_button(
            library_frame,
            "CLEAR LIBRARY",
            self.clear_library,
        )

        clear_library_button.pack(
            anchor="w",
            padx=20,
            pady=(12, 20),
            ipadx=10,
            ipady=5,
        )

        # ==========================================
        # Application
        # ==========================================

        self.create_section_title(
            "APPLICATION"
        )

        application_frame = self.create_section()

        reset_button = self.create_action_button(
            application_frame,
            "RESET SETTINGS",
            self.reset_settings,
        )

        reset_button.pack(
            anchor="w",
            padx=20,
            pady=20,
            ipadx=10,
            ipady=5,
        )

    # =================================================
    # Volume Icon
    # =================================================

    def draw_volume_icon(
        self,
        canvas,
    ):
        """Draw a simple speaker icon."""

        canvas.delete(
            "all"
        )

        icon_color = TEXT_SECONDARY

        canvas.create_rectangle(
            3,
            11,
            9,
            20,
            fill=icon_color,
            outline="",
        )

        canvas.create_polygon(
            9,
            11,
            18,
            6,
            18,
            25,
            9,
            20,
            fill=icon_color,
            outline="",
        )

        canvas.create_arc(
            13,
            5,
            29,
            27,
            start=-55,
            extent=110,
            style="arc",
            outline=icon_color,
            width=2,
        )

    # =================================================
    # Setting Helpers
    # =================================================

    def create_setting_label(
        self,
        parent,
        title,
        description,
    ):
        """Create a setting title and description."""

        title_label = tk.Label(
            parent,
            text=title,
            font=(
                "Segoe UI",
                10,
                "bold",
            ),
            bg="#1B1B1B",
            fg=TEXT_PRIMARY,
        )

        title_label.pack(
            anchor="w",
            padx=20,
            pady=(18, 3),
        )

        description_label = tk.Label(
            parent,
            text=description,
            font=(
                "Segoe UI",
                9,
            ),
            bg="#1B1B1B",
            fg=TEXT_SECONDARY,
        )

        description_label.pack(
            anchor="w",
            padx=20,
        )

    def create_action_button(
        self,
        parent,
        text,
        command,
    ):
        """Create a consistent settings action button."""

        button = tk.Button(
            parent,
            text=text,
            font=(
                "Segoe UI",
                9,
                "bold",
            ),
            bg="#242424",
            fg=TEXT_PRIMARY,
            activebackground=ACCENT_COLOR,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=command,
        )

        button.bind(
            "<Enter>",
            lambda event:
            button.config(
                bg="#302B42"
            ),
        )

        button.bind(
            "<Leave>",
            lambda event:
            button.config(
                bg="#242424"
            ),
        )

        return button

    def create_section_title(
        self,
        text,
    ):
        """Create a section heading."""

        label = tk.Label(
            self.content_frame,
            text=text,
            font=(
                "Segoe UI",
                9,
                "bold",
            ),
            bg=BACKGROUND_COLOR,
            fg=TEXT_SECONDARY,
        )

        label.pack(
            anchor="w",
            pady=(15, 8),
        )

    def create_section(self):
        """Create a settings section container."""

        frame = tk.Frame(
            self.content_frame,
            bg="#1B1B1B",
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
        )

        frame.pack(
            fill="x",
        )

        return frame

    # =================================================
    # Settings Loading
    # =================================================

    def load_settings(self):
        """Load saved settings from the database."""

        if self.database_service is None:
            return

        saved_volume = (
            self.database_service.get_setting(
                "default_volume",
                "70",
            )
        )

        try:

            volume = float(
                saved_volume or 70
            )

        except (
            TypeError,
            ValueError,
        ):

            volume = 70

        volume = max(
            0,
            min(100, volume),
        )

        self.volume_slider.set(
            volume
        )

        self.volume_value_label.config(
            text=f"{int(volume)}%"
        )

    # =================================================
    # Volume
    # =================================================

    def handle_volume_change(
        self,
        value,
    ):
        """Save and apply the default volume."""

        if self.loading_settings:
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
            text=f"{int(volume)}%"
        )

        # ==========================================
        # Save
        # ==========================================

        if self.database_service is not None:

            self.database_service.set_setting(
                "default_volume",
                int(volume),
            )

        # ==========================================
        # Apply immediately
        # ==========================================

        if self.audio_service is not None:

            self.audio_service.set_volume(
                volume
            )

        # ==========================================
        # Synchronize player
        # ==========================================

        if self.on_volume_change:

            self.on_volume_change(
                volume
            )

    # =================================================
    # Clear History
    # =================================================

    def clear_history(self):
        """Clear recently played history."""

        if self.database_service is None:
            return

        confirm = messagebox.askyesno(
            "Clear History",
            (
                "Are you sure you want to clear "
                "your recently played history?"
            ),
        )

        if not confirm:
            return

        self.database_service.clear_play_history()

        messagebox.showinfo(
            "History Cleared",
            (
                "Recently played history "
                "has been cleared."
            ),
        )

    # =================================================
    # Clear Library
    # =================================================

    def clear_library(self):
        """Clear the complete music library."""

        if self.database_service is None:
            return

        confirm = messagebox.askyesno(
            "Clear Library",
            (
                "This will remove all songs "
                "from your library. Continue?"
            ),
        )

        if not confirm:
            return

        self.database_service.clear_library()

        messagebox.showinfo(
            "Library Cleared",
            "Your music library has been cleared.",
        )

    # =================================================
    # Reset Settings
    # =================================================

    def reset_settings(self):
        """Reset application preferences."""

        if self.database_service is None:
            return

        confirm = messagebox.askyesno(
            "Reset Settings",
            "Reset your saved application settings?",
        )

        if not confirm:
            return

        self.database_service.clear_settings()

        # ==========================================
        # Reset UI
        # ==========================================

        self.loading_settings = True

        self.volume_slider.set(
            70
        )

        self.volume_value_label.config(
            text="70%"
        )

        self.loading_settings = False

        # ==========================================
        # Reset audio
        # ==========================================

        if self.audio_service is not None:

            self.audio_service.set_volume(
                70
            )

        # ==========================================
        # Synchronize player
        # ==========================================

        if self.on_volume_change:

            self.on_volume_change(
                70
            )

        if self.on_settings_reset:

            self.on_settings_reset()

        messagebox.showinfo(
            "Settings Reset",
            "Your application settings have been reset.",
        )
