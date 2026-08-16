"""
Centralized visual theme for the Personalized Music Player.

All UI components should import colors, fonts,
dimensions, and spacing from this file.
"""

# ==========================================================
# COLOR PALETTE
# ==========================================================

# ----------------------------------------------------------
# Application surfaces
# ----------------------------------------------------------

BACKGROUND_COLOR = "#101116"

NAVIGATION_BG = "#15171D"

CASSETTE_BG = "#191B22"

PLAYLIST_BG = "#14161B"

CONTROLS_BG = "#121419"

# ----------------------------------------------------------
# Cards / elevated surfaces
# ----------------------------------------------------------

CARD_BG = "#1A1D24"

CARD_BG_HOVER = "#20232C"

CARD_BG_ACTIVE = "#242832"

SURFACE_BG = "#181A20"

SURFACE_SECONDARY = "#1D2027"

# ----------------------------------------------------------
# Borders
# ----------------------------------------------------------

BORDER_COLOR = "#2A2E38"

BORDER_LIGHT = "#343946"

# ----------------------------------------------------------
# Accent
# ----------------------------------------------------------

ACCENT_COLOR = "#8A5CF6"

ACCENT_HOVER = "#9B70FF"

ACCENT_ACTIVE = "#7548E8"

ACCENT_MUTED = "#302550"

# ----------------------------------------------------------
# Semantic colors
# ----------------------------------------------------------

SUCCESS_COLOR = "#4CAF50"

WARNING_COLOR = "#FFC107"

ERROR_COLOR = "#F44336"

INFO_COLOR = "#4DA3FF"

# ==========================================================
# TEXT COLORS
# ==========================================================

TEXT_PRIMARY = "#F5F5F7"

TEXT_SECONDARY = "#B4B7C2"

TEXT_MUTED = "#777C89"

TEXT_DISABLED = "#50545F"

TEXT_ACCENT = ACCENT_COLOR

# ==========================================================
# BUTTON COLORS
# ==========================================================

BUTTON_BG = "#20232A"

BUTTON_HOVER = "#2B2F38"

BUTTON_ACTIVE = ACCENT_COLOR

BUTTON_TEXT = TEXT_PRIMARY

BUTTON_SECONDARY_BG = "#1B1E25"

BUTTON_SECONDARY_HOVER = "#252932"

# ==========================================================
# FONT SETTINGS
# ==========================================================

FONT_FAMILY = "Segoe UI"

# Main headings
TITLE_FONT = (
    FONT_FAMILY,
    26,
    "bold",
)

PAGE_TITLE_FONT = (
    FONT_FAMILY,
    24,
    "bold",
)

SECTION_TITLE_FONT = (
    FONT_FAMILY,
    13,
    "bold",
)

SUBTITLE_FONT = (
    FONT_FAMILY,
    18,
    "bold",
)

# Body
BODY_FONT = (
    FONT_FAMILY,
    11,
)

BODY_BOLD_FONT = (
    FONT_FAMILY,
    11,
    "bold",
)

SMALL_FONT = (
    FONT_FAMILY,
    9,
)

SMALL_BOLD_FONT = (
    FONT_FAMILY,
    9,
    "bold",
)

# Statistics / large numbers
STAT_VALUE_FONT = (
    FONT_FAMILY,
    24,
    "bold",
)

STAT_LABEL_FONT = (
    FONT_FAMILY,
    8,
    "bold",
)

# Song information
SONG_TITLE_FONT = (
    FONT_FAMILY,
    10,
    "bold",
)

SONG_ARTIST_FONT = (
    FONT_FAMILY,
    9,
)

# ==========================================================
# DIMENSIONS
# ==========================================================

WINDOW_WIDTH = 1500

WINDOW_HEIGHT = 850

MIN_WINDOW_WIDTH = 1200

MIN_WINDOW_HEIGHT = 700

NAVIGATION_WIDTH = 220

PLAYLIST_WIDTH = 300

CONTROLS_HEIGHT = 120

CASSETTE_WIDTH = 550

# ==========================================================
# SPACING
# ==========================================================

PADDING_XS = 4

PADDING_SMALL = 8

PADDING_MEDIUM = 12

PADDING_LARGE = 20

PADDING_XL = 30

PADDING_XXL = 40

# Dashboard spacing
DASHBOARD_PADDING_X = 40

DASHBOARD_PADDING_Y = 30

SECTION_GAP = 24

CARD_GAP = 12

# ==========================================================
# BORDER SETTINGS
# ==========================================================

BORDER_WIDTH = 1

# ==========================================================
# ICON SETTINGS
# ==========================================================

ICON_SIZE = 22

ICON_SMALL = 18

ICON_LARGE = 28

# ==========================================================
# COMPONENT HEIGHTS
# ==========================================================

NAV_BUTTON_HEIGHT = 44

SEARCH_HEIGHT = 36

CARD_MIN_HEIGHT = 100

SONG_ROW_HEIGHT = 52

# ==========================================================
# CORNER / VISUAL STYLE TOKENS
# ==========================================================

# Tkinter Frame does not support true rounded corners,
# but these values provide consistent visual references
# for components that may use custom drawing later.

CARD_CORNER_RADIUS = 10

BUTTON_CORNER_RADIUS = 8

# ==========================================================
# OPACITY-STYLE TOKENS
# ==========================================================

# Tkinter does not support per-widget opacity,
# so these are represented using muted colors.

OVERLAY_BG = "#0C0D11"

DIVIDER_COLOR = BORDER_COLOR

# ==========================================================
# DASHBOARD SPECIFIC COLORS
# ==========================================================

# Home
HOME_HERO_BG = "#181A22"

HOME_HERO_ACCENT = ACCENT_COLOR

HOME_RECENT_BG = SURFACE_BG

# Statistics
STATS_PANEL_BG = "#171A21"

STATS_CHART_BG = "#13151B"

STATS_ACCENT = INFO_COLOR

STATS_SECONDARY = ACCENT_COLOR

# ==========================================================
# PLAYER COLORS
# ==========================================================

PLAYER_BG = CONTROLS_BG

PLAYER_TRACK = "#292D36"

PLAYER_PROGRESS = ACCENT_COLOR

PLAYER_BUTTON_BG = CONTROLS_BG

PLAYER_BUTTON_HOVER = BUTTON_HOVER

# ==========================================================
# NAVIGATION COLORS
# ==========================================================

NAV_ACTIVE_BG = "#26202F"

NAV_HOVER_BG = "#20232A"

NAV_ACTIVE_TEXT = TEXT_PRIMARY

NAV_INACTIVE_TEXT = TEXT_SECONDARY

NAV_ICON_COLOR = ACCENT_COLOR
