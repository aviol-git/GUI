# functions.py

import os
import shutil
import pandas as pd

from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QColor, QPalette, QPixmap, QMovie
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QFrame, QLabel, QSizePolicy, QSpacerItem, QPushButton,
    QFileDialog, QTabWidget
)

from config import (
    APP_FONT_FAMILY, APP_FONT_SIZE_PT, APP_FONT_COLOR,
    LOGO_PATH, LOGO_MAX_WIDTH_PX, HEADER_TEXT, HEADER_STYLE_CSS,
    HEADER_BOTTOM_SPACING, TEAL_SIDEBAR_WIDTH, TEAL,
    BUTTONS_GROUP_SPACING, BUTTONS_GROUP_VOFFSET_PX,
    GIF_PATH, GIF_WIDTH_PX, GIF_DURATION_MS,
    PROCESS_STYLE_CSS, DONE_STYLE_CSS,
    DATA_TABLE_MIN_HEIGHT_FRAC, DATA_TABLE_MAX_HEIGHT_FRAC,
    DATA_TABLE_MIN_WIDTH_FRAC, DATA_TABLE_MAX_WIDTH_FRAC,
)
from tabs import create_tabs


# -------------------- Fractional sizing for the data table --------------------
def apply_data_table_fractional_sizes(win: QMainWindow):
    page  = win.tabs.data_page
    table = win.tabs.data_table.table
    page_w = max(1, page.width())
    page_h = max(1, page.height())
    hmin = int(DATA_TABLE_MIN_HEIGHT_FRAC * page_h) if DATA_TABLE_MIN_HEIGHT_FRAC > 0 else 0
    hmax = int(DATA_TABLE_MAX_HEIGHT_FRAC * page_h) if DATA_TABLE_MAX_HEIGHT_FRAC > 0 else 0
    wmin = int(DATA_TABLE_MIN_WIDTH_FRAC  * page_w) if DATA_TABLE_MIN_WIDTH_FRAC  > 0 else 0
    wmax = int(DATA_TABLE_MAX_WIDTH_FRAC  * page_w) if DATA_TABLE_MAX_WIDTH_FRAC  > 0 else 0
    if hmin: table.setMinimumHeight(hmin)
    if hmax: table.setMaximumHeight(hmax)
    if wmin: table.setMinimumWidth(wmin)
    if wmax: table.setMaximumWidth(wmax)


# -------------------- Upload logic --------------------
def upload_file_and_display(tabs: QTabWidget):
    file_path, _ = QFileDialog.getOpenFileName(None, "Open File", "", "Data Files (*.csv *.xlsx *.tsv)")
    if not file_path:
        return
    try:
        if file_path.endswith(".csv") or file_path.endswith(".tsv"):
            sep = "," if file_path.endswith(".csv") else "\t"
            df = pd.read_csv(file_path, sep=sep)
        else:
            df = pd.read_excel(file_path)

        tabs.data_table.display_dataframe(df)

        # populate selectors
        if hasattr(tabs.data_page, "data_selector"):
            tabs.data_page.data_selector.load_columns(df.columns.astype(str).tolist())
        if hasattr(tabs.data_page, "data_individuals"):
            # first column as IDs
            ids = df.iloc[:, 0].dropna().astype(str).unique().tolist()
            tabs.data_page.data_individuals.load_items(ids)

        if tabs.data_page.title:
            tabs.data_page.title.setText(
                f"Data Preview — {len(df)} individuals, {len(df.columns)} observables"
            )
        tabs.setCurrentWidget(tabs.data_page)
    except Exception as e:
        print(f"[ERROR] Failed to load file: {e}")


# -------------------- Results tab creator helper --------------------
def ensure_results_tab_and_open(tabs: QTabWidget):
    if not getattr(tabs, "_results_tab_added", False):
        tabs.addTab(tabs.results_page, "Results")
        tabs._results_tab_added = True
    tabs.setCurrentWidget(tabs.results_page)


