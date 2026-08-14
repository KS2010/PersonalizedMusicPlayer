from src.ui.theme import *
import tkinter as tk


class NavigationPanel(tk.Frame):
    """Left navigation panel."""

    def __init__(self, parent, on_navigate=None):
        super().__init__(
            parent,
            bg="#1B1B1B",
            width=220,
        )

        self.on_navigate = on_navigate

        self.pack_propagate(False)

        self.create_widgets()

    def create_widgets(self):
        """Create navigation panel widgets."""

        # ==========================================
        # Logo
        # ==========================================

        logo = tk.Label(
            self,
            text="🎵",
            font=("Segoe UI Emoji", 40),
            bg=NAVIGATION_BG,
            fg="#8A5CF6",
        )

        logo.pack(
            pady=(30, 5),
        )

        # ==========================================
        # Application title
        # ==========================================

        title = tk.Label(
            self,
            text="Personalized\nMusic Player",
            font=SUBTITLE_FONT,
            bg="#1B1B1B",
            fg=TEXT_PRIMARY,
            justify="center",
        )

        title.pack(
            pady=(0, 35),
        )

        # ==========================================
        # Navigation buttons
        # ==========================================

        menu_items = [
            ("🏠  Home", "home"),
            ("🎵  Library", "library"),
            ("❤  Favorites", "favorites"),
            ("🕒  Recent", "recent"),
            ("📊  Statistics", "statistics"),
            ("⚙  Settings", "settings"),
        ]

        for label, page in menu_items:

            button = tk.Button(
                self,
                text=label,
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
                cursor="hand2",
                command=lambda selected_page=page: self.navigate(
                    selected_page
                ),
            )

            button.pack(
                fill="x",
            )

        # ==========================================
        # Footer
        # ==========================================

        footer = tk.Label(
            self,
            text="Version 1.0",
            bg="#1B1B1B",
            fg=TEXT_MUTED,
            font=SMALL_FONT,
        )

        footer.pack(
            side="bottom",
            pady=20,
        )

    def navigate(self, page):
        """Notify MainWindow about navigation changes."""

        if callable(self.on_navigate):
            self.on_navigate(page)
