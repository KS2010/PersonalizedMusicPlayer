"""
Main application window.
"""

import tkinter as tk

from src.ui.theme import BACKGROUND_COLOR
from src.ui.cassette import CassettePanel
from src.ui.navigation import NavigationPanel
from src.ui.playlist_view import PlaylistView
from src.ui.player_controls import PlayerControls
from src.ui.statistics_view import StatisticsView
from src.ui.home_view import HomeView
from src.ui.settings_view import SettingsView

from src.services.audio_service import AudioService
from src.services.database_service import DatabaseService


class MainWindow:
    """Main application window."""

    def __init__(self):

        # ==========================================
        # Core services
        # ==========================================

        self.root = tk.Tk()

        self.database_service = DatabaseService()

        self.audio_service = AudioService()

        self.current_song_index = None

        # ==========================================
        # Window configuration
        # ==========================================

        self.configure_window()

        # ==========================================
        # Create UI
        # ==========================================

        self.create_frames()

        # ==========================================
        # Load persistent settings
        # ==========================================

        self.load_saved_settings()

        # ==========================================
        # Start playback progress updater
        # ==========================================

        self.start_progress_updater()

    # =================================================
    # Window
    # =================================================

    def configure_window(self):
        """Configure the main application window."""

        self.root.title(
            "🎵 Personalized Music Player"
        )

        self.root.geometry(
            "1500x850"
        )

        self.root.minsize(
            1200,
            700,
        )

        self.root.configure(
            bg=BACKGROUND_COLOR
        )

    # =================================================
    # UI Layout
    # =================================================

    def create_frames(self):
        """Create and arrange all major UI sections."""

        # ==========================================
        # Main container
        # ==========================================

        self.main_container = tk.Frame(
            self.root,
            bg=BACKGROUND_COLOR,
        )

        self.main_container.pack(
            fill="both",
            expand=True,
        )

        # ==========================================
        # Top section
        # ==========================================

        self.top_section = tk.Frame(
            self.main_container,
            bg=BACKGROUND_COLOR,
        )

        self.top_section.pack(
            fill="both",
            expand=True,
        )

        # ==========================================
        # Navigation
        # ==========================================

        self.navigation_frame = NavigationPanel(
            self.top_section,
            on_navigate=self.handle_navigation,
        )

        self.navigation_frame.pack(
            side="left",
            fill="y",
        )

        # ==========================================
        # Content area
        # ==========================================

        self.content_frame = tk.Frame(
            self.top_section,
            bg=BACKGROUND_COLOR,
        )

        self.content_frame.pack(
            side="left",
            fill="both",
            expand=True,
        )

        # ==========================================
        # Player / Cassette
        # ==========================================

        self.cassette_frame = CassettePanel(
            self.content_frame
        )

        self.cassette_frame.pack(
            side="left",
            fill="both",
            expand=True,
        )

        # ==========================================
        # Playlist
        # ==========================================

        self.playlist_frame = PlaylistView(
            self.content_frame,
            on_song_selected=self.handle_song_selection,
            database_service=self.database_service,
        )

        self.playlist_frame.pack(
            side="right",
            fill="y",
            padx=(0, 0),
        )

        self.playlist_frame.configure(
        width=320,
        )

        # ==========================================
        # Home
        # ==========================================

        self.home_frame = HomeView(
            self.content_frame,
            database_service=self.database_service,
            on_song_selected=self.handle_song_selection,
        )

        # ==========================================
        # Statistics
        # ==========================================

        self.statistics_frame = StatisticsView(
            self.content_frame,
            database_service=self.database_service,
        )

        # ==========================================
        # Settings
        # ==========================================

        self.settings_frame = SettingsView(
            self.content_frame,
            database_service=self.database_service,
            audio_service=self.audio_service,
            on_volume_change=self.handle_settings_volume_change,
        )

        # ==========================================
        # Bottom playback controls
        # ==========================================

        self.controls_frame = PlayerControls(
            self.main_container,
            on_play_pause=self.handle_play_pause,
            on_volume_change=self.handle_volume_change,
            on_seek=self.handle_seek,
            on_previous=self.handle_previous,
            on_next=self.handle_next,
        )

        self.controls_frame.pack(
            side="bottom",
            fill="x",
        )

    # =================================================
    # Page Switching
    # =================================================

    def show_library_area(self):
        """Show the player and playlist area."""

        self.home_frame.pack_forget()

        self.statistics_frame.pack_forget()

        self.settings_frame.pack_forget()

        self.cassette_frame.pack(
            side="left",
            fill="both",
            expand=True,
        )

        self.playlist_frame.pack(
            side="right",
            fill="y",
        )

    def show_home_area(self):
        """Show the Home dashboard."""

        self.cassette_frame.pack_forget()

        self.playlist_frame.pack_forget()

        self.statistics_frame.pack_forget()

        self.settings_frame.pack_forget()

        self.home_frame.pack(
            fill="both",
            expand=True,
        )

        self.home_frame.refresh_home()

    def show_statistics_area(self):
        """Show the Statistics dashboard."""

        self.cassette_frame.pack_forget()

        self.playlist_frame.pack_forget()

        self.home_frame.pack_forget()

        self.settings_frame.pack_forget()

        self.statistics_frame.pack(
            fill="both",
            expand=True,
        )

        self.statistics_frame.refresh_statistics()

    def show_settings_area(self):
        """Show the Settings dashboard."""

        self.cassette_frame.pack_forget()

        self.playlist_frame.pack_forget()

        self.home_frame.pack_forget()

        self.statistics_frame.pack_forget()

        self.settings_frame.pack(
            fill="both",
            expand=True,
        )

        self.settings_frame.load_settings()

    # =================================================
    # Song Selection
    # =================================================

    def handle_song_selection(
        self,
        song,
    ):
        """Load and play the selected song."""

        try:

            self.current_song_index = (
                self.playlist_frame
                .songs
                .index(song)
            )

        except ValueError:

            self.current_song_index = None

        # Update cassette display.
        self.cassette_frame.update_song(
            song
        )

        # Load selected song.
        self.audio_service.load_song(
            song
        )

        # Start playback.
        self.audio_service.play()

        # ==========================================
        # Update playlist active-song state
        # ==========================================


        # ==========================================
        # Record playback
        # ==========================================

        self.database_service.record_play(
            song.filepath
        )

        # ==========================================
        # Update player controls
        # ==========================================

        self.controls_frame.set_duration(
            song.duration
        )

        self.controls_frame.update_progress(
            0
        )

        self.controls_frame.set_playing(
            True
        )

    # =================================================
    # Play / Pause
    # =================================================

    def handle_play_pause(self):
        """Toggle between playing and paused states."""

        if self.audio_service.current_song is None:
            return

        # ==========================================
        # Resume
        # ==========================================

        if self.audio_service.is_paused:

            self.audio_service.resume()

            self.controls_frame.set_playing(
                True
            )

        # ==========================================
        # Pause
        # ==========================================

        elif self.audio_service.is_playing:

            self.audio_service.pause()

            self.controls_frame.set_playing(
                False
            )

        # ==========================================
        # Start loaded song
        # ==========================================

        else:

            self.audio_service.play()

            self.database_service.record_play(
                self.audio_service.current_song.filepath
            )

            self.controls_frame.set_playing(
                True
            )

    # =================================================
    # Volume
    # =================================================

    def handle_volume_change(
        self,
        value,
    ):
        """Change playback volume."""

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

        # Apply immediately.
        self.audio_service.set_volume(
            volume
        )

        # Save as the new default.
        self.database_service.set_setting(
            "default_volume",
            int(volume),
        )

    def handle_settings_volume_change(
        self,
        value,
    ):
        """Synchronize Settings volume with player controls."""

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

        # Apply to audio engine.
        self.audio_service.set_volume(
            volume
        )

        # Update player slider.
        self.controls_frame.set_volume(
            volume
        )

    # =================================================
    # Persistent Settings
    # =================================================

    def load_saved_settings(self):
        """Load saved application settings."""

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

        # Apply saved volume.
        self.audio_service.set_volume(
            volume
        )

        # Synchronize player slider.
        self.controls_frame.set_volume(
            volume
        )

    # =================================================
    # Playback Progress
    # =================================================

    def start_progress_updater(self):
        """Start periodically updating playback progress."""

        self.update_playback_progress()

    def update_playback_progress(self):
        """Update progress and detect finished songs."""

        if (
            self.audio_service.current_song
            is not None
            and self.audio_service.is_playing
        ):

            if self.audio_service.has_song_ended():

                self.handle_song_finished()

            else:

                position = (
                    self.audio_service
                    .get_position()
                )

                duration = (
                    self.audio_service
                    .current_song
                    .duration
                )

                position = min(
                    position,
                    duration,
                )

                self.controls_frame.update_progress(
                    position
                )

        self.root.after(
            500,
            self.update_playback_progress,
        )

    # =================================================
    # Song Finished
    # =================================================

    def handle_song_finished(self):
        """Automatically play the next song."""

        songs = (
            self.playlist_frame
            .songs
        )

        if not songs:
            return

        if self.current_song_index is None:

            next_index = 0

        else:

            next_index = (
                self.current_song_index + 1
            ) % len(songs)

        self.play_song_at_index(
            next_index
        )

    # =================================================
    # Seeking
    # =================================================

    def handle_seek(
        self,
        position,
    ):
        """Seek the current song."""

        if self.audio_service.current_song is None:
            return

        self.audio_service.seek(
            position
        )

        self.controls_frame.update_progress(
            position
        )

    # =================================================
    # Play Song By Index
    # =================================================

    def play_song_at_index(
        self,
        index,
    ):
        """Load and play a song from the playlist."""

        songs = (
            self.playlist_frame
            .songs
        )

        if not songs:
            return

        index %= len(songs)

        self.current_song_index = index

        song = songs[index]

        # ==========================================
        # Update cassette
        # ==========================================

        self.cassette_frame.update_song(
            song
        )

        # ==========================================
        # Load song
        # ==========================================

        self.audio_service.load_song(
            song
        )

        # ==========================================
        # Play song
        # ==========================================

        self.audio_service.play()

        # ==========================================
        # Update active playlist row
        # ==========================================

        # ==========================================
        # Record playback
        # ==========================================

        self.database_service.record_play(
            song.filepath
        )

        # ==========================================
        # Update controls
        # ==========================================

        self.controls_frame.set_duration(
            song.duration
        )

        self.controls_frame.update_progress(
            0
        )

        self.controls_frame.set_playing(
            True
        )

    # =================================================
    # Next
    # =================================================

    def handle_next(self):
        """Play the next song."""

        songs = (
            self.playlist_frame
            .songs
        )

        if not songs:
            return

        if self.current_song_index is None:

            next_index = 0

        else:

            next_index = (
                self.current_song_index + 1
            ) % len(songs)

        self.play_song_at_index(
            next_index
        )

    # =================================================
    # Previous
    # =================================================

    def handle_previous(self):
        """Play the previous song."""

        songs = (
            self.playlist_frame
            .songs
        )

        if not songs:
            return

        if self.current_song_index is None:

            previous_index = (
                len(songs) - 1
            )

        else:

            previous_index = (
                self.current_song_index - 1
            ) % len(songs)

        self.play_song_at_index(
            previous_index
        )

    # =================================================
    # Navigation
    # =================================================

    def handle_navigation(
        self,
        page,
    ):
        """Handle sidebar navigation."""

        # ==========================================
        # Home
        # ==========================================

        if page == "home":

            self.show_home_area()

        # ==========================================
        # Library
        # ==========================================

        elif page == "library":

            self.show_library_area()

            self.playlist_frame.show_library()

        # ==========================================
        # Favorites
        # ==========================================

        elif page == "favorites":

            self.show_library_area()

            self.playlist_frame.show_favorites()

        # ==========================================
        # Recent
        # ==========================================

        elif page == "recent":

            self.show_library_area()

            self.playlist_frame.show_recent()

        # ==========================================
        # Statistics
        # ==========================================

        elif page == "statistics":

            self.show_statistics_area()

        # ==========================================
        # Settings
        # ==========================================

        elif page == "settings":

            self.show_settings_area()

    # =================================================
    # Run
    # =================================================

    def run(self):
        """Start the Tkinter event loop."""

        self.root.mainloop()
