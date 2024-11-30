from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import QUrl
class Side:
    def __init__(self, color, sound):
        self.color = color
        self.turn = 1 if color == "red" else 2
        
        self.sound = QSoundEffect()
        self.sound.setSource(QUrl.fromLocalFile(sound))
        self.sound.setLoopCount(1)
        self.sound.setVolume(0.7)

    # To Be Overriden
    def move(self):
        pass