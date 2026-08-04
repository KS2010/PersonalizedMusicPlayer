from src.ui.theme import *
import tkinter as tk


class NavigationPanel(tk.Frame):
    """Left navigation panel."""

    def __init__(self, parent):
        super().__init__(
            parent,
            bg="#1B1B1B",
            width=220
        )

        self.pack_propagate(False)

        self.create_widgets()

    def create_widgets(self):

        logo = tk.Label(
            self,
            text="🎵",
            font=("Segoe UI Emoji", 40),
            bg=NAVIGATION_BG,
            fg="#8A5CF6"
        )

        logo.pack(pady=(30, 5))

        title = tk.Label(
            self,
            text="Personalized\nMusic Player",
            font=SUBTITLE_FONT,
            bg="#1B1B1B",
            fg=TEXT_PRIMARY,
            justify="center"
        )

        title.pack(pady=(0, 35))

        menu_items = [
            "🏠  Home",
            "🎵  Library",
            "❤  Favorites",
            "🕒  Recent",
            "📊  Statistics",
            "⚙  Settings"
        ]

        for item in menu_items:

            button = tk.Button(
                self,
                text=item,
                anchor="w",
                font=BODY_FONT,
                bg="#1B1B1B",
                fg="white",
                activebackground=BUTTON_HOVER,
                activeforeground=ACCENT_COLOR,
                relief="flat",
                bd=0,
                padx=20,
                pady=12,
                cursor="hand2"
            )

            button.pack(fill="x")

        footer = tk.Label(
            self,
            text="Version 1.0",
            bg="#1B1B1B",
            fg=TEXT_MUTED,
            font=SMALL_FONT
        )

        footer.pack(side="bottom", pady=20)
