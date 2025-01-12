from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QListWidget, QLabel,
                           QListWidgetItem)
from PyQt6.QtCore import Qt

class AuthorSelectionDialog(QDialog):
    def __init__(self, authors, parent=None):
        super().__init__(parent)
        self.setWindowTitle("选择作者")
        self.setMinimumWidth(300)
        
        layout = QVBoxLayout(self)
        
        # 说明标签
        label = QLabel("请选择要包含的作者（可多选）：")
        layout.addWidget(label)
        
        # 作者列表
        self.author_list = QListWidget()
        self.author_list.setSelectionMode(
            QListWidget.SelectionMode.MultiSelection
        )
        
        # 添加作者到列表
        for author in sorted(authors):
            item = QListWidgetItem(author)
            self.author_list.addItem(item)
            item.setSelected(True)  # 默认全选
        
        layout.addWidget(self.author_list)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        # 全选/取消全选按钮
        select_all_btn = QPushButton("全选")
        select_all_btn.clicked.connect(self.select_all)
        
        deselect_all_btn = QPushButton("取消全选")
        deselect_all_btn.clicked.connect(self.deselect_all)
        
        # 确定/取消按钮
        ok_button = QPushButton("确定")
        ok_button.clicked.connect(self.accept)
        
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(select_all_btn)
        button_layout.addWidget(deselect_all_btn)
        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
    
    def select_all(self):
        for i in range(self.author_list.count()):
            self.author_list.item(i).setSelected(True)
    
    def deselect_all(self):
        for i in range(self.author_list.count()):
            self.author_list.item(i).setSelected(False)
    
    def get_selected_authors(self):
        return [
            item.text() 
            for item in self.author_list.selectedItems()
        ] 