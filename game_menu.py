import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QLabel, QPushButton, QComboBox, QSpinBox, QStackedWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont


class GameMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Menu System")
        self.setFixedSize(400, 300)

        # Set Windows-friendly font
        self.setFont(QFont("Segoe UI", 10))

        # Create stacked widget to manage different pages
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create pages
        self.main_menu_page = self.create_main_menu()
        self.algorithm_page = self.create_algorithm_page()
        self.parameter_page = self.create_parameter_page()

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.main_menu_page)
        self.stacked_widget.addWidget(self.algorithm_page)
        self.stacked_widget.addWidget(self.parameter_page)

        # Initialize game settings
        self.selected_mode = ""
        self.selected_algorithm = ""
        self.k_parameter = 3

        # Set style for all buttons
        self.setStyleSheet("""
            QPushButton {
                padding: 8px;
                background-color: #0078D4;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #106EBE;
            }
            QComboBox {
                padding: 5px;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
            }
            QSpinBox {
                padding: 5px;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
            }
        """)

    def create_main_menu(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("Game Mode Selection")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px; color: #000000;")

        # Mode buttons
        modes = ["Human vs Human", "Agent vs Human", "Agent vs Agent"]
        for mode in modes:
            btn = QPushButton(mode)
            btn.setFixedHeight(40)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, m=mode: self.mode_selected(m))
            layout.addWidget(btn)

        page.setLayout(layout)
        return page

    def create_algorithm_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Select Algorithm")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px; color: #000000;")

        self.algorithm_combo = QComboBox()
        self.algorithm_combo.addItems([
            "Minimax",
            "Minimax with Pruning",
            "ExpectiminMax"
        ])
        self.algorithm_combo.setFixedHeight(35)

        next_btn = QPushButton("Next")
        next_btn.setFixedHeight(40)
        next_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        next_btn.clicked.connect(self.algorithm_selected)

        back_btn = QPushButton("Back")
        back_btn.setFixedHeight(40)
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        layout.addWidget(title)
        layout.addWidget(self.algorithm_combo)
        layout.addWidget(next_btn)
        layout.addWidget(back_btn)

        page.setLayout(layout)
        return page

    def create_parameter_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Set K Parameter")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px; color: #000000;")

        self.k2_spinbox = QSpinBox()
        self.k2_spinbox.setRange(1, 42)
        self.k2_spinbox.setValue(3)
        self.k2_spinbox.setFixedHeight(35)

        start_btn = QPushButton("Start Game")
        start_btn.setFixedHeight(40)
        start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        start_btn.clicked.connect(self.start_game)

        back_btn = QPushButton("Back")
        back_btn.setFixedHeight(40)
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        layout.addWidget(title)
        layout.addWidget(self.k2_spinbox)
        layout.addWidget(start_btn)
        layout.addWidget(back_btn)

        page.setLayout(layout)
        return page

    def mode_selected(self, mode):
        self.selected_mode = mode
        if mode == "Human vs Human":
            # Skip algorithm selection for Human vs Human
            self.selected_algorithm = "None"
            self.stacked_widget.setCurrentIndex(2)
        else:
            self.stacked_widget.setCurrentIndex(1)

    def algorithm_selected(self):
        self.selected_algorithm = self.algorithm_combo.currentText()
        self.stacked_widget.setCurrentIndex(2)

    def start_game(self):
        self.k_parameter = self.k2_spinbox.value()
        print(f"""
Game Settings:
Mode: {self.selected_mode}
Algorithm: {self.selected_algorithm}
K Parameter: {self.k_parameter}
        """)

       #link here


def main():
    app = QApplication(sys.argv)
    window = GameMenu()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()