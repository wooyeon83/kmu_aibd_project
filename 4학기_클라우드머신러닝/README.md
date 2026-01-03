# AWS SageMaker를 활용한 클라우드 머신러닝 실습

* 산출물 : 
  * 01_SageMaker_xgboost.ipynb
  * 02_SageMaker_LightGBM.ipynb
  * 03_SageMaker_CatBoost.ipynb
  * 04_SageMaker_BatchTransformer.ipynb

## 1. 프로젝트 개요

### 1.1 목적
* 국민대학교 대학원 클라우드머신러닝 과목 과제 수행
* AWS SageMaker를 활용한 클라우드 기반 머신러닝 파이프라인 구축
* 다양한 머신러닝 알고리즘의 클라우드 배포 및 운영 실습
* 실시간 추론 및 배치 추론 구현

### 1.2 연구 배경
* 클라우드 기반 머신러닝 서비스의 확산
* AWS SageMaker의 관리형 ML 서비스 활용
* 모델 학습, 배포, 모니터링의 통합 플랫폼 경험
* 실무에서 요구되는 클라우드 ML 운영 역량 강화

## 2. 프로젝트 내용

### 2.1 연구 주제
AWS SageMaker를 활용한 클라우드 머신러닝 실습

### 2.2 주요 연구 내용
* AWS SageMaker 환경 설정 및 구성
* S3 데이터 로드 및 전처리
* 다양한 ML 알고리즘 학습 (XGBoost, LightGBM, CatBoost)
* 모델 엔드포인트 배포 및 실시간 추론
* 배치 추론(Batch Transform) 구현
* 모델 성능 평가 및 비교 분석

### 2.3 기술 스택
* 클라우드 플랫폼: AWS SageMaker
* ML 알고리즘: XGBoost, LightGBM, CatBoost
* 데이터 저장: Amazon S3
* 데이터 처리: pandas, numpy, awswrangler
* 시각화: matplotlib, seaborn, plotly
* 개발 환경: SageMaker Notebook Instance

## 3. 데이터셋

### 3.1 서울 자전거 공유 데이터
* 데이터 파일: `SeoulBikeData.csv`
* 데이터 크기: 8,760행 (시간당 데이터)
* 주요 변수:
  * **종속변수**: Rented Bike Count (시간당 자전거 대여 수)
  * **독립변수**: 
    * 시간 정보: Hour, Date, Seasons
    * 날씨 정보: Temperature, Humidity, Wind speed, Visibility, Solar Radiation
    * 강수 정보: Rainfall, Snowfall
    * 기타: Holiday, Functioning Day

### 3.2 데이터 전처리
* 날짜/시간 변수 변환 및 파생 변수 생성
* 범주형 변수 인코딩
* 결측치 처리
* 학습/검증/테스트 데이터 분할

## 4. 실습 내용

### 4.1 실습 1: XGBoost 회귀 모델
* **목표**: 시간당 자전거 대여 수 예측
* **모델 타입**: 회귀 (Regression)
* **평가 지표**: MSE, RMSE, MAE, R²
* **주요 내용**:
  * XGBoost 내장 알고리즘을 사용한 모델 학습
  * SageMaker 엔드포인트 배포
  * 실시간 추론 수행
  * 실제값 vs 예측값 시각화

### 4.2 실습 2: LightGBM 분류 모델
* **목표**: 높은 수요 vs 낮은 수요 분류
* **모델 타입**: 분류 (Classification)
* **평가 지표**: Accuracy, Precision, Recall, F1-Score, AUC
* **주요 내용**:
  * LightGBM 내장 알고리즘을 사용한 모델 학습
  * 엔드포인트 배포 및 추론
  * 혼동 행렬(Confusion Matrix) 시각화
  * 분류 성능 평가

### 4.3 실습 3: CatBoost 분류 모델
* **목표**: 높은 수요 vs 낮은 수요 분류
* **모델 타입**: 분류 (Classification)
* **평가 지표**: Accuracy, Precision, Recall, F1-Score, AUC
* **주요 내용**:
  * CatBoost 내장 알고리즘을 사용한 모델 학습
  * LightGBM vs CatBoost 성능 비교 분석
  * 혼동 행렬 시각화
  * 모델 선택 및 최적화

### 4.4 실습 4: 배치 트랜스포머 (Batch Transformer)
* **목표**: 대량 데이터에 대한 배치 예측
* **모델**: XGBoost 내장 알고리즘
* **주요 내용**:
  * RecordIO 형식으로 데이터 변환
  * 배치 추론 작업 생성 및 실행
  * 배치 예측 결과 분석
  * 실시간 추론 vs 배치 추론 비교

## 5. SageMaker 주요 기능

### 5.1 모델 학습
* 내장 알고리즘 활용 (XGBoost, LightGBM, CatBoost)
* 하이퍼파라미터 튜닝
* 학습 작업 관리 및 모니터링

### 5.2 모델 배포
* 실시간 엔드포인트 배포
* 배치 변환 작업 생성
* 엔드포인트 관리 및 스케일링

### 5.3 데이터 관리
* S3 데이터 저장 및 로드
* 학습/검증/테스트 데이터 분할
* RecordIO 형식 변환

## 6. 평가 지표

### 6.1 회귀 모델
* **MSE** (Mean Squared Error): 평균 제곱 오차
* **RMSE** (Root Mean Squared Error): 평균 제곱근 오차
* **MAE** (Mean Absolute Error): 평균 절대 오차
* **R²** (R-squared): 결정 계수

### 6.2 분류 모델
* **Accuracy**: 정확도
* **Precision**: 정밀도
* **Recall**: 재현율
* **F1-Score**: F1 점수
* **AUC**: ROC 곡선 아래 면적

## 7. 주요 결과

### 7.1 모델 성능
* 각 알고리즘별 성능 평가 및 비교
* 하이퍼파라미터 최적화 결과
* 모델 선택 및 배포 결정

### 7.2 클라우드 운영
* SageMaker를 통한 모델 학습 및 배포 경험
* 실시간 추론 및 배치 추론 구현
* 클라우드 기반 ML 파이프라인 구축

## 8. 참고사항

* 본 프로젝트는 교육 목적으로 수행된 과제입니다.
* AWS 계정 및 SageMaker 접근 권한이 필요합니다.
* S3 버킷 및 데이터 경로는 프로젝트별로 다를 수 있습니다.
* 모델 엔드포인트 사용 시 비용이 발생할 수 있으므로 사용 후 삭제를 권장합니다.

