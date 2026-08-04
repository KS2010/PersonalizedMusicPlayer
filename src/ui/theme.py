"""
theme.py

Centralized theme configuration for the Personalized Music Player.
All UI components should import colors, fonts, and spacing
from this file instead of hardcoding values.
"""

# ==========================================================
# COLOR PALETTE
# ==========================================================

# Application Background
BACKGROUND_COLOR = "#121212"

# Navigation Panel
NAVIGATION_BG = "#1B1B1B"

# Center Panel (Cassette Area)
CASSETTE_BG = "#222222"

# Playlist Panel
PLAYLIST_BG = "#191919"

# Bottom Controls
CONTROLS_BG = "#181818"

# Cards / Panels
CARD_BG = "#252525"

# Borders
BORDER_COLOR = "#323232"

# Accent Color
ACCENT_COLOR = "#8A5CF6"

# Success
SUCCESS_COLOR = "#4CAF50"

# Warning
WARNING_COLOR = "#FFC107"

# Error
ERROR_COLOR = "#F44336"

# ==========================================================
# TEXT COLORS
# ==========================================================

TEXT_PRIMARY = "#FFFFFF"

TEXT_SECONDARY = "#B3B3B3"

TEXT_MUTED = "#7A7A7A"

# ==========================================================
# BUTTON COLORS
# ==========================================================

BUTTON_BG = "#2A2A2A"

BUTTON_HOVER = "#363636"

BUTTON_ACTIVE = ACCENT_COLOR

BUTTON_TEXT = "#FFFFFF"

# ==========================================================
# FONT SETTINGS
# ==========================================================

FONT_FAMILY = "Segoe UI"

TITLE_FONT = (FONT_FAMILY, 26, "bold")

SUBTITLE_FONT = (FONT_FAMILY, 18, "bold")

HEADING_FONT = (FONT_FAMILY, 14, "bold")

BODY_FONT = (FONT_FAMILY, 12)

SMALL_FONT = (FONT_FAMILY, 10)

# ==========================================================
# DIMENSIONS
# ==========================================================

WINDOW_WIDTH = 1500

WINDOW_HEIGHT = 850

NAVIGATION_WIDTH = 220

PLAYLIST_WIDTH = 300

CONTROLS_HEIGHT = 120

CASSETTE_WIDTH = 550

# ==========================================================
# SPACING
# ==========================================================

PADDING_SMALL = 5

PADDING_MEDIUM = 10

PADDING_LARGE = 20

PADDING_XL = 30

# ==========================================================
# BORDER SETTINGS
# ==========================================================

BORDER_WIDTH = 1

# ==========================================================
# ICON SIZE
# ==========================================================

ICON_SIZE = 22
