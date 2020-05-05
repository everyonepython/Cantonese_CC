# coding=utf-8
import json
import time
import base64
from pathlib import Path

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QLineEdit

from ui_mainwindow import Ui_MainWindow
from translate import baidu_translate
from translate_file import translate_srt


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.appid = ''
        self.secretkey = ''
        self.is_premium = False

        # 檢測是否以記住帳戶信息。
        p = Path('login_info')
        if p.exists():
            self.remember_checkBox.setChecked(True)
            self.get_info()
            self.login()

        # 帳戶信息。
        self.appid_lineEdit.textChanged.connect(self.set_appid)
        self.secretkey_lineEdit.textChanged.connect(self.set_secretkey)
        self.secretkey_lineEdit.setEchoMode(QLineEdit.Password)

        # 登陸操作。
        self.login_pushButton.clicked.connect(self.login)
        self.remember_checkBox.toggled.connect(self.del_info)

        # 翻譯操作。
        self.openfile_pushButton.clicked.connect(self.openfile)
        self.start_pushButton.clicked.connect(self.start)
        # TODO: 拖放文件，獲取路徑。
        # self.openfile_pushButton.setAcceptDrops(True)

    def set_appid(self):
        self.appid = self.appid_lineEdit.text()
        print(f'appid {self.appid}')

    def set_secretkey(self):
        self.secretkey = self.secretkey_lineEdit.text()
        print(f'secretkey {self.secretkey}')

    def remember_info(self):
        with open('login_info', 'wb') as f:
            info = base64.b64encode(f'{self.appid}-{self.secretkey}'.encode('utf8'))
            f.write(info)

    def del_info(self):
        p = Path('login_info')
        if not self.remember_checkBox.isChecked() and p.exists():
            p.unlink()
        self.appid_lineEdit.setDisabled(False)
        self.secretkey_lineEdit.setDisabled(False)
        self.login_pushButton.setDisabled(False)

    def get_info(self):
        with open('login_info', 'rb') as f:
            b_info = f.read()
            info = base64.b64decode(b_info).decode('utf8')
            self.appid, self.secretkey = info.split('-')
            self.appid_lineEdit.setText(self.appid)
            self.secretkey_lineEdit.setText(self.secretkey)

    def login(self):
        '''
        模擬登陸。
        測試 appid 及 secretKey 是否合法，是否高級帳戶。
        記錄用戶是否記住帳戶信息。
        '''
        test_translation = ''
        for i in range(2):
            res = baidu_translate('呢個係登陸測試！', appid=self.appid, secretkey=self.secretkey)
            test_translation = res.get('trans_result')
            print(res)

            # 連續發起兩次請求，第二次驗證是否高級版。
            # 第一次請求。
            if test_translation and i == 0:
                self.login_pushButton.setDisabled(True)
                if self.remember_checkBox.isChecked():
                    self.remember_info()
                    self.appid_lineEdit.setDisabled(True)
                    self.secretkey_lineEdit.setDisabled(True)
                self.log('驗證成功！')
            # 第二次請求。
            elif test_translation and i == 1:
                self.is_premium = True
                self.log('API權限 - 高級版')
            elif res.get('code') == '45003' and i == 1:
                self.log('API權限 - 普通版\n')
            else:
                print(res)
                self.log(json.dumps(res))

    def log(self, new_text):
        '''繼續打印日誌。'''
        old_text = self.logging_textBrowser.toPlainText()
        self.logging_textBrowser.setText('\n\n'.join([old_text, new_text]))

    def new_log(self, text):
        '''重新打印日誌。'''
        self.logging_textBrowser.setText(text)

    def openfile(self):
        '''獲取文件路徑。'''
        filename, filetype = QFileDialog.getOpenFileName(self,
                                                         'Choose a file',
                                                         './',
                                                         'SRT File (*.srt)')
        print(filename, filetype)
        self.filepath_label.setText(filename)
        return filename

    def start(self):
        '''獲取翻譯並生成 srt 翻譯文件。'''
        path = Path(self.filepath_label.text())
        if not path.is_file():
            self.new_log('請先選擇 SRT 文件。')
            return

        self.start_pushButton.setDisabled(True)
        try:
            # TODO: 選擇語言。
            trans_gen = translate_srt(path, is_premium=self.is_premium)  # 生成器用於進度條。

            maximum = trans_gen.send(None)   # 第一個返回的是 total_count 總字數。
            self.trans_progressBar.setMaximum(maximum)

            new_path = ''
            # 之後返回值 count 是已經處理的字數。
            for count in trans_gen:
                self.trans_progressBar.setValue(count)

            self.new_log('翻譯完成！')
            self.log(f'文件路徑：{Path(new_path + "_translated.srt").absolute().__str__()}')
            self.start_pushButton.setDisabled(False)
        except Exception as e:
            print(e)

