# tabs.py

import os
import shutil

from PyQt5.QtCore import Qt, QStandardPaths
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import (
    QTabWidget, QWidget,
    QHBoxLayout, QVBoxLayout, QGridLayout,   # <-- add QGridLayout here
    QFrame, QLabel, QSizePolicy, QSpacerItem, QPushButton,
    QTableWidget, QTableWidgetItem,
    QFormLayout, QLineEdit, QTextEdit,
    QDialog, QScrollArea, QMessageBox,
    QListWidget, QListWidgetItem, QComboBox,
    QRadioButton, QButtonGroup, QCheckBox,
)

from config import (
    APP_FONT_FAMILY,
    APP_FONT_COLOR,
    ORELHA_FONT_FAMILY, ORELHA_FONT_SIZE_PT, ORELHA_FONT_WEIGHT,
    ORELHA_LETTER_SPACING_PX, ORELHA_TEXT_COLOR,
    TITLE_FONT_FAMILY, TITLE_FONT_SIZE_PT, TITLE_FONT_WEIGHT,
    TITLE_COLOR, TITLE_LETTER_SPACING,
    FORM_LABEL_SIZE_PT, FORM_LABEL_WEIGHT, INPUT_FONT_SIZE_PT,
    TAB_RADIUS_PX, TAB_PADDING_V, TAB_PADDING_H, TAB_GAP_RIGHT,
    TAB_MIN_WIDTH, TABBAR_LEFT_OFFSET, TABBAR_TOP_OFFSET,
    PANE_MARGIN_TOP, TAB_INACTIVE, ORELHA_ACTIVE_TEXT_COLOR,
    DATA_BG, PARAM_BG, INFO_BG, RESULTS_BG,
    DATA_TABLE_MAX_ROWS, DATA_TABLE_STRETCH, DATA_TITLE_STRETCH,
    DATA_BOTTOM_SPACER_STR, DATA_PAGE_MARGINS, DATA_PAGE_SPACING,
    TEXT_COLOR,
    RESULT_WIN_WIDTH, RESULT_WIN_HEIGHT,
    RESULT_HEADER_BG, RESULT_HEADER_FG, RESULT_HEADER_HEIGHT,
    RESULT_HEADER_FONT_FAM, RESULT_HEADER_SIZE_PT, RESULT_HEADER_WEIGHT,
    RESULT_SCROLL_BG, RESULT_SCROLL_MARGINS, RESULT_SCROLL_SPACING,
    RESULT_BOX_BG, RESULT_BOX_BORDER, RESULT_BOX_RADIUS,
    RESULT_BOX_MIN_WIDTH, RESULT_BOX_HEIGHTS,
    TEAL
)

# -------------------- Helper widgets (selectors) --------------------
class ColumnSelector(QWidget):
    """Left/Right selector with search and 'Select All'."""
    def __init__(self, parent=None):
        super().__init__(parent)
        row = QHBoxLayout(self)

        # Left: search + available list
        left = QVBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search observables...")
        self.search.textChanged.connect(self._filter)
        self.available = QListWidget()
        self.available.setSelectionMode(QListWidget.SingleSelection)
        btn_all = QPushButton("Select All")
        btn_all.clicked.connect(self._select_all)
        left.addWidget(self.search)
        left.addWidget(self.available)
        left.addWidget(btn_all)

        # Middle: add/remove
        mid = QVBoxLayout()
        mid.setAlignment(Qt.AlignCenter)
        btn_add = QPushButton("→"); btn_add.clicked.connect(self._move_to_selected)
        btn_rem = QPushButton("←"); btn_rem.clicked.connect(self._remove_from_selected)
        mid.addWidget(QLabel("Add/Remove"))
        mid.addWidget(btn_add)
        mid.addWidget(btn_rem)

        # Right: selected
        right = QVBoxLayout()
        self.selected = QListWidget()
        self.selected.setSelectionMode(QListWidget.ExtendedSelection)
        right.addWidget(QLabel("Selected Observables"))
        right.addWidget(self.selected)

        row.addLayout(left)
        row.addLayout(mid)
        row.addLayout(right)

        self._all_cols = []
        self._filtered = []

    def load_columns(self, cols):
        self._all_cols = list(cols)
        self._filtered = list(cols)
        self._refresh_available()

    def _refresh_available(self):
        self.available.clear()
        for c in self._filtered:
            self.available.addItem(QListWidgetItem(c))

    def _filter(self):
        t = self.search.text().lower()
        self._filtered = [c for c in self._all_cols if t in c.lower()]
        self._refresh_available()

    def _move_to_selected(self):
        it = self.available.currentItem()
        if it and not self.selected.findItems(it.text(), Qt.MatchExactly):
            self.selected.addItem(QListWidgetItem(it.text()))

    def _remove_from_selected(self):
        for it in self.selected.selectedItems():
            self.selected.takeItem(self.selected.row(it))

    def _select_all(self):
        for c in self._all_cols:
            if not self.selected.findItems(c, Qt.MatchExactly):
                self.selected.addItem(QListWidgetItem(c))

    def get_selected(self):
        return [self.selected.item(i).text() for i in range(self.selected.count())]


