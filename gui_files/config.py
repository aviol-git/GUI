# config.py

# =========================== FONT CONFIG (GLOBAL) ===========================
APP_FONT_FAMILY      = "Calibri"  # "Segoe UI Variable"
APP_FONT_SIZE_PT     = 15
APP_FONT_COLOR       = "#1A1A1A"

# Tab labels (“orelhas”)
ORELHA_FONT_FAMILY   = APP_FONT_FAMILY
ORELHA_FONT_SIZE_PT  = 15
ORELHA_FONT_WEIGHT   = 300
ORELHA_LETTER_SPACING_PX = 0.2
ORELHA_TEXT_COLOR    = "#0F0F0F"

# Page titles (only used where explicitly enabled)
TITLE_FONT_FAMILY    = APP_FONT_FAMILY
TITLE_FONT_SIZE_PT   = 15
TITLE_FONT_WEIGHT    = 300
TITLE_COLOR          = "#202020"
TITLE_LETTER_SPACING = 0.4

# Form label + input fonts (Info tab)
FORM_LABEL_SIZE_PT   = 15
FORM_LABEL_WEIGHT    = 700
INPUT_FONT_SIZE_PT   = 14
# ===========================================================================

# -------- Logo + Headline (external file + text controlled here) -----------
LOGO_PATH            = "logo.png"
LOGO_MAX_WIDTH_PX    = 160
HEADER_TEXT          = "Biopsichological\nProfile"
APP_FONT_FAMILY_HEADER = "Bodoni 72 Oldstyle"

HEADER_STYLE_CSS = (
    "color: white;"
    f"font-family: '{APP_FONT_FAMILY_HEADER}', 'Calibri', 'Calibri', Calibri, Calibri;"
    "font-weight: 800;"
    "font-size: 22pt;"
    "letter-spacing: 0.4px;"
)

HEADER_BOTTOM_SPACING = 12
# ===========================================================================

# ===================== GLOBAL UI CONSTANTS =====================
TEAL_SIDEBAR_WIDTH   = 260
TAB_RADIUS_PX        = 22
TAB_PADDING_V        = 12
TAB_PADDING_H        = 28
TAB_GAP_RIGHT        = 1
TAB_MIN_WIDTH        = 190
TABBAR_LEFT_OFFSET   = 24
TABBAR_TOP_OFFSET    = 8
PANE_MARGIN_TOP      = 7.5

# Colors
TEAL         = "#3E9A92"
TEXT_COLOR   = "#0F0F0F"
ORELHA_ACTIVE_TEXT_COLOR = "#28706A"
TAB_INACTIVE = "#E0E0E0"
DATA_BG      = "#F2F2F2"
PARAM_BG     = "#F2F2F2"
INFO_BG      = "#F2F2F2"
RESULTS_BG   = "#F2F2F2"

# Data table sizing (fractions of page)
DATA_TABLE_MAX_ROWS        = 5000
DATA_TABLE_MIN_HEIGHT_FRAC = 0.85
DATA_TABLE_MAX_HEIGHT_FRAC = 0.85
DATA_TABLE_MIN_WIDTH_FRAC  = 0.00
DATA_TABLE_MAX_WIDTH_FRAC  = 0.55

# Page paddings/spacings
DATA_TITLE_STRETCH         = 0
DATA_TABLE_STRETCH         = 1
DATA_BOTTOM_SPACER_STR     = 1
DATA_PAGE_MARGINS          = (24, 24, 24, 24)
DATA_PAGE_SPACING          = 12

# --------- ONLY NEW KNOBS (for vertical-centering the three left buttons) ---------
BUTTONS_GROUP_SPACING      = 8
BUTTONS_GROUP_VOFFSET_PX   = +100
# ----------------------------------------------------------------------------------

# --------- GIF LOADER --------------
GIF_PATH        = "lotus_running.gif"
GIF_WIDTH_PX    = 96
GIF_DURATION_MS = 12000 #time to show the gif
# -----------------------------------

# ---- Status caption styles ----
PROCESS_STYLE_CSS = (
    f"color: white; font-family: '{APP_FONT_FAMILY_HEADER}', 'Calibri',Calibri, Calibri; "
    "font-weight: 600; font-size: 11pt;"
)
DONE_STYLE_CSS = (
    f"color: white; font-family: '{APP_FONT_FAMILY_HEADER}', 'Calibri', Calibri, Calibri; "
    "font-weight: 800; font-size: 20pt;"
)
# ---------------------------------

# ---- Results window styling ----
RESULT_WIN_WIDTH        = 1120
RESULT_WIN_HEIGHT       = 720

RESULT_HEADER_BG        = TEAL
RESULT_HEADER_FG        = "white"
RESULT_HEADER_HEIGHT    = 48
RESULT_HEADER_FONT_FAM  = TITLE_FONT_FAMILY
RESULT_HEADER_SIZE_PT   = 22
RESULT_HEADER_WEIGHT    = 800

RESULT_SCROLL_MARGINS   = (24, 24, 24, 24)
RESULT_SCROLL_SPACING   = 28
RESULT_SCROLL_BG        = "#F2F5F8"

RESULT_BOX_BG           = "white"
RESULT_BOX_RADIUS       = 22
RESULT_BOX_BORDER       = "1px solid #E6EBF2"
RESULT_BOX_MIN_WIDTH    = 900
RESULT_BOX_HEIGHTS      = [220, 260, 260]
TEAL = "#3E9A92"
# ---------------------------------