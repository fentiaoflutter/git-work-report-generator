import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from gui.main_window import MainWindow
from gui.splash_screen import SplashScreen

def main():
    app = QApplication(sys.argv)
    
    # 显示启动画面
    splash = SplashScreen()
    splash.show()
    
    # 创建主窗口
    window = MainWindow()
    
    # 2秒后关闭启动画面并显示主窗口
    def show_main_window():
        splash.finish(window)
        window.show()
    
    QTimer.singleShot(2000, show_main_window)
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 