from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

class GamePawn(QWidget):
    def __init__(self, color):
        super().__init__()

        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

        self.setFixedSize(QSize(100, 100))
        
        # self.setStyleSheet("""
        #     background-color: red;
        #     border-radius: 50px;
        #     border: 2px solid black;
        # """)


class GameBoard(QWidget):
    def __init__(self):
        super().__init__()
        
        # Define Colors of Board
        self.setAutoFillBackground(True)
        
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("navy"))
        self.setPalette(palette)
        
        # Create The Grid
        layout = QGridLayout()
        layout.setSpacing(10)

        self.currentState = [[1,0,0,2,0,2,1],[1,0,0,2,0,2,1],[1,0,0,2,0,2,1],[1,0,0,2,0,2,1],[1,0,0,2,0,2,1],[1,0,0,2,0,2,1]]
        for i in range(len(self.currentState)):
            for j in range(len(self.currentState[i])):
                color = "red" if self.currentState[i][j] == 1 else "yellow" if self.currentState[i][j] == 2 else "white"
                layout.addWidget(GamePawn(color), i, j)

        self.setLayout(layout)

class MainLayout(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.setSpacing(20)

        # First Widget Game Board
        self.addWidget(GameBoard(), 6)

        # Second Widget Game Tree
        self.addWidget(Color("grey"), 4)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Connect - 4")

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        
        width = int(screen_geometry.width() * 0.75)
        height = int(screen_geometry.height() * 0.85)
        self.resize(width, height)

        x = int((screen_geometry.width() - width) / 2)
        y = int((screen_geometry.height() - height) / 2)
        self.move(x, y)
        
        layout = MainLayout()

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

app = QApplication([])

window = MainWindow()
window.show()

app.exec()