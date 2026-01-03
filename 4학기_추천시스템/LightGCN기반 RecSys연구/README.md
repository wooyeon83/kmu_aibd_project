# LightGCN 기반 추천시스템 연구

* 산출물 : 
  * (2020 GCN) LightGCN - Simplifying and Powering Graph Convolution Network for Recommendation.pdf
  * 9조 RecSys_Proposal.pdf
  * LightGCN_Cornac.ipynb

## 1. 프로젝트 개요

### 1.1 목적
* 국민대학교 대학원 추천시스템 과목 조별 과제 수행
* LightGCN 기반 추천시스템 구현 및 성능 개선 실험
* 그래프 신경망을 활용한 협업 필터링 추천 모델 연구

### 1.2 연구 배경
* 기존 GCN 기반 추천 모델의 복잡성 문제
* LightGCN의 단순화된 아키텍처를 통한 성능 향상
* 그래프 구조를 활용한 사용자-아이템 상호작용 학습
* 추천시스템 성능 평가 및 비교 분석

## 2. 프로젝트 내용

### 2.1 연구 주제
LightGCN 기반 추천시스템 연구

### 2.2 주요 연구 내용
* LightGCN 모델 아키텍처 이해 및 구현
* Cornac 프레임워크를 활용한 모델 학습
* 다양한 하이퍼파라미터 조정 실험
* 성능 평가 지표 비교 분석 (NDCG, Recall, Precision 등)
* 기존 추천 모델과의 성능 비교

### 2.3 기술 스택
* 추천시스템 프레임워크: Cornac
* 그래프 신경망: LightGCN
* 딥러닝 프레임워크: PyTorch
* 그래프 라이브러리: DGL (Deep Graph Library)
* 데이터 처리: pandas, numpy
* 개발 환경: Jupyter Notebook

## 3. 데이터셋

### 3.1 MovieLens 100K
* 사용자 수: 943명
* 아이템 수: 1,651개
* 평점 데이터: 100,000개
* 평점 범위: 1.0 ~ 5.0
* 데이터 분할: Train 80%, Test 20%

### 3.2 데이터 전처리
* 긍정적 상호작용 기준: 4점 이상 (rating_threshold=4.0)
* 사용자-아이템 상호작용 그래프 구성
* 학습/테스트 데이터 분할

## 4. LightGCN 모델

### 4.1 모델 특징
* 단순화된 그래프 컨볼루션 네트워크
* 불필요한 특징 변환 및 비선형 활성화 함수 제거
* 그래프 구조를 통한 사용자-아이템 임베딩 학습
* 다층 그래프 전파를 통한 고차원 연결 정보 활용

### 4.2 주요 하이퍼파라미터
* `num_layers`: 그래프 전파 레이어 수 (기본값: 3)
* `embedding_dim`: 임베딩 차원
* `learning_rate`: 학습률
* `reg`: 정규화 계수

## 5. 평가 지표

### 5.1 추천 성능 지표
* **NDCG** (Normalized Discounted Cumulative Gain): 순위 품질 평가
* **Recall**: 재현율 (관련 아이템 중 추천된 비율)
* **Precision**: 정밀도 (추천된 아이템 중 관련 아이템 비율)

### 5.2 평점 예측 지표
* **MAE** (Mean Absolute Error): 평균 절대 오차
* **RMSE** (Root Mean Square Error): 평균 제곱근 오차

## 6. 실험 결과

### 6.1 모델 성능
* 다양한 하이퍼파라미터 조합에 대한 실험 수행
* 레이어 수, 임베딩 차원 등에 따른 성능 변화 분석
* 최적 하이퍼파라미터 탐색

### 6.2 비교 분석
* 기존 추천 모델과의 성능 비교
* LightGCN의 장단점 분석
* 실무 적용 가능성 평가

## 7. 문서 구조

### 7.1 논문
* (2020 GCN) LightGCN - Simplifying and Powering Graph Convolution Network for Recommendation.pdf
  * LightGCN 논문 원본
  * 모델 아키텍처 및 이론적 배경

### 7.2 연구 제안서
* 9조 RecSys_Proposal.pdf
  * 연구 목적 및 배경
  * 실험 설계 및 방법론
  * 예상 결과 및 기대 효과

### 7.3 구현 코드
* LightGCN_Cornac.ipynb
  * Cornac 프레임워크를 활용한 LightGCN 구현
  * 데이터 로드 및 전처리
  * 모델 학습 및 평가
  * 성능 개선 실험

## 8. 참고사항

* 본 프로젝트는 교육 목적으로 수행된 연구입니다.
* 모델 성능은 데이터셋의 특성과 하이퍼파라미터 설정에 크게 의존합니다.
* 실제 서비스 적용 시 Cold Start 문제 및 확장성 고려가 필요합니다.

