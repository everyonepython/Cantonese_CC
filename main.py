# coding=utf-8
import sys

from PyQt5.QtWidgets import QApplication

from call_mainwindow import MyMainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
