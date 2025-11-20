# main.py

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from config import APP_FONT_FAMILY, APP_FONT_SIZE_PT, APP_FONT_COLOR
from functions import create_main_window


def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setStyleSheet(
        f"* {{ font-family: '{APP_FONT_FAMILY}', 'Segoe UI', Arial, sans-serif; "
        f"font-size: {APP_FONT_SIZE_PT}pt; color: {APP_FONT_COLOR}; }}"
    )

    window = create_main_window()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()