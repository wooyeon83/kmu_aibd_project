# 정기 예금 가입 여부 예측 모델링

* 산출물 : 
  * 머신러닝_AutoML.pdf
  * Project_2Tream_ML_ver02_최고성능_20241127.ipynb

## 1. 프로젝트 개요

### 1.1 목적
* 국민대학교 대학원 머신러닝 과목 조별 과제 수행
* 은행 고객 데이터를 활용한 정기 예금 가입 여부 예측 모델 개발
* AutoML을 활용한 최적 모델 선정 및 성능 평가


## 2. 프로젝트 내용

### 2.1 연구 주제
정기 예금 가입 여부 예측 모델링

### 2.2 주요 연구 내용
* 은행 고객 데이터 탐색적 데이터 분석(EDA)
* 데이터 전처리 및 특성 공학
* 다양한 머신러닝 모델 학습 및 비교
* H2O AutoML을 활용한 최적 모델 선정
* 모델 성능 평가 및 최종 예측

### 2.3 기술 스택
* 데이터 처리: pandas, numpy
* 머신러닝: scikit-learn
* AutoML: H2O AutoML
* 시각화: matplotlib, seaborn
* 개발 환경: Jupyter Notebook

## 3. 데이터 구조

### 3.1 데이터셋
* train.csv: 학습용 데이터 (31,647건)
* test.csv: 테스트용 데이터 (13,564건)

### 3.2 주요 변수
| 변수명 | 데이터타입 | 설명 | 범주 값 |
|--------|-----------|------|---------|
| age | 수치형 | 나이 | - |
| job | 범주형 | 직업 | admin, management, technician, services 등 |
| marital | 범주형 | 결혼상태 | married, divorced, single |
| education | 범주형 | 학력 | unknown, secondary, primary, tertiary |
| default | 범주형 | 신용 채무 불이행 상태 | yes, no |
| balance | 수치형 | 연평균 잔액(유로) | - |
| housing | 범주형 | 주택대출 여부 | yes, no |
| loan | 범주형 | 개인대출 여부 | yes, no |
| contact | 범주형 | 최근 연락 방법 | unknown, telephone, cellular |
| duration | 수치형 | 최근 연락 시 통화 시간 | - |
| campaign | 수치형 | 이번 캠페인 연락 횟수 | - |
| pdays | 수치형 | 지난 캠페인 마지막 연락으로부터 경과 일수 | -1: 연락 없음 |
| poutcome | 범주형 | 이전 캠페인 참여 여부 | unknown, other, failure, success |
| label | 범주형 | 가입 여부(종속변수) | 가입(1), 미가입(0) |

## 4. 분석 과정

### 4.1 데이터 전처리
* 결측치 처리
* 범주형 변수 인코딩 (One-Hot Encoding, Label Encoding)
* 수치형 변수 스케일링
* 특성 선택 및 공학

### 4.2 모델링
* H2O AutoML을 활용한 자동 모델 탐색
* 다양한 알고리즘 비교 (GBM, XGBoost, DRF, StackedEnsemble 등)
* 교차 검증을 통한 모델 평가
* 최적 모델 선정

### 4.3 모델 평가
* AUC, 정확도, 정밀도, 재현율 등 다양한 지표 활용
* 최종 모델: StackedEnsemble (AUC: 0.615)

## 5. 주요 결과

### 5.1 모델 성능
* H2O AutoML을 통해 다양한 모델 학습 및 비교
* StackedEnsemble 모델이 최고 성능 달성
* 최종 모델의 예측 성능 평가 완료

### 5.2 인사이트
* 고객 특성별 정기 예금 가입 패턴 분석
* 마케팅 캠페인 효과성 평가
* 고객 세그먼트별 타겟팅 전략 수립 가능

