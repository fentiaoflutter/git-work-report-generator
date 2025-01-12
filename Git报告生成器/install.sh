#!/bin/bash
    echo "正在安装Git报告生成器..."
    
    # 检查Python3
    if ! command -v python3 &> /dev/null; then
        echo "未检测到Python3，请先安装Python3"
        exit 1
    fi
    
    # 安装依赖
    echo "正在安装依赖..."
    python3 -m pip install -r "Git报告生成器.app/Contents/Resources/requirements.txt"
    
    # 复制应用到Applications目录
    echo "正在安装应用..."
    cp -r "Git报告生成器.app" /Applications/
    
    echo "安装完成！"
    