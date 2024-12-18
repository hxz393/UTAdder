"""
批量添加动作，连接 UI 和逻辑。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2024, hxz393. 保留所有权利。
"""

import logging
import os

from PyQt5.QtCore import pyqtSignal, QThread

from lib.add_to_ut import add_to_ut
from ui.config_manager import ConfigManager
from ui.lang_manager import LangManager

logger = logging.getLogger(__name__)


class ActionAdd(QThread):
    """
    退出动作的类。

    :param lang_manager: 语言管理器，用于更新动作的显示语言。
    :param config_manager: 配置管理器，用于读取和修改设置。
    :param sub_dir: 设置此批种子储存文件夹。
    """
    initialize_signal = pyqtSignal()
    finalize_signal = pyqtSignal()
    status_updated = pyqtSignal(str)

    def __init__(self,
                 lang_manager: LangManager,
                 config_manager: ConfigManager,
                 sub_dir: str):
        super().__init__()
        self.lang_manager = lang_manager
        self.lang = self.lang_manager.get_lang()
        self.config_manager = config_manager
        self.config = self.config_manager.get_config()
        # 拼接设置中的下载根目录目录和用户输入保存目录名
        self.config['save_path'] = os.path.join(self.config['save_path'], sub_dir)

    def run(self) -> None:
        """
        线程执行方法。

        :return: 无返回值。
        """
        try:
            # 开始初始化准备工作
            self.initialize_signal.emit()
            self.status_updated.emit(self.lang['ui.action_add_1'])
            # 开始执行批量添加
            result = add_to_ut(self.config)
            if not result:
                self.status_updated.emit(self.lang['ui.action_add_2'])
                return
            # 收尾工作
            self.status_updated.emit(f"{result} {self.lang['ui.action_add_3']}")
        except Exception:
            logger.exception('Error during running')
            self.status_updated.emit(self.lang['label_status_error'])
        finally:
            self.finalize_signal.emit()
