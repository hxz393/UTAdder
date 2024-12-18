"""
UI 相关函数
为了方便导入，在 ui/__init__.py 中导入了所有的 UI 相关类和函数，这样在其他模块中就可以直接导入 ui 模块，而不需要导入 ui 中的每个类和函数。
"""
from .lang_manager import LangManager
from .config_manager import ConfigManager
from .status_bar import StatusBar
from .main_widget import MainWidget
from .action_setup import ActionSetup
from .action_add import ActionAdd
