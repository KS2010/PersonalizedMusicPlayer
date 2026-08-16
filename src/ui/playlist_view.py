"""
Playlist panel for the music player.
"""

import tkinter as tk
from tkinter import filedialog

from src.services.metadata_service import load_song_metadata
from src.ui.theme import (
    ACCENT_COLOR,
    BORDER_COLOR,
    PLAYLIST_BG,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
)


class PlaylistView(tk.Frame):
    """Displays and manages the current playlist."""

    def __init__(
        self,
        parent,
        on_song_selected=None,
        database_service=None,
    ):
        super().__init__(
            parent,
            bg=PLAYLIST_BG,
            width=300,
        )

        # ==========================================
        # Services / callbacks
        # ==========================================

        self.on_song_selected = on_song_selected
        self.database_service = database_service

        self.pack_propagate(False)

        # ==========================================
        # Playlist data
        # ==========================================

        # Master library.
        self.songs = []

        # Current navigation view.
        self.current_view = "library"

        # Load songs from database if available.
        if self.database_service is not None:
            self.songs = (
                self.database_service.get_all_songs()
            )

        # ==========================================
        # Create UI
        # ==========================================

        self.create_widgets()

    # =================================================
    # UI
    # =================================================

    def create_widgets(self):
        """Create playlist widgets."""

        # ==========================================
        # Header
        # ==========================================

        header_frame = tk.Frame(
            self,
            bg=PLAYLIST_BG,
        )

        header_frame.pack(
            fill="x",
            padx=22,
            pady=(25, 10),
        )

        self.title_label = tk.Label(
            header_frame,
            text="YOUR PLAYLIST",
            font=("Segoe UI", 14, "bold"),
            bg=PLAYLIST_BG,
            fg=TEXT_PRIMARY,
        )

        self.title_label.pack(
            anchor="w"
        )

        self.song_count_label = tk.Label(
            header_frame,
            text="0 songs",
            font=("Segoe UI", 9),
            bg=PLAYLIST_BG,
            fg=TEXT_SECONDARY,
        )

        self.song_count_label.pack(
            anchor="w",
            pady=(8, 0),
        )

        # ==========================================
        # Add Music
        # ==========================================

        self.add_music_button = tk.Button(
            self,
            text="+  ADD MUSIC",
            font=("Segoe UI", 9, "bold"),
            bg=ACCENT_COLOR,
            fg=TEXT_PRIMARY,
            activebackground=ACCENT_COLOR,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.add_music,
        )

        self.add_music_button.pack(
            fill="x",
            padx=22,
            pady=(5, 10),
            ipady=6,
        )

        # ==========================================
        # Search
        # ==========================================

        self.search_entry = tk.Entry(
            self,
            font=("Segoe UI", 10),
            bg="#242424",
            fg=TEXT_PRIMARY,
            insertbackground=TEXT_PRIMARY,
            relief="flat",
            bd=0,
        )

        self.search_entry.insert(
            0,
            "Search songs...",
        )

        self.search_entry.bind(
            "<FocusIn>",
            self.clear_search_placeholder,
        )

        self.search_entry.bind(
            "<FocusOut>",
            self.restore_search_placeholder,
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.filter_playlist,
        )

        self.search_entry.pack(
            fill="x",
            padx=22,
            pady=(0, 15),
            ipady=8,
        )

        # ==========================================
        # Separator
        # ==========================================

        separator = tk.Frame(
            self,
            bg=BORDER_COLOR,
            height=1,
        )

        separator.pack(
            fill="x",
            padx=22,
        )

        # ==========================================
        # Song list
        # ==========================================

        self.song_list_frame = tk.Frame(
            self,
            bg=PLAYLIST_BG,
        )

        self.song_list_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15,
        )

        # Initial render.
        self.refresh_playlist()

    # =================================================
    # Import Music
    # =================================================

    def add_music(self):
        """Open a file picker and add selected songs."""

        filepaths = filedialog.askopenfilenames(
            title="Select Music",
            filetypes=[
                (
                    "Audio Files",
                    "*.mp3 *.wav *.ogg *.flac *.m4a",
                ),
                ("MP3 Files", "*.mp3"),
                ("All Files", "*.*"),
            ],
        )

        if not filepaths:
            return

        for filepath in filepaths:

            # Avoid duplicate songs.
            if self.song_exists(filepath):
                continue

            song = load_song_metadata(filepath)

            self.songs.append(song)

            # Persist song in database.
            if self.database_service is not None:
                self.database_service.add_song(song)

        # Return to library after importing.
        self.current_view = "library"

        self.title_label.config(
            text="YOUR PLAYLIST"
        )

        self.refresh_playlist()

    # =================================================
    # Song existence
    # =================================================

    def song_exists(self, filepath):
        """Check whether a song already exists."""

        return any(
            song.filepath == filepath
            for song in self.songs
        )

    # =================================================
    # Playlist Rendering
    # =================================================

    def refresh_playlist(self):
        """Redraw the current playlist view."""

        # ==========================================
        # Determine which songs to display
        # ==========================================

        if self.current_view == "favorites":

            songs_to_display = [
                song
                for song in self.songs
                if song.is_favorite
            ]

        elif self.current_view == "recent":

            if self.database_service is None:
                songs_to_display = []

            else:
                songs_to_display = (
                    self.database_service.get_recent_songs()
                )

        else:

            # Library.
            songs_to_display = self.songs

        # ==========================================
        # Render
        # ==========================================

        self.render_songs(
            songs_to_display
        )

    def render_songs(self, songs):
        """Render the provided songs."""

        # Remove existing rows.
        for widget in self.song_list_frame.winfo_children():
            widget.destroy()

        song_count = len(songs)

        # Update count.
        self.song_count_label.config(
            text=(
                f"{song_count} "
                f"{'song' if song_count == 1 else 'songs'}"
            )
        )

        # Empty state.
        if not songs:
            self.show_empty_state()
            return

        # Create rows.
        for index, song in enumerate(songs):

            self.create_song_row(
                song,
                index,
            )

    # =================================================
    # Song Row
    # =================================================

    def create_song_row(self, song, index):
        """Create one song entry."""

        song_frame = tk.Frame(
            self.song_list_frame,
            bg=PLAYLIST_BG,
            cursor="hand2",
        )

        song_frame.pack(
            fill="x",
            pady=4,
        )

        # ==========================================
        # Song information
        # ==========================================

        info_frame = tk.Frame(
            song_frame,
            bg=PLAYLIST_BG,
        )

        info_frame.pack(
            side="left",
            fill="x",
            expand=True,
        )

        title_label = tk.Label(
            info_frame,
            text=song.title,
            font=("Segoe UI", 10, "bold"),
            bg=PLAYLIST_BG,
            fg=TEXT_PRIMARY,
            anchor="w",
            width=24,
        )

        title_label.pack(
            fill="x",
        )

        artist_label = tk.Label(
            info_frame,
            text=song.artist,
            font=("Segoe UI", 9),
            bg=PLAYLIST_BG,
            fg=TEXT_SECONDARY,
            anchor="w",
        )

        artist_label.pack(
            fill="x",
            pady=(2, 0),
        )

        # ==========================================
        # Favorite button
        # ==========================================

        favorite_button = tk.Button(
            song_frame,
            text=(
                "♥"
                if song.is_favorite
                else "♡"
            ),
            font=("Segoe UI Symbol", 11),
            bg=PLAYLIST_BG,
            fg=(
                ACCENT_COLOR
                if song.is_favorite
                else TEXT_SECONDARY
            ),
            activebackground=PLAYLIST_BG,
            activeforeground=ACCENT_COLOR,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda selected_song=song:
                self.toggle_favorite(
                    selected_song
                ),
        )

        favorite_button.pack(
            side="right",
            padx=(6, 0),
        )

        # ==========================================
        # Duration
        # ==========================================

        duration_label = tk.Label(
            song_frame,
            text=song.formatted_duration,
            font=("Segoe UI", 9),
            bg=PLAYLIST_BG,
            fg=TEXT_SECONDARY,
            width=5,
        )

        duration_label.pack(
            side="right",
            padx=(5, 0),
        )

        # ==========================================
        # Clickable widgets
        # ==========================================

        clickable_widgets = [
            song_frame,
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
        """Handle song selection."""

        if self.on_song_selected:
            self.on_song_selected(song)

    # =================================================
    # Empty State
    # =================================================

    def show_empty_state(self):
        """Display the empty playlist message."""

        empty_container = tk.Frame(
            self.song_list_frame,
            bg=PLAYLIST_BG,
        )

        empty_container.pack(
            expand=True,
        )

        if self.current_view == "favorites":

            title = "No favorite songs"

            subtitle = (
                "Add songs to your favorites"
            )

        elif self.current_view == "recent":

            title = "No recent songs"

            subtitle = (
                "Play some music to see it here"
            )

        else:

            title = "No songs yet"

            subtitle = "Add music to your library"

        empty_title = tk.Label(
            empty_container,
            text=title,
            font=("Segoe UI", 10, "bold"),
            bg=PLAYLIST_BG,
            fg=TEXT_PRIMARY,
        )

        empty_title.pack()

        empty_subtitle = tk.Label(
            empty_container,
            text=subtitle,
            font=("Segoe UI", 9),
            bg=PLAYLIST_BG,
            fg=TEXT_SECONDARY,
        )

        empty_subtitle.pack(
            pady=(8, 0),
        )

    # =================================================
    # Search
    # =================================================

    def clear_search_placeholder(self, event):
        """Remove the search placeholder."""

        if self.search_entry.get() == "Search songs...":

            self.search_entry.delete(
                0,
                tk.END,
            )

    def restore_search_placeholder(self, event):
        """Restore the search placeholder."""

        if not self.search_entry.get().strip():

            self.search_entry.insert(
                0,
                "Search songs...",
            )

    def filter_playlist(self, event=None):
        """Filter songs according to the current view."""

        query = (
            self.search_entry
            .get()
            .strip()
            .lower()
        )

        # Treat placeholder as empty search.
        if query == "search songs...":
            query = ""

        # ==========================================
        # Get songs for current view
        # ==========================================

        if self.current_view == "favorites":

            songs_to_filter = [
                song
                for song in self.songs
                if song.is_favorite
            ]

        elif self.current_view == "recent":

            if self.database_service is None:
                songs_to_filter = []

            else:
                songs_to_filter = (
                    self.database_service.get_recent_songs()
                )

        else:

            songs_to_filter = self.songs

        # ==========================================
        # Empty search
        # ==========================================

        if not query:

            self.render_songs(
                songs_to_filter
            )

            return

        # ==========================================
        # Search
        # ==========================================

        filtered_songs = [
            song
            for song in songs_to_filter
            if (
                query in song.title.lower()
                or query in song.artist.lower()
                or query in song.album.lower()
            )
        ]

        # ==========================================
        # No results
        # ==========================================

        if not filtered_songs:

            for widget in (
                self.song_list_frame.winfo_children()
            ):
                widget.destroy()

            self.song_count_label.config(
                text="0 songs"
            )

            self.show_no_results()

            return

        # ==========================================
        # Display results
        # ==========================================

        self.render_songs(
            filtered_songs
        )

    def show_no_results(self):
        """Display a no-results message."""

        empty_container = tk.Frame(
            self.song_list_frame,
            bg=PLAYLIST_BG,
        )

        empty_container.pack(
            expand=True,
        )

        empty_title = tk.Label(
            empty_container,
            text="No matching songs",
            font=("Segoe UI", 10, "bold"),
            bg=PLAYLIST_BG,
            fg=TEXT_PRIMARY,
        )

        empty_title.pack()

        empty_subtitle = tk.Label(
            empty_container,
            text=(
                "Try another title, artist, or album"
            ),
            font=("Segoe UI", 9),
            bg=PLAYLIST_BG,
            fg=TEXT_SECONDARY,
        )

        empty_subtitle.pack(
            pady=(8, 0),
        )

    # =================================================
    # Favorites
    # =================================================

    def toggle_favorite(self, song):
        """Toggle a song's favorite status."""

        song.is_favorite = not song.is_favorite

        # Save to database.
        if self.database_service is not None:

            self.database_service.set_favorite(
                song.filepath,
                song.is_favorite,
            )

        # Refresh current view.
        self.refresh_playlist()

    # =================================================
    # Navigation: Library
    # =================================================

    def show_library(self):
        """Display all songs."""

        self.current_view = "library"

        self.title_label.config(
            text="YOUR PLAYLIST"
        )

        self.search_entry.delete(
            0,
            tk.END,
        )

        self.search_entry.insert(
            0,
            "Search songs...",
        )

        self.refresh_playlist()

    # =================================================
    # Navigation: Favorites
    # =================================================

    def show_favorites(self):
        """Display favorite songs only."""

        self.current_view = "favorites"

        self.title_label.config(
            text="FAVORITES"
        )

        self.search_entry.delete(
            0,
            tk.END,
        )

        self.search_entry.insert(
            0,
            "Search songs...",
        )

        self.refresh_playlist()

    # =================================================
    # Navigation: Recent
    # =================================================

    def show_recent(self):
        """Display recently played songs."""

        self.current_view = "recent"

        self.title_label.config(
            text="RECENTLY PLAYED"
        )

        self.search_entry.delete(
            0,
            tk.END,
        )

        self.search_entry.insert(
            0,
            "Search songs...",
        )

        self.refresh_playlist()
