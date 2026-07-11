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
            bg="#1B1B1B",
            fg="#8A5CF6"
        )

        logo.pack(pady=(30, 5))

        title = tk.Label(
            self,
            text="Personalized\nMusic Player",
            font=("Segoe UI", 16, "bold"),
            bg="#1B1B1B",
            fg="white",
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
                font=("Segoe UI", 12),
                bg="#1B1B1B",
                fg="white",
                activebackground="#2C2C2C",
                activeforeground="#8A5CF6",
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
            fg="#777777",
            font=("Segoe UI", 9)
        )

        footer.pack(side="bottom", pady=20)