class IndividualSelector(QWidget):
    """
    Same layout pattern as ColumnSelector, but:
    - Filters Individuals (rows) with search
    - Limits selection to max_select (default 3)
    - Selected list is the vertical box on the RIGHT
    """
    def __init__(self, max_select=3, parent=None):
        super().__init__(parent)
        self.max_select = max_select

        row = QHBoxLayout(self)

        # Left: search + available individuals
        left = QVBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search individuals...")
        self.search.textChanged.connect(self._filter)

        self.available = QListWidget()
        self.available.setSelectionMode(QListWidget.SingleSelection)
        btn_all = QPushButton("Select All")
        btn_all.clicked.connect(self._select_all_capped)
        left.addWidget(self.search)
        left.addWidget(self.available)
        # left.addWidget(btn_all)  # still optional

        # Middle: add/remove
        mid = QVBoxLayout()
        mid.setAlignment(Qt.AlignCenter)
        btn_add = QPushButton("→"); btn_add.clicked.connect(self._add_one)
        btn_rem = QPushButton("←"); btn_rem.clicked.connect(self._remove_selected)
        mid.addWidget(QLabel("Add/Remove"))
        mid.addWidget(btn_add)
        mid.addWidget(btn_rem)

        # Right: selected (vertical list)
        right = QVBoxLayout()
        self.selected = QListWidget()
        self.selected.setSelectionMode(QListWidget.ExtendedSelection)
        right.addWidget(QLabel(f"Selected (max {self.max_select})"))
        right.addWidget(self.selected)

        row.addLayout(left)
        row.addLayout(mid)
        row.addLayout(right)

        self._all_people = []
        self._filtered = []

    def load_items(self, people_list):
        self._all_people = list(people_list)
        self._filtered = list(people_list)
        self._refresh_available()

    def _refresh_available(self):
        self.available.clear()
        for p in self._filtered:
            self.available.addItem(QListWidgetItem(str(p)))

    def _filter(self):
        # fixed to use QLineEdit API
        t = self.search.text().lower()
        self._filtered = [p for p in self._all_people if t in str(p).lower()]
        self._refresh_available()

    def _add_one(self):
        it = self.available.currentItem()
        if not it:
            return
        if self.selected.count() >= self.max_select:
            return  # hard cap
        if not self.selected.findItems(it.text(), Qt.MatchExactly):
            self.selected.addItem(QListWidgetItem(it.text()))

    def _remove_selected(self):
        for it in self.selected.selectedItems():
            self.selected.takeItem(self.selected.row(it))

    def _select_all_capped(self):
        already = set(self.get_selected())
        for p in self._all_people:
            if len(self.get_selected()) >= self.max_select:
                break
            if p not in already:
                self.selected.addItem(QListWidgetItem(str(p)))
                already.add(p)

    def get_selected(self):
        return [self.selected.item(i).text() for i in range(self.selected.count())]






# ------------------------------------------------------------------------------
#




