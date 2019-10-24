import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets,uic
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class MyWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self,None)
        self.setupUI()

    def setupUI(self):
        self.setGeometry(600, 200, 1200, 600)
        self.setWindowTitle("PyChart Viewer v0.1")

        self.lineEdit = QLineEdit()
        self.pushButton = QPushButton("차트그리기")
        self.pushButton.clicked.connect(self.pushButtonClicked)

        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)

        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.canvas)

        # Right Layout
        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.lineEdit)
        rightLayout.addWidget(self.pushButton)
        rightLayout.addStretch(1)

        layout = QHBoxLayout()
        layout.addLayout(leftLayout)
        layout.addLayout(rightLayout)
        layout.setStretchFactor(leftLayout, 1)
        layout.setStretchFactor(rightLayout, 0)

        self.setLayout(layout)

    def pushButtonClicked(self):

        ax = self.fig.add_subplot(111)

        pop = pd.read_csv('./populationMergedWithID.csv')
        df = pd.DataFrame(pop)


        self.drawKorea('인구수합계',df,'Blues')
        self.canvas.draw()

    def drawKorea(self,targetData, blockedMap, cmapname):

        ax = self.fig.add_subplot(111)

        BORDER_LINES = [
            [(5, 1), (5, 2), (7, 2), (7, 3), (11, 3), (11, 0)],  # 인천
            [(5, 4), (5, 5), (2, 5), (2, 7), (4, 7), (4, 9), (7, 9), (7, 7), (9, 7), (9, 5), (10, 5), (10, 4), (5, 4)],
            # 서울
            [(1, 7), (1, 8), (3, 8), (3, 10), (10, 10), (10, 7), (12, 7), (12, 6), (11, 6), (11, 5), (12, 5), (12, 4),
             (11, 4), (11, 3)],  # 경기
            [(8, 10), (8, 11), (6, 11), (6, 12)],  # 강원
            [(12, 5), (13, 5), (13, 4), (14, 4), (14, 5), (15, 5), (15, 4), (16, 4), (16, 2)],  # 충북
            [(16, 4), (17, 4), (17, 5), (16, 5), (16, 6), (19, 6), (19, 5), (20, 5), (20, 4), (21, 4), (21, 3), (19, 3),
             (19, 1)],  # 전북
            [(13, 5), (13, 6), (16, 6)],  # 대전
            [(13, 6), (14, 5)],  # 세종
            [(21, 2), (21, 3), (22, 3), (22, 4), (24, 4), (24, 2), (21, 2)],  # 광주
            [(20, 5), (21, 5), (21, 6), (23, 6)],  # 전남
            [(10, 8), (12, 8), (12, 9), (14, 9), (14, 8), (16, 8), (16, 6)],  # 충남
            [(14, 9), (14, 11), (14, 12), (13, 12), (13, 13)],  # 경북
            [(15, 8), (17, 8), (17, 10), (16, 10), (16, 11), (14, 11)],  # 대구
            [(17, 9), (18, 9), (18, 8), (19, 8), (19, 9), (20, 9), (20, 10), (21, 10)],  # 부산
            [(16, 11), (16, 13)],  # 울산
            # [(9,14),(9,15)], 알수없는 좌표
            [(27, 5), (27, 6), (25, 6)]  # 제주?
        ]

        gamma = 0.75
        whitelabelmin = (max(blockedMap[targetData]) - min(blockedMap[targetData])) * 0.25 + \
                        min(blockedMap[targetData])

        datalabel = targetData

        vmin = min(blockedMap[targetData])
        vmax = max(blockedMap[targetData])

        mapdata = blockedMap.pivot_table(index='y', columns='x', values=targetData)
        masked_mapdata = np.ma.masked_where(np.isnan(mapdata), mapdata)


        plt.figure(figsize=(6, 6))

        plt.pcolor(masked_mapdata, vmin=vmin, vmax=vmax, cmap=cmapname,
                   edgecolor='#aaaaaa', linewidth=0.5)

        ax.pcolor(masked_mapdata, vmin=vmin, vmax=vmax, cmap=cmapname,
                   edgecolor='#aaaaaa', linewidth=0.5)


        # 지역이름 표시
        for idx, row in blockedMap.iterrows():
            if len(row['ID'].split()) == 2:
                dispname = '{}\n{}'.format(row['ID'].split()[0], row['ID'].split()[1])
            elif row['ID'][:2] == '고성':
                dispname = '고성'
            else:
                dispname = row['ID']

            if len(dispname.splitlines()[-1]) >= 3:
                fontsize, linespacing = 10.0, 1.1
            else:
                fontsize, linespacing = 11, 1.

            annocolor = 'white' if row[targetData] > whitelabelmin else 'black'

            ax.annotate(dispname, (row['x'] + 0.5, row['y'] + 0.5), weight='bold',
                         fontsize=fontsize, ha='center', va='center', color=annocolor,
                         linespacing=linespacing)

        for path in BORDER_LINES:
            ys, xs = zip(*path)
            ax.plot(xs, ys, c='black', lw=2)

        # plt.gca().invert_yaxis()
        # plt.gca().set_aspect(1)
        ax.axis('equal')

        cb = plt.colorbar(shrink=.1, aspect=10,ax=ax)
        cb.set_label(datalabel)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()

class koreamapCanvas(FigureCanvas):
    def __init__(self, parent = None, width =5, height=5 ,dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self,fig)
        self.setParent(parent)

        self.plot()


