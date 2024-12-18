"""
此文件定义了 MainTable 类，一个基于 PyQt5 的 QTableWidget 的高级实现。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, QLabel

from config.settings import GITHUB_URL
from ui.action_add import ActionAdd
from ui.action_setup import ActionSetup
from ui.config_manager import ConfigManager
from ui.lang_manager import LangManager
from lib.get_resource_path import get_resource_path

logger = logging.getLogger(__name__)


class MainWidget(QWidget):
    """
    主功能类，用于展示输入框和按钮。

    :param lang_manager: 用于管理界面语言的 LangManager 实例。
    :param config_manager: 用于管理配置的 ConfigManager 实例。
    """
    status_updated = pyqtSignal(str)

    def __init__(self,
                 lang_manager: LangManager,
                 config_manager: ConfigManager):
        super().__init__()
        # 接受更新信号，更新语言和配置
        self.lang_manager = lang_manager
        self.lang_manager.lang_updated.connect(self.update_lang)
        self.config_manager = config_manager

        self.init_ui()
        self.update_lang()

    def update_lang(self) -> None:
        """
        更新界面语言设置。

        :return: 无返回值。
        """
        self.lang = self.lang_manager.get_lang()
        self.label.setText(f"<b>{self.lang['main_2']}</b>")
        self.btn_set.setText(self.lang['main_3'])
        self.btn_add.setText(self.lang['main_4'])

    def init_ui(self) -> None:
        """
        初始化用户界面。

        :return: 无返回值。
        """
        # 第一行：标签 + 输入框
        self.label = QLabel(self)
        self.line_edit = QLineEdit(self)

        h_layout_top = QHBoxLayout()
        h_layout_top.addWidget(self.label)
        h_layout_top.addWidget(self.line_edit)

        # 第二行：设置 + 添加按钮
        self.btn_set = QPushButton(self)
        self.btn_set.clicked.connect(self.on_set_clicked)
        self.btn_set.setIcon(QIcon(get_resource_path('media/icons8-setup-30.png')))
        self.btn_add = QPushButton(self)
        self.btn_add.clicked.connect(self.on_add_clicked)
        self.btn_add.setIcon(QIcon(get_resource_path('media/icons8-add-30.png')))
        # 添加帮助按钮
        help_label = QLabel(f"<a href='{GITHUB_URL}'>?</a>")
        help_label.setOpenExternalLinks(True)

        h_layout_bottom = QHBoxLayout()
        h_layout_bottom.addWidget(self.btn_set)
        h_layout_bottom.addWidget(self.btn_add)
        h_layout_bottom.addWidget(help_label)

        # 整体布局
        main_layout = QVBoxLayout()
        main_layout.addLayout(h_layout_top)
        main_layout.addLayout(h_layout_bottom)

        self.setLayout(main_layout)

    def on_set_clicked(self) -> None:
        """
        点击设置按钮时，打开设置窗口。

        :return: 无返回值。
        """
        self.actionSetup = ActionSetup(self.lang_manager, self.config_manager)
        self.actionSetup.status_updated.connect(self.forward_status)
        self.actionSetup.open_dialog()

    def on_add_clicked(self) -> None:
        """
        点击添加按钮时，在新线程执行添加操作。

        :return: 无返回值。
        """
        self.sub_dir = self.line_edit.text()
        self.actionAdd = ActionAdd(self.lang_manager, self.config_manager, self.sub_dir)
        self.actionAdd.status_updated.connect(self.forward_status)
        self.actionAdd.initialize_signal.connect(self.initialize)
        self.actionAdd.finalize_signal.connect(self.finalize)
        self.actionAdd.start()

    def initialize(self) -> None:
        """
        初始化界面和状态，在开始操作前执行。

        :return: 无返回值。
        """
        logger.info('Start running')
        # 按钮不可点击
        self.btn_add.setEnabled(False)
        self.btn_set.setEnabled(False)

    def finalize(self) -> None:
        """
        完成后的收尾工作。

        :return: 无返回值。
        """
        # 启用按钮
        self.btn_add.setEnabled(True)
        self.btn_set.setEnabled(True)
        self.line_edit.setText("")
        logger.info('Done')

    def forward_status(self, message: str) -> None:
        """
        用于转发状态信号。

        :param message: 要转发的消息。
        :return: 无返回值。
        """
        self.status_updated.emit(message)
