# Git工作报告生成器

一个基于 Python 的桌面应用程序，可以自动分析 Git 仓库的提交记录，生成美观的工作报告。该工具特别适合需要定期汇报工作内容的开发人员使用。

## 功能特点

- 🚀 **可视化界面**: 使用 PyQt6 构建的现代化图形界面
- 📊 **多种报告格式**: 支持生成简单、中等、详细三种格式的报告
- 🔍 **智能分析**: 自动识别并分类不同类型的工作内容
- 📅 **时间筛选**: 支持按日期范围筛选工作内容
- 👥 **作者筛选**: 支持按提交作者筛选工作内容
- 🎨 **美观报告**: 生成美观的 HTML 格式报告
- 🔄 **实时进度**: 展示报告生成的实时进度
- ⚡️ **高效处理**: 快速处理大量的 Git 提交记录

## 安装说明

### 环境要求

- Python 3.8 或更高版本
- Git

### 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/fentiaoflutter/git-work-report-generator.git
cd git-work-report-generator
```

2. 创建并激活虚拟环境（推荐）：
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

1. 启动应用：
```bash
python run.py
```

2. 在应用界面中：
   - 选择 Git 仓库目录
   - 设置时间范围
   - 选择作者（可选）
   - 选择报告类型（简单/中等/详细）
   - 点击生成报告

3. 报告类型说明：
   - **简单报告**: 包含工作内容的基本统计信息
   - **中等报告**: 包含统计信息和工作内容的简要描述
   - **详细报告**: 包含完整的工作详情，包括具体的代码变更记录

## 功能截图
![Uploading 截屏2025-01-12 11.51.35.png…]()


## 项目结构

```
git-work-report-generator/
├── src/
│   ├── core/
│   │   ├── git_analyzer.py    # Git 分析核心逻辑
│   │   └── report_generator.py # 报告生成器
│   ├── gui/
│   │   ├── main_window.py     # 主窗口界面
│   │   ├── splash_screen.py   # 启动画面
│   │   └── author_dialog.py   # 作者选择对话框
│   └── utils/                 # 工具函数
├── requirements.txt           # 项目依赖
└── run.py                    # 启动脚本
```

## 开发说明

### 主要依赖

- PyQt6: 用于构建图形界面
- GitPython: 用于分析 Git 仓库
- Jinja2: 用于生成 HTML 报告
- pandas: 用于数据处理

### 代码风格

项目遵循 PEP 8 编码规范，使用 pylint 进行代码质量检查。

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

[您的姓名] - [您的邮箱]

项目链接: [https://github.com/fentiaoflutter/git-work-report-generator](https://github.com/fentiaoflutter/git-work-report-generator) 
