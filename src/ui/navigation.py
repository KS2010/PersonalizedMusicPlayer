"""
Sidebar navigation panel for the music player.
"""

import tkinter as tk

from src.ui.theme import (
    NAVIGATION_BG,
    ACCENT_COLOR,
    BUTTON_HOVER,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TEXT_MUTED,
    BODY_FONT,
    SUBTITLE_FONT,
    SMALL_FONT,
)


class NavigationPanel(tk.Frame):
    """Left navigation panel."""

    def __init__(self, parent, on_navigate=None):
        super().__init__(
            parent,
            bg=NAVIGATION_BG,
            width=220,
        )

        self.on_navigate = on_navigate

        # Track the currently active page.
        self.active_page = "home"

        # Store navigation buttons.
        self.nav_buttons = {}

        # Store button labels so we can update
        # their visual state.
        self.nav_labels = {}

        self.pack_propagate(False)

        self.create_widgets()

        # Home is selected when the application starts.
        self.set_active_page("home")

    # =================================================
    # Create UI
    # =================================================

    def create_widgets(self):
        """Create navigation panel widgets."""

        # ==========================================
        # Logo / Branding
        # ==========================================

        branding_frame = tk.Frame(
            self,
            bg=NAVIGATION_BG,
        )

        branding_frame.pack(
            fill="x",
            pady=(28, 0),
        )

        logo = tk.Label(
            branding_frame,
            text="♫",
            font=("Segoe UI Symbol", 38, "bold"),
            bg=NAVIGATION_BG,
            fg=ACCENT_COLOR,
        )

        logo.pack(
            pady=(0, 4),
        )

        title = tk.Label(
            branding_frame,
            text="PERSONALIZED\nMUSIC PLAYER",
            font=(
                "Segoe UI",
                10,
                "bold",
            ),
            bg=NAVIGATION_BG,
            fg=TEXT_PRIMARY,
            justify="center",
        )

        title.pack(
            pady=(0, 28),
        )

        # ==========================================
        # Main Navigation
        # ==========================================

        self.create_section_label(
            "MAIN"
        )

        self.create_navigation_button(
            "Home",
            "home",
            "⌂",
        )

        self.create_navigation_button(
            "Library",
            "library",
            "♫",
        )

        self.create_navigation_button(
            "Favorites",
            "favorites",
            "♥",
        )

        self.create_navigation_button(
            "Recent",
            "recent",
            "◷",
        )

        # ==========================================
        # Insights
        # ==========================================

        self.create_section_label(
            "INSIGHTS",
            pady=(22, 6),
        )

        self.create_navigation_button(
            "Statistics",
            "statistics",
            "▥",
        )

        # ==========================================
        # System
        # ==========================================

        self.create_section_label(
            "SYSTEM",
            pady=(22, 6),
        )

        self.create_navigation_button(
            "Settings",
            "settings",
            "⚙",
        )

        # ==========================================
        # Footer
        # ==========================================

        self.create_footer()

    # =================================================
    # Section Labels
    # =================================================

    def create_section_label(
        self,
        text,
        pady=(0, 6),
    ):
        """Create a navigation section heading."""

        label = tk.Label(
            self,
            text=text,
            font=(
                "Segoe UI",
                8,
                "bold",
            ),
            bg=NAVIGATION_BG,
            fg=TEXT_MUTED,
            anchor="w",
        )

        label.pack(
            fill="x",
            padx=22,
            pady=pady,
        )

    # =================================================
    # Navigation Button
    # =================================================

    def create_navigation_button(
        self,
        text,
        page,
        icon,
    ):
        """Create a styled navigation button."""

        # Outer container makes the active
        # indicator easier to control.
        button_container = tk.Frame(
            self,
            bg=NAVIGATION_BG,
            height=42,
        )

        button_container.pack(
            fill="x",
            padx=10,
            pady=2,
        )

        button_container.pack_propagate(False)

        # Active indicator.
        indicator = tk.Frame(
            button_container,
            bg=NAVIGATION_BG,
            width=3,
        )

        indicator.pack(
            side="left",
            fill="y",
        )

        # Button.
        button = tk.Button(
            button_container,
            text=f"{icon}   {text}",
            anchor="w",
            font=BODY_FONT,
            bg=NAVIGATION_BG,
            fg=TEXT_SECONDARY,
            activebackground=NAVIGATION_BG,
            activeforeground=TEXT_PRIMARY,
            relief="flat",
            bd=0,
            highlightthickness=0,
            padx=12,
            cursor="hand2",
            command=lambda selected_page=page: self.navigate(
                selected_page
            ),
        )

        button.pack(
            side="left",
            fill="both",
            expand=True,
        )

        # Save references.
        self.nav_buttons[page] = button
        self.nav_labels[page] = {
            "container": button_container,
            "indicator": indicator,
        }

        # Hover effects.
        button.bind(
            "<Enter>",
            lambda event, selected_page=page:
            self.handle_hover(
                selected_page,
                True,
            ),
        )

        button.bind(
            "<Leave>",
            lambda event, selected_page=page:
            self.handle_hover(
                selected_page,
                False,
            ),
        )

    # =================================================
    # Hover
    # =================================================

    def handle_hover(
        self,
        page,
        hovering,
    ):
        """Apply hover styling."""

        # Never override the active page styling.
        if page == self.active_page:
            return

        button = self.nav_buttons.get(
            page
        )

        if button is None:
            return

        if hovering:
            button.config(
                bg=BUTTON_HOVER,
                fg=TEXT_PRIMARY,
            )

        else:
            button.config(
                bg=NAVIGATION_BG,
                fg=TEXT_SECONDARY,
            )

    # =================================================
    # Active Page
    # =================================================

    def set_active_page(self, page):
        """Update the highlighted navigation item."""

        # Ignore invalid pages.
        if page not in self.nav_buttons:
            return

        # Reset previous active button.
        if self.active_page in self.nav_buttons:

            previous_button = self.nav_buttons[
                self.active_page
            ]

            previous_data = self.nav_labels[
                self.active_page
            ]

            previous_button.config(
                bg=NAVIGATION_BG,
                fg=TEXT_SECONDARY,
            )

            previous_data[
                "container"
            ].config(
                bg=NAVIGATION_BG,
            )

            previous_data[
                "indicator"
            ].config(
                bg=NAVIGATION_BG,
            )

        # Set new active page.
        self.active_page = page

        current_button = self.nav_buttons[
            page
        ]

        current_data = self.nav_labels[
            page
        ]

        current_button.config(
            bg=BUTTON_HOVER,
            fg=ACCENT_COLOR,
        )

        current_data[
            "container"
        ].config(
            bg=BUTTON_HOVER,
        )

        current_data[
            "indicator"
        ].config(
            bg=ACCENT_COLOR,
        )

    # =================================================
    # Footer
    # =================================================

    def create_footer(self):
        """Create the sidebar footer."""

        footer_frame = tk.Frame(
            self,
            bg=NAVIGATION_BG,
        )

        footer_frame.pack(
            side="bottom",
            fill="x",
            padx=22,
            pady=(10, 20),
        )

        separator = tk.Frame(
            footer_frame,
            bg="#292929",
            height=1,
        )

        separator.pack(
            fill="x",
            pady=(0, 12),
        )

        status_frame = tk.Frame(
            footer_frame,
            bg=NAVIGATION_BG,
        )

        status_frame.pack(
            fill="x",
        )

        status_indicator = tk.Label(
            status_frame,
            text="●",
            font=("Segoe UI", 8),
            bg=NAVIGATION_BG,
            fg="#5AC85A",
        )

        status_indicator.pack(
            side="left",
            padx=(0, 7),
        )

        status_label = tk.Label(
            status_frame,
            text="Music Player",
            font=(
                "Segoe UI",
                8,
                "bold",
            ),
            bg=NAVIGATION_BG,
            fg=TEXT_SECONDARY,
        )

        status_label.pack(
            side="left",
        )

        version_label = tk.Label(
            footer_frame,
            text="Version 1.0",
            font=SMALL_FONT,
            bg=NAVIGATION_BG,
            fg=TEXT_MUTED,
        )

        version_label.pack(
            anchor="w",
            pady=(4, 0),
            padx=(17, 0),
        )

    # =================================================
    # Navigation
    # =================================================

    def navigate(self, page):
        """Notify MainWindow about navigation changes."""

        # Update sidebar immediately.
        self.set_active_page(
            page
        )

        # Notify MainWindow.
        if callable(self.on_navigate):
            self.on_navigate(
                page
            )
