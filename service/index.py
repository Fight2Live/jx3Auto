import os
import sys
import datetime
import service.JX3Operate as jx3
import config.global_var as gv

from utils import windows_operate
from PyQt5.QtWidgets import *


TASK_LIST = []

class AutoStandPlatform(QWidget):
    def __init__(self, parent=None):
        super(AutoStandPlatform, self).__init__(parent)

        self.mainGrid = QGridLayout()

        self.init_data()
        self.init_main_layout()

        self.setLayout(self.mainGrid)

    def init_data(self):
        """
        初始化数据
        :return:
        """
        gv._init()
        gv.set_value('EXECUTING', False)
        windows_operate.refresh_windows_hwnd_dict()
        self._executing = False  # true - 正在执行


    def init_main_layout(self):
        """
        初始化主界面
        :return:
        """

        # 窗口选择
        windowsSelectLabel = QLabel("目标窗口")
        self.windowsSelect = QComboBox()
        for h, t in windows_operate.windows_hwnd_dict.items():
            if "剑网3" in t:
                self.windowsSelect.addItem(t, h)
        self.windowsSelectRefresh = QPushButton("刷新")

        # 功能区域
        functionAreaLabel = QLabel("功能选择")
        startArtBtn = QPushButton("艺人")
        startAnimalBtn = QPushButton("御兽（施工中）")

        # 执行情况
        self.executingName = QLabel("正在执行：XX")
        self.lastExcuteInfoLabel = QLabel("开始时间：----- --:--")
        stopExcuteBtn = QPushButton("停止")

        # 窗口选择
        self.mainGrid.addWidget(windowsSelectLabel, 0, 0)
        self.mainGrid.addWidget(self.windowsSelect, 0, 1)
        self.mainGrid.addWidget(self.windowsSelectRefresh, 0, 2)

        # 功能区域
        self.mainGrid.addWidget(functionAreaLabel, 1, 0)
        self.mainGrid.addWidget(startArtBtn, 2, 0)
        self.mainGrid.addWidget(startAnimalBtn, 3, 0)

        # 执行情况
        self.mainGrid.addWidget(self.executingName, 1, 1)
        self.mainGrid.addWidget(self.lastExcuteInfoLabel, 2, 1)
        self.mainGrid.addWidget(stopExcuteBtn, 2, 2)

        # self.windowsSelectRefresh.clicked.connect(windows_operate.refresh_windows_hwnd_dict)
        startArtBtn.clicked.connect(self.startArtMet)
        stopExcuteBtn.clicked.connect(self.stopTask)

    def startArtMet(self):
        if gv.get_value("EXECUTING"):
            QMessageBox.warning(self, "提示", "已有正在执行的任务，请先停止", QMessageBox.Yes)
        else:
            gv.set_value('EXECUTING', True)
            t = jx3.JX3Operate(self.windowsSelect.currentData(), 1)
            t.start()
            TASK_LIST.append(t)
            self.executingName.setText(f'正在执行: 艺人')
            self.lastExcuteInfoLabel.setText(f'开始时间: {datetime.datetime.now().strftime("%m-%d %H:%M")}')

    def stopTask(self):
        gv.set_value('EXECUTING', False)
        TASK_LIST[0].join()
        TASK_LIST.pop(0)
        self.executingName.setText(f'正在执行: 无')
        self.lastExcuteInfoLabel.setText(f'开始时间: ----- --:--')

    def quit(self):
        gv.set_value('EXECUTING', False)
        TASK_LIST[0].join()

    def closeEvent(self, event):
        """
        对MainWindow的函数closeEvent进行重构
        退出软件时结束所有进程
        """

        reply = QMessageBox.question(self, '提示', "确认退出吗？", QMessageBox.Yes | QMessageBox.No,
                                               QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            # 用过sys.exit(0)和sys.exit(app.exec_())，但没起效果
            os._exit(0)
        else:
            event.ignore()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AutoStandPlatform()
    ex.show()
    sys.exit(app.exec_())