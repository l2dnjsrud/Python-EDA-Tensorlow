# -*- coding: utf-8 -*-
"""6. 텐서플로를 통한 자동차 연비 데이터 예측-input.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1r6n8TKCXZNLstvvXPrESADaj3dymP5b2

## 텐서플로를 통한 자동차 연비 예측하기
* 참고 : [자동차 연비 예측하기: 회귀  |  TensorFlow Core](https://www.tensorflow.org/tutorials/keras/regression)

## 필요 도구 가져오기
"""

# 데이터 분석을 위한 pandas, 시각화를 위한 seaborn 불러오기
import pandas as pd
import seaborn as sns

"""## 데이터셋 로드"""

# 자동차연비 데이터셋인 mpg 데이터셋을 불러옵니다.
df = sns.load_dataset("mpg")
df.shape

"""## 결측치 확인"""

# 결측치의 합계 구하기
df.isna().sum()
df.shape

"""## 결측치 제거"""

# dropna로 결측치를 제거합니다.
df = df.dropna()
df.shape

"""## 수치 데이터만 가져오기
* 머신러닝이나 딥러닝 모델은 내부에서 수치계산을 하기 때문에 숫자가 아닌 데이터를 넣어주면 모델이 학습과 예측을 할 수 없습니다.
"""

# select_dtypes 를 통해 object 타입을 제외하고 가져옵니다.
df = df.select_dtypes(exclude="object")

"""## 전체 데이터에 대한 기술 통계 확인"""

# describe 를 통해 기술 통계값을 확인합니다.
df.describe(include="all")

"""## 데이터셋 나누기"""

# 전체 데이터프레임에서 df, train, test를 분리합니다.
# train_dataset : 학습에 사용 (예: 기출문제)
# test_dataset : 실제 예측에 사용 (예 : 실전문제)
# 기출문제로 공부하고 실전 시험을 보는 과정과 유사합니다.
train_dataset = df.sample(frac=0.8, random_state=42)
train_dataset.shape

test_dataset = df.drop(train_dataset.index)
test_dataset.shape

# train_dataset, test_dataset 에서 label(정답) 값을 꺼내 label 을 따로 생성합니다.
# 문제에서 정답을 분리하는 과정입니다.
# train_labels : train_dataset(예: 기출문제) 에서 정답을 꺼내서 분리합니다.
# test_labels : test_labels(예: 실전문제) 에서 정답을 꺼내서 분리합니다.
train_labels = train_dataset.pop("mpg")
train_labels.shape

test_labels = test_dataset.pop("mpg")
test_labels.shape

train_dataset.shape, test_dataset.shape

train_dataset.head(2)

train_labels.head(2)

"""## 딥러닝 모델 만들기
<img src="https://cs231n.github.io/assets/nn1/neural_net.jpeg" width="30%"> <img src="https://cs231n.github.io/assets/nn1/neural_net2.jpeg" width="40%">

* 이미지 출처 : https://cs231n.github.io/neural-networks-1/

* 두 개의 완전 연결(densely connected) 은닉층으로 Sequential 모델을 만들겠습니다. 
* 출력 층은 하나의 연속적인 값을 반환합니다. 
"""

# tensorflow 를 불러옵니다.
import tensorflow as tf
tf.__version__

"""### 딥러닝 층 구성"""

model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(64, activation="relu", input_shape=[len(train_dataset.keys())]))                          
model.add(tf.keras.layers.Dense(64, activation="relu"))
model.add(tf.keras.layers.Dense(64, activation="relu"))
model.add(tf.keras.layers.Dense(1))

"""### 모델 컴파일"""

model.compile(loss="mse", metrics=["mae", "mse"])

"""### 만든 모델 확인하기"""

model.summary()

"""## 딥러닝 모델로 학습하기"""

model.fit(train_dataset, train_labels, epochs=100, verbose=0)

"""## 딥러닝 모델로 평가하기"""

model.evaluate(test_dataset,test_labels)

"""## 딥러닝 모델의 예측하기"""

predict_labels = model.predict(test_dataset).flatten()
predict_labels[:5]

"""## 딥러닝 모델의 예측결과 평가하기"""

sns.jointplot(x=test_labels, y=predict_labels, kind="reg")

