"""
全局静态变量
"""
# 程序信息
PROGRAM_NAME = 'UTAdder'
VERSION_INFO = 'v1.0.0'
AUTHOR_NAME = 'assassing'
CONTACT_MAIL = 'hxz393@gmail.com'
WEBSITE_URL = 'https://blog.x2b.net'
GITHUB_PROFILE = 'https://github.com/hxz393'
GITHUB_URL = 'https://github.com/hxz393/UTAdder'

# 配置路径
CONFIG_PATH = 'config/config.json'
# 默认配置
DEFAULT_CONFIG = {
    'lang': 'English',  # 语言选项 en cn
    'ut_path': 'utorrent.exe',  # ut 主程序路径
    'save_path': '',  # 任务保存路径
    'torrent_path': '',  # 载入种子路径
}
# 用户输入检查正则。不检查
REGEX_INVALID = r'<>:"/\\|?*'
