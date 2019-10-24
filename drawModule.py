# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets,uic

import pandas as pd
from pandas import Series
import numpy as np
import seaborn as sns

import TripModelWithRandomForestFunc as foresttest
from sklearn import preprocessing

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import style

import platform
import matplotlib.pyplot as plt

path = "c:/Windows/Fonts/malgun.ttf"
from matplotlib import font_manager, rc
if platform.system() == "Darwin":
    rc('font',family='AppleGothic')
elif platform.system() == 'Windows':
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
else:
    print('Unknown System.')


csv_2016 = pd.read_csv('./data/2016full.csv')
csv_2017 = pd.read_csv('./data/2017full.csv')
maphelper = pd.read_csv('./data/populationMergedWithID.csv')




def getLatLon(Sido,Sigungu):

    lonlat = []

    a1 = csv_2016.loc[csv_2016['여행한 도시'] == Sido ,["여행한 시/군","Latitude","Longitude"]]
    a2 = a1.loc[a1["여행한 시/군"] == Sigungu ,["Latitude","Longitude"]]

    a2 = a2.drop_duplicates()

    a2 = a2.reset_index()
    del a2["index"]

    lonlat1 = Series([a2["Latitude"][0],a2["Longitude"][0]],index=['Latitude','Longitude'])

    return lonlat1




def getMyFavorite(Sido ,Sigungu):

    favorit_list = []

    for j in range(len(csv_2016["여행지 선택이유 1순위"].unique())):
        a1 = csv_2016.loc[csv_2016['여행한 도시'] == Sido, ["여행한 도시", "여행한 시/군", "여행지 선택이유 1순위"]]
        a2 = a1.loc[csv_2016['여행한 시/군'] == Sigungu, ["여행한 시/군"]]
        a3 = a2.loc[csv_2016['여행지 선택이유 1순위'] == csv_2016['여행지 선택이유 1순위'].unique()[j]]
        a4 = int(a3.count())
        favorit_list.append(a4)

    return favorit_list

def getSatisFaction(Sido ,Sigungu):

    satis_list = []

    satis_data = []

    a1 = csv_2016.loc[csv_2016['여행한 도시'] == Sido, ["여행한 도시", "여행한 시/군", "전반적 만족도"]]
    a2 = a1.loc[a1['여행한 시/군'] == Sigungu, ["전반적 만족도"]]

    a2 = a2.reset_index()
    del a2["index"]

    for i in range(len(a2)):
        if a2["전반적 만족도"][i] == '없음':
            a2 = a2.drop(i, 0)

    a2 = a2.reset_index()
    del a2["index"]

    for j in range(len(a2["전반적 만족도"].unique())):
        a3 = a2.loc[a2["전반적 만족도"] == a2["전반적 만족도"].unique()[j]]
        a4 = int(a3.count())

        satis_data.append(a4)

    satis_label = a2["전반적 만족도"].unique()

    for k in range(len(satis_label)):
        if satis_label[k] == "1":
            satis_label[k] = "매우 불만족"
        if satis_label[k] == "2":
            satis_label[k] = "불만족"
        if satis_label[k] == "3":
            satis_label[k] = "보통"
        if satis_label[k] == "4":
            satis_label[k] = "만족"
        if satis_label[k] == "5":
            satis_label[k] = "매우 만족"

    satis_list = pd.DataFrame(satis_data ,index=satis_label ,columns=["갯수"])

    satis_list = satis_list.reset_index()

    satis_list.columns.values[0] = "전반적 만족도"

    return satis_list

