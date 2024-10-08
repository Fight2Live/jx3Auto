import sys
from PyQt5.QtWidgets import QApplication

from service.index import AutoStandPlatform


def quit(app, ex):
    ex.quit()
    app.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AutoStandPlatform()
    ex.setWindowTitle("小小脚本")
    ex.show()
    sys.exit(app.exec_())