from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtMultimedia import *

from PlayerFactory import PlayerFactory
from GUI_Controller.Player import Player
from GUI_Controller.Agent import Agent

from datetime import datetime
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
    game_over = pyqtSignal()
    agent_turn = pyqtSignal()
    def __init__(self):
        super().__init__()
        
        # Create Players
        # Should be from main menu
        # Player 1 Must Be the red color
        self.player1 = PlayerFactory("red", True).create_player("assets/sound1.wav")
        # self.player2 = PlayerFactory("yellow", True).create_player("assets/sound2.wav")
        self.player2 = PlayerFactory("yellow", False).create_player("assets/sound2.wav", 3, "Minmax", "Lecture")

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

        self.moves_left = 0
        self.currentState = [['0','0','0','0','0','0','0'], ['0','0','0','0','0','0','0'], ['0','0','0','0','0','0','0'], ['0','0','0','0','0','0','0'], ['0','0','0','0','0','0','0'], ['0','0','0','0','0','0','0']]
        for i in range(len(self.currentState)):
            row_widgets = []
            for j in range(len(self.currentState[i])):
                color = "red" if self.currentState[i][j] == '1' else "yellow" if self.currentState[i][j] == '2' else "white"
                self.moves_left += self.currentState[i][j] == '0'
                pawn = GamePawn(color, i, j, self)
                pawn.setPalette(self.default_palette())
                pawn.hovered.connect(self.on_hover)
                pawn.clicked.connect(self.player_turn)
                layout.addWidget(pawn, i, j)
                row_widgets.append(pawn)
            self.widgets.append(row_widgets)
        
        self.game_over.connect(self.end_game)

        if isinstance(self.player1, Agent):
            QTimer.singleShot(1500, self.agent_play)

        
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
        if isinstance(self.currentPlayer, Agent):
            return
        if col == -1:
            for row_widgets in self.widgets:
                for widget in row_widgets:
                    widget.setPalette(self.default_palette())
        else:
            for r in range(len(self.widgets)):
                for c in range(len(self.widgets[r])):
                    if c == col:
                        self.widgets[r][c].setPalette(self.hover_palette())

    def update_board(self, col):
        if self.currentState[0][col] != '0':
            return
        for i in range(len(self.currentState) - 1, -1, -1):
            if self.currentState[i][col] == '0':
                turn = self.currentPlayer.turn
                self.currentState[i][col] = str(turn)
                self.widgets[i][col].set_color(self.currentPlayer.color)
                self.currentPlayer.sound.play()
                self.moves_left -= 1
                break
        
    def player_turn(self, col):
        if isinstance(self.currentPlayer, Agent):
            return
        
        self.update_board(col)

        if self.moves_left == 0:
            self.game_over.emit()
            return
        
        self.swap_turn()

        if isinstance(self.currentPlayer, Agent):
            QTimer.singleShot(1000, self.agent_play)
    
    def swap_turn(self):
        turn = self.currentPlayer.turn
        if turn == 1:
            self.currentPlayer = self.player2
        else:
            self.currentPlayer = self.player1

        if isinstance(self.currentPlayer, Agent):
            for row_widgets in self.widgets:
                for widget in row_widgets:
                    widget.setPalette(self.default_palette())

    def agent_play(self):
        if isinstance(self.currentPlayer, Player):
            return
        
        st_time = datetime.now()
        col, self.game_score = self.currentPlayer.solver.play(self.currentState)

        print(f"Agent Chooses: {col}")
        print(self.game_score)
        print((datetime.now() - st_time).total_seconds())
        self.update_board(col)

        if self.moves_left == 0:
            self.game_over.emit()
            return
        
        self.swap_turn()

    def end_game(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Game Over")
        
        winner = ""
        if self.game_score > 0:
                winner = "Player 1: Red"
        elif self.game_score < 0:
                winner = "Player 2: Yellow"
        else:
            winner = "Draw"
        
        dlg_text = "Draw, Replay?" if winner == "Draw" else f"Winner {winner}, With Score {self.game_score/10000}, Replay?"
        dlg.setText(dlg_text)
        dlg.setStandardButtons(
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.No
        )
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Yes:
            print("OK!")
        else:
            print("NO")
            
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