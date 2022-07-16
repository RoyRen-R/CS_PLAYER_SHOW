# -*- coding: utf-8 -*- 
# @Time : 2022/7/15 13:56 
# @Author : 任浩天
# @File : run.py.py
import sys

from corecode.main import *
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win2 = Datashow_action()
    win = login_action(win2)
    win.show()
    sys.exit(app.exec_())