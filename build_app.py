from src.utils.create_default_icons import create_all_icons
from src.utils.build_release import create_release_package
import os

def ensure_directory_structure():
    # 确保必要的目录结构存在
    directories = [
        'src/assets',
        'src/gui',
        'src/core',
        'src/utils'
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

if __name__ == "__main__":
    # 确保目录结构存在
    ensure_directory_structure()
    
    # 创建图标
    create_all_icons()
    
    # 创建发布包
    create_release_package()
    
    print("构建完成！") 