from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtMultimedia import *

from datetime import datetime

from GUI_Controller.Player import Player
from GUI_Controller.Agent import Agent

from TreeGraphicsView import TreeGraphicsView

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
    root_node_updated = pyqtSignal(object)
    game_over = pyqtSignal()
    agent_turn = pyqtSignal()

    def __init__(self, p1, p2):
        super().__init__()
        self.player1 = p1
        self.player2 = p2

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
        res = self.currentPlayer.solver.play(self.currentState)
        col = res[0]
        self.game_score = res[1]
        self.tree_node = res[2]
        print(f"Agent Chooses: {col}")
        print(self.game_score)
        print((datetime.now() - st_time).total_seconds())
        self.update_board(col)
        self.root_node_updated.emit(self.tree_node)
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
    def __init__(self, p1, p2):
        super().__init__()
        self.player1 = p1
        self.player2 = p2
        self.root_node = None
        self.setSpacing(10)
        self.setContentsMargins(10, 10, 10, 10)
        
        # First Widget Game Board
        self.gameBoard = GameBoard(self.player1, self.player2)
        self.tree = TreeGraphicsView(self.root_node)
        
        self.gameBoard.root_node_updated.connect(self.tree.update_tree)

        self.addWidget(self.gameBoard, 6)
        self.addWidget(self.tree, 6)

class MainGame(QWidget):
    def __init__(self, p1, p2):
        super().__init__()
        self.player1 = p1
        self.player2 = p2
        
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        
        width = int(screen_geometry.width() * 0.75)
        height = int(screen_geometry.height() * 0.85)

        self.setMinimumSize(width, height)
        layout = MainLayout(self.player1, self.player2)

        self.setLayout(layout)