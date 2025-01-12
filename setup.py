from setuptools import setup

APP = ['src/main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['PyQt6', 'git', 'pandas', 'jinja2'],
    'iconfile': 'assets/icon.icns',  # 应用程序图标
    'plist': {
        'CFBundleName': 'Git报告生成器',
        'CFBundleDisplayName': 'Git报告生成器',
        'CFBundleIdentifier': 'com.gitreport.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'LSMinimumSystemVersion': '10.10',
    }
}

setup(
    name='Git报告生成器',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
) 