# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 427)
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.appid_label = QtWidgets.QLabel(self.centralwidget)
        self.appid_label.setGeometry(QtCore.QRect(48, 29, 34, 16))
        self.appid_label.setWhatsThis("")
        self.appid_label.setObjectName("appid_label")
        self.remember_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.remember_checkBox.setGeometry(QtCore.QRect(465, 56, 161, 20))
        self.remember_checkBox.setObjectName("remember_checkBox")
        self.secretkey_label = QtWidgets.QLabel(self.centralwidget)
        self.secretkey_label.setGeometry(QtCore.QRect(48, 53, 61, 16))
        self.secretkey_label.setWhatsThis("")
        self.secretkey_label.setObjectName("secretkey_label")
        self.openfile_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.openfile_pushButton.setGeometry(QtCore.QRect(160, 90, 311, 111))
        self.openfile_pushButton.setObjectName("openfile_pushButton")
        self.file_label = QtWidgets.QLabel(self.centralwidget)
        self.file_label.setGeometry(QtCore.QRect(11, 211, 81, 20))
        self.file_label.setObjectName("file_label")
        self.filepath_label = QtWidgets.QLabel(self.centralwidget)
        self.filepath_label.setGeometry(QtCore.QRect(100, 211, 501, 20))
        self.filepath_label.setText("")
        self.filepath_label.setObjectName("filepath_label")
        self.trans_progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.trans_progressBar.setGeometry(QtCore.QRect(0, 240, 641, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trans_progressBar.sizePolicy().hasHeightForWidth())
        self.trans_progressBar.setSizePolicy(sizePolicy)
        self.trans_progressBar.setProperty("value", 0)
        self.trans_progressBar.setObjectName("trans_progressBar")
        self.logging_textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.logging_textBrowser.setGeometry(QtCore.QRect(0, 291, 641, 111))
        self.logging_textBrowser.setObjectName("logging_textBrowser")
        self.logging_label = QtWidgets.QLabel(self.centralwidget)
        self.logging_label.setGeometry(QtCore.QRect(30, 270, 41, 16))
        self.logging_label.setObjectName("logging_label")
        self.yue2chs_radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.yue2chs_radioButton.setGeometry(QtCore.QRect(30, 96, 101, 20))
        self.yue2chs_radioButton.setObjectName("yue2chs_radioButton")
        self.yue2cht_radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.yue2cht_radioButton.setGeometry(QtCore.QRect(30, 122, 121, 20))
        self.yue2cht_radioButton.setObjectName("yue2cht_radioButton")
        self.zh2en_radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.zh2en_radioButton.setGeometry(QtCore.QRect(30, 172, 121, 20))
        self.zh2en_radioButton.setObjectName("zh2en_radioButton")
        self.chs2cht_radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.chs2cht_radioButton.setGeometry(QtCore.QRect(30, 147, 121, 20))
        self.chs2cht_radioButton.setObjectName("chs2cht_radioButton")
        self.start_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.start_pushButton.setGeometry(QtCore.QRect(487, 160, 131, 31))
        self.start_pushButton.setObjectName("start_pushButton")
        self.login_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.login_pushButton.setGeometry(QtCore.QRect(460, 23, 131, 32))
        self.login_pushButton.setObjectName("login_pushButton")
        self.secretkey_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.secretkey_lineEdit.setGeometry(QtCore.QRect(124, 53, 301, 21))
        self.secretkey_lineEdit.setObjectName("secretkey_lineEdit")
        self.appid_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.appid_lineEdit.setGeometry(QtCore.QRect(124, 30, 301, 21))
        self.appid_lineEdit.setObjectName("appid_lineEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Translate spoken Cantonese to written Chinese"))
        self.appid_label.setText(_translate("MainWindow", "appid"))
        self.remember_checkBox.setText(_translate("MainWindow", "Remember Login"))
        self.secretkey_label.setText(_translate("MainWindow", "secretKey"))
        self.openfile_pushButton.setText(_translate("MainWindow", "Open File"))
        self.file_label.setText(_translate("MainWindow", "File Location"))
        self.logging_textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.SF NS Text\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This is an application to translate spoken Cantonese text to written Chinese text for SRT files using Baidu translation API.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">進行中英翻譯前，建議先將中文文本修改成更通順的語句，可以提高翻譯質量。</p></body></html>"))
        self.logging_label.setText(_translate("MainWindow", "Log"))
        self.yue2chs_radioButton.setText(_translate("MainWindow", "粵語->简体"))
        self.yue2cht_radioButton.setText(_translate("MainWindow", "粵語->繁體"))
        self.zh2en_radioButton.setText(_translate("MainWindow", "中文->英文"))
        self.chs2cht_radioButton.setText(_translate("MainWindow", "简体->繁體"))
        self.start_pushButton.setText(_translate("MainWindow", "START"))
        self.login_pushButton.setText(_translate("MainWindow", "Login"))
