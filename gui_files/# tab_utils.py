# tab_utils.py
import numpy as np
from PyQt5.QtWidgets import (
    QMenu, QAction, QDialog, QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt, QPoint

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class DistributionDialog(QDialog):
    def __init__(self, column_name, values, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Distribution – {column_name}")
        self.resize(500, 400)

        layout = QVBoxLayout(self)

        fig = Figure(figsize=(5, 4))
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

        ax = fig.add_subplot(111)

        ax.hist(values, bins="auto", alpha=0.8)
        ax.set_title(f"Histogram – {column_name}")
        ax.set_xlabel(column_name)
        ax.set_ylabel("Frequency")

        mean = float(np.mean(values))
        std = float(np.std(values))

        ax.text(
            0.05,
            0.95,
            f"mean = {mean:.3f}\nstd = {std:.3f}",
            transform=ax.transAxes,
            va="top",
            ha="left",
            fontsize=10,
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.7),
        )

        fig.tight_layout()
        canvas.draw()


def enable_column_distribution_menu(table_view, get_dataframe_callable):
    table_view.setContextMenuPolicy(Qt.CustomContextMenu)

    def on_context_menu_requested(pos: QPoint):
        index = table_view.indexAt(pos)
        selection_model = table_view.selectionModel()

        if selection_model is not None and selection_model.selectedColumns():
            col = selection_model.selectedColumns()[0].column()
        else:
            if not index.isValid():
                return
            col = index.column()

        df = get_dataframe_callable()
        if df is None or df.empty:
            return

        if col < 0 or col >= df.shape[1]:
            return

        column_name = df.columns[col]

        menu = QMenu(table_view)
        action_distribution = QAction(
            f"Show distribution of '{column_name}'",
            menu
        )

        def show_distribution():
            series = df[column_name].dropna()
            numeric = series.select_dtypes(include=[np.number])

            if numeric.empty:
                QMessageBox.information(
                    table_view,
                    "Non-numeric column",
                    f"Column '{column_name}' has no numeric data to plot."
                )
                return

            dialog = DistributionDialog(
                column_name,
                numeric.values,
                parent=table_view
            )
            dialog.exec_()

        action_distribution.triggered.connect(show_distribution)
        menu.addAction(action_distribution)
        menu.exec_(table_view.viewport().mapToGlobal(pos))

    table_view.customContextMenuRequested.connect(on_context_menu_requested)