"""
在 Windows 系统下隐藏控制台窗口功能。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import ctypes


def hide_console(hide: bool = True) -> None:
    """
    隐藏当前运行的控制台窗口。

    :param hide: 隐藏开关，默认为 True。
    :return: 无返回值。
    """
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')
    hWnd = kernel32.GetConsoleWindow()
    if hWnd and hide:
        # 0 表示 SW_HIDE
        user32.ShowWindow(hWnd, 0)
