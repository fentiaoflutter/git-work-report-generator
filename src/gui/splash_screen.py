from PyQt6.QtWidgets import QSplashScreen, QProgressBar
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QPainter, QColor, QLinearGradient, QFont, QPainterPath
import os

class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        
        # 创建一个空白的QPixmap
        pixmap = QPixmap(600, 400)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        # 创建画家对象
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 创建渐变背景
        gradient = QLinearGradient(0, 0, 600, 400)
        gradient.setColorAt(0, QColor(41, 128, 185))  # 蓝色
        gradient.setColorAt(1, QColor(109, 213, 237))  # 浅蓝色
        
        # 绘制圆角矩形背景
        path = QPainterPath()
        path.addRoundedRect(0, 0, 600, 400, 15, 15)
        painter.fillPath(path, gradient)
        
        # 设置字体
        title_font = QFont('Arial', 24, QFont.Weight.Bold)
        subtitle_font = QFont('Arial', 12)
        
        # 绘制标题
        painter.setFont(title_font)
        painter.setPen(Qt.GlobalColor.white)
        painter.drawText(0, 100, 600, 50, Qt.AlignmentFlag.AlignCenter, 'Git工作报告生成器')
        
        # 绘制副标题
        painter.setFont(subtitle_font)
        painter.drawText(0, 150, 600, 30, Qt.AlignmentFlag.AlignCenter, '正在启动应用...')
        
        # 绘制装饰性元素
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(255, 255, 255, 30))
        painter.drawEllipse(50, 50, 100, 100)
        painter.drawEllipse(450, 250, 80, 80)
        
        painter.end()
        
        self.setPixmap(pixmap)
        
        # 创建进度条
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(100, 250, 400, 8)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background: rgba(255, 255, 255, 0.3);
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background: white;
                border-radius: 4px;
            }
        """)
        
        # 设置动画定时器
        self.progress = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(30)  # 每30毫秒更新一次
    
    def update_progress(self):
        """更新进度条"""
        self.progress += 1
        if self.progress <= 100:
            self.progress_bar.setValue(self.progress)
        else:
            self.timer.stop()
    
    def mousePressEvent(self, event):
        """处理鼠标点击事件"""
        event.ignore()  # 忽略所有鼠标事件，防止点击关闭 