# -------------------- Core Page + Table --------------------
class DataTable(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.table = QTableWidget()
        sp = self.table.sizePolicy()
        sp.setHorizontalPolicy(QSizePolicy.Expanding)
        sp.setVerticalPolicy(QSizePolicy.Preferred)
        self.table.setSizePolicy(sp)
        layout.addWidget(self.table)

        # Jamovi-like table styling
        self.table.setStyleSheet("""
            QTableWidget {
                font-family: 'Segoe UI Variable', 'Segoe UI', Arial, sans-serif;
                font-size: 11pt;
                color: #202124;
                gridline-color: #E5E7EB;
                selection-background-color: #DDEBF7;
                selection-color: #111;
            }
            QHeaderView::section {
                font-weight: 600;
                background: #F3F4F6;
                padding: 6px 8px;
                border: 0px;
                border-bottom: 1px solid #E5E7EB;
            }
        """)

    def display_dataframe(self, df):
        self.table.clear()
        rows = min(DATA_TABLE_MAX_ROWS, len(df))
        self.table.setRowCount(rows)
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns.astype(str).tolist())
        for i in range(rows):
            for j, val in enumerate(df.iloc[i]):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))


class ContentPage(QWidget):
    def __init__(self, bg_hex: str, title: str = "", show_title: bool = False):
        super().__init__()
        self.bg_hex = bg_hex
        self.setAutoFillBackground(True)
        pal = self.palette()
        pal.setColor(QPalette.Window, QColor(bg_hex))
        self.setPalette(pal)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        container = QFrame(objectName="pageContainer")
        container.setStyleSheet(f"""
            QFrame#pageContainer {{
                background: {bg_hex};
                border: 0px;
                border-top-left-radius: {TAB_RADIUS_PX}px;
                border-top-right-radius: {TAB_RADIUS_PX}px;
            }}
        """)

        inner = QVBoxLayout(container)
        inner.setContentsMargins(*DATA_PAGE_MARGINS)
        inner.setSpacing(DATA_PAGE_SPACING)

        self.title = None
        if show_title and title:
            self.title = QLabel(title)
            self.title.setStyleSheet(f"""
                font-family: '{TITLE_FONT_FAMILY}', 'Segoe UI', Arial, sans-serif;
                font-size: {TITLE_FONT_SIZE_PT}pt;
                font-weight: {TITLE_FONT_WEIGHT};
                letter-spacing: {TITLE_LETTER_SPACING}px;
                color: {TITLE_COLOR};
            """)
            inner.addWidget(self.title, DATA_TITLE_STRETCH)

        self.body = inner
        inner.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))
        inner.setStretch(inner.count() - 1, DATA_BOTTOM_SPACER_STR)
        root.addWidget(container)


# -------- Results sub-window --------
class ResultWindow(QDialog):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(RESULT_WIN_WIDTH, RESULT_WIN_HEIGHT)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        header = QFrame()
        header.setFixedHeight(RESULT_HEADER_HEIGHT)
        header.setStyleSheet(f"QFrame {{ background: {RESULT_HEADER_BG}; border: 0; }}")
        hbox = QHBoxLayout(header)
        hbox.setContentsMargins(0, 0, 0, 0)
        title_lbl = QLabel(title)
        title_lbl.setAlignment(Qt.AlignCenter)
        title_lbl.setStyleSheet(
            f"color: {RESULT_HEADER_FG};"
            f"font-family: '{RESULT_HEADER_FONT_FAM}', 'Segoe UI', Arial, sans-serif;"
            f"font-size: {RESULT_HEADER_SIZE_PT}pt;"
            f"font-weight: {RESULT_HEADER_WEIGHT};"
            "letter-spacing: 0.3px;"
        )
        hbox.addWidget(title_lbl)
        root.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        root.addWidget(scroll, 1)

        content = QWidget()
        content.setStyleSheet(f"background: {RESULT_SCROLL_BG};")
        scroll.setWidget(content)

        cv = QVBoxLayout(content)
        L, T, R, B = RESULT_SCROLL_MARGINS
        cv.setContentsMargins(L, T, R, B)
        cv.setSpacing(RESULT_SCROLL_SPACING)

        def make_box(min_h):
            box = QFrame()
            box.setMinimumHeight(int(min_h))
            box.setMinimumWidth(RESULT_BOX_MIN_WIDTH)
            box.setStyleSheet(
                "QFrame {"
                f"  background: {RESULT_BOX_BG};"
                f"  border: {RESULT_BOX_BORDER};"
                f"  border-radius: {RESULT_BOX_RADIUS}px;"
                "}"
            )
            inner = QVBoxLayout(box)
            inner.setContentsMargins(16, 16, 16, 16)
            hint = QLabel("⟪ Add content here ⟫")
            hint.setAlignment(Qt.AlignCenter)
            hint.setStyleSheet("color:#6B6F76; font-size: 12pt;")
            inner.addStretch(1)
            inner.addWidget(hint, 0, Qt.AlignCenter)
            inner.addStretch(1)
            return box

        for h in RESULT_BOX_HEIGHTS:
            cv.addWidget(make_box(h))
        cv.addStretch(1)

