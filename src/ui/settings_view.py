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
    ):
        super().__init__(
            parent,
            bg=BACKGROUND_COLOR,
        )

        self.database_service = database_service
        self.audio_service = audio_service
        self.on_settings_reset = on_settings_reset

        self.create_widgets()
        self.load_settings()

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
            font=("Segoe UI", 22, "bold"),
            bg=BACKGROUND_COLOR,
            fg=TEXT_PRIMARY,
        )

        title_label.pack(
            anchor="w",
        )

        subtitle_label = tk.Label(
            self.content_frame,
            text="Customize your music player",
            font=("Segoe UI", 10),
            bg=BACKGROUND_COLOR,
            fg=TEXT_SECONDARY,
        )

        subtitle_label.pack(
            anchor="w",
            pady=(5, 25),
        )

        # ==========================================
        # Playback section
        # ==========================================

        self.create_section_title(
            "PLAYBACK"
        )

        playback_frame = self.create_section()

        volume_label = tk.Label(
            playback_frame,
            text="Default Volume",
            font=("Segoe UI", 10, "bold"),
            bg="#1B1B1B",
            fg=TEXT_PRIMARY,
        )

        volume_label.pack(
            anchor="w",
            padx=20,
            pady=(18, 3),
        )

        volume_description = tk.Label(
            playback_frame,
            text="Volume used when the application starts.",
            font=("Segoe UI", 9),
            bg="#1B1B1B",
            fg=TEXT_SECONDARY,
        )

        volume_description.pack(
            anchor="w",
            padx=20,
        )

        volume_control_frame = tk.Frame(
            playback_frame,
            bg="#1B1B1B",
        )

        volume_control_frame.pack(
            fill="x",
            padx=20,
            pady=(12, 20),
        )

        self.volume_value_label = tk.Label(
            volume_control_frame,
            text="70%",
            font=("Segoe UI", 9, "bold"),
            bg="#1B1B1B",
            fg=ACCENT_COLOR,
            width=5,
        )

        self.volume_value_label.pack(
            side="right",
        )

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

        self.volume_slider.set(70)

        self.volume_slider.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 15),
        )

        # ==========================================
        # History section
        # ==========================================

        self.create_section_title(
            "HISTORY"
        )

        history_frame = self.create_section()

        history_label = tk.Label(
            history_frame,
            text="Recently Played",
            font=("Segoe UI", 10, "bold"),
            bg="#1B1B1B",
            fg=TEXT_PRIMARY,
        )

        history_label.pack(
            anchor="w",
            padx=20,
            pady=(18, 3),
        )

        history_description = tk.Label(
            history_frame,
            text="Remove all recorded playback history.",
            font=("Segoe UI", 9),
            bg="#1B1B1B",
            fg=TEXT_SECONDARY,
        )

        history_description.pack(
            anchor="w",
            padx=20,
        )

        clear_history_button = tk.Button(
            history_frame,
            text="CLEAR HISTORY",
            font=("Segoe UI", 9, "bold"),
            bg="#242424",
            fg=TEXT_PRIMARY,
            activebackground=ACCENT_COLOR,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.clear_history,
        )

        clear_history_button.pack(
            anchor="w",
            padx=20,
            pady=(12, 20),
            ipadx=10,
            ipady=5,
        )

        # ==========================================
        # Library section
        # ==========================================

        self.create_section_title(
            "LIBRARY"
        )

        library_frame = self.create_section()

        library_label = tk.Label(
            library_frame,
            text="Music Library",
            font=("Segoe UI", 10, "bold"),
            bg="#1B1B1B",
            fg=TEXT_PRIMARY,
        )

        library_label.pack(
            anchor="w",
            padx=20,
            pady=(18, 3),
        )

        library_description = tk.Label(
            library_frame,
            text="Remove all songs from the local library.",
            font=("Segoe UI", 9),
            bg="#1B1B1B",
            fg=TEXT_SECONDARY,
        )

        library_description.pack(
            anchor="w",
            padx=20,
        )

        clear_library_button = tk.Button(
            library_frame,
            text="CLEAR LIBRARY",
            font=("Segoe UI", 9, "bold"),
            bg="#242424",
            fg=TEXT_PRIMARY,
            activebackground=ACCENT_COLOR,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.clear_library,
        )

        clear_library_button.pack(
            anchor="w",
            padx=20,
            pady=(12, 20),
            ipadx=10,
            ipady=5,
        )

        # ==========================================
        # Application section
        # ==========================================

        self.create_section_title(
            "APPLICATION"
        )

        application_frame = self.create_section()

        reset_button = tk.Button(
            application_frame,
            text="RESET SETTINGS",
            font=("Segoe UI", 9, "bold"),
            bg="#242424",
            fg=TEXT_PRIMARY,
            activebackground=ACCENT_COLOR,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.reset_settings,
        )

        reset_button.pack(
            anchor="w",
            padx=20,
            pady=20,
            ipadx=10,
            ipady=5,
        )

    # =================================================
    # Section Helpers
    # =================================================

    def create_section_title(self, text):
        """Create a section heading."""

        label = tk.Label(
            self.content_frame,
            text=text,
            font=("Segoe UI", 9, "bold"),
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
    # Settings
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
            volume = float(saved_volume)
        except (TypeError, ValueError):
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

    def handle_volume_change(self, value):
        """Save the default volume."""

        volume = float(value)

        self.volume_value_label.config(
            text=f"{int(volume)}%"
        )

        if self.database_service is not None:

            self.database_service.set_setting(
                "default_volume",
                int(volume),
            )

        if self.audio_service is not None:

            self.audio_service.set_volume(
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
            "Are you sure you want to clear your recently played history?",
        )

        if not confirm:
            return

        self.database_service.clear_play_history()

        messagebox.showinfo(
            "History Cleared",
            "Recently played history has been cleared.",
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
            "This will remove all songs from your library. Continue?",
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

        self.load_settings()

        if self.on_settings_reset:
            self.on_settings_reset()

        messagebox.showinfo(
            "Settings Reset",
            "Your application settings have been reset.",
        )