def getReason(Sido ,Sigungu):

    reason_list = []

    for j in range(21):
        a1 = csv_2016.loc[csv_2016['여행한 도시'] == Sido, ["여행한 시/군", '자연 및 풍경 감상', '음식관광', '야외 위락 및 스포츠 활동', '역사유적지 방문',
                                                       '테마파크 놀이시설 동식물원 방문', '휴식/휴양', '온천/스파', '쇼핑', '지역 문화예술/공연/전시시설 관람',
                                                       '스포츠 경기 관람', '지역 축제/이벤트 참가', '교육/체험프로그램 참가', '종교/성지순례', '겜블링', '시티투어',
                                                       '드라마 촬영지 방문', '가족/친지/친구 방문', '회의참가/시찰', '교육/훈련/연수', '유흥/오락', '기타']]
        a2 = a1.loc[csv_2016['여행한 시/군'] == Sigungu, ["여행한 시/군", '자연 및 풍경 감상', '음식관광', '야외 위락 및 스포츠 활동', '역사유적지 방문',
                                                     '테마파크 놀이시설 동식물원 방문', '휴식/휴양', '온천/스파', '쇼핑', '지역 문화예술/공연/전시시설 관람',
                                                     '스포츠 경기 관람', '지역 축제/이벤트 참가', '교육/체험프로그램 참가', '종교/성지순례', '겜블링', '시티투어',
                                                     '드라마 촬영지 방문', '가족/친지/친구 방문', '회의참가/시찰', '교육/훈련/연수', '유흥/오락', '기타']]

        reason_1 = a2.loc[a2['자연 및 풍경 감상'] == "y"].count()
        reason_1 = reason_1["자연 및 풍경 감상"]

        reason_2 = a2.loc[a2['음식관광'] == "y"].count()
        reason_2 = reason_2["음식관광"]

        reason_3 = a2.loc[a2['야외 위락 및 스포츠 활동'] == "y"].count()
        reason_3 = reason_3["야외 위락 및 스포츠 활동"]

        reason_4 = a2.loc[a2['역사유적지 방문'] == "y"].count()
        reason_4 = reason_4["역사유적지 방문"]

        reason_5 = a2.loc[a2['테마파크 놀이시설 동식물원 방문'] == "y"].count()
        reason_5 = reason_5["테마파크 놀이시설 동식물원 방문"]

        reason_6 = a2.loc[a2['휴식/휴양'] == "y"].count()
        reason_6 = reason_6["휴식/휴양"]

        reason_7 = a2.loc[a2['온천/스파'] == "y"].count()
        reason_7 = reason_7["온천/스파"]

        reason_8 = a2.loc[a2['쇼핑'] == "y"].count()
        reason_8 = reason_8["쇼핑"]

        reason_9 = a2.loc[a2['지역 문화예술/공연/전시시설 관람'] == "y"].count()
        reason_9 = reason_9["지역 문화예술/공연/전시시설 관람"]

        reason_10 = a2.loc[a2['스포츠 경기 관람'] == "y"].count()
        reason_10 = reason_10["스포츠 경기 관람"]

        reason_11 = a2.loc[a2['지역 축제/이벤트 참가'] == "y"].count()
        reason_11 = reason_11["지역 축제/이벤트 참가"]

        reason_12 = a2.loc[a2['교육/체험프로그램 참가'] == "y"].count()
        reason_12 = reason_12["교육/체험프로그램 참가"]

        reason_13 = a2.loc[a2['종교/성지순례'] == "y"].count()
        reason_13 = reason_13["종교/성지순례"]

        reason_14 = a2.loc[a2['겜블링'] == "y"].count()
        reason_14 = reason_14["겜블링"]

        reason_15 = a2.loc[a2['시티투어'] == "y"].count()
        reason_15 = reason_15["시티투어"]

        reason_16 = a2.loc[a2['드라마 촬영지 방문'] == "y"].count()
        reason_16 = reason_16["드라마 촬영지 방문"]

        reason_17 = a2.loc[a2['가족/친지/친구 방문'] == "y"].count()
        reason_17 = reason_17["가족/친지/친구 방문"]

        reason_18 = a2.loc[a2['회의참가/시찰'] == "y"].count()
        reason_18 = reason_18["회의참가/시찰"]

        reason_19 = a2.loc[a2['교육/훈련/연수'] == "y"].count()
        reason_19 = reason_19["교육/훈련/연수"]

        reason_20 = a2.loc[a2['유흥/오락'] == "y"].count()
        reason_20 = reason_20["유흥/오락"]

        reason_21 = a2.loc[a2['기타'] == "y"].count()
        reason_21 = reason_21["기타"]

    reason_list = [reason_1 ,reason_2 ,reason_3 ,reason_4 ,reason_5 ,reason_6 ,reason_7 ,reason_8 ,reason_9 ,reason_10,
                   reason_11 ,reason_12 ,reason_13 ,reason_14 ,reason_15 ,reason_16 ,reason_17 ,reason_18 ,reason_19,
                   reason_20 ,reason_21]

    return reason_list

