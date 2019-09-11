from PyQt5 import QtCore,QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget
import sys
import requests
from lxml import etree
import re
from concurrent.futures import ThreadPoolExecutor
import threading
import csv
import os
Tlock = threading.Lock()

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(832, 522)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 1, 0, 1, 5)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 3, 2, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 4, 2, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 3, 3, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 4, 3, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 3, 0, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.pushButton_5, 4, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "luvm的招聘信息获取软件_彭迪"))
        self.pushButton_2.setText(_translate("Form", "武汉理工就业网招聘会"))
        self.pushButton_3.setText(_translate("Form", "华科就业网招聘信息"))
        self.pushButton.setText(_translate("Form", "华科就业网招聘会"))
        self.pushButton_4.setText(_translate("Form", "武汉理工就业网招聘信息"))
        self.pushButton_5.setText(_translate("Form", "关键字搜索"))

class mwindow(QWidget, Ui_Form):
    def __init__(self):
        super(mwindow, self).__init__()
        self.setupUi(self)
        self.li = ['./whut_meeting.csv','./hust_meeting.csv','./whut_job.csv','./hust_job.csv']
        for i in self.li:
            if os.path.exists(i):
                os.remove(i)

    def csv_saver(self,name,cont):
        with open(name, 'at', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(cont)


    def whut_meeting(self):
        self.textBrowser.setText('武汉理工就业网未来几天招聘会信息:')
        self.textBrowser.append("-" * 60)
        if os.path.exists('./whut_meeting.csv'):
            with open('./whut_meeting.csv','rt',encoding='utf-8') as f:
                for i in f.readlines():
                    name, place, time_, url = i.strip().split(',')
                    self.textBrowser.append(name + ' ' + place + ' ' + time_)
                    self.textBrowser.append(url)
                    self.textBrowser.append("-" * 60)
        else:
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
            self.csv_saver('./whut_meeting.csv', [name,place,time_,url])
            self.textBrowser.append('-' * 30)
        self.textBrowser.append("-" * 60)
        Tlock.release()

    def hust_meeting(self):
        self.textBrowser.setText('华科就业网未来几天招聘会信息:')
        self.textBrowser.append("-" * 60)
        if os.path.exists('./hust_meeting.csv'):
            with open('./hust_meeting.csv','r',encoding='utf-8') as f:
                for i in f.readlines():
                    name, place, time_, url = i.strip().split(',')
                    self.textBrowser.append(name + ' ' + place + ' ' + time_)
                    self.textBrowser.append(url)
                    self.textBrowser.append("-" * 60)
        else:
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
        places = re.findall(r'<span>([\u4e00-\u9fa5]+[A-Z]*[\u4e00-\u9fa5]*[0-9]*[\u4e00-\u9fa5]*)</span>', html)[:-2]
        for n, name in enumerate(names):
            time_ = time_s[n]
            place = places[n]
            url = 'http://job.hust.edu.cn' + urls[n][:-1]
            self.textBrowser.append(name + ' ' + time_ + ' ' + place)
            self.textBrowser.append(url)
            self.textBrowser.append('-' * 30)
            self.csv_saver('./hust_meeting.csv', [name, place, time_, url])
        self.textBrowser.append('-' * 60)
        Tlock.release()

    def whut_job(self):
        self.textBrowser.setText('武汉理工就业网最近几天发布的招聘信息:')
        self.textBrowser.append('-'*60)
        if os.path.exists('./whut_job.csv'):
            with open('./whut_job.csv','r',encoding='utf-8') as f:
                for i in f.readlines():
                    name, time_, url = i.strip().split(',')
                    self.textBrowser.append(name + ' ' + time_)
                    self.textBrowser.append(url)
                    self.textBrowser.append("-" * 60)
        else:
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
            self.csv_saver('./whut_job.csv', [name, time_, url])
            self.textBrowser.append('-' * 60)
        Tlock.release()

    def hust_job(self):
        self.textBrowser.setText('华科就业网最近几天发布的招聘信息:')
        self.textBrowser.append('-'*60)
        if os.path.exists('./hust_job.csv'):
            with open('./hust_job.csv','r',encoding='utf-8') as f:
                for i in f.readlines():
                    try:
                        name,time_, url = i.strip().split(',')
                        self.textBrowser.append(name + ' ' + time_ )
                        self.textBrowser.append(url)
                        self.textBrowser.append("-" * 60)
                    except:
                        pass
        else:
            executor = ThreadPoolExecutor(max_workers=10)
            for i in range(1, 11):
                executor.submit(self.hust_job_more, i)
            executor.shutdown(wait=True)

    def hust_job_more(self,i):
        Tlock.acquire()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"}
        url1 = 'http://job.hust.edu.cn/searchJob_{}.jspx?type=2&fbsj='.format(i)
        html = requests.get(url1, headers).text
        names = re.findall('title="(.*?)"', html)
        times = re.findall('<td width="120" valign="top">\[(.*?)\]</td>', html)
        urls = re.findall('<a href="(.*?)" title=', html)
        for n, name in enumerate(names):
            time_ = times[n]
            url = 'http://job.hust.edu.cn' + urls[n]
            self.textBrowser.append(name + ' ' + time_)
            self.textBrowser.append(url)
            self.csv_saver('./hust_job.csv', [name, time_, url])
            self.textBrowser.append('-' * 60)
        Tlock.release()

    def search(self):
        keyword = self.lineEdit.text()
        self.textBrowser.setText('针对关键字为“{}”搜索：'.format(keyword))
        self.textBrowser.append('-'*60)
        for file in self.li:
            if os.path.exists(file) :
                if 'meeting' in file:
                    with open(file, 'r', encoding='utf-8') as f:
                        for i in f.readlines():
                            name, place, time_, url = i.strip().split(',')
                            if keyword in name:
                                self.textBrowser.append(name + ' '+place+' ' + time_)
                                self.textBrowser.append(url)
                                self.textBrowser.append("-" * 60)
                else:
                    with open(file, 'r', encoding='utf-8') as f:
                        for j in f.readlines():
                            name, time_, url = j.strip().split(',')
                            if keyword in name:
                                self.textBrowser.append(name + ' ' + time_)
                                self.textBrowser.append(url)
                                self.textBrowser.append("-" * 60)
        self.lineEdit.clear()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = mwindow()
    w.pushButton.clicked.connect(w.hust_meeting)
    w.pushButton_3.clicked.connect(w.hust_job)
    w.pushButton_2.clicked.connect(w.whut_meeting)
    w.pushButton_4.clicked.connect(w.whut_job)
    w.pushButton_5.clicked.connect(w.search)
    w.lineEdit.returnPressed.connect(w.search)
    w.show()
    sys.exit(app.exec_())

