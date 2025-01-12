from PyQt6.QtWidgets import QSplashScreen
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class SplashScreen(QSplashScreen):
    def __init__(self):
        splash_pix = QPixmap('assets/splash.png')
        super().__init__(splash_pix)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | 
                          Qt.WindowType.SplashScreen) 