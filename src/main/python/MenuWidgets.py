import os
import shutil

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon,QColor,QPalette,QFont,QPixmap,QPainter,QPen,QImage,QTransform,QPolygon,QBrush,\
    QPolygonF, QPalette, QGradient, QLinearGradient
from PyQt5.QtCore import *








import numpy as np

from Backends import *



class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget,self).__init__()
        self.layout = QHBoxLayout()
        self.initialise_status()
        self.initialise_actions()
        self.setLayout(self.layout)


    def initialise_status(self):
        vlayout = QVBoxLayout()
        self.qline_edits = {}
        for descr in ['Profits','Open Bets','Cash','Credit Balance','Transit']:
            hlayout = QHBoxLayout()
            label   = QLabel(descr)
            self.qline_edits[descr] = QLineEdit()
            self.qline_edits[descr].setMaximumSize(130,30)
            self.qline_edits[descr].setMinimumSize(130,30)
            self.qline_edits[descr].setReadOnly(True)

            hlayout.addWidget(label)
            hlayout.addWidget(self.qline_edits[descr])
            dummy_widget = QWidget()
            dummy_widget.setLayout(hlayout)
            vlayout.addWidget(dummy_widget)
        self.layout.addLayout(vlayout)




    def initialise_actions(self):
        vlayout = QVBoxLayout()
        self.buttons = {}
        for descr in ['Place Free Bet','Place Qual Bet']:
            self.buttons[descr] = QPushButton(descr)
            vlayout.addWidget(self.buttons[descr])
        self.layout.addLayout(vlayout)


class FREE_BET_CALCULATOR(QWidget):
    def __init__(self):
        super(FREE_BET_CALCULATOR,self).__init__()
        self.layout = QVBoxLayout()
        self.initialise_back_bets()
        self.initialise_lay_bets()
        self.initialise_info()
        self.initilise_actions()
        self.setLayout(self.layout)

    def initialise_back_bets(self):






if __name__=='__main__':
    import sys
    app = QApplication(sys.argv)
    w = MainWidget()
    w.show()
    sys.exit(app.exec_())
