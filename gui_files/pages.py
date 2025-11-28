# pages.py (v0 - reference preserved)

from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


def create_image_frame(image_path, image_width, image_height,
                       margin_top=10, margin_bottom=10, margin_left=10, margin_right=10,
                       border_radius=20, border_color="#B0B0B0", border_thickness=1):
    # === Load image ===
    pixmap = QPixmap(image_path)
    if pixmap.isNull():
        error = QLabel(f"Image not found: {image_path}")
        error.setAlignment(Qt.AlignCenter)
        error.setStyleSheet("color: red; font-size: 14px;")
        return error

    scaled_pixmap = pixmap.scaled(image_width, image_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    # === Image label ===
    label = QLabel()
    label.setPixmap(scaled_pixmap)
    label.setAlignment(Qt.AlignCenter)

    # === Frame container ===
    frame = QFrame()
    frame.setStyleSheet(f"""
        QFrame {{
            background-color: white;
            border-style: solid;
            border-width: {border_thickness}px;
            border-color: {border_color};
            border-radius: {border_radius}px;
        }}
    """)

    # === Layout ===
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(margin_left, margin_top, margin_right, margin_bottom)
    layout.addWidget(label)

    total_width = image_width + margin_left + margin_right
    total_height = image_height + margin_top + margin_bottom
    frame.setFixedSize(total_width, total_height)

    return frame

def trait_latent_page():
    container = QWidget()
    layout = QVBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(20)


    # === Frame 1 ===
    frame0 = create_image_frame(
        image_path="results/traits_vs_features.png",
        image_width=1200,
        image_height=1500
    )
    layout.addWidget(frame0, alignment=Qt.AlignCenter)

    # === Frame 1 ===
    frame1 = create_image_frame(
        image_path="results/traits_radar.png",
        image_width=1200,
        image_height=1500
    )
    layout.addWidget(frame1, alignment=Qt.AlignCenter)

    # === Frame 2  ===
    frame2 = create_image_frame(
        image_path="results/traits_bars.png",  # replace with actual path
        image_width=1200,
        image_height=800
    )
    layout.addWidget(frame2, alignment=Qt.AlignCenter)

        # === Frame 3 ===
    frame3 = create_image_frame(
        image_path="results/trait_informativeness.png",  # replace with actual path
        image_width=1200,
        image_height=800
    )
    layout.addWidget(frame3, alignment=Qt.AlignCenter)

            # === Frame 4 ===
    frame4 = create_image_frame(
        image_path="results/traits_orthogonality.png",  # replace with actual path
        image_width=1200,
        image_height=800
    )
    layout.addWidget(frame4, alignment=Qt.AlignCenter)

    return container




def bp_profile_page():
    def create_image_frame(image_path, width, height, margins=(10, 10, 10, 10), border_radius=20, border_color="#B0B0B0", border_thickness=1):
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            error = QLabel(f"Image not found: {image_path}")
            error.setAlignment(Qt.AlignCenter)
            error.setStyleSheet("color: red; font-size: 14px;")
            return error

        scaled_pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label = QLabel()
        label.setPixmap(scaled_pixmap)
        label.setAlignment(Qt.AlignCenter)

        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-style: solid;
                border-width: {border_thickness}px;
                border-color: {border_color};
                border-radius: {border_radius}px;
            }}
        """)
        layout = QVBoxLayout(frame)
        L, T, R, B = margins
        layout.setContentsMargins(L, T, R, B)
        layout.addWidget(label)
        frame.setFixedSize(width + L + R, height + T + B)
        return frame

    # === Main Container ===
    container = QWidget()
    layout = QVBoxLayout(container)
    layout.setSpacing(20)
    layout.setContentsMargins(10, 20, 10, 20)

    # === Patient Blocks ===
    patient_blocks = [
        ("A04545", "results/a04545.png", "results/A04545_piramide.png"),
        ("A05694", "results/a05694.png", "results/A05694_piramide.png"),
        ("A05889", "results/a05889.png", "results/A05889_piramide.png"),
    ]

    for name, path_left, path_right in patient_blocks:
        wrapper = QWidget()
        vbox = QVBoxLayout(wrapper)
        vbox.setSpacing(8)

        label = QLabel(f"Patient: <b>{name}</b>")
        label.setAlignment(Qt.AlignLeft)
        label.setStyleSheet("font-size: 14pt; margin-left: 6px;")
        vbox.addWidget(label)

        row = QHBoxLayout()
        row.setSpacing(20)
        row.addWidget(create_image_frame(path_left, 620, 500))
        row.addWidget(create_image_frame(path_right, 620, 500))
        vbox.addLayout(row)

        layout.addWidget(wrapper)

    layout.addStretch(1)

    return container

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt

def traits_ecosystem_analysis_page():
    container = QWidget()
    layout = QVBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(20)

    # === Frame 1 ===
    frame1 = create_image_frame(
        "results/trait_network.png",
        1000,
        600
    )
    layout.addWidget(frame1, alignment=Qt.AlignCenter)

    # === Text Frame as Placeholder for Frame 2 and 3 ===
    text_frame = QFrame()
    text_frame.setStyleSheet("""
        QFrame {
            background-color: #FAFAFA;
            border: 1px solid #B0B0B0;
            border-radius: 15px;
            padding: 20px;
        }
    """)
    text_layout = QVBoxLayout(text_frame)
    text_label = QLabel("Complex network topological analysis (to be added).")
    text_label.setAlignment(Qt.AlignCenter)
    text_label.setStyleSheet("font-size: 18px; color: #333333;")
    text_layout.addWidget(text_label)

    layout.addWidget(text_frame, alignment=Qt.AlignCenter)

    # === Frame 2 (temporarily disabled) ===
    # frame2 = create_image_frame(
    #     "results/eco_analysis_2.png",
    #     1000,
    #     600
    # )
    # layout.addWidget(frame2, alignment=Qt.AlignCenter)

    # === Frame 3 (temporarily disabled) ===
    # frame3 = create_image_frame(
    #     "results/eco_analysis_3.png",
    #     1000,
    #     600
    # )
    # layout.addWidget(frame3, alignment=Qt.AlignCenter)

    return container


from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt

def group_analysis_page():
    container = QWidget()
    layout = QVBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(20)

    # === Frame 1: Full width, centered ===
    title1 = QLabel("Trait Popularity Overview")
    title1.setStyleSheet("font-weight: bold; font-size: 14px;")
    layout.addWidget(title1, alignment=Qt.AlignCenter)

    frame1 = create_image_frame("results/trait_popularity.png", 1000, 600)
    layout.addWidget(frame1, alignment=Qt.AlignCenter)

    # === Row 1: Profile Distribution + Heterogeneity ===
    title2 = QLabel("Group Heterogeneity")
    title2.setStyleSheet("font-weight: bold; font-size: 14px;")
    layout.addWidget(title2, alignment=Qt.AlignCenter)

    row1 = QHBoxLayout()
    row1.setSpacing(40)

    frame2 = create_image_frame("results/profiles_distribution.png", 500, 400)
    frame3 = create_image_frame("results/profile_heterogeneity.png", 500, 400)

    row1.addWidget(frame2)
    row1.addWidget(frame3)
    layout.addLayout(row1)

    # === Row 2: Trait Co-activation + Network ===
    title3 = QLabel("Trait ecosystem mapping")
    title3.setStyleSheet("font-weight: bold; font-size: 14px;")
    layout.addWidget(title3, alignment=Qt.AlignCenter)

    row2 = QHBoxLayout()
    row2.setSpacing(40)

    frame4 = create_image_frame("results/trait_coactivation.png", 500, 400)
    frame5 = create_image_frame("results/trait_network.png", 500, 400)

    row2.addWidget(frame4)
    row2.addWidget(frame5)
    layout.addLayout(row2)

    return container