import numpy as np
from PyQt5.QtWidgets import (
    QMenu, QAction, QDialog, QVBoxLayout, QMessageBox, QTableView
)
from PyQt5.QtCore import Qt, QPoint

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class DistributionDialog(QDialog):
    """
    Dialog showing a histogram for a given column,
    with mean and std written inside the figure.
    """
    def __init__(self, column_name, values, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Distribution – {column_name}")
        self.resize(500, 400)
  
        layout = QVBoxLayout(self)

        fig = Figure(figsize=(5, 4))
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

        ax = fig.add_subplot(111)

# --- manual histogram, normalized so sum = 1 ---
        counts, bin_edges = np.histogram(values, bins="auto")
        probs = counts / len(values)                  # sum(probs) == 1
        bin_widths = np.diff(bin_edges)

        ax.bar(
            bin_edges[:-1],
            probs,
            width=bin_widths,
            align="edge",
            alpha=0.8,
            color="green",
        )

        ax.set_title("Distribution")
        ax.set_xlabel(column_name)
        ax.set_ylabel("Probability")

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        mean = float(np.mean(values))
        std = float(np.std(values))

 

        ax.text(
            0.05, 0.95,
            f"mean = {mean:.3f}\nstd = {std:.3f}",
            transform=ax.transAxes,
            va="top", ha="left",
            fontsize=10,
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.7),
        )

        fig.tight_layout()
        canvas.draw()
        self.dataframe = None

def enable_column_distribution_menu(table_widget,
                                    get_dataframe_callable,
                                    get_view_callable=None):
    """
    Attach a right-click 'Show distribution' option.

    Parameters
    ----------
    table_widget : QWidget
        Your DataTable instance (wrapper).
    get_dataframe_callable : () -> pandas.DataFrame
        Returns the current dataframe backing the table.
    get_view_callable : () -> QTableView, optional
        Returns the inner QTableView/QTableWidget.
        If None, this function will try to find it automatically.
    """

    # --- Resolve the real QTableView/QTableWidget -------------------------
    if get_view_callable is not None:
        view = get_view_callable()
    else:
        # If DataTable already *is* a QTableView/QTableWidget
        if isinstance(table_widget, QTableView):
            view = table_widget
        else:
            # Try to find a QTableView child inside DataTable
            view = table_widget.findChild(QTableView)
            if view is None:
                # No valid view – silently abort wiring
                return

    view.setContextMenuPolicy(Qt.CustomContextMenu)

    def on_context_menu_requested(pos: QPoint):
        index = view.indexAt(pos)
        selection_model = view.selectionModel()

        # Prefer selected column if available
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

        menu = QMenu(view)
        action_distribution = QAction(
            f"Show distribution of '{column_name}'",
            menu
        )

        def show_distribution():
            series = df[column_name].dropna()
            try:
                numeric = series.astype(float)
            except Exception:
                QMessageBox.information(
                    view,
                    "Non-numeric column",
                    f"Column '{column_name}' has no numeric data to plot.",
                )
                return

            dialog = DistributionDialog(
                column_name,
                numeric.values,
                parent=view,
            )
            dialog.exec_()

        action_distribution.triggered.connect(show_distribution)
        menu.addAction(action_distribution)
        menu.exec_(view.viewport().mapToGlobal(pos))

    view.customContextMenuRequested.connect(on_context_menu_requested)