# -------------------- Main window --------------------
def create_main_window() -> QMainWindow:
    win = QMainWindow()
    win.setWindowTitle("Biopsychological profiles")
    win.resize(1368, 768)

    central = QWidget()
    win.setCentralWidget(central)
    root = QHBoxLayout(central)
    root.setContentsMargins(0, 0, 0, 0)
    root.setSpacing(0)

    # Left sidebar (teal)
    left = QFrame()
    left.setFixedWidth(TEAL_SIDEBAR_WIDTH)
    left.setAutoFillBackground(True)
    pal = left.palette()
    pal.setColor(QPalette.Window, QColor(TEAL))
    left.setPalette(pal)

    left_layout = QVBoxLayout(left)
    left_layout.setContentsMargins(16, 16, 16, 16)
    left_layout.setSpacing(0)

    # Header block
    header = QWidget()
    hvl = QVBoxLayout(header)
    hvl.setContentsMargins(0, 0, 0, 0)
    hvl.setSpacing(10)

    logo_lbl = QLabel()
    logo_lbl.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
    if LOGO_PATH:
        pm = QPixmap(LOGO_PATH)
        if not pm.isNull():
            if pm.width() > LOGO_MAX_WIDTH_PX:
                pm = pm.scaledToWidth(LOGO_MAX_WIDTH_PX, Qt.SmoothTransformation)
            logo_lbl.setPixmap(pm)
    hvl.addWidget(logo_lbl)

    title_lbl = QLabel(HEADER_TEXT)
    title_lbl.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
    title_lbl.setStyleSheet(HEADER_STYLE_CSS)
    hvl.addWidget(title_lbl)

    hvl.addSpacing(HEADER_BOTTOM_SPACING)
    left_layout.addWidget(header)

    # Top spacer for centering the button group
    top_spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Fixed)
    left_layout.addItem(top_spacer)

    # Shared button style
    pill_btn_css = """
        QPushButton {
            background: white;
            color: #0F2B28;
            font-weight: 600;
            padding: 10px 12px;
            border-radius: 10px;
        }
        QPushButton:hover { background: #F0FDF4; }
        QPushButton:pressed { background: #E8F5E9; }
    """

    btn_upload = QPushButton("Upload Data")
    btn_upload.setStyleSheet(pill_btn_css)
    btn_upload.setMinimumHeight(32)

    btn_params = QPushButton("Parameters definition")
    btn_params.setStyleSheet(pill_btn_css)
    btn_params.setMinimumHeight(32)

    btn_info = QPushButton("Add info")
    btn_info.setStyleSheet(pill_btn_css)
    btn_info.setMinimumHeight(32)

    group_container = QWidget()
    gvl = QVBoxLayout(group_container)
    gvl.setContentsMargins(0, 0, 0, 0)
    gvl.setSpacing(BUTTONS_GROUP_SPACING)
    gvl.addWidget(btn_upload)
    gvl.addWidget(btn_params)
    gvl.addWidget(btn_info)

    left_layout.addWidget(group_container)

    # GIF + status
    gif_label = QLabel()
    gif_label.setVisible(False)
    gif_label.setAlignment(Qt.AlignCenter)
    left_layout.addWidget(gif_label, 0, Qt.AlignHCenter)

    status_label = QLabel("")
    status_label.setAlignment(Qt.AlignCenter)
    status_label.setStyleSheet(PROCESS_STYLE_CSS)
    status_label.setVisible(False)
    left_layout.addWidget(status_label, 0, Qt.AlignHCenter)

    # Bottom "Go"
    left_layout.addStretch(1)
    go_css = """
        QPushButton {
            background: white;
            color: #0F2B28;
            font-weight: 700;
            padding: 12px 16px;
            border-radius: 14px;
        }
        QPushButton:hover { background: #F0FDF4; }
        QPushButton:pressed { background: #E8F5E9; }
    """
    btn_go = QPushButton("Go")
    btn_go.setStyleSheet(go_css)
    btn_go.setMinimumWidth(120)

    go_row = QHBoxLayout()
    go_row.addStretch(1)
    go_row.addWidget(btn_go)
    go_row.addStretch(1)
    left_layout.addLayout(go_row)

    # Right: tabs
    right = QWidget()
    rlay = QVBoxLayout(right)
    rlay.setContentsMargins(0, 0, 0, 0)
    rlay.setSpacing(0)
    win.tabs = create_tabs()
    rlay.addWidget(win.tabs)

    # Wire actions
    btn_upload.clicked.connect(lambda: upload_file_and_display(win.tabs))
    btn_params.clicked.connect(lambda: win.tabs.setCurrentWidget(win.tabs.param_page))
    btn_info.clicked.connect(lambda: win.tabs.setCurrentWidget(win.tabs.info))

    # GIF movie
    movie = QMovie(GIF_PATH) if GIF_PATH else None
    if movie and movie.isValid() and GIF_WIDTH_PX > 0:
        movie.setScaledSize(QSize(GIF_WIDTH_PX, GIF_WIDTH_PX))

    def run_gif_then_results():
        gif_label.setVisible(True)
        status_label.setText("Processing…")
        status_label.setStyleSheet(PROCESS_STYLE_CSS)
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setVisible(True)

        if movie and movie.isValid():
            gif_label.setMovie(movie)
            movie.start()
        else:
            gif_label.setText("")

        for b in (btn_upload, btn_params, btn_info, btn_go):
            b.setEnabled(False)

        def _finish():
            if movie and movie.isValid():
                movie.stop()
            gif_label.setVisible(False)
            status_label.setText("Done!")
            status_label.setStyleSheet(DONE_STYLE_CSS)
            status_label.setAlignment(Qt.AlignCenter)
            for b in (btn_upload, btn_params, btn_info, btn_go):
                b.setEnabled(True)
            ensure_results_tab_and_open(win.tabs)

        QTimer.singleShot(GIF_DURATION_MS, _finish)

    btn_go.clicked.connect(run_gif_then_results)

    root.addWidget(left)
    root.addWidget(right)

    # Center the three-button group with offset
    def recenter_group():
        left_h = left.height()
        go_h = btn_go.sizeHint().height() + 16
        m = left_layout.contentsMargins()
        margins_h = m.top() + m.bottom()
        header_h = header.sizeHint().height()

        gh = (btn_upload.sizeHint().height()
              + btn_params.sizeHint().height()
              + btn_info.sizeHint().height()
              + 2 * BUTTONS_GROUP_SPACING)

        avail = max(0, left_h - go_h - margins_h - header_h)
        top_h = max(0, int((avail - gh) / 2 + BUTTONS_GROUP_VOFFSET_PX))

        top_spacer.changeSize(0, top_h, QSizePolicy.Minimum, QSizePolicy.Fixed)
        left_layout.invalidate()
        left_layout.activate()

    QTimer.singleShot(0, recenter_group)

    old_resize = left.resizeEvent

    def _left_resize(ev):
        recenter_group()
        if old_resize:
            old_resize(ev)

    left.resizeEvent = _left_resize

    # Apply data-table sizing once + on data page resize
    QTimer.singleShot(0, lambda: apply_data_table_fractional_sizes(win))
    old_data_resize = win.tabs.data_page.resizeEvent

    def _data_page_resize(ev):
        apply_data_table_fractional_sizes(win)
        if old_data_resize:
            old_data_resize(ev)

    win.tabs.data_page.resizeEvent = _data_page_resize

    return win