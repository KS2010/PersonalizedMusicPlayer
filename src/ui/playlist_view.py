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

    PLAYLIST_WIDTH = 320

    def __init__(
        self,
        parent,
        on_song_selected=None,
        database_service=None,
    ):
        super().__init__(
            parent,
            bg=PLAYLIST_BG,
            width=self.PLAYLIST_WIDTH,
        )

        self.on_song_selected = on_song_selected
        self.database_service = database_service

        # IMPORTANT:
        # Prevent child widgets from changing the
        # playlist panel width.
        self.pack_propagate(False)
        self.grid_propagate(False)

        # Stores Song objects.
        self.songs = []

        self.current_view = "library"

        if self.database_service:
            self.songs = (
                self.database_service.get_all_songs()
            )

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
            anchor="w",
        )

        self.title_label.pack(
            fill="x",
        )

        self.song_count_label = tk.Label(
            header_frame,
            text="0 songs",
            font=("Segoe UI", 9),
            bg=PLAYLIST_BG,
            fg=TEXT_SECONDARY,
            anchor="w",
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

        # Make sure the list itself never requests
        # a larger width because of its children.
        self.song_list_frame.pack_propagate(False)

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

            if self.song_exists(filepath):
                continue

            song = load_song_metadata(filepath)

            self.songs.append(song)

            if self.database_service:

                self.database_service.add_song(
                    song
                )

        self.refresh_playlist()

    # =================================================
    # Song Exists
    # =================================================

    def song_exists(self, filepath):
        """Check whether a song is already in playlist."""

        return any(
            song.filepath == filepath
            for song in self.songs
        )

    # =================================================
    # Playlist Rendering
    # =================================================

    def refresh_playlist(self):
        """Redraw the current playlist view."""

        if self.current_view == "favorites":

            songs_to_display = [
                song
                for song in self.songs
                if song.is_favorite
            ]

        elif self.current_view == "recent":

            if self.database_service:

                songs_to_display = (
                    self.database_service
                    .get_recent_songs()
                )

            else:

                songs_to_display = []

        else:

            songs_to_display = self.songs

        self.render_songs(
            songs_to_display
        )

    # =================================================
    # Render Songs
    # =================================================

    def render_songs(self, songs):
        """Render the provided songs."""

        for widget in (
            self.song_list_frame.winfo_children()
        ):
            widget.destroy()

        song_count = len(songs)

        self.song_count_label.config(
            text=(
                f"{song_count} "
                f"{'song' if song_count == 1 else 'songs'}"
            )
        )

        if not songs:

            self.show_empty_state()

            return

        for index, song in enumerate(songs):

            self.create_song_row(
                song,
                index,
            )

    # =================================================
    # Song Row
    # =================================================

    def create_song_row(
        self,
        song,
        index,
    ):
        """Create a fixed-width song entry."""

        # ==========================================
        # Row
        # ==========================================

        song_frame = tk.Frame(
            self.song_list_frame,
            bg=PLAYLIST_BG,
            cursor="hand2",
            height=62,
        )

        song_frame.pack(
            fill="x",
            pady=4,
        )

        # IMPORTANT:
        # The row itself cannot resize according
        # to the song title.
        song_frame.pack_propagate(False)

        # ==========================================
        # RIGHT-SIDE CONTROLS
        #
        # These are created FIRST so they reserve
        # their space before the title area.
        # ==========================================

        controls_frame = tk.Frame(
            song_frame,
            bg=PLAYLIST_BG,
            width=92,
        )

        controls_frame.pack(
            side="right",
            fill="y",
            padx=(4, 5),
        )

        controls_frame.pack_propagate(False)

        # ==========================================
        # Favorite
        # ==========================================

        favorite_button = tk.Button(
            controls_frame,
            text=(
                "♥"
                if song.is_favorite
                else "♡"
            ),
            font=(
                "Segoe UI Symbol",
                11,
            ),
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
            width=2,
            command=lambda selected_song=song:
                self.toggle_favorite(
                    selected_song
                ),
        )

        favorite_button.pack(
            side="right",
            padx=(2, 0),
            pady=15,
        )

        # ==========================================
        # Duration
        # ==========================================

        duration_label = tk.Label(
            controls_frame,
            text=song.formatted_duration,
            font=("Segoe UI", 9),
            bg=PLAYLIST_BG,
            fg=TEXT_SECONDARY,
            width=5,
            anchor="e",
        )

        duration_label.pack(
            side="right",
            padx=(0, 4),
            pady=21,
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
            fill="both",
            expand=True,
            padx=(10, 2),
            pady=8,
        )

        # ==========================================
        # Title
        # ==========================================

        title_label = tk.Label(
            info_frame,
            text=self.truncate_text(
                song.title,
                24,
            ),
            font=(
                "Segoe UI",
                10,
                "bold",
            ),
            bg=PLAYLIST_BG,
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
                22,
            ),
            font=(
                "Segoe UI",
                9,
            ),
            bg=PLAYLIST_BG,
            fg=TEXT_SECONDARY,
            anchor="w",
        )

        artist_label.pack(
            fill="x",
            pady=(2, 0),
        )

        # ==========================================
        # Click handling
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

        # ==========================================
        # Hover
        # ==========================================

        hover_widgets = [
            song_frame,
            info_frame,
            title_label,
            artist_label,
            duration_label,
            controls_frame,
        ]

        for widget in hover_widgets:

            widget.bind(
                "<Enter>",
                lambda event,
                widgets=hover_widgets,
                fav=favorite_button:
                self.set_row_hover(
                    widgets,
                    fav,
                    True,
                ),
            )

            widget.bind(
                "<Leave>",
                lambda event,
                widgets=hover_widgets,
                fav=favorite_button:
                self.set_row_hover(
                    widgets,
                    fav,
                    False,
                ),
            )

    # =================================================
    # Text Truncation
    # =================================================

    def truncate_text(
        self,
        text,
        max_length,
    ):
        """Prevent long metadata from affecting layout."""

        if text is None:
            return ""

        text = str(text)

        if len(text) <= max_length:
            return text

        return (
            text[:max_length - 3]
            + "..."
        )

    # =================================================
    # Row Hover
    # =================================================

    def set_row_hover(
        self,
        widgets,
        favorite_button,
        hovering,
    ):
        """Apply row hover styling."""

        background = (
            "#24242A"
            if hovering
            else PLAYLIST_BG
        )

        for widget in widgets:

            try:

                widget.configure(
                    bg=background
                )

            except tk.TclError:

                pass

        try:

            favorite_button.configure(
                bg=background
            )

        except tk.TclError:

            pass

    # =================================================
    # Song Selection
    # =================================================

    def select_song(self, song):
        """Handle song selection."""

        if self.on_song_selected:

            self.on_song_selected(
                song
            )

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

        empty_title = tk.Label(
            empty_container,
            text="No songs yet",
            font=(
                "Segoe UI",
                10,
                "bold",
            ),
            bg=PLAYLIST_BG,
            fg=TEXT_PRIMARY,
        )

        empty_title.pack()

        empty_subtitle = tk.Label(
            empty_container,
            text="Add music to your library",
            font=(
                "Segoe UI",
                9,
            ),
            bg=PLAYLIST_BG,
            fg=TEXT_SECONDARY,
        )

        empty_subtitle.pack(
            pady=(8, 0),
        )

    # =================================================
    # Search
    # =================================================

    def clear_search_placeholder(
        self,
        event,
    ):
        """Remove search placeholder."""

        if (
            self.search_entry.get()
            == "Search songs..."
        ):

            self.search_entry.delete(
                0,
                tk.END,
            )

    def restore_search_placeholder(
        self,
        event,
    ):
        """Restore search placeholder."""

        if not self.search_entry.get().strip():

            self.search_entry.insert(
                0,
                "Search songs...",
            )

    def filter_playlist(
        self,
        event=None,
    ):
        """Filter songs."""

        query = (
            self.search_entry
            .get()
            .strip()
            .lower()
        )

        if query == "search songs...":
            query = ""

        if not query:

            self.refresh_playlist()

            return

        filtered_songs = [
            song
            for song in self.songs
            if (
                query in song.title.lower()
                or query in song.artist.lower()
                or query in song.album.lower()
            )
        ]

        if not filtered_songs:

            for widget in (
                self.song_list_frame
                .winfo_children()
            ):
                widget.destroy()

            self.song_count_label.config(
                text="0 songs"
            )

            self.show_no_results()

            return

        self.render_songs(
            filtered_songs
        )

    # =================================================
    # No Search Results
    # =================================================

    def show_no_results(self):
        """Display no search results."""

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
            font=(
                "Segoe UI",
                10,
                "bold",
            ),
            bg=PLAYLIST_BG,
            fg=TEXT_PRIMARY,
        )

        empty_title.pack()

        empty_subtitle = tk.Label(
            empty_container,
            text=(
                "Try another title, artist, "
                "or album"
            ),
            font=(
                "Segoe UI",
                9,
            ),
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
        """Toggle favorite status."""

        song.is_favorite = (
            not song.is_favorite
        )

        if self.database_service:

            self.database_service.set_favorite(
                song.filepath,
                song.is_favorite,
            )

        self.refresh_playlist()

    # =================================================
    # Library
    # =================================================

    def show_library(self):
        """Display all songs."""

        self.current_view = "library"

        self.title_label.config(
            text="YOUR PLAYLIST"
        )

        self.reset_search()

        self.refresh_playlist()

    # =================================================
    # Favorites View
    # =================================================

    def show_favorites(self):
        """Display favorite songs."""

        self.current_view = "favorites"

        self.title_label.config(
            text="FAVORITES"
        )

        self.reset_search()

        self.refresh_playlist()

    # =================================================
    # Recent View
    # =================================================

    def show_recent(self):
        """Display recently played songs."""

        self.current_view = "recent"

        self.title_label.config(
            text="RECENTLY PLAYED"
        )

        self.reset_search()

        if self.database_service:

            recent_songs = (
                self.database_service
                .get_recent_songs()
            )

            self.render_songs(
                recent_songs
            )

        else:

            self.render_songs([])

    # =================================================
    # Reset Search
    # =================================================

    def reset_search(self):
        """Reset the playlist search field."""

        self.search_entry.delete(
            0,
            tk.END,
        )

        self.search_entry.insert(
            0,
            "Search songs...",
        )
