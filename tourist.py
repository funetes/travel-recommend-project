import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QUrl

import PyQt5.QtWebEngineWidgets
import folium
from folium.plugins import MarkerCluster

import pandas as pd
import numpy as np
import seaborn as sns

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import style

import platform
import matplotlib.pyplot as plt
import matplotlib

import drawModule as dmo
import TripModelWithRandomForestFunc as ranfor
import borderline as bd


path = "c:/Windows/Fonts/malgun.ttf"
from matplotlib import font_manager, rc
if platform.system() == "Darwin":
    rc('font',family='AppleGothic')
elif platform.system() == 'Windows':
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
else:
    print('Unknown System.')

ui = './tourist.ui'

gender = "남성"
age = "전체"
month = "봄"
marry = "기혼"
year = "2016"
dosi= "서울"
sigun = "마포구"

an_dosi = "서울"
an_sigun = "마포구"
an_season = "가을"
an_trip_purpose = "추천"
an_transfer = "자가용"
an_s_fac = "펜션"
an_s_day = "1"
an_age = "40대"
an_gender = "남성"
an_living ="서울"
an_job = "전문가 및 관련 종사자"
an_marry = "배우자있음"
an_family = "1"
an_name = ""

an_amuse = "0"
an_tour = "0"
an_rest = "0"
an_etc = "0"
an_shopping = "0"
an_exp = "0"

month_list = []
favorit_list = []
reason_list = []
satis_list = []
mapDrawdata = []
predmodel = []

csv_2016 = pd.read_csv('./data/2016full.csv')
maphelper = pd.read_csv('./data/populationMergedWithID.csv')
analy_csv = pd.read_csv('./data/pretreatment_All.csv')
recommand_csv = pd.read_csv('./data/TripTotal.csv')

df = pd.DataFrame(csv_2016)

class TouristDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self,None)
        uic.loadUi(ui,self)

        global predmodel

        self.agecomboBox.addItem("전체")
        self.agecomboBox.addItem("10대")
        self.agecomboBox.addItem("20대")
        self.agecomboBox.addItem("30대")
        self.agecomboBox.addItem("40대")
        self.agecomboBox.addItem("50대")
        self.agecomboBox.addItem("60대 이상")
        self.agecomboBox.currentTextChanged.connect(self.cbAge)


        listdosi = csv_2016['여행한 도시'].unique()
        initbox = csv_2016[csv_2016["여행한 도시"].isin(['서울'])]["여행한 시/군"].unique()
        anal_season = analy_csv["여행계절"].unique()
        anal_trip_purpose = analy_csv["여행지 선택이유"].unique()
        anal_transfer = analy_csv["주요 이동(교통)수단"].unique()
        anal_s_fac = analy_csv["숙박시설"].unique()
        anal_gender = analy_csv["성별"].unique()
        anal_living = analy_csv["거주시도"].unique()
        anal_job = analy_csv["직업"].unique()
        anal_marry = analy_csv["혼인상태"].unique()
        anal_age = analy_csv["나이"].unique()


        predmodel = ranfor.modelingPredictSaticefaction(self)

        for i in range(len(listdosi)):
            self.dosicomboBox.addItem(str(listdosi[i]))

        for i in range(len(initbox)):
            self.siguncomboBox.addItem(initbox[i])

        for i in range(len(listdosi)):
            self.analy_dosi.addItem(str(listdosi[i]))

        for i in range(len(initbox)):
            self.analy_sigungu.addItem(initbox[i])

        for i in range(len(anal_season)):
            self.analy_season.addItem(anal_season[i])

        for i in range(len(anal_trip_purpose)):
            self.analy_trip_purpose.addItem(anal_trip_purpose[i])

        for i in range(len(anal_transfer)):
            self.analy_transfer.addItem(anal_transfer[i])

        for i in range(len(anal_age)):
            self.analy_age.addItem(anal_age[i])

        for i in range(len(anal_gender)):
            self.analy_gender.addItem(anal_gender[i])

        for i in range(len(anal_s_fac)):
            self.analy_s_fac.addItem(anal_s_fac[i])

        for i in range(len(anal_living)):
            self.analy_living.addItem(anal_living[i])

        for i in range(len(anal_marry)):
            self.analy_marry.addItem(anal_marry[i])

        for i in range(len(anal_job)):
            self.analy_job.addItem(anal_job[i])


        self.dosicomboBox.currentTextChanged.connect(self.cbSi)
        self.siguncomboBox.currentTextChanged.connect(self.cbSigun)

        self.analy_sigungu.currentTextChanged.connect(self.Analy_cbSigun)
        self.analy_dosi.currentTextChanged.connect(self.Analy_cbSi)
        self.analy_s_fac.currentTextChanged.connect(self.cbAnal_s_fac)
        self.analy_transfer.currentTextChanged.connect(self.cbAnal_transfer)
        self.analy_gender.currentTextChanged.connect(self.cbAnal_gender)
        self.analy_job.currentTextChanged.connect(self.cbAnal_job)
        self.analy_living.currentTextChanged.connect(self.cbAnal_living)
        self.analy_marry.currentTextChanged.connect(self.cbAnal_marry)
        self.analy_season.currentTextChanged.connect(self.cbAnal_season)
        self.analy_trip_purpose.currentTextChanged.connect(self.cbAnal_trip_purpose)
        self.analy_age.currentTextChanged.connect(self.cbAnal_age)

        self.cbAmuse.stateChanged.connect(self.getcbAmuse)
        self.cbTour.stateChanged.connect(self.getcbTour)
        self.cbRest.stateChanged.connect(self.getcbRest)
        self.cbEtc.stateChanged.connect(self.getcbEtc)
        self.cbExp.stateChanged.connect(self.getcbExp)
        self.cbShopping.stateChanged.connect(self.getcbShopping)

        self.r_male.clicked.connect(self.rdGender)
        self.r_female.clicked.connect(self.rdGender)
        self.r_gender_all.clicked.connect(self.rdGender)

        self.r_one.clicked.connect(self.rdMonth)
        self.r_two.clicked.connect(self.rdMonth)
        self.r_three.clicked.connect(self.rdMonth)
        self.r_four.clicked.connect(self.rdMonth)
        self.r_season_all.clicked.connect(self.rdMonth)

        self.y_2016.clicked.connect(self.rdYear)
        self.y_2017.clicked.connect(self.rdYear)

        self.r_no_marry.clicked.connect(self.rdMarry)
        self.r_marry.clicked.connect(self.rdMarry)
        self.r_marry_all.clicked.connect(self.rdMarry)

        self.btnOk.clicked.connect(self.searchOn)
        self.btnSerach.clicked.connect(self.update)
        self.btnAnaly.clicked.connect(self.Analysatis)

        regex = QtCore.QRegExp("[0-9_]+")

        validator = QtGui.QRegExpValidator(regex)

        self.analy_s_day.setValidator(validator)
        self.analy_family.setValidator(validator)

        self.r_male.setChecked(1)
        self.r_one.setChecked(1)
        self.r_marry.setChecked(1)
        self.y_2016.setChecked(1)

        self.scale_1 = QPixmap("./image/satis_1")
        self.scale_2 = QPixmap("./image/satis_2")
        self.scale_3 = QPixmap("./image/satis_3")
        self.scale_4 = QPixmap("./image/satis_4")
        self.scale_5 = QPixmap("./image/satis_5")

        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvas(self.fig)

        self.canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        self.canvas.updateGeometry()
        self.maplayout.addWidget(self.canvas)

        self.fig2 = Figure()

        self.ax2 = self.fig2.add_subplot(111)
        self.canvas2 = FigureCanvas(self.fig2)

        self.canvas2.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)

        self.canvas2.updateGeometry()
        self.graphlayout.addWidget(self.canvas2)

        self.fig3 = Figure()
        self.ax3 = self.fig3.add_subplot(111)

        self.canvas3 = FigureCanvas(self.fig3)

        self.canvas3.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        self.canvas3.updateGeometry()
        self.favoritlayout.addWidget(self.canvas3)

        self.fig4 = Figure()
        self.ax4 = self.fig4.add_subplot(111)

        self.canvas4 = FigureCanvas(self.fig4)

        self.canvas4.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        self.canvas4.updateGeometry()
        self.reasonlayout.addWidget(self.canvas4)

        self.fig5 = Figure()
        self.ax5 = self.fig5.add_subplot(111)

        self.canvas5 = FigureCanvas(self.fig5)

        self.canvas5.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        self.canvas5.updateGeometry()
        self.satislayout.addWidget(self.canvas5)

        self.fig6 = Figure()

        self.ax6 = self.fig6.add_subplot(111)
        self.canvas6 = FigureCanvas(self.fig6)

        self.canvas6.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)

        self.canvas6.updateGeometry()
        self.alltripreasonlayout.addWidget(self.canvas6)

        self.fig7 = Figure()

        self.ax7 = self.fig7.add_subplot(111)
        self.canvas7 = FigureCanvas(self.fig7)

        self.canvas7.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)

        self.canvas7.updateGeometry()
        self.alltripdolayout.addWidget(self.canvas7)

        self.fig8 = Figure()

        self.ax8 = self.fig8.add_subplot(111)
        self.canvas8 = FigureCanvas(self.fig8)

        self.canvas8.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)

        self.canvas8.updateGeometry()
        self.alltripseasonlayout.addWidget(self.canvas8)

        self.fig9 = Figure()

        self.ax9 = self.fig9.add_subplot(111)
        self.canvas9 = FigureCanvas(self.fig9)

        self.canvas9.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)

        self.canvas9.updateGeometry()
        self.satismaplayout.addWidget(self.canvas9)

        self.fig10 = Figure()

        self.ax10 = self.fig10.add_subplot(111)
        self.canvas10 = FigureCanvas(self.fig10)

        self.canvas10.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)

        self.canvas10.updateGeometry()
        self.importancelayout.addWidget(self.canvas10)

        mapDrawdata = dmo.getAlltrip(age,month,marry,gender,year)
        satisDrawdata = dmo.getAllSatisFaction(age,month,marry,gender,year)

        self.drawKorea('여행 지수', mapDrawdata, 'YlOrBr')
        self.drawKoreaSatis('만족도 지수',satisDrawdata,'Blues')


        month_list = dmo.getSpecMonth(age,month,marry,gender,year)
        favorit_list= dmo.getSpecMyFavorite(age,month,marry,gender,year)
        reason_list = dmo.getSpecReason(age,month,marry,gender,year)

        month_list1 = pd.DataFrame(month_list[0])
        month_list1['여행 횟수'] = month_list1[0]
        month_list1['계절'] = ['봄','여름','가을','겨울']

        month_list2 =  pd.DataFrame(month_list[1])
        month_list2['여행 횟수'] = month_list2[0]
        month_list2['계절'] = ['봄','여름','가을','겨울']


        favorit_list1 = pd.DataFrame(favorit_list)

        favorit_list1['횟수'] = favorit_list1[0]

        favorit_list1['이유'] = ['볼거리 제공', '지명도', '없음', '기타', '경험자의 추천', '여행동반자', '음식',
                                 '이동거리', '편의시설', '시간', '여행경비', '숙박시설', '교통편', '쇼핑',
                                 '체험', '교육성']


        recom = favorit_list1['횟수'][4] + favorit_list1['횟수'][1]
        food_shopping = favorit_list1['횟수'][6] + favorit_list1['횟수'][13]
        cond = favorit_list1['횟수'][7] + favorit_list1['횟수'][9] + favorit_list1['횟수'][10] + favorit_list1['횟수'][12]
        exp = favorit_list1['횟수'][0] + favorit_list1['횟수'][14] + favorit_list1['횟수'][15]
        fac = favorit_list1['횟수'][8] + favorit_list1['횟수'][11]
        etc = favorit_list1['횟수'][3] + favorit_list1['횟수'][5]

        favorit_list2 = pd.DataFrame()

        favorit_list2['횟수'] = [recom,food_shopping,cond,exp,fac,etc]
        favorit_list2['이유'] = ['추천','음식/쇼핑','여건','문화/체험','편의시설','기타']

        reason_list1 = pd.DataFrame(reason_list)

        reason_list1['횟수'] = reason_list1[0]
        reason_list1['행동'] = ['자연 및 풍경 감상', '음식관광', '스포츠 활동', '유적지 방문',
                                '테마파크 방문', '휴식/휴양', '온천/스파', '쇼핑', '문화예술/공연 관람',
                                '스포츠 경기', '지역 축제/이벤트 참가', '교육/체험', '종교/성지순례', '겜블링', '시티투어',
                                '드라마 촬영지 방문', '지인 방문', '회의참가/시찰', '훈련/연수', '유흥/오락', '기타']



        r_amuse = reason_list1['횟수'][13] + reason_list1['횟수'][19] + reason_list1['횟수'][9]
        r_tour = reason_list1['횟수'][0] + reason_list1['횟수'][3] + reason_list1['횟수'][15] + reason_list1['횟수'][14] + reason_list1['횟수'][4]
        r_rest = reason_list1['횟수'][6] + reason_list1['횟수'][1] + reason_list1['횟수'][2] + reason_list1['횟수'][8]
        r_etc = reason_list1['횟수'][16]  + reason_list1['횟수'][20] + reason_list1['횟수'][12] + reason_list1['횟수'][17] + reason_list1['횟수'][18]
        r_shopping = reason_list1['횟수'][7]
        r_exp = reason_list1['횟수'][10] + reason_list1['횟수'][11]


        reason_list2 = pd.DataFrame()
        reason_list2['횟수'] = [r_amuse,r_tour,r_rest,r_etc,r_shopping,r_exp]
        reason_list2['행동'] = ['오락','투어','휴식','기타','쇼핑','체험']

        del month_list1[0]

        favorit = favorit_list2['횟수']
        favorit_label = favorit_list2['이유']

        reason = reason_list2['횟수']
        reason_label = reason_list2['행동']

        for i in range(len(favorit_list2['횟수'])):
            if(favorit_list2["횟수"][i] == 0):
                favorit_list2 = favorit_list2.drop(i,0)

        for i in range(len(reason_list2['횟수'])):
            if(reason_list2["횟수"][i] == 0):
                reason_list2 = reason_list2.drop(i,0)

        sns.barplot(x="계절",y="여행 횟수",data=month_list2,ax=self.ax8)
        self.ax7.pie(favorit, labels=favorit_label, rotatelabels=0, autopct='%.2f', textprops={'size': 'smaller'})
        self.ax6.pie(reason, labels=reason_label, rotatelabels=0, autopct='%.2f', textprops={'size': 'smaller'})


        self.ax6.axis=('equal')
        self.ax7.axis=('equal')

        self.ax6.set_title("여행지 를 간 이유")
        self.ax7.set_title("여행지 에서 주로 한 일")


        month_list = dmo.getMonth(dosi,sigun)
        favorit_list= dmo.getMyFavorite(dosi,sigun)
        reason_list = dmo.getReason(dosi,sigun)
        satis_list = dmo.getSatisFaction(dosi,sigun)
        getlatlon = dmo.getLatLon(dosi,sigun)

        month_list1 = pd.DataFrame(month_list)
        month_list1['여행 횟수'] = month_list1[0]
        month_list1['계절'] = ['봄','여름','가을','겨울']

        favorit_list1 = pd.DataFrame(favorit_list)
        favorit_list1['횟수'] = favorit_list1[0]
        favorit_list1['이유'] = ['볼거리 제공', '지명도', '없음', '기타', '경험자의 추천', '여행동반자', '음식',
                                 '이동거리', '편의시설', '시간', '여행경비', '숙박시설', '교통편', '쇼핑',
                                 '체험', '교육성']

        recom = favorit_list1['횟수'][4] + favorit_list1['횟수'][1]
        food_shopping = favorit_list1['횟수'][6] + favorit_list1['횟수'][13]
        cond = favorit_list1['횟수'][7] + favorit_list1['횟수'][9] + favorit_list1['횟수'][10] + favorit_list1['횟수'][12]
        exp = favorit_list1['횟수'][0] + favorit_list1['횟수'][14] + favorit_list1['횟수'][15]
        fac = favorit_list1['횟수'][8] + favorit_list1['횟수'][11]
        etc = favorit_list1['횟수'][3] + favorit_list1['횟수'][5]

        favorit_list2 = pd.DataFrame()

        favorit_list2['횟수'] = [recom,food_shopping,cond,exp,fac,etc]
        favorit_list2['이유'] = ['추천','음식/쇼핑','여건','문화/체험','편의시설','기타']




        reason_list1 = pd.DataFrame(reason_list)

        reason_list1['횟수'] = reason_list1[0]
        reason_list1['행동'] = ['자연 및 풍경 감상', '음식관광', '스포츠 활동', '유적지 방문',
                                '테마파크 방문', '휴식/휴양', '온천/스파', '쇼핑', '문화예술/공연 관람',
                                '스포츠 경기', '지역 축제/이벤트 참가', '교육/체험', '종교/성지순례', '겜블링', '시티투어',
                                '드라마 촬영지 방문', '지인 방문', '회의참가/시찰', '훈련/연수', '유흥/오락', '기타']



        r_amuse = reason_list1['횟수'][13] + reason_list1['횟수'][19] + reason_list1['횟수'][9]
        r_tour = reason_list1['횟수'][0] + reason_list1['횟수'][3] + reason_list1['횟수'][15] + reason_list1['횟수'][14] + reason_list1['횟수'][4]
        r_rest = reason_list1['횟수'][6] + reason_list1['횟수'][1] + reason_list1['횟수'][2] + reason_list1['횟수'][8]
        r_etc = reason_list1['횟수'][16]  + reason_list1['횟수'][20] + reason_list1['횟수'][12] + reason_list1['횟수'][17] + reason_list1['횟수'][18]
        r_shopping = reason_list1['횟수'][7]
        r_exp = reason_list1['횟수'][10] + reason_list1['횟수'][11]


        reason_list2 = pd.DataFrame()
        reason_list2['횟수'] = [r_amuse,r_tour,r_rest,r_etc,r_shopping,r_exp]
        reason_list2['행동'] = ['오락','투어','휴식','기타','쇼핑','체험']





        del month_list1[0]
        del month_list2[0]
        # del favorit_list1[0]
        # del reason_list1[0]

        # for i in range(len(favorit_list1['횟수'])):
        #     if(favorit_list1["횟수"][i] == 0):
        #         favorit_list1 = favorit_list1.drop(i,0)
        #     elif(favorit_list1["이유"][i] is '없음'):
        #         favorit_list1 = favorit_list1.drop(i,0)

        # for i in range(len(reason_list1['횟수'])):
        #     if(reason_list1["횟수"][i] == 0):
        #         reason_list1 = reason_list1.drop(i,0)

        favorit = favorit_list2['횟수']
        favorit_label = favorit_list2['이유']

        reason = reason_list2['횟수']
        reason_label = reason_list2['행동']

        satis = satis_list["갯수"]
        satis_label = satis_list["전반적 만족도"]

        for i in range(len(favorit_list2['횟수'])):
            if(favorit_list2["횟수"][i] == 0):
                favorit_list2 = favorit_list2.drop(i,0)

        for i in range(len(reason_list2['횟수'])):
            if(reason_list2["횟수"][i] == 0):
                reason_list2 = reason_list2.drop(i,0)


        sns.barplot(x="계절",y="여행 횟수",data=month_list1,ax=self.ax)
        # sns.barplot(x="전반적 만족도", y="갯수", data=satis_list, ax=self.ax5)
        # month_list1.plot(x='계절',kind='bar',figsize=(3,2),ax=self.ax,rot=0)

        # rects = self.ax4.barh(reason_label,reason,align='center',height=0.5)
        # for i, rect in enumerate(rects):
        #     self.ax4.text(0.95 * rect.get_width(), rect.get_y() + rect.get_height() / 2.0, str(reason[i]) + '%',
        #             ha='right', va='center')

        self.ax3.pie(favorit,labels=favorit_label,rotatelabels=0,autopct='%.2f',textprops={'size': 'smaller'})
        self.ax4.pie(reason, labels=reason_label, rotatelabels=0,autopct='%.2f', textprops={'size': 'smaller'})
        self.ax5.pie(satis, labels=satis_label,rotatelabels=0,autopct='%.2f',textprops={'size': 'smaller'})

        lat = float(getlatlon["Latitude"])
        lon = float(getlatlon["Longitude"])



        map_folium = folium.Map(location=[lat,lon],zoom_start=10)

        dosimarker = recommand_csv.loc[recommand_csv["여행지"] == dosi+sigun, ["Latitude","Longitude"]]
        tripData = recommand_csv.loc[recommand_csv["여행지"] == dosi+sigun, ["장소","주소","상세설명"]]

        dosimarker = dosimarker.reset_index()
        del dosimarker["index"]

        tripData = tripData.reset_index()
        del tripData["index"]

        for i in range(len(tripData)):
            self.recommandTable.removeRow(i)

        for i2 in range(len(tripData)+1):
            self.recommandTable.setColumnCount(3)
            self.recommandTable.setRowCount(i2)

        column_headers = ['이름', '주소','설명']
        self.recommandTable.setHorizontalHeaderLabels(column_headers)

        for k in range(len(dosimarker)):
            folium.Marker(
                location=[dosimarker["Latitude"][k], dosimarker["Longitude"][k]],
                # popup = tripData["장소"][k],
                tooltip= tripData["장소"][k],
                icon=folium.Icon(color='red', icon='star')
            ).add_to(map_folium)

        map_folium.save('./Map/Map.html')

        self.foliumlayout.load(QUrl("file:///C:/Users/user/Desktop/TripProject1/venv/Scripts/design/Map/Map.html"))

        # self.ax3.legend(loc="best")
        # self.ax4.legend(loc="best")

        for col in range(len(tripData)):
            self.recommandTable.setItem(col, 0, QTableWidgetItem(tripData["장소"][col]))
            self.recommandTable.setItem(col, 1, QTableWidgetItem(tripData["주소"][col]))
            try:
                self.recommandTable.setItem(col, 2, QTableWidgetItem(tripData["상세설명"][col]))
            except TypeError:
                pass

        self.recommandTable.resizeColumnsToContents()
        self.recommandTable.resizeRowsToContents()

        self.ax3.axis=('equal')
        self.ax4.axis=('equal')
        self.ax5.axis=('equal')

        self.ax3.set_title(dosi+" "+sigun+"을(를) 간 이유")
        self.ax4.set_title(dosi + " " + sigun + "에서 주로 한 일")
        self.ax5.set_title(dosi + " "+ sigun + "의 만족도")

        month_list = []
        month_list1 = []

        favorit_list = []
        favorit_list1 = []

        reason_list = []
        reason_list1 = []

        satis_list = []

        lat = 0
        lon = 0



        importance_rate = ranfor.feature_importances(predmodel).sort_values(by='중요도',ascending=False)

        importance_rate = importance_rate.reset_index()
        importance_rate.columns.values[0] = "특성"

        importance_rate["특성"][3] = "여행자 수"
        importance_rate["특성"][6] = "선택이유"
        importance_rate["특성"][7] = "교통수단"

        sns.barplot(x="중요도",y="특성",data=importance_rate,ax=self.ax10)

    def drawKorea(self,targetData, blockedMap, cmapname):

        ax2 = self.fig2.add_subplot(111)

        BORDER_LINES = bd.borderline()

        gamma = 0.75
        whitelabelmin = (max(blockedMap[targetData]) - min(blockedMap[targetData])) * 0.25 + \
                        min(blockedMap[targetData])

        datalabel = targetData

        # vmin = min(blockedMap[targetData])
        # vmax = max(blockedMap[targetData])

        vmin = -1
        vmax = 1

        mapdata = blockedMap.pivot_table(index='y', columns='x', values=targetData)
        masked_mapdata = np.ma.masked_where(np.isnan(mapdata), mapdata)

        plt.figure(figsize=(6, 6))

        plt.pcolor(masked_mapdata, vmin=vmin, vmax=vmax, cmap=cmapname,
                   edgecolor='#aaaaaa', linewidth=0.5)

        ax2.pcolor(masked_mapdata, vmin=vmin, vmax=vmax, cmap=cmapname,
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
                fontsize, linespacing = 6.0, 1.1
            else:
                fontsize, linespacing = 6.5, 1.



            annocolor = 'white' if row[targetData] > whitelabelmin else 'black'

            ax2.annotate(dispname, (row['x'] + 0.5, row['y'] + 0.5), weight='bold',
                         fontsize=fontsize, ha='center', va='center', color=annocolor,
                         linespacing=linespacing)

        for path in BORDER_LINES:
            ys, xs = zip(*path)
            ax2.plot(xs, ys, c='black', lw=2)

        ax2.invert_yaxis()
        # plt.gca().set_aspect(1)
        ax2.axis('equal')

        cb = plt.colorbar(shrink=.1, aspect=10,ax=ax2)
        cb.set_label(datalabel)

    def drawKoreaSatis(self,targetData, blockedMap, cmapname):

        ax9 = self.fig9.add_subplot(111)

        BORDER_LINES = bd.borderline()

        gamma = 0.75
        whitelabelmin = (max(blockedMap[targetData]) - min(blockedMap[targetData])) * 0.25 + \
                        min(blockedMap[targetData])

        datalabel = targetData

        # vmin = min(blockedMap[targetData])
        # vmax = max(blockedMap[targetData])

        vmin = -1
        vmax = 1

        mapdata = blockedMap.pivot_table(index='y', columns='x', values=targetData)
        masked_mapdata = np.ma.masked_where(np.isnan(mapdata), mapdata)

        plt.figure(figsize=(6, 6))

        plt.pcolor(masked_mapdata, vmin=vmin, vmax=vmax, cmap=cmapname,
                   edgecolor='#aaaaaa', linewidth=0.5)

        ax9.pcolor(masked_mapdata, vmin=vmin, vmax=vmax, cmap=cmapname,
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
                fontsize, linespacing = 6.0, 1.1
            else:
                fontsize, linespacing = 6.5, 1.



            annocolor = 'white' if row[targetData] > whitelabelmin else 'black'

            ax9.annotate(dispname, (row['x'] + 0.5, row['y'] + 0.5), weight='bold',
                         fontsize=fontsize, ha='center', va='center', color=annocolor,
                         linespacing=linespacing)

        for path in BORDER_LINES:
            ys, xs = zip(*path)
            ax9.plot(xs, ys, c='black', lw=2)

        ax9.invert_yaxis()
        # plt.gca().set_aspect(1)
        ax9.axis('equal')

        cb = plt.colorbar(shrink=.1, aspect=10,ax=ax9)
        cb.set_label(datalabel)

    def update(self):

        global csv_2016,dosi,sigun,month_list,favorit_list,reason_list,satis_list

        self.ax.clear()
        self.ax3.clear()
        self.ax4.clear()
        self.ax5.clear()

        self.fig.clear()
        self.fig3.clear()
        self.fig4.clear()
        self.fig5.clear()

        self.ax = self.fig.add_subplot(111)
        self.ax3 = self.fig3.add_subplot(111)
        self.ax4 = self.fig4.add_subplot(111)
        self.ax5 = self.fig5.add_subplot(111)


        month_list = dmo.getMonth(dosi,sigun)
        favorit_list= dmo.getMyFavorite(dosi,sigun)
        reason_list = dmo.getReason(dosi,sigun)
        satis_list = dmo.getSatisFaction(dosi,sigun)
        getlatlon = dmo.getLatLon(dosi,sigun)

        month_list1 = pd.DataFrame(month_list)
        month_list1['여행 횟수'] = month_list1[0]
        month_list1['계절'] = ['봄','여름','가을','겨울']


        favorit_list1 = pd.DataFrame(favorit_list)
        favorit_list1['횟수'] = favorit_list1[0]
        favorit_list1['이유'] = ['볼거리 제공', '지명도', '없음', '기타', '경험자의 추천', '여행동반자', '음식',
                                 '이동거리', '편의시설', '시간', '여행경비', '숙박시설', '교통편', '쇼핑',
                                 '체험', '교육성']

        recom = favorit_list1['횟수'][4] + favorit_list1['횟수'][1]
        food_shopping = favorit_list1['횟수'][6] + favorit_list1['횟수'][13]
        cond = favorit_list1['횟수'][7] + favorit_list1['횟수'][9] + favorit_list1['횟수'][10] + favorit_list1['횟수'][12]
        exp = favorit_list1['횟수'][0] + favorit_list1['횟수'][14] + favorit_list1['횟수'][15]
        fac = favorit_list1['횟수'][8] + favorit_list1['횟수'][11]
        etc = favorit_list1['횟수'][3] + favorit_list1['횟수'][5]

        favorit_list2 = pd.DataFrame()

        favorit_list2['횟수'] = [recom,food_shopping,cond,exp,fac,etc]
        favorit_list2['이유'] = ['추천','음식/쇼핑','여건','문화/체험','편의시설','기타']



        reason_list1 = pd.DataFrame(reason_list)

        reason_list1['횟수'] = reason_list1[0]
        reason_list1['행동'] = ['자연 및 풍경 감상', '음식관광', '스포츠 활동', '유적지 방문',
                                '테마파크 방문', '휴식/휴양', '온천/스파', '쇼핑', '문화예술/공연 관람',
                                '스포츠 경기', '지역 축제/이벤트 참가', '교육/체험', '종교/성지순례', '겜블링', '시티투어',
                                '드라마 촬영지 방문', '지인 방문', '회의참가/시찰', '훈련/연수', '유흥/오락', '기타']



        r_amuse = reason_list1['횟수'][13] + reason_list1['횟수'][19] + reason_list1['횟수'][9]
        r_tour = reason_list1['횟수'][0] + reason_list1['횟수'][3] + reason_list1['횟수'][15] + reason_list1['횟수'][14] + reason_list1['횟수'][4]
        r_rest = reason_list1['횟수'][6] + reason_list1['횟수'][1] + reason_list1['횟수'][2] + reason_list1['횟수'][8]
        r_etc = reason_list1['횟수'][16]  + reason_list1['횟수'][20] + reason_list1['횟수'][12] + reason_list1['횟수'][17] + reason_list1['횟수'][18]
        r_shopping = reason_list1['횟수'][7]
        r_exp = reason_list1['횟수'][10] + reason_list1['횟수'][11]


        reason_list2 = pd.DataFrame()
        reason_list2['횟수'] = [r_amuse,r_tour,r_rest,r_etc,r_shopping,r_exp]
        reason_list2['행동'] = ['오락','투어','휴식','기타','쇼핑','체험']





        del month_list1[0]

        # del favorit_list1[0]
        # del reason_list1[0]

        # for i in range(len(favorit_list1['횟수'])):
        #     if(favorit_list1["횟수"][i] == 0):
        #         favorit_list1 = favorit_list1.drop(i,0)
        #     elif(favorit_list1["이유"][i] is '없음'):
        #         favorit_list1 = favorit_list1.drop(i,0)

        # for i in range(len(reason_list1['횟수'])):
        #     if(reason_list1["횟수"][i] == 0):
        #         reason_list1 = reason_list1.drop(i,0)

        favorit = favorit_list2['횟수']
        favorit_label = favorit_list2['이유']

        reason = reason_list2['횟수']
        reason_label = reason_list2['행동']

        satis = satis_list["갯수"]
        satis_label = satis_list["전반적 만족도"]

        for i in range(len(favorit_list2['횟수'])):
            if(favorit_list2["횟수"][i] == 0):
                favorit_list2 = favorit_list2.drop(i,0)

        for i in range(len(reason_list2['횟수'])):
            if(reason_list2["횟수"][i] == 0):
                reason_list2 = reason_list2.drop(i,0)


        sns.barplot(x="계절",y="여행 횟수",data=month_list1,ax=self.ax)
        # sns.barplot(x="전반적 만족도", y="갯수", data=satis_list, ax=self.ax5)
        # month_list1.plot(x='계절',kind='bar',figsize=(3,2),ax=self.ax,rot=0)

        # rects = self.ax4.barh(reason_label,reason,align='center',height=0.5)
        # for i, rect in enumerate(rects):
        #     self.ax4.text(0.95 * rect.get_width(), rect.get_y() + rect.get_height() / 2.0, str(reason[i]) + '%',
        #             ha='right', va='center')

        self.ax3.pie(favorit,labels=favorit_label,rotatelabels=0,autopct='%.2f',textprops={'size': 'smaller'})
        self.ax4.pie(reason, labels=reason_label, rotatelabels=0,autopct='%.2f', textprops={'size': 'smaller'})
        self.ax5.pie(satis, labels=satis_label,rotatelabels=0,autopct='%.2f',textprops={'size': 'smaller'})

        lat = float(getlatlon["Latitude"])
        lon = float(getlatlon["Longitude"])



        map_folium = folium.Map(location=[lat,lon],zoom_start=10)

        dosimarker = recommand_csv.loc[recommand_csv["여행지"] == dosi+sigun, ["Latitude","Longitude"]]
        tripData = recommand_csv.loc[recommand_csv["여행지"] == dosi+sigun, ["장소","주소","상세설명"]]

        dosimarker = dosimarker.reset_index()
        del dosimarker["index"]

        tripData = tripData.reset_index()
        del tripData["index"]

        for i in range(len(tripData)):
            self.recommandTable.removeRow(i)

        for i2 in range(len(tripData)+1):
            self.recommandTable.setColumnCount(3)
            self.recommandTable.setRowCount(i2)

        column_headers = ['이름', '주소','설명']
        self.recommandTable.setHorizontalHeaderLabels(column_headers)

        for k in range(len(dosimarker)):
            folium.Marker(
                location=[dosimarker["Latitude"][k], dosimarker["Longitude"][k]],
                # popup = tripData["장소"][k],
                tooltip= tripData["장소"][k],
                icon=folium.Icon(color='red', icon='star')
            ).add_to(map_folium)

        map_folium.save('./Map/Map.html')

        self.foliumlayout.load(QUrl("file:///C:/Users/user/Desktop/TripProject1/venv/Scripts/design/Map/Map.html"))

        # self.ax3.legend(loc="best")
        # self.ax4.legend(loc="best")

        for col in range(len(tripData)):
            self.recommandTable.setItem(col, 0, QTableWidgetItem(tripData["장소"][col]))
            self.recommandTable.setItem(col, 1, QTableWidgetItem(tripData["주소"][col]))
            try:
                self.recommandTable.setItem(col, 2, QTableWidgetItem(tripData["상세설명"][col]))
            except TypeError:
                pass

        self.recommandTable.resizeColumnsToContents()
        self.recommandTable.resizeRowsToContents()

        self.ax3.axis=('equal')
        self.ax4.axis=('equal')
        self.ax5.axis=('equal')

        self.ax3.set_title(dosi+" "+sigun+"을(를) 간 이유")
        self.ax4.set_title(dosi + " " + sigun + "에서 주로 한 일")
        self.ax5.set_title(dosi + " "+ sigun + "의 만족도")

        month_list = []
        month_list1 = []

        favorit_list = []
        favorit_list1 = []

        reason_list = []
        reason_list1 = []

        satis_list = []

        lat = 0
        lon = 0

        self.fig.canvas.draw_idle()
        self.fig3.canvas.draw_idle()
        self.fig4.canvas.draw_idle()
        self.fig5.canvas.draw_idle()

    def rdGender(self):

        global gender
        if self.r_male.isChecked():
           gender = "남성"
        elif self.r_female.isChecked():
           gender = "여성"
        elif self.r_gender_all.isChecked():
           gender = "전체"

    def cbAge(self):
        global age
        age = self.agecomboBox.currentText()

    def cbAnal_season(self):
        global an_season
        an_season = self.analy_season.currentText()

    def cbAnal_trip_purpose(self):
        global an_trip_purpose
        an_trip_purpose = self.analy_trip_purpose.currentText()

    def cbAnal_transfer(self):
        global an_transfer
        an_transfer = self.analy_transfer.currentText()

    def cbAnal_gender(self):
        global an_gender
        an_gender = self.analy_gender.currentText()

    def cbAnal_s_fac(self):
        global an_s_fac
        an_s_fac = self.analy_s_fac.currentText()

    def cbAnal_house(self):
        global an_house
        an_house = self.analy_house.currentText()

    def cbAnal_local(self):
        global an_local
        an_local = self.analy_local.currentText()

    def cbAnal_gradu(self):
        global an_gradu
        an_gradu = self.analy_gradu.currentText()

    def cbAnal_last_stu(self):
        global an_last_stu
        an_last_stu = self.analy_last_stu.currentText()

    def cbAnal_dosi(self):
        global an_dosi
        an_dosi = self.analy_dosi.currentText()

    def cbAnal_age(self):
        global an_age
        an_age = self.analy_age.currentText()

    def cbAnal_sigun(self):
        global an_sigun
        an_sigun = self.analy_sigungu.currentText()

    def cbAnal_living(self):
        global an_living
        an_living = self.analy_living.currentText()

    def cbAnal_job(self):
        global an_job
        an_job = self.analy_job.currentText()

    def cbAnal_marry(self):
        global an_marry
        an_marry = self.analy_marry.currentText()

    def cbSigun(self):
        global sigun
        sigun = self.siguncomboBox.currentText()

    def Analy_cbSigun(self):
        global an_sigun
        an_sigun = self.analy_sigungu.currentText()

    def Analy_cbSi(self):

        global csv_2016,an_dosi,an_sigun

        if self.analy_dosi.currentText() == "경기":
            self.analy_sigungu.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['경기'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.analy_sigungu.addItem(boxIn[i])
        elif self.analy_dosi.currentText() == "서울":
            self.analy_sigungu.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['서울'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.analy_sigungu.addItem(boxIn[i])
        elif self.analy_dosi.currentText() == "강원":
            self.analy_sigungu.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['강원'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.analy_sigungu.addItem(boxIn[i])
        elif self.analy_dosi.currentText() == "충북":
            self.analy_sigungu.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['충북'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.analy_sigungu.addItem(boxIn[i])
        elif self.analy_dosi.currentText() == "충남":
            self.analy_sigungu.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['충남'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.analy_sigungu.addItem(boxIn[i])
        elif self.analy_dosi.currentText() == "전남":
            self.analy_sigungu.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['전남'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.analy_sigungu.addItem(boxIn[i])
        elif self.analy_dosi.currentText() == "전북":
            self.analy_sigungu.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['전북'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.analy_sigungu.addItem(boxIn[i])
        elif self.analy_dosi.currentText() == "경남":
            self.analy_sigungu.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['경남'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.analy_sigungu.addItem(boxIn[i])
        elif self.analy_dosi.currentText() == "경북":
            self.analy_sigungu.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['경북'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.analy_sigungu.addItem(boxIn[i])
        elif self.analy_dosi.currentText() == "인천":
            self.analy_sigungu.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['인천'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.analy_sigungu.addItem(boxIn[i])
        elif self.analy_dosi.currentText() == "대전":
            self.analy_sigungu.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['대전'])]["여행한 시/군"].unique()

            for i in range(len(boxIn)):
                self.analy_sigungu.addItem(boxIn[i])

        elif self.analy_dosi.currentText() == "광주":
            self.analy_sigungu.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['광주'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.analy_sigungu.addItem(boxIn[i])

        elif self.analy_dosi.currentText() == "부산":
            self.analy_sigungu.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['부산'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.analy_sigungu.addItem(boxIn[i])

        elif self.analy_dosi.currentText() == "제주":
            self.analy_sigungu.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['제주'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.analy_sigungu.addItem(boxIn[i])

        elif self.analy_dosi.currentText() == "대구":
            self.analy_sigungu.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['대구'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.analy_sigungu.addItem(boxIn[i])

        elif self.analy_dosi.currentText() == "울산":
            self.analy_sigungu.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['울산'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.analy_sigungu.addItem(boxIn[i])

        elif self.analy_dosi.currentText() == "세종":
            self.analy_sigungu.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['세종'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.analy_sigungu.addItem(boxIn[i])

        an_dosi = self.analy_dosi.currentText()

    def cbSi(self):
        global csv_2016,dosi,sigun

        if self.dosicomboBox.currentText() == "경기":
            self.siguncomboBox.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['경기'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.siguncomboBox.addItem(boxIn[i])
        elif self.dosicomboBox.currentText() == "서울":
            self.siguncomboBox.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['서울'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.siguncomboBox.addItem(boxIn[i])
        elif self.dosicomboBox.currentText() == "강원":
            self.siguncomboBox.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['강원'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.siguncomboBox.addItem(boxIn[i])
        elif self.dosicomboBox.currentText() == "충북":
            self.siguncomboBox.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['충북'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.siguncomboBox.addItem(boxIn[i])
        elif self.dosicomboBox.currentText() == "충남":
            self.siguncomboBox.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['충남'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.siguncomboBox.addItem(boxIn[i])
        elif self.dosicomboBox.currentText() == "전남":
            self.siguncomboBox.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['전남'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.siguncomboBox.addItem(boxIn[i])
        elif self.dosicomboBox.currentText() == "전북":
            self.siguncomboBox.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['전북'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.siguncomboBox.addItem(boxIn[i])
        elif self.dosicomboBox.currentText() == "경남":
            self.siguncomboBox.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['경남'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.siguncomboBox.addItem(boxIn[i])
        elif self.dosicomboBox.currentText() == "경북":
            self.siguncomboBox.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['경북'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.siguncomboBox.addItem(boxIn[i])
        elif self.dosicomboBox.currentText() == "인천":
            self.siguncomboBox.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['인천'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.siguncomboBox.addItem(boxIn[i])
        elif self.dosicomboBox.currentText() == "대전":
            self.siguncomboBox.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['대전'])]["여행한 시/군"].unique()

            for i in range(len(boxIn)):
                self.siguncomboBox.addItem(boxIn[i])

        elif self.dosicomboBox.currentText() == "광주":
            self.siguncomboBox.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['광주'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.siguncomboBox.addItem(boxIn[i])

        elif self.dosicomboBox.currentText() == "부산":
            self.siguncomboBox.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['부산'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.siguncomboBox.addItem(boxIn[i])

        elif self.dosicomboBox.currentText() == "제주":
            self.siguncomboBox.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['제주'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.siguncomboBox.addItem(boxIn[i])

        elif self.dosicomboBox.currentText() == "대구":
            self.siguncomboBox.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['대구'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.siguncomboBox.addItem(boxIn[i])

        elif self.dosicomboBox.currentText() == "울산":
            self.siguncomboBox.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['울산'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.siguncomboBox.addItem(boxIn[i])

        elif self.dosicomboBox.currentText() == "세종":
            self.siguncomboBox.clear()
            boxIn = csv_2016[csv_2016["여행한 도시"].isin(['세종'])]["여행한 시/군"].unique()
            for i in range(len(boxIn)):
                self.siguncomboBox.addItem(boxIn[i])

        dosi = self.dosicomboBox.currentText()

    def rdMonth(self):
        global month
        if self.r_one.isChecked():
           month = "봄"
        elif self.r_two.isChecked():
           month = "여름"
        elif self.r_three.isChecked():
           month = "가을"
        elif self.r_four.isChecked():
           month = "겨울"
        elif self.r_season_all.isChecked():
            month = "전체"

    def rdMarry(self):
        global marry
        if self.r_marry.isChecked():
           marry = "기혼"
        elif self.r_no_marry.isChecked():
           marry = "미혼"
        elif self.r_marry_all.isChecked():
            marry = "전체"

    def rdYear(self):
        global year
        if self.y_2016.isChecked():
           year = "2016"
        elif self.y_2017.isChecked():
           year = "2017"

    def searchOn(self):

        global age,gender,month,marry,year,csv_2016,mapDrawdata,year

        self.ax2.clear()
        self.fig2.clear()
        self.ax9.clear()
        self.fig9.clear()

        self.ax6.clear()
        self.fig6.clear()
        self.ax7.clear()
        self.fig7.clear()
        self.ax8.clear()
        self.fig8.clear()

        self.ax6 = self.fig6.add_subplot(111)
        self.ax7 = self.fig7.add_subplot(111)
        self.ax8 = self.fig8.add_subplot(111)


        # print("성별은 " + gender + " 분기는 " + month + " 나이는 " + age + " 년도는 " + year + " 결혼여부는 " + marry)

        mapDrawdata = dmo.getAlltrip(age,month,marry,gender,year)
        satisDrawdata = dmo.getAllSatisFaction(age,month,marry,gender,year)

        self.drawKorea('여행 지수', mapDrawdata, 'YlOrBr')
        self.drawKoreaSatis('만족도 지수',satisDrawdata,'Blues')

        month_list = dmo.getSpecMonth(age,month,marry,gender,year)
        favorit_list= dmo.getSpecMyFavorite(age,month,marry,gender,year)
        reason_list = dmo.getSpecReason(age,month,marry,gender,year)

        month_list1 = pd.DataFrame(month_list[0])
        month_list1['여행 횟수'] = month_list1[0]
        month_list1['계절'] = ['봄','여름','가을','겨울']

        month_list2 = pd.DataFrame(month_list[1])
        month_list2['여행 횟수'] = month_list2[0]
        month_list2['계절'] = ['봄','여름','가을','겨울']

        favorit_list1 = pd.DataFrame(favorit_list)

        favorit_list1['횟수'] = favorit_list1[0]

        favorit_list1['이유'] = ['볼거리 제공', '지명도', '없음', '기타', '경험자의 추천', '여행동반자', '음식',
                                 '이동거리', '편의시설', '시간', '여행경비', '숙박시설', '교통편', '쇼핑',
                                 '체험', '교육성']


        recom = favorit_list1['횟수'][4] + favorit_list1['횟수'][1]
        food_shopping = favorit_list1['횟수'][6] + favorit_list1['횟수'][13]
        cond = favorit_list1['횟수'][7] + favorit_list1['횟수'][9] + favorit_list1['횟수'][10] + favorit_list1['횟수'][12]
        exp = favorit_list1['횟수'][0] + favorit_list1['횟수'][14] + favorit_list1['횟수'][15]
        fac = favorit_list1['횟수'][8] + favorit_list1['횟수'][11]
        etc = favorit_list1['횟수'][3] + favorit_list1['횟수'][5]

        favorit_list2 = pd.DataFrame()

        favorit_list2['횟수'] = [recom,food_shopping,cond,exp,fac,etc]
        favorit_list2['이유'] = ['추천','음식/쇼핑','여건','문화/체험','편의시설','기타']

        reason_list1 = pd.DataFrame(reason_list)

        reason_list1['횟수'] = reason_list1[0]
        reason_list1['행동'] = ['자연 및 풍경 감상', '음식관광', '스포츠 활동', '유적지 방문',
                                '테마파크 방문', '휴식/휴양', '온천/스파', '쇼핑', '문화예술/공연 관람',
                                '스포츠 경기', '지역 축제/이벤트 참가', '교육/체험', '종교/성지순례', '겜블링', '시티투어',
                                '드라마 촬영지 방문', '지인 방문', '회의참가/시찰', '훈련/연수', '유흥/오락', '기타']



        r_amuse = reason_list1['횟수'][13] + reason_list1['횟수'][19] + reason_list1['횟수'][9]
        r_tour = reason_list1['횟수'][0] + reason_list1['횟수'][3] + reason_list1['횟수'][15] + reason_list1['횟수'][14] + reason_list1['횟수'][4]
        r_rest = reason_list1['횟수'][6] + reason_list1['횟수'][1] + reason_list1['횟수'][2] + reason_list1['횟수'][8]
        r_etc = reason_list1['횟수'][16]  + reason_list1['횟수'][20] + reason_list1['횟수'][12] + reason_list1['횟수'][17] + reason_list1['횟수'][18]
        r_shopping = reason_list1['횟수'][7]
        r_exp = reason_list1['횟수'][10] + reason_list1['횟수'][11]


        reason_list2 = pd.DataFrame()
        reason_list2['횟수'] = [r_amuse,r_tour,r_rest,r_etc,r_shopping,r_exp]
        reason_list2['행동'] = ['오락','투어','휴식','기타','쇼핑','체험']

        del month_list1[0]
        del month_list2[0]

        favorit = favorit_list2['횟수']
        favorit_label = favorit_list2['이유']

        reason = reason_list2['횟수']
        reason_label = reason_list2['행동']

        for i in range(len(favorit_list2['횟수'])):
            if(favorit_list2["횟수"][i] == 0):
                favorit_list2 = favorit_list2.drop(i,0)

        for i in range(len(reason_list2['횟수'])):
            if(reason_list2["횟수"][i] == 0):
                reason_list2 = reason_list2.drop(i,0)

        sns.barplot(x="계절",y="여행 횟수",data=month_list2,ax=self.ax8)
        self.ax7.pie(favorit, labels=favorit_label, rotatelabels=0, autopct='%.2f', textprops={'size': 'smaller'})
        self.ax6.pie(reason, labels=reason_label, rotatelabels=0, autopct='%.2f', textprops={'size': 'smaller'})


        self.ax6.axis=('equal')
        self.ax7.axis=('equal')

        self.ax6.set_title("여행지 를 간 이유")
        self.ax7.set_title("여행지 에서 주로 한 일")


        month_list = []
        month_list1 = []
        month_list2 = []

        favorit_list = []
        favorit_list1 = []
        favorit_list2 = []

        reason_list = []
        reason_list1 = []
        reason_list2 = []

        self.fig6.canvas.draw_idle()
        self.fig7.canvas.draw_idle()
        self.fig8.canvas.draw_idle()

        self.fig2.canvas.draw_idle()
        self.fig9.canvas.draw_idle()

        mapDrawdata = []
        satisDrawdata = []

    def Analysatis(self):
        global an_season,an_age,an_dosi,an_gender,an_job,an_living,an_marry,an_s_day,an_s_fac,an_sigun,an_transfer,an_trip_purpose,an_etc,an_exp,an_shopping,an_amuse,an_tour,an_rest,predmodel,an_local,an_house,an_family,an_last_stu,an_gradu,an_name

        an_s_day = self.analy_s_day.text()
        an_family = self.analy_family.text()
        an_name = self.edtname.text()


        an_s_day1 = int(an_s_day)
        an_family1 = int(an_family)

        analy_Data =[{'여행계절': an_season, '여행한 도시': an_dosi, '여행한 시/군' : an_sigun, '여행지 선택이유': an_trip_purpose,
                     '주요 이동(교통)수단': an_transfer, '숙박시설': an_s_fac,  '숙박일수': an_s_day1,
                     '오락': int(an_amuse),'투어' : int(an_tour), '휴식' : int(an_rest), '체험' : int(an_exp) , '쇼핑' : int(an_shopping) , '기타' : int(an_etc),
                     '나이': an_age, '성별' : an_gender, '거주시도' : an_living, '직업' : an_job, '혼인상태' : an_marry ,'가구원 수' : an_family1}]



        result = ranfor.predictSatisfaction(analy_Data,predmodel)

        your_satis = result[0]
        satisScale = result[1] / 20
        satisScale = round(satisScale,2)

        if your_satis == 1:
            if satisScale <= 1.0:
                self.result_label.setText(str(satisScale))
                self.lblimage.setPixmap(QPixmap(self.scale_1))
                self.lblexplain.setText(an_name+"님의 이번 여행에 있어서 매우 불만족 하실 확률이 높으시네요 다른 여행지를 가는 것을 추천드립니다. <br> 그러나 이 여행지를 가신다면 아래의 여행지를 추천드립니다.")
            elif satisScale <=2.0:
                self.result_label.setText(str(satisScale))
                self.lblimage.setPixmap(QPixmap(self.scale_2))
                self.lblexplain.setText(an_name+"님의 이번 여행에 있어서 불만족 하실 확률이 높으시네요 다른 여행지를 가는 것을 추천드립니다. <br>v하지만 이 지표가 늘 들어맞는 것은 아니니 가고싶으시면 가시는걸 추천드립니다.<br> 이 여행지를 가신다면 아래의 여행지를 추천드립니다.")
            elif satisScale <= 3.0:
                self.result_label.setText(str(satisScale))
                self.lblimage.setPixmap(QPixmap(self.scale_3))
                self.lblexplain.setText(an_name+"님의 이번 여행에 있어서 평범하게 보낼 것입니다. 평범하지만 기억에 남는 좋은 여행이 되실 수도 있습니다. <br> 이 여행지를 가신다면 아래의 여행지를 추천드립니다.")
            elif satisScale <= 4.0:
                self.result_label.setText(str(satisScale))
                self.lblimage.setPixmap(QPixmap(self.scale_4))
                self.lblexplain.setText(an_name+"님의 이번 여행에 있어서 충분히 만족 하실 수 있는 여행이 되실겁니다 지수의 수치가 대부분 좋게 나타나며 <br> 기억에 남는 좋은 여행이 되실겁니다. 좋은 추억 남기시길 바랍니다. <br> 이 여행지를 가신다면 아래의 여행지를 추천드립니다.")
            elif satisScale <= 5.0:
                self.result_label.setText(str(satisScale))
                self.lblimage.setPixmap(QPixmap(self.scale_5))
                self.lblexplain.setText(+an_name+"님의 이번 여행에 있어서 최고의 여행이 되실겁니다. 기억에 남는 좋은 추억 많이 남기시기 바랍니다.<br> 그러나 이 여행지를 가신다면 아래의 여행지를 추천드립니다.")

        tripData = recommand_csv.loc[recommand_csv["여행지"] == an_dosi + an_sigun, ["장소", "주소", "상세설명"]]
        tripData = tripData.reset_index()

        del tripData["index"]

        for i in range(len(tripData)):
            self.analy_recommandTable.removeRow(i)

        for i2 in range(len(tripData) + 1):
            self.analy_recommandTable.setColumnCount(3)
            self.analy_recommandTable.setRowCount(i2)

        column_headers = ['이름', '주소', '설명']
        self.analy_recommandTable.setHorizontalHeaderLabels(column_headers)

        for col in range(len(tripData)):
            self.analy_recommandTable.setItem(col, 0, QTableWidgetItem(tripData["장소"][col]))
            self.analy_recommandTable.setItem(col, 1, QTableWidgetItem(tripData["주소"][col]))
            try:
                self.analy_recommandTable.setItem(col, 2, QTableWidgetItem(tripData["상세설명"][col]))
            except TypeError:
                pass

        self.analy_recommandTable.resizeColumnsToContents()
        self.analy_recommandTable.resizeRowsToContents()

    def getcbAmuse(self):
        global an_amuse

        if self.cbAmuse.isChecked() == True:
            an_amuse = "1"
        else:
            an_amuse = "0"

    def getcbTour(self):
        global an_tour

        if self.cbTour.isChecked() == True:
            an_tour = "1"
        else:
            an_tour = "0"

    def getcbRest(self):
        global an_rest

        if self.cbRest.isChecked() == True:
            an_rest = "1"
        else:
            an_rest = "0"

    def getcbEtc(self):
        global an_etc

        if self.cbEtc.isChecked() == True:
            an_etc = "1"
        else:
            an_etc = "0"

    def getcbShopping(self):
        global an_shopping

        if self.cbShopping.isChecked() == True:
            an_shopping = "1"
        else:
            an_shopping = "0"

    def getcbExp(self):
        global an_exp

        if self.cbExp.isChecked() == True:
            an_exp = "1"
        else:
            an_exp = "0"

app = QApplication(sys.argv)
tourist = TouristDialog()
tourist.show()
app.exec_()