def getMonth(Sido ,Sigungu):

    month_list = []

    column1 = ['봄', '여름', '가을', '겨울']

    a1 = csv_2016.loc[csv_2016['여행한 도시'] == Sido, ["여행한 도시", "여행한 시/군", "여행 계절"]]
    a2 = a1.loc[csv_2016['여행한 시/군'] == Sigungu, ["여행한 시/군"]]

    for j in range(4):
        a3 = a2.loc[csv_2016["여행 계절"] == column1[j]]
        a4 = int(a3.count())
        month_list.append(a4)

    return month_list






def getSpecMyFavorite(age,month,marry,gender,year):

    favorit_list = []

    if year == '2016':
        csv = csv_2016
    elif year == '2017':
        csv  =csv_2017

    if age  == '전체':
        a1 = csv.loc[:, ["여행한 도시", "여행한 시/군","성별","여행 계절" ,"혼인상태","여행지 선택이유 1순위" ]]
    else:
        a1 = csv.loc[csv['나이'] == age, ["여행한 도시","여행한 시/군","성별","여행 계절" ,"혼인상태","여행지 선택이유 1순위" ]]

    if month == "전체":
        a2 = a1.loc[:, ["여행한 도시", "여행한 시/군","성별","혼인상태","여행지 선택이유 1순위" ]]
    else:
        a2 = a1.loc[a1['여행 계절'] == month, ["여행한 도시", "여행한 시/군","성별","혼인상태","여행지 선택이유 1순위" ]]

    if marry == "전체":
        a3 = a2.loc[:, ["여행한 도시","여행한 시/군","성별","여행지 선택이유 1순위" ]]
    else:
        a3 = a2.loc[a2["혼인상태"] == marry ,["여행한 도시","여행한 시/군","성별","여행지 선택이유 1순위" ]]

    if gender == "전체":
        a4 = a3.loc[:, ["여행한 도시","여행한 시/군","여행지 선택이유 1순위" ]]
    else:
        a4 = a3.loc[a3["성별"] == gender , ["여행한 도시","여행한 시/군","여행지 선택이유 1순위" ]]

    for j in range(len(csv_2016["여행지 선택이유 1순위"].unique())):
        a5 = a4.loc[a4['여행지 선택이유 1순위'] == csv_2016['여행지 선택이유 1순위'].unique()[j]]
        a6 = int(a5['여행지 선택이유 1순위'].count())
        favorit_list.append(a6)

    return favorit_list

