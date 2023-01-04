#!/usr/bin/env/python3
# coding=UTF-8
'''
@file          :   DBCheckTool.py
@Author        :   程牧扬
@Time          :   2022/9/8 10:48
@Version       :   1.0
@Describetion  :
'''
import PyQt5.QtCore
import pymysql
import sys
import checkDBInformation
import time
from PyQt5.Qt import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox, QTextBrowser, QLineEdit, QLabel, QMainWindow
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QHBoxLayout, QVBoxLayout, QFormLayout

global conn
conn = None


class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.iniUI()

    def iniUI(self):
        self.setWindowTitle("数据库性能巡检工具")
        self.setGeometry(300, 300, 400, 300)
        # 总垂直布局
        vbox = QVBoxLayout(self)
        groupbox = QGroupBox(self)
        # 文本框
        self.host = QLineEdit(self)
        self.port = QLineEdit(self)
        self.user = QLineEdit(self)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)

        # 标签
        label_host = QLabel("主机地址")
        label_port = QLabel("端口")
        label_user = QLabel("用户名")
        label_password = QLabel("密码")

        # 表单布局
        form = QFormLayout()
        form.addRow(label_host, self.host)
        form.addRow(label_port, self.port)
        form.addRow(label_user, self.user)
        form.addRow(label_password, self.password)

        hbox = QHBoxLayout(self)
        hbox.addLayout(form)
        hbox.addStretch(1)  # 在hbox.addLayout()函数前添加伸缩量表示左对齐,函数后执行表示右对齐
        vbox.addLayout(hbox)

        Btn = QPushButton("连接")
        Btn.clicked.connect(self.buttonbClick)

        self.combox = QComboBox(self)
        self.combox.addItems(['请选择数据库类型', 'mysql', 'oracle', 'SQLServer', 'Postgres', 'Kingbase', 'OceanBase'])
        hbox = QHBoxLayout()
        hbox.addWidget(Btn)
        hbox.addWidget(self.combox)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        # 文本显示框
        self.text_browser = QTextBrowser(self)
        # 格子布局
        grid = self.setGrid()
        hbox2 = QHBoxLayout(self)
        hbox2.addLayout(grid)
        hbox2.addStretch(1)
        vbox.addLayout(hbox2)
        # 水平布局3
        hbox3 = QHBoxLayout()

        hbox3.addWidget(self.text_browser)
        vbox.addLayout(hbox3)

        # 状态提示信息栏
        self.statusBar = QStatusBar(self)
        self.statusBar.showMessage("未连接")
        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.statusBar)
        vbox.addLayout(hbox4)
        vbox.addSpacing(20)
        vbox.addStretch(1)

        self.setLayout(vbox)

    def buttonbClick(self) -> "测试连接按钮点击功能":
        currentText = self.combox.currentText()
        try:
            if currentText == "mysql":
                global conn
                conn = pymysql.Connect(host=self.host.text(), port=int(self.port.text()), user=self.user.text(),
                                       password=self.password.text(), database="test")

            elif currentText == "oracle":
                pass
            else:
                pass

            if conn:
                self.statusBar.showMessage("已连接")

        except Exception as e:
            self.statusBar.showMessage("连接数据库失败,请检查账户信息以及端口")
            conn = None

    def setGrid(self) -> "梳理格子布局":
        res = [
            ['慢查询', 'sql性能', '执行次数最多的sql'],
            ['平均响应时间最大的sql', '排序记录最多的sql', '扫描记录做多得sql'],
            ['临时表做多的sql', '返回结果最多的sql', '物理IO最多表'],
            ['逻辑读最多表', '索引访问最多', '从未使用过索引', '等待时间最长事件']
        ]
        grid = QGridLayout()
        for x in range(len(res)):
            for y in range(len(res[x])):
                button = QPushButton(res[x][y])
                grid.addWidget(button, x, y)
                button.clicked.connect(self.checkButton)
        return grid

    # 格子布局按钮绑定事件
    def checkButton(self: "sender函数可以判断信号得发出者是谁"):
        text = self.sender().text()
        if conn:
            if text == "慢查询":
                result = checkDBInformation.test(conn)
                self.text_browser.setText(str(result))
                return

            if text == "执行次数最多的sql":
                result = checkDBInformation.exec_max_times_sql(conn)
                # self.text_browser.setText(str(result))
                return

            if text == "平均响应时间最大的sql":
                result = checkDBInformation.response_max_spend_sec_sql(conn)
                self.text_browser.setText(str(result))
                return

            if text == "排序记录最多的sql":
                result = checkDBInformation.exec_max_order_rows_sql(conn)
                self.text_browser.setText(str(result))
                return

            if text == "扫描记录最多的sql":
                result = checkDBInformation.scan_max_rows_sql(conn)
                self.text_browser.setText(str(result))
                return

            if text == "临时表最多的sql":
                result = checkDBInformation.create_max_tmp_tables_sql(conn)
                self.text_browser.setText(str(result))
                return

            if text == "返回结果最多的sql":
                result = checkDBInformation.get_max_result_sql(conn)
                self.text_browser.setText(str(result))
                return

            if text == "物理IO最多表":
                result = checkDBInformation.max_physical_IO_sql(conn)
                self.text_browser.setText(str(result))
                return

            if text == "逻辑读最多表":
                result = checkDBInformation.max_logical_read_sql(conn)
                self.text_browser.setText(str(result))
                return

            if text == "索引访问最多":
                result = checkDBInformation.test(conn)
                self.text_browser.setText(str(result))
                return

            if text == "等待时间最长事件":
                result = checkDBInformation.wait_event_max_time(conn)
                self.text_browser.setText(str(result))
                return

        else:
            self.statusBar.showMessage("连接数据库失败")
            self.text_browser.setText(" ")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())