class YesNoToggle(QWidget):
    """
    Compact yes/no radio group in a single row.
    value() -> True (yes), False (no), or None (none selected).
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.yes = QRadioButton("yes")
        self.no  = QRadioButton("no")

        self.group = QButtonGroup(self)
        self.group.addButton(self.yes)
        self.group.addButton(self.no)

        layout.addWidget(self.yes)
        layout.addWidget(self.no)

    def value(self):
        if self.yes.isChecked():
            return True
        if self.no.isChecked():
            return False
        return None

    def set_value(self, flag: bool):
        if flag is True:
            self.yes.setChecked(True)
        elif flag is False:
            self.no.setChecked(True)
        else:
            self.group.setExclusive(False)
            self.yes.setChecked(False)
            self.no.setChecked(False)
            self.group.setExclusive(True)




# ===================== TAB BUILDERS =====================
def build_data_tab(page: ContentPage) -> DataTable:
    row = QHBoxLayout()

    data_table = DataTable()
    row.addWidget(data_table, 1)

    side = QFrame()
    sv = QVBoxLayout(side)
    sv.setContentsMargins(0, 0, 0, 0)
    sv.setSpacing(12)

    # Observables
    sv.addWidget(QLabel("Observable selection"))
    page.data_selector = ColumnSelector()
    sv.addWidget(page.data_selector)

    # Individuals
    sv.addWidget(QLabel("Individual selection"))
    page.data_individuals = IndividualSelector(max_select=3)
    sv.addWidget(page.data_individuals)

    sv.addStretch(1)
    row.addWidget(side, 1)

    page.body.insertLayout(1 if page.title else 0, row, DATA_TABLE_STRETCH)
    return data_table

def build_parameters_tab(page: ContentPage):
    """
    Parameters tab UI:
    Left column:
        - Cutoff number of traits
        - Traits activation rate
        - Prune (yes/no)
        - Traits assignment weights (yes/no)
        - Z-score standardization (yes/no)
    Right column:
        - Section title: Model dynamics
        - Regularization (yes/no)
        - Optimizer learn rate
        - noise ratio
    Bottom:
        - Analytical report: Clinician / Researcher / Developer (independent checkboxes)
    """
    # ---- Styles ----
    label_css = (
        f"font-family: '{APP_FONT_FAMILY}', 'Segoe UI', Arial, sans-serif;"
        f"font-size: {FORM_LABEL_SIZE_PT}pt;"
        f"font-weight: {FORM_LABEL_WEIGHT};"
        f"color: {TEXT_COLOR};"
    )
    input_css = (
        f"QLineEdit {{"
        f"  background: white; border: 1px solid #E6E6E6; border-radius: 6px;"
        f"  padding: 4px 8px;"
        f"  font-family: '{APP_FONT_FAMILY}', 'Segoe UI', Arial, sans-serif;"
        f"  font-size: {INPUT_FONT_SIZE_PT}pt; color: #111;"
        f"}}"
    )
    yesno_css = (
        f"QRadioButton {{"
        f"  font-family: '{APP_FONT_FAMILY}', 'Segoe UI', Arial, sans-serif;"
        f"  font-size: {INPUT_FONT_SIZE_PT}pt; color: #111;"
        f"}}"
    )

    # Outer vertical layout inside the page
    outer = QVBoxLayout()
    outer.setSpacing(30)

    # Top hint
    hint = QLabel("")
    hint.setStyleSheet("font-size: 14px; color: #444;")
    outer.addWidget(hint)

    # Two-column layout
    row = QHBoxLayout()
    row.setSpacing(80)

    left_form = QFormLayout()
    left_form.setHorizontalSpacing(24)
    left_form.setVerticalSpacing(18)

    # Right side: title + form stacked vertically
    right_col = QVBoxLayout()
    right_col.setSpacing(12)

    right_form = QFormLayout()
    right_form.setHorizontalSpacing(24)
    right_form.setVerticalSpacing(18)

    # ========= LEFT COLUMN =========
    # Cutoff number of traits
    lbl_cutoff = QLabel("Cutoff number of traits:")
    lbl_cutoff.setStyleSheet(label_css)
    cutoff_traits = QLineEdit()
    cutoff_traits.setFixedWidth(80)
    cutoff_traits.setStyleSheet(input_css)
    cutoff_traits.setPlaceholderText("1000")        # suggestion only
    left_form.addRow(lbl_cutoff, cutoff_traits)

    # Traits activation rate
    lbl_act = QLabel("Traits activation rate:")
    lbl_act.setStyleSheet(label_css)
    traits_activation = QLineEdit()
    traits_activation.setFixedWidth(80)
    traits_activation.setStyleSheet(input_css)
    traits_activation.setPlaceholderText("1.0")     # suggestion only
    left_form.addRow(lbl_act, traits_activation)

    # Prune yes/no
    lbl_prune = QLabel("Prune:")
    lbl_prune.setStyleSheet(label_css)
    prune_toggle = YesNoToggle()
    prune_toggle.setStyleSheet(yesno_css)
    left_form.addRow(lbl_prune, prune_toggle)

    # Traits assignment weights yes/no
    lbl_weights = QLabel("Traits assignment weights:")
    lbl_weights.setStyleSheet(label_css)
    weights_toggle = YesNoToggle()
    weights_toggle.setStyleSheet(yesno_css)
    left_form.addRow(lbl_weights, weights_toggle)

    # Z-score standardization yes/no
    lbl_zscore = QLabel("Z-score standardization:")
    lbl_zscore.setStyleSheet(label_css)
    zscore_toggle = YesNoToggle()
    zscore_toggle.setStyleSheet(yesno_css)
    left_form.addRow(lbl_zscore, zscore_toggle)

    # ========= RIGHT COLUMN =========
    # Section title: Model dynamics
    dyn_title = QLabel("Model dynamics:")
    dyn_title.setStyleSheet(
        f"{label_css} font-weight: 800; font-size: {FORM_LABEL_SIZE_PT + 1}pt;"
    )
    right_col.addWidget(dyn_title)

    # Regularization yes/no
    lbl_reg = QLabel("Regularization:")
    lbl_reg.setStyleSheet(label_css)
    regularization_toggle = YesNoToggle()
    regularization_toggle.setStyleSheet(yesno_css)
    right_form.addRow(lbl_reg, regularization_toggle)

    # Optimizer learn rate
    lbl_lr = QLabel("Optimizer learn rate:")
    lbl_lr.setStyleSheet(label_css)
    optimizer_lr = QLineEdit()
    optimizer_lr.setFixedWidth(80)
    optimizer_lr.setStyleSheet(input_css)
    optimizer_lr.setPlaceholderText("0.05")         # suggestion only
    right_form.addRow(lbl_lr, optimizer_lr)

    # noise ratio
    lbl_noise = QLabel("noise ratio:")
    lbl_noise.setStyleSheet(label_css)
    noise_ratio = QLineEdit()
    noise_ratio.setFixedWidth(80)
    noise_ratio.setStyleSheet(input_css)
    noise_ratio.setPlaceholderText("0.4")           # suggestion only
    right_form.addRow(lbl_noise, noise_ratio)

    # Assemble columns
    row.addLayout(left_form)
    right_col.addLayout(right_form)
    row.addLayout(right_col)
    outer.addLayout(row)

    # ========= ANALYTICAL REPORT SECTION (BOTTOM) =========
    outer.addSpacerItem(QSpacerItem(0, 80, QSizePolicy.Minimum, QSizePolicy.Fixed))

    report_block = QVBoxLayout()
    report_block.setSpacing(16)

    report_label = QLabel("Analytical report:")
    report_label.setAlignment(Qt.AlignCenter)
    report_label.setStyleSheet(
        f"{label_css} font-weight: 800; font-size: {FORM_LABEL_SIZE_PT + 1}pt;"
    )
    report_block.addWidget(report_label)

    report_row = QHBoxLayout()
    report_row.setSpacing(60)
    report_row.addStretch(1)

    cb_clin = QCheckBox("Clinician")
    cb_res  = QCheckBox("Researcher")
    cb_dev  = QCheckBox("Developer")
    for cb in (cb_clin, cb_res, cb_dev):
        cb.setStyleSheet(yesno_css)
        report_row.addWidget(cb)

    report_row.addStretch(1)
    report_block.addLayout(report_row)

    outer.addLayout(report_block)

    # Insert at top of the page body
    page.body.insertLayout(0, outer)

    # Expose handles for later retrieval
    page.parameters = {
        "cutoff_traits": cutoff_traits,
        "traits_activation": traits_activation,
        "prune": prune_toggle,
        "traits_assignment_weights": weights_toggle,
        "zscore_standardization": zscore_toggle,
        "regularization": regularization_toggle,
        "optimizer_lr": optimizer_lr,
        "noise_ratio": noise_ratio,
        "report_checkboxes": {
            "clinician": cb_clin,
            "researcher": cb_res,
            "developer": cb_dev,
        },
    }
    
def build_info_tab(page: ContentPage):
    form = QFormLayout()
    form.setLabelAlignment(Qt.AlignLeft | Qt.AlignTop)
    form.setFormAlignment(Qt.AlignTop)
    form.setHorizontalSpacing(32)
    form.setVerticalSpacing(20)

    label_css = (
        f"font-family: '{APP_FONT_FAMILY}', 'Segoe UI', Arial, sans-serif;"
        f"font-size: {FORM_LABEL_SIZE_PT}pt;"
        f"font-weight: {FORM_LABEL_WEIGHT};"
        f"color: {TEXT_COLOR};"
    )
    input_css = (
        f"QLineEdit, QTextEdit {{"
        f"  background: white; border: 1px solid #E6E6E6; border-radius: 6px;"
        f"  padding: 8px 10px;"
        f"  font-family: '{APP_FONT_FAMILY}', 'Segoe UI', Arial, sans-serif;"
        f"  font-size: {INPUT_FONT_SIZE_PT}pt; color: #111;"
        f"}}"
        f"QTextEdit {{ line-height: 140%; }}"
    )

    project_name = QLineEdit()
    project_name.setPlaceholderText("Type the project name…")
    project_name.setMinimumWidth(760)
    project_name.setStyleSheet(input_css)

    analyst = QLineEdit()
    analyst.setPlaceholderText("Type the researcher / analyst name…")
    analyst.setMinimumWidth(760)
    analyst.setStyleSheet(input_css)

    desc = QTextEdit()
    desc.setPlaceholderText("Briefly describe the project…")
    desc.setMinimumSize(760, 360)
    desc.setStyleSheet(input_css)

    notes = QTextEdit()
    notes.setPlaceholderText("Any extra notes…")
    notes.setMinimumSize(760, 140)
    notes.setStyleSheet(input_css)

    lbl_name  = QLabel("Project name:");        lbl_name.setStyleSheet(label_css)
    lbl_ra    = QLabel("Researcher Analyst:");  lbl_ra.setStyleSheet(label_css)
    lbl_desc  = QLabel("Project description:"); lbl_desc.setStyleSheet(label_css)
    lbl_notes = QLabel("Notes:");               lbl_notes.setStyleSheet(label_css)

    form.addRow(lbl_name,  project_name)
    form.addRow(lbl_ra,    analyst)
    form.addRow(lbl_desc,  desc)
    form.addRow(lbl_notes, notes)

    page.body.addLayout(form)

    page.fields = {
        "project_name": project_name,
        "researcher_analyst": analyst,
        "description": desc,
        "notes": notes,
    }
def build_results_tab(page: ContentPage):
    """
    Results tab:
    - 4 large cards (2x2 grid), centered horizontally and vertically.
    - Download button centered below the cards.
    """

    # --- Clear the default spacer that ContentPage adds ---
    while page.body.count():
        item = page.body.takeAt(0)
        w = item.widget()
        if w is not None:
            w.deleteLater()

    root = QVBoxLayout()
    root.setSpacing(24)

    # -------- central widget (cards + button) --------
    center_widget = QWidget()
    center_layout = QVBoxLayout(center_widget)
    center_layout.setSpacing(32)
    center_layout.setContentsMargins(0, 0, 0, 0)
    center_layout.setAlignment(Qt.AlignCenter)

    # --- Card buttons (2 x 2 grid) ---
    card_css = """
        QPushButton {
            background: white;
            color: #14524C;
            border-radius: 22px;
            padding: 22px 28px;
            border: 1px solid #E2E8F0;
            font-family: 'Segoe UI Variable', 'Segoe UI', Arial, sans-serif;
            font-size: 18pt;
            font-weight: 600;
            text-align: center;
        }
        QPushButton:hover {
            background: #F3FAFB;
            border-color: #CBD5E1;
        }
        QPushButton:pressed {
            background: #E0F2F1;
            border-color: #94A3B8;
        }
    """

    grid = QGridLayout()
    grid.setHorizontalSpacing(40)
    grid.setVerticalSpacing(28)

    btn_bp    = QPushButton("B-P Profiles")
    btn_grp   = QPushButton("Group Analysis")
    btn_trait = QPushButton("Traits Ecosystem")
    btn_stat  = QPushButton("Statistics")

    for b in (btn_bp, btn_grp, btn_trait, btn_stat):
        b.setStyleSheet(card_css)
        b.setMinimumHeight(160)
        b.setMinimumWidth(320)

    grid.addWidget(btn_bp,    0, 0)
    grid.addWidget(btn_grp,   0, 1)
    grid.addWidget(btn_trait, 1, 0)
    grid.addWidget(btn_stat,  1, 1)

    grid_wrapper = QHBoxLayout()
    grid_wrapper.addStretch(1)
    grid_wrapper.addLayout(grid)
    grid_wrapper.addStretch(1)

    center_layout.addLayout(grid_wrapper)

    # --- Download report primary button ---
    dl = QPushButton("Download analytical report")
    dl.setStyleSheet(f"""
        QPushButton {{
            background: {TEAL};
            color: white;
            border: none;
            border-radius: 20px;
            padding: 12px 26px;
            font-family: '{APP_FONT_FAMILY}', 'Segoe UI', Arial, sans-serif;
            font-size: 13pt;
            font-weight: 600;
        }}
        QPushButton:hover {{
            background: #2F7E76;
        }}
        QPushButton:pressed {{
            background: #24635C;
        }}
    """)
    dl_row = QHBoxLayout()
    dl_row.addStretch(1)
    dl_row.addWidget(dl)
    dl_row.addStretch(1)

    center_layout.addLayout(dl_row)

    # -------- add central widget to page, vertically centered --------
    root.addStretch(1)                                      # top
    root.addWidget(center_widget, 0, Qt.AlignCenter)        # middle
    root.addStretch(1)                                      # bottom

    page.body.addLayout(root)

    # -------- Behaviour (unchanged) --------
    def open_win(title):
        w = ResultWindow(title, page)
        w.show()
        w.raise_()

    btn_bp.clicked.connect(lambda: open_win("B-P profiles"))
    btn_grp.clicked.connect(lambda: open_win("Group analysis"))
    btn_trait.clicked.connect(lambda: open_win("Traits ecosystem"))
    btn_stat.clicked.connect(lambda: open_win("Statistics"))

    def _unique_path(path):
        if not os.path.exists(path):
            return path
        rootp, ext = os.path.splitext(path)
        i = 1
        while True:
            cand = f"{rootp} ({i}){ext}"
            if not os.path.exists(cand):
                return cand
            i += 1

    def download_report():
        downloads_dir = (
            QStandardPaths.writableLocation(QStandardPaths.DownloadLocation)
            or os.path.expanduser("~/Downloads")
        )
        os.makedirs(downloads_dir, exist_ok=True)
        dest = _unique_path(os.path.join(downloads_dir, "report.pdf"))
        src = os.path.join(os.getcwd(), "report.pdf")
        try:
            if os.path.exists(src):
                shutil.copyfile(src, dest)
            else:
                with open(dest, "wb") as f:
                    f.write(b"%PDF-1.4\n1 0 obj<<>>endobj\ntrailer<<>>\n%%EOF")
            QMessageBox.information(page, "Report downloaded",
                                    f"Report saved to:\n{dest}")
        except Exception as e:
            QMessageBox.critical(page, "Download failed",
                                 f"Could not download the report:\n{e}")

    dl.clicked.connect(download_report)

# -------------------- Tab widget styling & creation --------------------
def _tab_stylesheet(active_bg: str) -> str:
    return f"""
        QTabWidget::tab-bar {{ left: {TABBAR_LEFT_OFFSET}px; top: {TABBAR_TOP_OFFSET}px; }}
        QTabWidget::pane {{ border: 0px; margin-top: {PANE_MARGIN_TOP}px; background: {active_bg}; }}
        QTabBar::tab {{
            background: {TAB_INACTIVE};
            color: {ORELHA_TEXT_COLOR};
            border: 0px;
            border-radius: {TAB_RADIUS_PX}px;
            padding: {TAB_PADDING_V}px {TAB_PADDING_H}px;
            margin-right: {TAB_GAP_RIGHT}px;
            font-family: '{ORELHA_FONT_FAMILY}', 'Segoe UI', Arial, sans-serif;
            font-size: {ORELHA_FONT_SIZE_PT}pt;
            font-weight: {ORELHA_FONT_WEIGHT};
            letter-spacing: {ORELHA_LETTER_SPACING_PX}px;
            min-width: {TAB_MIN_WIDTH}px;
        }}
        QTabBar::tab:selected {{
            background: {active_bg};
            color: {ORELHA_ACTIVE_TEXT_COLOR};
        }}    """


def create_tabs() -> QTabWidget:
    tabs = QTabWidget()
    tabs.setTabPosition(QTabWidget.North)
    tabs.setMovable(False)
    tabs.setTabsClosable(False)
    tabs.setElideMode(Qt.ElideNone)
    tabs.setUsesScrollButtons(False)

    # Pages
    tabs.data_page    = ContentPage(DATA_BG,  "Data Preview", show_title=True)
    tabs.param_page   = ContentPage(PARAM_BG, "", show_title=False)
    tabs.info         = ContentPage(INFO_BG,  "", show_title=False)
    tabs.results_page = ContentPage(RESULTS_BG, "", show_title=False)

    # Build content
    tabs.data_table = build_data_tab(tabs.data_page)
    build_parameters_tab(tabs.param_page)
    build_info_tab(tabs.info)
    build_results_tab(tabs.results_page)

    # Tabs (add only the first three now)
    tabs.addTab(tabs.data_page, "Data")
    tabs.addTab(tabs.param_page, "Parameters")
    tabs.addTab(tabs.info, "Info")

    # mark results tab as hidden initially
    tabs._results_tab_added = False

    tabs.setStyleSheet(_tab_stylesheet(DATA_BG))

    def on_tab_changed(_):
        active_bg = getattr(tabs.currentWidget(), "bg_hex", DATA_BG)
        tabs.setStyleSheet(_tab_stylesheet(active_bg))

    tabs.currentChanged.connect(on_tab_changed)

    return tabs