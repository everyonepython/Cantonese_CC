# coding=utf-8
import json
import time
import base64
from pathlib import Path

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QLineEdit, QMessageBox

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
        self.from_lang = 'yue'
        self.to_lang = 'cht'

        # 未登陸前禁止發出請求。
        self.start_pushButton.setDisabled(True)
        # 檢測是否以記住帳戶信息。
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

        # 選擇語言。
        self.yue2cht_radioButton.setChecked(True)
        self.yue2cht_radioButton.toggled.connect(self.ch_lang)
        self.yue2zh_radioButton.toggled.connect(self.ch_lang)
        self.zh2en_radioButton.toggled.connect(self.ch_lang)
        self.zh2en_radioButton.clicked.connect(self.ch_en_lang_alert)

        # 翻譯操作。
        self.openfile_pushButton.clicked.connect(self.openfile)
        self.start_pushButton.clicked.connect(self.start)
        # TODO: 拖放文件，獲取路徑。
        # self.openfile_pushButton.setAcceptDrops(True)

    def set_appid(self):
        self.appid = self.appid_lineEdit.text()

    def set_secretkey(self):
        self.secretkey = self.secretkey_lineEdit.text()

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
        p = Path('login_info')
        if p.exists():
            with open('login_info', 'rb') as f:
                b_info = f.read()
        else:  # Test Account
            from info import sharekey
            b_info = sharekey

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
            res = baidu_translate('呢個係登陸測試！', self.appid, self.secretkey, from_lang='yue')
            test_translation = res.get('trans_result')
            print(res)

            # 連續發起兩次請求。
            # 第一次請求，驗證帳號密鑰是否正確。
            if test_translation and i == 0:
                self.login_pushButton.setDisabled(True)   # 驗證成功後，不需要再次登陸。
                self.start_pushButton.setDisabled(False)  # 登陸後允許發出翻譯請求。
                self.appid_lineEdit.setDisabled(True)  # 登陸成功後禁止修改帳號密碼。
                self.secretkey_lineEdit.setDisabled(True)
                if self.remember_checkBox.isChecked():
                    self.remember_info()
                self.new_log('驗證成功！')
            # 第二次請求，驗證是否高級版 API，可以調整請求速度。
            elif test_translation and i == 1:
                self.is_premium = True
                self.log('API權限 - 高級版')
            # 錯誤代碼解釋。
            elif res.get('error_code') == '54003' and i == 1:
                self.log('API權限 - 普通版\n')
            elif res.get('error_code') == '52003':
                self.new_log('請檢查 appid 或 secretkey 是否正確。')
            # 其他錯誤代碼。
            else:
                print(res)
                self.new_log(json.dumps(res))

    def log(self, new_text):
        '''繼續打印日誌。'''
        old_text = self.logging_textBrowser.toPlainText()
        self.logging_textBrowser.setText('\n\n'.join([old_text, new_text]))

    def new_log(self, text):
        '''重新打印日誌。'''
        self.logging_textBrowser.setText(text)

    def ch_lang(self):
        '''更改翻譯語言。'''
        lang_radio_btn = self.sender()
        if lang_radio_btn.isChecked():
            # lang_radio_btn 的 accessibleName 的值在 UI 設計時已設定為:
            # <from_lang>-<to_lang> eg. 'yue-cht'
            self.from_lang, self.to_lang = lang_radio_btn.accessibleName().split('-')
            print(self.from_lang, self.to_lang)

    def ch_en_lang_alert(self):
        alert = QMessageBox()
        alert.setText('建議翻譯前將中文語句理順，可以提高翻譯質量。')
        alert.exec_()

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
        if len(self.appid) != 17 and len(self.secretkey) != 20:
            self.new_log('請檢查 appid 或 secretkey 是否正確。')
            return

        self.new_log('正在翻譯...')
        path = Path(self.filepath_label.text())
        if not path.is_file():
            self.new_log('請先選擇 SRT 文件。')
            return

        self.start_pushButton.setDisabled(True)
        try:
            trans_gen = translate_srt(path,
                                      appid=self.appid,
                                      secretkey=self.secretkey,
                                      is_premium=self.is_premium,
                                      from_lang=self.from_lang,
                                      to_lang=self.to_lang)  # 生成器用於進度條。

        except Exception as e:
            print(e)
            self.new_log(e)

        else:
            maximum = trans_gen.send(None)   # 第一個返回的是 total_count 總字數。
            self.progress_label.setText(f'共 {maximum} 字')
            self.trans_progressBar.setMaximum(maximum)

            # 之後返回值 count 是已經處理的字數。
            for value in trans_gen:
                if type(value) == int:
                    step = maximum - value
                    self.trans_progressBar.setValue(step)
                    self.progress_label.setText(f'已翻譯 {step} / {maximum} 字')
                else:
                    # 生成器最後一個返回值是路徑，是字符串，有且只有這個返回值是字符串。
                    new_path = value
                    self.new_log(f'翻譯文件路徑： {new_path}')

            # 日誌。

            # 提醒。
            alert = QMessageBox()
            alert.setText('翻譯完成！')
            alert.exec_()

            # 清空路徑，以免重複提交翻譯。
            self.filepath_label.setText('')

        finally:
            self.trans_progressBar.setValue(0)
            self.start_pushButton.setDisabled(False)
