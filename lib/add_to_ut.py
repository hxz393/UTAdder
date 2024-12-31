"""
批量添加种子。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2024, hxz393. 保留所有权利。
"""

import logging
import os
import shutil
import subprocess
from typing import Dict, Optional

logger = logging.getLogger(__name__)


def add_to_ut(config: Dict[str, str]) -> Optional[int]:
    """
    执行添加操作并返回结果。

    :param config: 主要配置参数。
    :return: 成功返回添加数量，否则返回 0。
    """
    ut_path = config['ut_path']
    save_path = config['save_path']
    torrent_path = config['torrent_path']
    pick_torrent_name = config['pick_torrent_name']
    added_path = os.path.join(torrent_path, "added")
    added = 0
    try:
        if not os.path.exists(added_path):
            os.makedirs(added_path)

        # 列出目录下所有文件和目录
        for item in os.listdir(torrent_path):
            # 分割文件名
            torrent_name, ext = os.path.splitext(item)
            # 构造完整路径
            full_path = os.path.join(torrent_path, item)
            # 检查是否是文件并以 .torrent 结尾
            if os.path.isfile(full_path) and ext == '.torrent':
                # 先移动到完成目录再添加
                shutil.move(full_path, added_path)
                add_path = os.path.join(added_path, item)
                save_path = f"{save_path}/{torrent_name}" if pick_torrent_name else save_path
                logger.info(add_path)
                subprocess.run([ut_path, "/DIRECTORY", save_path, add_path], capture_output=True, text=True)
                added += 1
        # 也可以一次性添加，torrent_paths 为所有种子路径列表
        # subprocess.run([ut_path, "/DIRECTORY", save_path]+torrent_paths, capture_output=True, text=True)
        return added
    except Exception:
        logger.exception("Exception occurred")
        return None
