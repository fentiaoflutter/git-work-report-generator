from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, text, filename):
    # 创建一个新的图片
    img = Image.new('RGB', (size, size), color='#2193b0')
    d = ImageDraw.Draw(img)
    
    # 添加文字
    font_size = size // 4
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        font = ImageFont.load_default()
    
    # 计算文字位置使其居中
    text_bbox = d.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    # 绘制文字
    d.text((x, y), text, fill='white', font=font)
    
    # 保存图片
    img.save(filename)

def create_all_icons():
    # 确保assets目录存在
    os.makedirs('src/assets', exist_ok=True)
    
    # 创建各种图标
    icons = {
        'folder.png': 'F',
        'report.png': 'R',
        'preview.png': 'P',
        'reset.png': 'X',
        'splash.png': 'Git报告生成器',
        'icon.png': 'G'
    }
    
    for filename, text in icons.items():
        size = 800 if filename == 'splash.png' else 96
        create_icon(size, text, f'src/assets/{filename}')
    
    print("图标创建完成！")

if __name__ == "__main__":
    create_all_icons() 