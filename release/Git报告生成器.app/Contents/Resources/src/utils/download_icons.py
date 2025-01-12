import requests
import os

def download_icon(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(f'assets/{filename}', 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
    else:
        print(f"Failed to download {filename}")

# 创建assets目录
os.makedirs('assets', exist_ok=True)

# 从Icons8下载免费图标
icons = {
    'folder.png': 'https://img.icons8.com/fluency/96/folder-invoices.png',
    'report.png': 'https://img.icons8.com/fluency/96/business-report.png',
    'preview.png': 'https://img.icons8.com/fluency/96/preview-pane.png',
    'reset.png': 'https://img.icons8.com/fluency/96/recurring-appointment.png'
}

for filename, url in icons.items():
    download_icon(url, filename)

# 创建启动画面
splash_html = '''
<html>
<head>
<style>
body {
    margin: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background: linear-gradient(45deg, #2193b0, #6dd5ed);
    font-family: Arial, sans-serif;
}
.container {
    text-align: center;
    color: white;
    padding: 40px;
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
}
h1 {
    font-size: 36px;
    margin-bottom: 10px;
}
p {
    font-size: 18px;
    opacity: 0.8;
}
</style>
</head>
<body>
    <div class="container">
        <h1>Git提交记录分析器</h1>
        <p>正在启动...</p>
    </div>
</body>
</html>
'''

# 使用wkhtmltoimage将HTML转换为启动画面图片
with open('assets/splash.html', 'w', encoding='utf-8') as f:
    f.write(splash_html)

print("\n请按照以下步骤完成图标准备：")
print("\n1. 安装wkhtmltopdf（用于生成启动画面）：")
print("   brew install wkhtmltopdf")
print("\n2. 生成启动画面：")
print("   wkhtmltoimage --width 800 --height 400 assets/splash.html assets/splash.png")
print("\n3. 准备应用图标：")
print("   a. 下载一个1024x1024的PNG图标")
print("   b. 将其命名为icon_1024.png并放在项目根目录")
print("   c. 运行icon_generator.sh脚本生成图标集")
print("   d. 运行以下命令生成.icns文件：")
print("      iconutil -c icns MyIcon.iconset -o assets/icon.icns") 