def getSpecSatisFaction(age,month,marry,gender,year):

    satis_list = []

    satis_data = []

    if year == '2016':
        csv = csv_2016
    elif year == '2017':
        csv  =csv_2017

    if age == "전체":
        a1 = csv.loc[:, ["여행한 도시", "여행한 시/군","전반적 만족도","여행 계절","혼인상태","성별"]]
    else:
        a1 = csv.loc[csv["나이"] == age, ["여행한 도시", "여행한 시/군","전반적 만족도","여행 계절","혼인상태","성별"]]

    if month == "전체":
        a2 = a1.loc[:, ["여행한 도시", "여행한 시/군","전반적 만족도","혼인상태","성별"]]
    else:
        a2 = a1.loc[a1['여행 계절'] == month, ["여행한 도시", "여행한 시/군","전반적 만족도","혼인상태","성별"]]

    if marry == "전체":
        a3 = a2.loc[:, ["여행한 도시", "여행한 시/군","전반적 만족도","성별"]]
    else:
        a3 = a2.loc[a2["혼인상태"] == marry , ["여행한 도시", "여행한 시/군","전반적 만족도","성별"]]

    if gender == "전체":
        a4 = a3.loc[:, ["여행한 도시", "여행한 시/군","전반적 만족도"]]
    else:
        a4 = a3.loc[a3["성별"] == gender, ["여행한 도시", "여행한 시/군","전반적 만족도"]]


    a4 = a4.reset_index()
    del a4["index"]

    for i in range(len(a4)):
        if a4["전반적 만족도"][i] == '없음':
            a4 = a4.drop(i, 0)

    a4 = a4.reset_index()
    del a4["index"]

    for j in range(len(a4["전반적 만족도"].unique())):
        a5 = a4.loc[a4["전반적 만족도"] == a4["전반적 만족도"].unique()[j]]
        a6 = int(a5["전반적 만족도"].count())

        satis_data.append(a6)

    satis_label = a4["전반적 만족도"].unique()

    for k in range(len(satis_label)):
        if satis_label[k] == "1":
            satis_label[k] = "매우 불만족"
        if satis_label[k] == "2":
            satis_label[k] = "불만족"
        if satis_label[k] == "3":
            satis_label[k] = "보통"
        if satis_label[k] == "4":
            satis_label[k] = "만족"
        if satis_label[k] == "5":
            satis_label[k] = "매우 만족"

    satis_list = pd.DataFrame(satis_data ,index=satis_label ,columns=["갯수"])

    satis_list = satis_list.reset_index()

    satis_list.columns.values[0] = "전반적 만족도"

    return satis_list

