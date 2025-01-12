import os
import shutil
from pathlib import Path

def create_release_package():
    # 创建发布目录
    release_dir = Path("release")
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir()
    
    # 创建应用目录
    app_dir = release_dir / "Git报告生成器.app"
    app_dir.mkdir(parents=True)
    
    # 复制所有源代码和资源文件
    src_dir = app_dir / "Contents/Resources/src"
    src_dir.mkdir(parents=True)
    shutil.copytree("src", src_dir, dirs_exist_ok=True)
    
    # 复制图标
    assets_dir = app_dir / "Contents/Resources/assets"
    if assets_dir.exists():
        shutil.rmtree(assets_dir)
    shutil.copytree("src/assets", assets_dir)
    
    # 创建启动脚本
    launcher = '''#!/bin/bash
    # 获取应用程序所在目录的绝对路径
    APP_DIR="$(cd "$(dirname "$0")/../Resources" && pwd)"
    cd "$APP_DIR"
    
    # 确保Python环境正确
    export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
    export PYTHONPATH="$APP_DIR:$PYTHONPATH"
    
    # 创建日志目录
    mkdir -p "$HOME/Library/Logs/Git报告生成器"
    LOG_FILE="$HOME/Library/Logs/Git报告生成器/app.log"
    
    # 运行程序并记录日志
    {
        echo "=== 程序启动 $(date) ==="
        echo "工作目录: $APP_DIR"
        echo "Python路径: $(which python3)"
        python3 -V
        echo "PYTHONPATH: $PYTHONPATH"
        echo "正在启动主程序..."
        
        # 运行主程序
        python3 src/main.py 2>&1
        
        echo "程序退出代码: $?"
        echo "=== 程序结束 $(date) ==="
    } >> "$LOG_FILE" 2>&1
    '''
    
    launcher_path = app_dir / "Contents/MacOS/launcher"
    launcher_path.parent.mkdir(parents=True)
    with open(launcher_path, 'w') as f:
        f.write(launcher)
    
    # 设置执行权限
    os.chmod(launcher_path, 0o755)
    
    # 创建Info.plist
    info_plist = '''<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>CFBundleName</key>
        <string>Git报告生成器</string>
        <key>CFBundleDisplayName</key>
        <string>Git报告生成器</string>
        <key>CFBundleIdentifier</key>
        <string>com.gitreport.app</string>
        <key>CFBundleVersion</key>
        <string>1.0.0</string>
        <key>CFBundleShortVersionString</key>
        <string>1.0.0</string>
        <key>CFBundleIconFile</key>
        <string>icon.png</string>
        <key>CFBundleExecutable</key>
        <string>launcher</string>
    </dict>
    </plist>
    '''
    
    plist_path = app_dir / "Contents/Info.plist"
    with open(plist_path, 'w') as f:
        f.write(info_plist)
    
    # 创建requirements.txt
    requirements = '''
PyQt6>=6.4.0
GitPython>=3.1.30
pandas>=1.5.3
jinja2>=3.1.2
python-dateutil>=2.8.2
Pillow>=9.0.0
setuptools>=65.5.1
wheel>=0.38.4
'''
    
    with open(app_dir / "Contents/Resources/requirements.txt", 'w') as f:
        f.write(requirements)
    
    # 创建安装脚本
    install_script = '''#!/bin/bash
    echo "正在安装Git报告生成器..."
    
    # 检查Python3
    if ! command -v python3 &> /dev/null; then
        echo "未检测到Python3，请先安装Python3"
        exit 1
    fi
    
    # 创建虚拟环境
    echo "正在创建虚拟环境..."
    VENV_PATH="/Applications/Git报告生成器.app/Contents/Resources/venv"
    python3 -m venv "$VENV_PATH"
    
    # 激活虚拟环境并安装依赖
    echo "正在安装依赖..."
    source "$VENV_PATH/bin/activate"
    pip install --upgrade pip
    pip install -r "Git报告生成器.app/Contents/Resources/requirements.txt"
    deactivate
    
    # 修改启动脚本以使用虚拟环境
    echo "正在配置环境..."
    LAUNCHER="/Applications/Git报告生成器.app/Contents/MacOS/launcher"
    sed -i '' "s|python3|$VENV_PATH/bin/python|g" "$LAUNCHER"
    
    # 复制应用到Applications目录
    echo "正在安装应用..."
    cp -r "Git报告生成器.app" /Applications/
    
    # 设置权限
    echo "正在设置权限..."
    chmod -R 755 "/Applications/Git报告生成器.app"
    
    echo "安装完成！"
    '''
    
    with open(release_dir / "install.sh", 'w') as f:
        f.write(install_script)
    
    os.chmod(release_dir / "install.sh", 0o755)
    
    # 创建README
    readme = '''# Git报告生成器

## 安装说明

1. 解压下载的压缩包
2. 打开终端，进入解压目录
3. 执行安装脚本：
   ```bash
   sudo ./install.sh
   ```

## 使用方法

1. 从启动台或应用程序文件夹启动"Git报告生成器"
2. 选择Git仓库目录
3. 设置时间范围和筛选条件
4. 选择报告类型
5. 点击生成报告

## 系统要求

- macOS 10.10 或更高版本
- Python 3.7 或更高版本

## 支持

如有问题，请联系技术支持。
'''
    
    with open(release_dir / "README.md", 'w') as f:
        f.write(readme)
    
    # 创建压缩包
    shutil.make_archive("Git报告生成器", 'zip', release_dir)
    
    print("发布包已创建完成：Git报告生成器.zip")

if __name__ == "__main__":
    create_release_package() 