from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtMultimedia import *

from PlayerFactory import PlayerFactory
from GUI_Controller.Player import Player
from GUI_Controller.Agent import Agent

class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)
        
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

class GamePawn(QWidget):
    hovered = pyqtSignal(int)
    clicked = pyqtSignal(int)

    def __init__(self, color, row, col, parent=None):
        super().__init__(parent)
        self.current_color = QColor(color)
        self.row = row
        self.col = col

        self.setFixedSize(QSize(100, 100))
        self.setAutoFillBackground(True)

    def set_color(self, color):
        self.current_color = QColor(color)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(self.current_color))
        painter.setPen(QPen(self.current_color))

        painter.drawEllipse(5,5,90,90)
    
    def enterEvent(self, event):
        self.hovered.emit(self.col)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hovered.emit(-1)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.col)
            super().mousePressEvent(event)

class GameBoard(QWidget):
    def __init__(self):
        super().__init__()
        
        # Create Players
        # Should be from main menu
        self.player1 = PlayerFactory("red", True).create_player("assets/sound1.wav")
        self.player2 = PlayerFactory("yellow", True).create_player("assets/sound2.wav")
        self.currentPlayer = self.player1
        
        # Define Colors of Board
        self.setAutoFillBackground(True)
        
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("navy"))
        self.setPalette(palette)
        

        # Create The Grid
        layout = QGridLayout()
        layout.setSpacing(10)
        
        self.widgets = []

        self.currentState = [[1,0,0,2,0,2,1],[1,0,0,2,0,2,1],[1,0,0,2,0,2,1],[1,0,0,2,0,2,1],[1,0,0,2,0,2,1],[1,0,0,2,0,2,1]]
        for i in range(len(self.currentState)):
            row_widgets = []
            for j in range(len(self.currentState[i])):
                color = "red" if self.currentState[i][j] == 1 else "yellow" if self.currentState[i][j] == 2 else "white"
                pawn = GamePawn(color, i, j, self)
                pawn.setPalette(self.default_palette())
                if isinstance(self.currentPlayer, Player): 
                    pawn.hovered.connect(self.on_hover)
                    pawn.clicked.connect(self.on_click)
                layout.addWidget(pawn, i, j)
                row_widgets.append(pawn)
            self.widgets.append(row_widgets)

        self.setLayout(layout)

    def default_palette(self):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("transparent"))
        return palette

    def hover_palette(self):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("lightblue"))
        return palette

    def on_hover(self, col):
        if col == -1:
            for row_widgets in self.widgets:
                for widget in row_widgets:
                    widget.setPalette(self.default_palette())
        else:
            for r in range(len(self.widgets)):
                for c in range(len(self.widgets[r])):
                    if c == col:
                        self.widgets[r][c].setPalette(self.hover_palette())

    def on_click(self, col):
        if self.currentState[0][col] != 0:
            return
        for i in range(len(self.currentState) - 1, -1, -1):
            if self.currentState[i][col] == 0:
                turn = self.currentPlayer.turn
                self.currentState[i][col] = turn
                self.widgets[i][col].set_color(self.currentPlayer.color)
                self.currentPlayer.sound.play()
                if turn == 1:
                    self.currentPlayer = self.player2
                else:
                    self.currentPlayer = self.player1
                return

class MainLayout(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.setSpacing(20)

        # First Widget Game Board
        self.gameBoard = GameBoard()

        self.addWidget(self.gameBoard, 6)

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