def getSpecReason(age,month,marry,gender,year):

    reason_list = []

    if year == '2016':
        csv = csv_2016
    elif year == '2017':
        csv  =csv_2017


    for j in range(21):

        if age == "전체":
            a1 = csv.loc[:, ["여행한 시/군", '자연 및 풍경 감상', '음식관광', '야외 위락 및 스포츠 활동', '역사유적지 방문',
                                                       '테마파크 놀이시설 동식물원 방문', '휴식/휴양', '온천/스파', '쇼핑', '지역 문화예술/공연/전시시설 관람',
                                                       '스포츠 경기 관람', '지역 축제/이벤트 참가', '교육/체험프로그램 참가', '종교/성지순례', '겜블링', '시티투어',
                                                       '드라마 촬영지 방문', '가족/친지/친구 방문', '회의참가/시찰', '교육/훈련/연수', '유흥/오락', '기타',
                                                        '여행 계절','혼인상태','성별']]
        else:
            a1 = csv.loc[csv['나이'] == age, ["여행한 시/군", '자연 및 풍경 감상', '음식관광', '야외 위락 및 스포츠 활동', '역사유적지 방문',
                                                       '테마파크 놀이시설 동식물원 방문', '휴식/휴양', '온천/스파', '쇼핑', '지역 문화예술/공연/전시시설 관람',
                                                       '스포츠 경기 관람', '지역 축제/이벤트 참가', '교육/체험프로그램 참가', '종교/성지순례', '겜블링', '시티투어',
                                                       '드라마 촬영지 방문', '가족/친지/친구 방문', '회의참가/시찰', '교육/훈련/연수', '유흥/오락', '기타',
                                                        '여행 계절','혼인상태','성별']]

        if month == "전체":
            a2 = a1.loc[:, ["여행한 시/군", '자연 및 풍경 감상', '음식관광', '야외 위락 및 스포츠 활동', '역사유적지 방문',
                                                       '테마파크 놀이시설 동식물원 방문', '휴식/휴양', '온천/스파', '쇼핑', '지역 문화예술/공연/전시시설 관람',
                                                       '스포츠 경기 관람', '지역 축제/이벤트 참가', '교육/체험프로그램 참가', '종교/성지순례', '겜블링', '시티투어',
                                                       '드라마 촬영지 방문', '가족/친지/친구 방문', '회의참가/시찰', '교육/훈련/연수', '유흥/오락', '기타',
                                                        '혼인상태','성별']]
        else:
            a2 = a1.loc[a1['여행 계절'] == month, ["여행한 시/군", '자연 및 풍경 감상', '음식관광', '야외 위락 및 스포츠 활동', '역사유적지 방문',
                                                       '테마파크 놀이시설 동식물원 방문', '휴식/휴양', '온천/스파', '쇼핑', '지역 문화예술/공연/전시시설 관람',
                                                       '스포츠 경기 관람', '지역 축제/이벤트 참가', '교육/체험프로그램 참가', '종교/성지순례', '겜블링', '시티투어',
                                                       '드라마 촬영지 방문', '가족/친지/친구 방문', '회의참가/시찰', '교육/훈련/연수', '유흥/오락', '기타',
                                                        '혼인상태','성별']]

        if marry == "전체":
            a3 = a2.loc[:,  ["여행한 시/군", '자연 및 풍경 감상', '음식관광', '야외 위락 및 스포츠 활동', '역사유적지 방문',
                                                       '테마파크 놀이시설 동식물원 방문', '휴식/휴양', '온천/스파', '쇼핑', '지역 문화예술/공연/전시시설 관람',
                                                       '스포츠 경기 관람', '지역 축제/이벤트 참가', '교육/체험프로그램 참가', '종교/성지순례', '겜블링', '시티투어',
                                                       '드라마 촬영지 방문', '가족/친지/친구 방문', '회의참가/시찰', '교육/훈련/연수', '유흥/오락', '기타',
                                                        '성별']]
        else:
            a3 = a2.loc[a2["혼인상태"] == marry ,["여행한 시/군", '자연 및 풍경 감상', '음식관광', '야외 위락 및 스포츠 활동', '역사유적지 방문',
                                                       '테마파크 놀이시설 동식물원 방문', '휴식/휴양', '온천/스파', '쇼핑', '지역 문화예술/공연/전시시설 관람',
                                                       '스포츠 경기 관람', '지역 축제/이벤트 참가', '교육/체험프로그램 참가', '종교/성지순례', '겜블링', '시티투어',
                                                       '드라마 촬영지 방문', '가족/친지/친구 방문', '회의참가/시찰', '교육/훈련/연수', '유흥/오락', '기타',
                                                        '성별']]

        if gender == "전체":
            a4 = a3.loc[:, ["여행한 시/군", '자연 및 풍경 감상', '음식관광', '야외 위락 및 스포츠 활동', '역사유적지 방문',
                                                       '테마파크 놀이시설 동식물원 방문', '휴식/휴양', '온천/스파', '쇼핑', '지역 문화예술/공연/전시시설 관람',
                                                       '스포츠 경기 관람', '지역 축제/이벤트 참가', '교육/체험프로그램 참가', '종교/성지순례', '겜블링', '시티투어',
                                                       '드라마 촬영지 방문', '가족/친지/친구 방문', '회의참가/시찰', '교육/훈련/연수', '유흥/오락', '기타']]
        else:
            a4 = a3.loc[a3["성별"] == gender, ["여행한 시/군", '자연 및 풍경 감상', '음식관광', '야외 위락 및 스포츠 활동', '역사유적지 방문',
                                                       '테마파크 놀이시설 동식물원 방문', '휴식/휴양', '온천/스파', '쇼핑', '지역 문화예술/공연/전시시설 관람',
                                                       '스포츠 경기 관람', '지역 축제/이벤트 참가', '교육/체험프로그램 참가', '종교/성지순례', '겜블링', '시티투어',
                                                       '드라마 촬영지 방문', '가족/친지/친구 방문', '회의참가/시찰', '교육/훈련/연수', '유흥/오락', '기타']]


        reason_1 = a4.loc[a4['자연 및 풍경 감상'] == "y"].count()
        reason_1 = reason_1["자연 및 풍경 감상"]

        reason_2 = a4.loc[a4['음식관광'] == "y"].count()
        reason_2 = reason_2["음식관광"]

        reason_3 = a4.loc[a4['야외 위락 및 스포츠 활동'] == "y"].count()
        reason_3 = reason_3["야외 위락 및 스포츠 활동"]

        reason_4 = a4.loc[a4['역사유적지 방문'] == "y"].count()
        reason_4 = reason_4["역사유적지 방문"]

        reason_5 = a4.loc[a2['테마파크 놀이시설 동식물원 방문'] == "y"].count()
        reason_5 = reason_5["테마파크 놀이시설 동식물원 방문"]

        reason_6 = a4.loc[a4['휴식/휴양'] == "y"].count()
        reason_6 = reason_6["휴식/휴양"]

        reason_7 = a4.loc[a4['온천/스파'] == "y"].count()
        reason_7 = reason_7["온천/스파"]

        reason_8 = a4.loc[a4['쇼핑'] == "y"].count()
        reason_8 = reason_8["쇼핑"]

        reason_9 = a4.loc[a4['지역 문화예술/공연/전시시설 관람'] == "y"].count()
        reason_9 = reason_9["지역 문화예술/공연/전시시설 관람"]

        reason_10 = a4.loc[a4['스포츠 경기 관람'] == "y"].count()
        reason_10 = reason_10["스포츠 경기 관람"]

        reason_11 = a4.loc[a4['지역 축제/이벤트 참가'] == "y"].count()
        reason_11 = reason_11["지역 축제/이벤트 참가"]

        reason_12 = a4.loc[a4['교육/체험프로그램 참가'] == "y"].count()
        reason_12 = reason_12["교육/체험프로그램 참가"]

        reason_13 = a4.loc[a4['종교/성지순례'] == "y"].count()
        reason_13 = reason_13["종교/성지순례"]

        reason_14 = a4.loc[a4['겜블링'] == "y"].count()
        reason_14 = reason_14["겜블링"]

        reason_15 = a4.loc[a4['시티투어'] == "y"].count()
        reason_15 = reason_15["시티투어"]

        reason_16 = a4.loc[a4['드라마 촬영지 방문'] == "y"].count()
        reason_16 = reason_16["드라마 촬영지 방문"]

        reason_17 = a4.loc[a4['가족/친지/친구 방문'] == "y"].count()
        reason_17 = reason_17["가족/친지/친구 방문"]

        reason_18 = a4.loc[a4['회의참가/시찰'] == "y"].count()
        reason_18 = reason_18["회의참가/시찰"]

        reason_19 = a4.loc[a4['교육/훈련/연수'] == "y"].count()
        reason_19 = reason_19["교육/훈련/연수"]

        reason_20 = a4.loc[a4['유흥/오락'] == "y"].count()
        reason_20 = reason_20["유흥/오락"]

        reason_21 = a4.loc[a4['기타'] == "y"].count()
        reason_21 = reason_21["기타"]

    reason_list = [reason_1 ,reason_2 ,reason_3 ,reason_4 ,reason_5 ,reason_6 ,reason_7 ,reason_8 ,reason_9 ,reason_10,
                   reason_11 ,reason_12 ,reason_13 ,reason_14 ,reason_15 ,reason_16 ,reason_17 ,reason_18 ,reason_19,
                   reason_20 ,reason_21]

    return reason_list

