import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QLabel, QPushButton, QComboBox, QSpinBox, QStackedWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont

from gameBoard import MainGame
from PlayerFactory import PlayerFactory

class GameMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connect - 4")
        
        # Initialize game settings
        self.player1 = None
        self.player2 = None
        self.selected_mode = ""
        self.selected_algorithm = ""
        self.k_parameter = 3

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        
        width = int(screen_geometry.width() * 0.8)
        height = int(screen_geometry.height() * 0.9)
        self.resize(width, height)
        x = int((screen_geometry.width() - width) / 2)
        y = int((screen_geometry.height() - height) / 2)
        self.move(x, y)

        # Set Windows-friendly font
        self.setFont(QFont("Segoe UI", 10))


        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create stacked widget to manage different pages
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setMinimumSize(800, 600)

        layout.addWidget(self.stacked_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        # Create pages
        self.main_menu_page = self.create_main_menu()
        self.algorithm_page = self.create_algorithm_page()
        self.parameter_page = self.create_parameter_page()

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.main_menu_page)
        self.stacked_widget.addWidget(self.algorithm_page)
        self.stacked_widget.addWidget(self.parameter_page)

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
        modes = ["Agent vs Human" ]# ,"Human vs Human", "Agent vs Agent"]
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
            "Minmax",
            "AlphaBeta",
            "Expectiminmax"
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
            self.player1 = PlayerFactory("red", True).create_player("assets/sound1.wav")
            self.player2 = PlayerFactory("yellow", True).create_player("assets/sound2.wav")
            self.selected_algorithm = "None"
            self.initialize_main_game()
        elif mode == "Agent vs Human":
            self.player1 = PlayerFactory("red", False)
            self.player2 = PlayerFactory("yellow", True).create_player("assets/sound2.wav")
            self.stacked_widget.setCurrentIndex(1)
        else:
            self.player1 = PlayerFactory("red", False)
            self.player2 = PlayerFactory("yellow", False)
            self.stacked_widget.setCurrentIndex(1)

    def algorithm_selected(self):
        self.selected_algorithm = self.algorithm_combo.currentText()
        self.stacked_widget.setCurrentIndex(2)

    def start_game(self):
        self.k_parameter = self.k2_spinbox.value()
        if self.selected_mode == "Agent vs Human":
            self.player1 = self.player1.create_player("assets/sound1.wav", self.k_parameter, self.selected_algorithm, "Lecture") 

        # Link To Game
        self.initialize_main_game()

    def initialize_main_game(self):
        self.main_game = MainGame(self.player1, self.player2, self.k_parameter)
        self.stacked_widget.addWidget(self.main_game)
        self.stacked_widget.setCurrentWidget(self.main_game)
        
def main():
    app = QApplication(sys.argv)
    window = GameMenu()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()