import sys
import traceback
import os
from datetime import datetime
from PyQt6.QtWidgets import QApplication
from src.gui.main_window import MainWindow
from src.gui.splash_screen import SplashScreen
from PyQt6.QtCore import QTimer

def setup_environment():
    # 确保资源路径正确
    if getattr(sys, 'frozen', False):
        # 如果是打包后的应用
        application_path = os.path.dirname(sys.executable)
    else:
        # 如果是开发环境
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    # 设置工作目录
    os.chdir(os.path.dirname(application_path))
    
    # 添加到Python路径
    if application_path not in sys.path:
        sys.path.insert(0, application_path)

def main():
    try:
        # 设置环境
        setup_environment()
        
        # 创建应用
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
        
        # 进入事件循环
        return app.exec()
        
    except Exception as e:
        # 记录错误到日志文件
        log_dir = os.path.expanduser("~/Library/Logs/Git报告生成器")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "error.log")
        
        with open(log_file, "a") as f:
            f.write(f"\n=== 错误报告 {datetime.now()} ===\n")
            f.write(f"异常类型: {type(e).__name__}\n")
            f.write(f"异常信息: {str(e)}\n")
            f.write("详细追踪:\n")
            f.write(traceback.format_exc())
            f.write("\n")
        
        # 显示错误对话框
        from PyQt6.QtWidgets import QMessageBox
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Icon.Critical)
        error_box.setWindowTitle("错误")
        error_box.setText("程序启动时发生错误")
        error_box.setDetailedText(f"详细错误信息已保存到:\n{log_file}")
        error_box.exec()
        
        return 1

if __name__ == "__main__":
    sys.exit(main()) 