def getSpecMonth(age,month,marry,gender,year):

    month_list = []
    month_list_all = []

    if year == '2016':
        csv = csv_2016
    elif year == '2017':
        csv  =csv_2017

    if age == "전체":
        a1 = csv.loc[:, ["여행한 도시", "여행한 시/군","여행 계절","혼인상태","성별"]]
    else:
        a1 = csv.loc[csv['나이'] == age, ["여행한 도시", "여행한 시/군","여행 계절","혼인상태","성별"]]

    if marry == "전체":
        a2 = a1.loc[:, ["여행한 도시", "여행한 시/군","여행 계절","성별"]]
    else:
        a2 = a1.loc[a1["혼인상태"] == marry , ["여행한 도시", "여행한 시/군","여행 계절","성별"]]

    if gender == "전체":
        a3 = a2.loc[:, ["여행한 도시", "여행한 시/군","여행 계절"]]
    else:
        a3 = a2.loc[a2["성별"] == gender,["여행한 도시", "여행한 시/군","여행 계절","성별"]]

    if month == "전체":
        a4 = a3.loc[:, ["여행한 도시", "여행한 시/군","여행 계절"]]
        a4_1 = a3.loc[:, ["여행한 도시", "여행한 시/군", "여행 계절"]]
    else:
        a4 = a3.loc[a3['여행 계절'] == month , ["여행한 도시","여행한 시/군","여행 계절"]]
        a4_1 = a3.loc[:, ["여행한 도시", "여행한 시/군", "여행 계절"]]

    column1 = ['봄', '여름', '가을', '겨울']
    for j in range(len(csv_2016["여행 계절"].unique())):

        a5 = a4.loc[a4["여행 계절"] == column1[j]]
        a5_1 = a4_1.loc[a4_1["여행 계절"] == column1[j]]

        a6 = int(a5["여행 계절"].count())
        a6_1 = int(a5_1["여행 계절"].count())


        month_list.append(a6)
        month_list_all.append(a6_1)

    return [month_list,month_list_all]



