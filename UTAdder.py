"""
uTorrent 批量添加种子工具。一键添加指定目录下种子文件，指定下载储存目录。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2024, hxz393. 保留所有权利。
"""

import logging
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget

from config.settings import CONFIG_PATH, DEFAULT_CONFIG, PROGRAM_NAME, VERSION_INFO
from lib.logging_config import logging_config
from lib.write_json import write_json
from lib.hide_console import hide_console
from lib.get_resource_path import get_resource_path
from ui import LangManager, ConfigManager, StatusBar, MainWidget

logger = logging.getLogger(__name__)


class UTAdder(QMainWindow):
    """
    主窗口类，UI 逻辑分离。
    """

    def __init__(self):
        super().__init__()
        # 初始化配置文件
        self.init_config()
        self.lang_manager = LangManager()
        self.config_manager = ConfigManager()
        self.init_ui()

    @staticmethod
    def init_config() -> None:
        """
        检查并初始化配置文件，配置文件若不存在，创建写入默认配置。

        :return: 无返回值。
        """
        try:
            if not os.path.isfile(CONFIG_PATH):
                write_json(CONFIG_PATH, DEFAULT_CONFIG)
        except Exception:
            logger.exception("Failed to initialize configuration")

    def init_ui(self) -> None:
        """
        初始化用户界面组件。

        :return: 无返回值。
        """
        # 创建状态栏
        self.status_bar = StatusBar(self.lang_manager)
        # 创建组件
        self.main_widget = MainWidget(self.lang_manager, self.config_manager)
        # 连接信号槽
        self.main_widget.status_updated.connect(self.status_bar.show_message)
        # 主窗口配置
        self._configure_main_window()

    def _configure_main_window(self) -> None:
        """
        配置主窗口的基本属性。

        :return: 无返回值。
        """
        # 设置窗口标志，只保留关闭按钮，无最小化和最大化
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle(f"{PROGRAM_NAME} {VERSION_INFO}")
        # 创建垂直布局，加入组件
        self.setStatusBar(self.status_bar)
        self.main_area = QVBoxLayout()
        self.main_area.addWidget(self.main_widget)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_area)
        self.central_widget.layout().setContentsMargins(0, 0, 0, 0)
        self.setWindowIcon(QIcon(get_resource_path('media/main.ico')))
        self.setCentralWidget(self.central_widget)
        # 调整到最小可用尺寸，然后固定为该尺寸
        self.resize(self.minimumSizeHint())
        self.setFixedSize(self.minimumSizeHint())
        # 展示主窗口
        self.show()


if __name__ == "__main__":
    hide_console()
    logging_config(console_output=True, max_log_size=1, log_level='INFO')
    app = QApplication(sys.argv)
    _ = UTAdder()
    sys.exit(app.exec_())
