from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QPushButton, QFileDialog, QDateEdit, QSpinBox,
                           QComboBox, QLabel, QMessageBox, QGroupBox,
                           QLineEdit, QTextEdit, QCheckBox, QGridLayout)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QIcon
from ..core.git_analyzer import GitAnalyzer
from ..core.report_generator import ReportGenerator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Git提交记录分析器")
        self.setMinimumSize(800, 600)
        
        # 主窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # 创建各个区域
        self.create_repository_section(main_layout)
        self.create_date_section(main_layout)
        self.create_filter_section(main_layout)
        self.create_report_section(main_layout)
        self.create_action_buttons(main_layout)
        
        self.repo_path = None
        self.apply_styles()
        
    def create_repository_section(self, parent_layout):
        group = QGroupBox("Git仓库设置")
        layout = QGridLayout()
        
        # 仓库选择
        self.repo_btn = QPushButton("选择Git仓库")
        self.repo_btn.setIcon(QIcon('assets/folder.png'))
        self.repo_btn.clicked.connect(self.select_repository)
        
        self.repo_path_label = QLineEdit()
        self.repo_path_label.setReadOnly(True)
        self.repo_path_label.setPlaceholderText("请选择Git仓库目录...")
        
        layout.addWidget(QLabel("仓库路径:"), 0, 0)
        layout.addWidget(self.repo_path_label, 0, 1)
        layout.addWidget(self.repo_btn, 0, 2)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)
        
    def create_date_section(self, parent_layout):
        group = QGroupBox("时间范围")
        layout = QGridLayout()
        
        # 日期选择
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        self.start_date.setCalendarPopup(True)
        
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        
        # 快捷按钮
        quick_date_layout = QHBoxLayout()
        
        last_week_btn = QPushButton("最近一周")
        last_week_btn.clicked.connect(lambda: self.set_date_range(7))
        
        last_month_btn = QPushButton("最近一月")
        last_month_btn.clicked.connect(lambda: self.set_date_range(30))
        
        last_quarter_btn = QPushButton("最近三月")
        last_quarter_btn.clicked.connect(lambda: self.set_date_range(90))
        
        quick_date_layout.addWidget(last_week_btn)
        quick_date_layout.addWidget(last_month_btn)
        quick_date_layout.addWidget(last_quarter_btn)
        
        layout.addWidget(QLabel("开始日期:"), 0, 0)
        layout.addWidget(self.start_date, 0, 1)
        layout.addWidget(QLabel("结束日期:"), 0, 2)
        layout.addWidget(self.end_date, 0, 3)
        layout.addLayout(quick_date_layout, 1, 0, 1, 4)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)
        
    def create_filter_section(self, parent_layout):
        group = QGroupBox("筛选条件")
        layout = QGridLayout()
        
        # 作者筛选
        self.author_filter = QLineEdit()
        self.author_filter.setPlaceholderText("输入作者名称（可选）...")
        
        # 文件类型筛选
        self.file_types = QLineEdit()
        self.file_types.setPlaceholderText("输入文件类型，用逗号分隔（例如: .py,.java）...")
        
        # 忽略文件
        self.ignore_files = QTextEdit()
        self.ignore_files.setPlaceholderText("输入要忽略的文件或目录，每行一个...")
        self.ignore_files.setMaximumHeight(80)
        
        layout.addWidget(QLabel("作者筛选:"), 0, 0)
        layout.addWidget(self.author_filter, 0, 1)
        layout.addWidget(QLabel("文件类型:"), 1, 0)
        layout.addWidget(self.file_types, 1, 1)
        layout.addWidget(QLabel("忽略文件:"), 2, 0)
        layout.addWidget(self.ignore_files, 2, 1)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)
        
    def create_report_section(self, parent_layout):
        group = QGroupBox("报告设置")
        layout = QGridLayout()
        
        # 报告类型选择
        self.report_type = QComboBox()
        self.report_type.addItems(["简介", "详细", "超详细"])
        
        # 报告选项
        self.include_charts = QCheckBox("包含统计图表")
        self.include_charts.setChecked(True)
        
        self.include_file_stats = QCheckBox("包含文件统计")
        self.include_file_stats.setChecked(True)
        
        self.include_commit_messages = QCheckBox("包含提交信息")
        self.include_commit_messages.setChecked(True)
        
        layout.addWidget(QLabel("报告类型:"), 0, 0)
        layout.addWidget(self.report_type, 0, 1)
        layout.addWidget(self.include_charts, 1, 0)
        layout.addWidget(self.include_file_stats, 1, 1)
        layout.addWidget(self.include_commit_messages, 2, 0)
        
        group.setLayout(layout)
        parent_layout.addWidget(group)
        
    def create_action_buttons(self, parent_layout):
        layout = QHBoxLayout()
        
        # 生成报告按钮
        self.generate_btn = QPushButton("生成报告")
        self.generate_btn.setIcon(QIcon('assets/report.png'))
        self.generate_btn.clicked.connect(self.generate_report)
        self.generate_btn.setMinimumHeight(40)
        
        # 预览按钮
        preview_btn = QPushButton("预览")
        preview_btn.setIcon(QIcon('assets/preview.png'))
        preview_btn.clicked.connect(self.preview_report)
        
        # 重置按钮
        reset_btn = QPushButton("重置")
        reset_btn.setIcon(QIcon('assets/reset.png'))
        reset_btn.clicked.connect(self.reset_form)
        
        layout.addWidget(reset_btn)
        layout.addWidget(preview_btn)
        layout.addWidget(self.generate_btn)
        
        parent_layout.addLayout(layout)
        
    def apply_styles(self):
        # 设置样式
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 6px;
                margin-top: 6px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 7px;
                padding: 0px 5px 0px 5px;
            }
            QPushButton {
                padding: 5px 15px;
                border-radius: 4px;
                background-color: #f0f0f0;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QLineEdit, QTextEdit, QDateEdit, QComboBox {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 4px;
            }
        """)
        
    def set_date_range(self, days):
        end_date = QDate.currentDate()
        start_date = end_date.addDays(-days)
        self.start_date.setDate(start_date)
        self.end_date.setDate(end_date)
        
    def select_repository(self):
        repo_path = QFileDialog.getExistingDirectory(
            self, "选择Git仓库目录"
        )
        if repo_path:
            self.repo_path = repo_path
            self.repo_path_label.setText(repo_path)
            
    def preview_report(self):
        # TODO: 实现报告预览功能
        QMessageBox.information(self, "预览", "报告预览功能即将推出...")
        
    def reset_form(self):
        self.repo_path = None
        self.repo_path_label.clear()
        self.author_filter.clear()
        self.file_types.clear()
        self.ignore_files.clear()
        self.set_date_range(30)  # 重置为最近一个月
        self.report_type.setCurrentIndex(0)
        self.include_charts.setChecked(True)
        self.include_file_stats.setChecked(True)
        self.include_commit_messages.setChecked(True)
            
    def generate_report(self):
        if not self.repo_path:
            QMessageBox.warning(self, "错误", "请先选择Git仓库！")
            return
            
        start_date = self.start_date.date().toPyDate()
        end_date = self.end_date.date().toPyDate()
        
        # 获取筛选条件
        filters = {
            'author': self.author_filter.text(),
            'file_types': [ft.strip() for ft in self.file_types.text().split(',') if ft.strip()],
            'ignore_files': self.ignore_files.toPlainText().splitlines(),
            'include_charts': self.include_charts.isChecked(),
            'include_file_stats': self.include_file_stats.isChecked(),
            'include_commit_messages': self.include_commit_messages.isChecked()
        }
        
        try:
            analyzer = GitAnalyzer(self.repo_path)
            commits = analyzer.analyze_commits(
                start_date, 
                end_date,
                filters
            )
            
            generator = ReportGenerator()
            report = generator.generate(
                commits,
                self.report_type.currentText(),
                start_date,
                end_date,
                filters
            )
            
            # 保存报告
            file_name, _ = QFileDialog.getSaveFileName(
                self,
                "保存报告",
                f"git_report_{start_date}_{end_date}.html",
                "HTML files (*.html)"
            )
            
            if file_name:
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(report)
                QMessageBox.information(
                    self, "成功", "报告生成成功！"
                )
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成报告时发生错误：{str(e)}") 