"""
获取资源的绝对路径。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2024, hxz393。保留所有权利。
"""
import logging
import os
import sys
from typing import Union, Optional

logger = logging.getLogger(__name__)


def get_resource_path(relative_path: Union[str, os.PathLike]) -> Optional[str]:
    """
    指定资源的相对路径，返回其绝对路径。

    :param relative_path: 相对路径，可以是字符串或 os.PathLike 对象。
    :return: 资源的绝对路径，如果发生错误则返回 None。
    """

    try:
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        return os.path.join(base_path, os.path.normpath(relative_path))
    except Exception:
        logger.exception("An error occurred while retrieving resource path")
        return None
