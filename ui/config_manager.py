"""
这个模块提供了配置管理功能，主要用于获取和更新应用程序的配置信息。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2024, hxz393. 保留所有权利。
"""

import copy
import logging
from typing import Dict, Optional, Any

from PyQt5.QtCore import QObject, pyqtSignal

from config.settings import CONFIG_PATH, DEFAULT_CONFIG
from lib.read_json import read_json
from lib.write_json import write_json

logger = logging.getLogger(__name__)


class ConfigManager(QObject):
    """
    配置管理器类，负责管理和更新应用程序的配置信息。

    :ivar config_updated: 当主配置更新时发出的信号。
    """
    config_updated = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.load_config()

    def load_config(self) -> None:
        """
        载入配置。

        :return: 无返回值。
        """
        self._config = read_json(CONFIG_PATH) or DEFAULT_CONFIG

    def get_config(self) -> Optional[Dict[str, Any]]:
        """
        获取配置副本。

        :return: 包含配置的字典副本，如果出现错误则返回 None。
        """
        try:
            return copy.deepcopy(self._config)
        except Exception:
            logger.exception(f"Failed to get config")
            return None

    def update_config(self, new_config: Dict[str, Any]) -> None:
        """
        更新配置。

        :param new_config: 新的配置。
        :return: 无
        """
        try:
            write_json(CONFIG_PATH, new_config)
            # 重载配置，发送更新信号
            self.load_config()
            self.config_updated.emit()
            logger.info(f"Config updated")
        except Exception:
            logger.exception(f"Failed to update config")
