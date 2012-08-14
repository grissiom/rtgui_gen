#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, traceback, time

import os, pprint

import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

from PyQt4.QtCore import *
from PyQt4.QtGui  import *
from PyQt4.QtSql  import *
from PyQt4.uic    import loadUiType
from PyQt4.QtCore import Qt

qapp = QApplication(sys.argv)
bt_dump_f = open('btdump.txt', 'a')

def excepthook(type, value, tb):
        lines = ''.join(traceback.format_exception(type, value, tb))
        QMessageBox.critical(None, u'出现异常', lines)
        bt_dump_f.write(lines + '\n')
        qapp.exit(255)
        # if Qt loop is not running
        sys.exit(255)

sys.excepthook = excepthook

class egg_window(QMdiArea):
    def __init__(self, p=None):
        super(egg_window, self).__init__(p)
        self._start_pos = None
        self.p = []

    def mousePressEvent(self, ev):
        self._start_pos = ev.pos()

    def mouseReleaseEvent(self, ev):
        nw = QPushButton(self)
        nw.setGeometry(QRect(self._start_pos, ev.pos()))
        nw.setStyleSheet('background-color: yellow')
        print 'add window on', nw.geometry()
        self.addSubWindow(nw)
        nw.show()

class main_wd(QMainWindow):
    def __init__(self, p=None):
        super(main_wd, self).__init__(p)

        self.the_egg = egg_window(self)
        dummy = QWidget(self)
        hlout = QHBoxLayout(dummy)
        hlout.addWidget(self.the_egg)
        self.setCentralWidget(dummy)

if __name__ == '__main__':
    #mw = main_wd()
    #mw.show()
    #sys.exit(qapp.exec_())
    import rtgui_sys
    from rtgui_sys import *
    execfile('sample.rui')
    print rtgui_sys.wins[0]['sample_ui'].serialize()