def getAllSatisFaction(age,month,marry,gender,year):

    satis_avg = []

    if year == '2016':
        csv = csv_2016
    elif year == '2017':
        csv  =csv_2017

    if gender == '전체':
        a1 = csv.loc[:,["전반적 만족도","여행한 도시" ,"여행한 시/군" ,"나이" ,"여행 계절" ,"혼인상태" ,"ID" ,"x" ,"y"]]
    else:
        a1 = csv.loc[csv["성별"] == gender, ["전반적 만족도","여행한 도시" ,"여행한 시/군" ,"나이" ,"여행 계절" ,"혼인상태" ,"ID" ,"x" ,"y"]]

    if month == '전체':
        a2 = a1.loc[:, ["전반적 만족도","여행한 도시" ,"여행한 시/군" ,"나이" ,"여행 계절" ,"혼인상태" ,"ID" ,"x" ,"y"]]
    else:
        a2 = a1.loc[a1["여행 계절"] == month, ["전반적 만족도","여행한 도시", "여행한 시/군" ,"나이" ,"혼인상태", "ID", "x", "y"]]

    if marry == '전체':
        a3 = a2.loc[:, ["전반적 만족도","여행한 도시", "여행한 시/군" ,"나이" ,"혼인상태", "ID", "x", "y"]]
    else:
        a3 = a2.loc[a2["혼인상태"] == marry, ["전반적 만족도","여행한 도시", "여행한 시/군" ,"나이" ,"ID", "x", "y"]]

    if age == '전체':
        a4 = a3.loc[:, ["전반적 만족도","여행한 도시" ,"여행한 시/군" ,"ID" ,"x" ,"y"]]
    else:
        a4 = a3.loc[a3["나이"] == age, ["전반적 만족도","여행한 도시" ,"여행한 시/군" ,"ID" ,"x" ,"y"]]


    a4 = a4.reset_index()
    del a4["index"]

    for i in range(len(a4)):
        if a4["전반적 만족도"][i] == '없음':
            a4 = a4.drop(i, 0)

    a4 = a4.reset_index()
    del a4["index"]

    a4["전반적 만족도"] = a4["전반적 만족도"].astype('float')

    a5 = a4.loc[:,["전반적 만족도", "ID"]]
    s1 = a5.groupby(["ID"], as_index=False).mean()

    s1.columns.values[1] = "평균 만족도"


    # satis_data = pd.merge(s1,a4,on="ID")

    data2 = pd.DataFrame(data={"ID": maphelper["ID"], "x": maphelper["x"], "y": maphelper["y"]})

    satis_data = pd.merge(s1, data2, how='right')
    satis_data = satis_data.fillna(0)

    col =["평균 만족도"]

    new_data = satis_data[col].values
    min_max_scaler = preprocessing.StandardScaler()

    new_data_scaled = min_max_scaler.fit_transform(new_data.astype(float))
    new_data_norm = pd.DataFrame(new_data_scaled, columns=col, index=satis_data.index)

    new_data_norm.columns.values[0] = "만족도 지수"
    new_data_norm['만족도 지수'] = (round(new_data_norm["만족도 지수"],2))

    satis_data2 = pd.concat([satis_data, new_data_norm], axis=1)

    return satis_data2

