from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget

class MainWindow(QMainWindow):
    pass

app = QApplication([])
window = MainWindow()
window.show()
app.exec()