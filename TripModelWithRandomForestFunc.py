# -*- coding:utf-8 -*-
#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import make_scorer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
import mapping as numericmap

import warnings
warnings.filterwarnings(module='sklearn*', action='ignore', category=DeprecationWarning)


# In[ ]:

# RMSLE 계산하는 사용자정의 함수
def rmsle(predicted_values, actual_values) :

        # 넘파이로 배열 형태로 변환
        predicted_values = np.array(predicted_values)
        actual_values = np.array(actual_values)

        # 예측값과 실제값에 1을 더하고 로그를 씌움
        log_predict = np.log(predicted_values + 1)
        log_actual = np.log(actual_values + 1)

        # 위에서 계산한 예측값에서 실제값을 빼주고 제곱을 함
        difference = log_predict - log_actual
        # difference = (log_predict - log_actual) ** 2
        difference = np.square(difference)

        # 평균값 구함
        mean_difference = difference.mean()

        # 다시 루트를 씌움
        score = np.sqrt(mean_difference)

        return score

def modelingPredictSaticefaction(self):
        rawData_org = pd.read_csv('./data/pretreatment_All.csv')

        # -----------------바뀐부분------------------
        feature_columns_to_use = ['여행계절', '여행지', '여행지 선택이유', '주요 이동(교통)수단','숙박시설', '숙박일수', '쇼핑','기타', '성별', '나이','거주시도', '직업', '가구원 수', '혼인상태', '오락', '투어','휴식', '체험', '만족도']
        # ------------------바뀐부분-------------------

        rawData = rawData_org[feature_columns_to_use]
        rawData = rawData.dropna()

        # 인덱스 재설정
        rawData.reset_index(inplace=True, drop=True)

        # -----------------바뀐부분------------------
        nonnumeric_columns = ['여행계절', '여행지', '여행지 선택이유', '주요 이동(교통)수단', '나이','숙박시설', '쇼핑', '기타', '성별', '거주시도', '직업', '혼인상태', '오락', '투어', '휴식', '체험', '만족도']
        # ------------------바뀐부분-------------------

        le = LabelEncoder()
        for feature in nonnumeric_columns:
                rawData[feature] = le.fit_transform(rawData[feature])
        # 소스 데이터프레임에서 분류(classification)을 위한 속성 집합
        X = rawData.loc[:, feature_columns_to_use[:-1]]
        y = rawData.loc[:, '만족도']  # 분류 클래스(class)
        # 자동으로 데이터셋을 트레이닝셋과 테스트셋으로 분리해주는 함수로
        # 트레이닝셋과 데이터셋의 비율을 7:3으로 세팅함
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
        # RMSLE 계산
        rmsle_scorer = make_scorer(rmsle)
        # DecisionTreeClassifier() : 의사결정트리를 생성하는 함수
        random_forest = RandomForestClassifier(n_estimators=20, random_state=0)
        # KFold 교차검증
        k_fold = KFold(n_splits=10, shuffle=True, random_state=0)
        # 트레이닝셋에 대한 KFold 교차검증 수
        score = cross_val_score(random_forest, X_train, y_train, cv=k_fold, scoring=rmsle_scorer)
        score = score.mean()
        # 0에 근접할수록 좋은 데이터
        # print("Score= {0:.5f}".format(score))
        # fit() : 트레이닝 데이터셋을 대상으로 의사결정트리 학습 진행
        random_forest.fit(X_train, y_train)
        y_pred_tr = random_forest.predict(X_test)
        y_pred_tr_prob = random_forest.predict_proba(X_test)
        # accuracy_score() 함수를 활용하여 테스트셋의 실제 클래스와 예측된 클래스 간 정확도 측정
        print('Accuracy: %.2f' % accuracy_score(y_test, y_pred_tr))  # 이 값을 사용자화면에 보여주기

        # modeling complete
        return [random_forest, accuracy_score(y_test, y_pred_tr)]

def predictSatisfaction(user,random_forestWithAccuracy):
        # dict 형태로 옴

        # user 전처리  여행한 도시, 여행한 시군이 오면 하나로 합치는 작업을 해야함

        user = pd.DataFrame.from_dict(user)
        #     user['여행지'] = np.nan
        user['여행지'] = user['여행한 도시'] + user['여행한 시/군']
        del user['여행한 도시']
        del user['여행한 시/군']

        #mapping 처리

        mappingData = numericmap.getMapping()

        user = user.to_dict('records')[0]
        for k, v in user.items():
                for mapValue in mappingData.values():
                        for keys, value in mapValue.items():
                                if v == keys:
                                        user[k] = value

        user = pd.DataFrame.from_dict([user])

        # index 0 에서 예측 : 형태로 0(불만족) or 1(만족)
        # index[1] 에서 만족도 : % 형태로 리턴됨

        predict = random_forestWithAccuracy[0].predict(user)[0]

        if predict == 1:
            predict_proba = random_forestWithAccuracy[0].predict_proba(user)[0][1] * 100
        else:
            predict_proba = random_forestWithAccuracy[0].predict_proba(user)[0][0] * 100


        return [predict, predict_proba]

    # 속성(feature) 별 중요도를 보여주는 데이터프레임
def feature_importances(random_forestWithAccuracy):
        feature_columns_to_use = ['여행계절', '여행지', '여행지 선택이유', '주요 이동(교통)수단',
                                  '숙박시설', '숙박일수', '쇼핑', '기타', '성별', '나이', '거주시도', '직업', '가구원 수', '혼인상태', '오락', '투어',
                                  '휴식', '체험', '만족도']
        sel_feature = pd.DataFrame({'중요도': random_forestWithAccuracy[0].feature_importances_},
                                   index=feature_columns_to_use[:-1])

        # 중요도의 내림차순으로 정렬
        return sel_feature.sort_values(by='중요도', ascending=False)
