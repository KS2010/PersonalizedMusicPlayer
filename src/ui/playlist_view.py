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

    def __init__(self, parent, on_song_selected=None,database_service=None):
        super().__init__(
            parent,
            bg=PLAYLIST_BG,
            width=300,
        )
        self.on_song_selected = on_song_selected
        self.database_service = database_service

        self.pack_propagate(False)

        # Stores Song objects.
        self.songs = []
        if self.database_service:
            self.songs = self.database_service.get_all_songs()

        self.create_widgets()

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

        title_label = tk.Label(
            header_frame,
            text="YOUR PLAYLIST",
            font=("Segoe UI", 14, "bold"),
            bg=PLAYLIST_BG,
            fg=TEXT_PRIMARY,
        )

        title_label.pack(anchor="w")

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
        # Add Music Button
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
        # Song List Container
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

        self.refresh_playlist()

    # ==============================================
    # Import Music
    # ==============================================

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
            # Avoid adding the same file twice.
            if self.song_exists(filepath):
                continue

            song = load_song_metadata(filepath)

            self.songs.append(song)

            if self.database_service:
                self.database_service.add_song(song)

        self.refresh_playlist()

    def song_exists(self, filepath):
        """Check whether a song is already in the playlist."""

        return any(
            song.filepath == filepath
            for song in self.songs
        )

    # ==============================================
    # Playlist Rendering
    # ==============================================

    def refresh_playlist(self):
        """Redraw the complete playlist."""

        self.render_songs(self.songs)

    def render_songs(self, songs):
        """Render the provided songs in the playlist."""

        # Remove currently displayed song rows.
        for widget in self.song_list_frame.winfo_children():
            widget.destroy()

        song_count = len(songs)

        self.song_count_label.config(
         text=f"{song_count} {'song' if song_count == 1 else 'songs'}"
        )

        if not songs:
            self.show_empty_state()
            return

        for index, song in enumerate(songs):
            self.create_song_row(
            song,
            index,
        )

    def create_song_row(self, song, index):
        """Create one song entry in the playlist."""

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

        favorite_button = tk.Button(
        song_frame,
        text="♥" if song.is_favorite else "♡",
        font=("Segoe UI Symbol", 11),
        bg=PLAYLIST_BG,
        fg=ACCENT_COLOR if song.is_favorite else TEXT_SECONDARY,
        activebackground=PLAYLIST_BG,
        activeforeground=ACCENT_COLOR,
        relief="flat",
        bd=0,
        cursor="hand2",
        command=lambda selected_song=song: self.toggle_favorite(
        selected_song
        ),
        )

        favorite_button.pack(
        side="right",
        padx=(6, 0),
        )

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
                lambda event, selected_song=song: self.select_song(
                selected_song
            ),
        )

    def select_song(self, song):
        """Handle song selection."""

        if self.on_song_selected:
            self.on_song_selected(song)
    # ==============================================
    # Empty State
    # ==============================================

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
            font=("Segoe UI", 10, "bold"),
            bg=PLAYLIST_BG,
            fg=TEXT_PRIMARY,
        )

        empty_title.pack()

        empty_subtitle = tk.Label(
            empty_container,
            text="Add music to your library",
            font=("Segoe UI", 9),
            bg=PLAYLIST_BG,
            fg=TEXT_SECONDARY,
        )

        empty_subtitle.pack(
            pady=(8, 0),
        )

    def clear_search_placeholder(self, event):
        """Remove the search placeholder when focused."""

        if self.search_entry.get() == "Search songs...":
            self.search_entry.delete(0, tk.END)


    def restore_search_placeholder(self, event):
        """Restore the placeholder when the search is empty."""

        if not self.search_entry.get().strip():
            self.search_entry.insert(
            0,
            "Search songs...",
        )

    def filter_playlist(self, event=None):
        """Filter playlist songs by title, artist, or album."""

        query = self.search_entry.get().strip().lower()

    # Treat placeholder text as an empty search.
        if query == "search songs...":
            query = ""

    # Empty search -> show complete playlist.
        if not query:
            self.refresh_playlist()
            return

    # Find matching songs.
        filtered_songs = [
            song
            for song in self.songs
            if (
            query in song.title.lower()
            or query in song.artist.lower()
            or query in song.album.lower()
        )
    ]

    # No matching songs.
        if not filtered_songs:
            for widget in self.song_list_frame.winfo_children():
                widget.destroy()

            self.song_count_label.config(
            text="0 songs"
            )

            self.show_no_results()
            return

        # Display matching songs.
        self.render_songs(filtered_songs)

    def show_no_results(self):
        """Display a message when search returns no matches."""

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
        text="Try another title, artist, or album",
        font=("Segoe UI", 9),
        bg=PLAYLIST_BG,
        fg=TEXT_SECONDARY,
    )

        empty_subtitle.pack(
        pady=(8, 0),
    )

    def toggle_favorite(self, song):
        """Toggle a song's favorite status."""

        song.is_favorite = not song.is_favorite

        if self.database_service:
            self.database_service.set_favorite(
            song.filepath,
            song.is_favorite,
        )

        self.refresh_playlist()