def getAlltrip(age, month, marry, gender,year):
    mapDrawdata = []

    if year == '2016':
        csv = csv_2016
    elif year == '2017':
        csv  =csv_2017

    cnt_trip = []
    if gender == '전체':
        a1 =csv.loc[:, ["여행한 도시" ,"여행한 시/군" ,"나이" ,"여행 계절" ,"혼인상태" ,"ID" ,"x" ,"y"]]
    else:
        a1 = csv.loc[csv["성별"] == gender, ["여행한 도시" ,"여행한 시/군" ,"나이" ,"여행 계절" ,"혼인상태" ,"ID" ,"x" ,"y"]]

    if month == '전체':
        a2 = a1.loc[:,["여행한 도시", "여행한 시/군" ,"나이" ,"혼인상태", "ID", "x", "y"]]
    else:
        a2 = a1.loc[a1["여행 계절"] == month, ["여행한 도시", "여행한 시/군" ,"나이" ,"혼인상태", "ID", "x", "y"]]

    if marry == '전체':
        a3 = a2.loc[:, ["여행한 도시", "여행한 시/군" ,"나이" ,"ID", "x", "y"]]
    else:
        a3 = a2.loc[a2["혼인상태"] == marry, ["여행한 도시", "여행한 시/군" ,"나이" ,"ID", "x", "y"]]

    if age == '전체':
        a4 = a3.loc[:,["여행한 도시" ,"여행한 시/군" ,"ID" ,"x" ,"y"]]
    else:
        a4 = a3.loc[a3["나이"] == age, ["여행한 도시" ,"여행한 시/군" ,"ID" ,"x" ,"y"]]

    a4 = a4.reset_index()

    del a4["index"]

    for j in range(len(a4["ID"].unique())):
        a5 = a4.loc[a4["ID"] == a4["ID"].unique()[j]]
        count = a5["ID"].count()
        cnt_trip.append(count)



    data = pd.DataFrame(data={"ID": a4["ID"].unique(), "여행지수": cnt_trip})

    data1 = pd.merge(a4, data, on='ID')

    data2 = pd.DataFrame(data={"ID": maphelper["ID"], "x": maphelper["x"], "y": maphelper["y"]})

    mapDrawdata = pd.merge(data1, data2, how='right')
    mapDrawdata = mapDrawdata.fillna(0)

    col = ["여행지수"]

    new_data = mapDrawdata[col].values
    min_max_scaler = preprocessing.StandardScaler()

    new_data_scaled = min_max_scaler.fit_transform(new_data.astype(float))
    new_data_norm = pd.DataFrame(new_data_scaled, columns=col, index=mapDrawdata.index)


    new_data_norm.columns.values[0] = "여행 지수"

    new_data_norm['여행 지수'] = (round(new_data_norm["여행 지수"],2))

    mapDrawdata2 = pd.concat([new_data_norm,mapDrawdata],axis=1)

    cnt_trip = []

    a1 = []
    a2 = []
    a3 = []
    a4 = []

    return mapDrawdata2