from PyQt5 import QtCore,QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget
import sys
import requests
import time
from lxml import etree
import re
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
import threading
Tlock = threading.Lock()

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(832, 522)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 1, 0, 1, 4)
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 3, 3, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 3, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 3, 0, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 3, 2, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "luvm的招聘信息软件_彭迪"))
        Form.setWindowIcon(QIcon('ico.ico'))
        self.pushButton_3.setText(_translate("Form", "华科就业网招聘信息"))
        self.pushButton.setText(_translate("Form", "华科就业网招聘会"))
        self.pushButton_2.setText(_translate("Form", "武汉理工就业网招聘会"))
        self.pushButton_4.setText(_translate("Form", "武汉理工就业网招聘信息"))

class mwindow(QWidget, Ui_Form):
    def __init__(self):
        super(mwindow, self).__init__()
        self.setupUi(self)

    def whut_meeting(self):
        self.textBrowser.setText('武汉理工就业网未来几天招聘会信息:')
        self.textBrowser.append("-" * 60)
        executor = ThreadPoolExecutor(max_workers=10)
        for i in range(1,11):
            executor.submit(self.whut_meeting_more, i)
        executor.shutdown(wait=True)

    def whut_meeting_more(self,i):
        Tlock.acquire()
        whut_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }
        res = requests.get('http://scc.whut.edu.cn/meetList.shtml?date=&searchForm=&pageNow={}'.format(i), headers=whut_headers)
        html = res.content
        parseHtml = etree.HTML(html)
        conts = parseHtml.xpath('/html/body/div[3]/div[2]/ul/li')
        for cont in conts:
            name = cont.xpath('./a/text()')[0].strip()
            place = cont.xpath('./span[2]/text()')[0].strip()
            time_ = cont.xpath('./span[1]/text()')[0].strip()
            url = 'http://scc.whut.edu.cn/' + cont.xpath('./a/@href')[0].strip()
            self.textBrowser.append(name + ' ' + place + ' ' + time_)
            self.textBrowser.append(url)
            self.textBrowser.append('-' * 30)
        self.textBrowser.append("-" * 60)
        Tlock.release()

    def hust_meeting(self):
        self.textBrowser.setText('华科就业网未来几天招聘会信息:')
        self.textBrowser.append("-" * 60)
        executor = ThreadPoolExecutor(max_workers=10)
        for i in range(1,11):
            executor.submit(self.hust_meeting_more, i)
        executor.shutdown(wait=True)

    def hust_meeting_more(self,i):
        Tlock.acquire()
        hust_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }
        res = requests.get('http://job.hust.edu.cn/searchJob_{}.jspx?type=0&fbsj=0'.format(i), headers=hust_headers)
        html = res.text
        names = re.findall('title="(.*?)"', html)
        urls = re.findall('href="(.*?) title="', html)
        time_s = re.findall('<span>(\d*-\d*-\d* \d*:\d* )</span>', html)
        places = re.findall(r'<span>([\u4e00-\u9fa5]+[A-Z]*[\u4e00-\u9fa5]*[0-9]*[\u4e00-\u9fa5]*)</span>', html)[
                 :-2]
        for n, name in enumerate(names):
            self.textBrowser.append(name + ' ' + time_s[n] + ' ' + places[n])
            self.textBrowser.append('http://job.hust.edu.cn/' + urls[n][:-1])
            self.textBrowser.append('-' * 30)
        self.textBrowser.append('-' * 60)
        Tlock.release()

    def whut_job(self):
        self.textBrowser.setText('武汉理工就业网最近几天发布的招聘信息:')
        self.textBrowser.append('-'*60)
        executor = ThreadPoolExecutor(max_workers=10)
        for i in range(1, 11):
            executor.submit(self.whut_job_more, i)
        executor.shutdown(wait=True)

    def whut_job_more(self,i):
        Tlock.acquire()
        whut_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }
        url = 'http://scc.whut.edu.cn/infoList.shtml?tid=1001&searchForm=&pageNow={}'.format(i)
        res = requests.get(url, headers=whut_headers)
        html = res.content
        parseHtml = etree.HTML(html)
        conts = parseHtml.xpath('/html/body/div[3]/div[2]/ul/li')
        for cont in conts:
            name = cont.xpath('./a/text()')[0].strip()
            time_ = cont.xpath('./span/text()')[0].strip()
            url = 'http://scc.whut.edu.cn/' + cont.xpath('./a/@href')[0].strip()
            self.textBrowser.append(name + ' ' + time_)
            self.textBrowser.append(url)
            self.textBrowser.append('-' * 60)
        Tlock.release()

    def hust_job(self):
        self.textBrowser.setText('华科就业网最近几天发布的招聘信息:')
        self.textBrowser.append('-'*60)
        executor = ThreadPoolExecutor(max_workers=10)
        for i in range(1, 11):
            executor.submit(self.hust_job_more, i)
        executor.shutdown(wait=True)

    def hust_job_more(self,i):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"}
        url1 = 'http://job.hust.edu.cn/searchJob_{}.jspx?type=2&fbsj='.format(i)
        html = requests.get(url1, headers).text
        content_li = re.findall("<a href=(.*)</a><br>", html)[4:-1]
        time_li = re.findall('<td width="120" valign="top">(.*)</td>', html)[4:]
        for n, i in enumerate(content_li):
            name = re.findall('title="(.*?)"', i)[0]
            url = 'http://job.hust.edu.cn/' + re.findall('"/(.*?)"', i)[0]
            time = time_li[n]
            self.textBrowser.append(name + ' ' + time)
            self.textBrowser.append(url)
            self.textBrowser.append('-' * 60)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = mwindow()
    w.pushButton.clicked.connect(w.hust_meeting)
    w.pushButton_3.clicked.connect(w.hust_job)
    w.pushButton_2.clicked.connect(w.whut_meeting)
    w.pushButton_4.clicked.connect(w.whut_job)
    w.show()
    sys.exit(app.exec_())

