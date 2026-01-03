# NCF with Side Information 확장 실험

* 산출물 : 
  * NCF_보고서.pdf
  * NCF_base_참고.ipynb
  * negative_sampling_참고.ipynb
  * 실험1_Addition조합.ipynb
  * 실험2_Concat조합.ipynb
  * 실험3_Addition최적화.ipynb
  * 실험4_Concat참여전략.ipynb

## 1. 프로젝트 개요

### 1.1 목적
* 국민대학교 대학원 추천시스템 과목 개인 과제 수행
* NCF(Neural Collaborative Filtering) 모델에 Side Information 통합
* 부가 정보(Category, Author, Publisher)를 활용한 추천 성능 개선 실험
* 다양한 조합 방식 및 최적화 전략 탐색

### 1.2 연구 배경
* 협업 필터링의 Cold Start 문제 해결 필요
* 아이템 메타데이터를 활용한 추천 성능 향상
* Side Information 통합 방식(Addition vs Concatenation) 비교
* 도서 추천 시스템에 특화된 실험 설계

## 2. 프로젝트 내용

### 2.1 연구 주제
NCF with Side Information 확장 실험

### 2.2 주요 연구 내용
* 기본 NCF 모델 구현 및 이해
* Side Information 임베딩 설계
* Addition 방식과 Concatenation 방식 비교
* 최적 Side Information 조합 탐색
* 임베딩 차원 할당 전략 연구
* 가중치 기반 조합 최적화

### 2.3 기술 스택
* 딥러닝 프레임워크: PyTorch
* 데이터 처리: pandas, numpy
* 성능 평가: sklearn.metrics
* 개발 환경: Google Colab, Jupyter Notebook

## 3. 데이터셋

### 3.1 도서 거래 데이터
* 데이터 파일: `book_transactions_8m.csv`
* 전처리 데이터: `book_train_test_1v3.pkl`
* 사용자 수: 9,057명
* 아이템 수: 26,695개
* 데이터 분할: Train 75%, Test 25% (1:3 비율)

### 3.2 Side Information
* **Category**: 도서 카테고리 정보
* **Author**: 작가 정보
* **Publisher**: 출판사 정보
* 각 Side Information은 고유 ID로 인코딩되어 사용

## 4. NCF 모델 구조

### 4.1 기본 NCF
* **GMF (Generalized Matrix Factorization)**: 선형적 상호작용 모델링
  * 유저 벡터와 아이템 벡터의 원소별 곱셈
* **MLP (Multi-Layer Perceptron)**: 비선형적 상호작용 학습
  * 유저 벡터와 아이템 벡터의 연결 후 은닉층 통과
* **NeuMF**: GMF와 MLP의 출력 결합

### 4.2 Side Information 통합 방식

#### Addition 방식
* 임베딩 벡터의 합 연산
* `enriched = item_emb + side_info_embs`
* 모든 임베딩 차원이 동일해야 함

#### Concatenation 방식
* 임베딩 벡터의 연결 연산
* `enriched = concat([item_emb, side_info_embs])`
* 차원이 달라도 가능

## 5. 실험 설계

### 5.1 실험 1: Addition 방식 조합 분석
* 목표: Addition 방식에서 최적 Side Information 조합 탐색
* 실험 케이스 (7가지):
  * 케이스1: Item + Category
  * 케이스2: Item + Author
  * 케이스3: Item + Publisher
  * 케이스4: Item + Category + Author
  * 케이스5: Item + Category + Publisher
  * 케이스6: Item + Author + Publisher
  * 케이스7: Item + Category + Author + Publisher (Full)

### 5.2 실험 2: Concatenation 방식 조합 분석
* 목표: Concatenation 방식에서 최적 Side Information 조합 탐색
* 실험 1과 동일한 7가지 조합 적용
* Concatenation 방식의 성능 비교

### 5.3 실험 3: Addition 방식 최적화
* 목표: 실험 1의 최적 조합에 대한 세부 튜닝
* 최적 조합: 케이스7 (Item + Category + Author + Publisher)
* 최적화 전략:
  * 전략 A: 단순 합 (Sum)
  * 전략 B: 평균 (Average)
  * 전략 C: 가중 합 (Weighted Sum) - 3가지 조합

### 5.4 실험 4: Concatenation 차원 전략
* 목표: 실험 2의 최적 조합에 대한 임베딩 차원 할당 전략
* 최적 조합: 케이스4 (Item + Category + Author)
* 차원 전략:
  * 전략 A: 동일 차원 (Uniform) - 8차원씩
  * 전략 B: 차등 차원1 (중요도 기반) - Item:16, Category:8, Author:12
  * 전략 C: 차등 차원2 (균형 조정) - Item:12, Category:10, Author:10

## 6. 모델 하이퍼파라미터

### 6.1 기본 설정
* `GMF_DIM`: 8 (GMF 임베딩 차원)
* `MLP_DIM`: 8 (MLP 임베딩 차원)
* `MLP_LAYERS`: [64, 32, 16, 8] (MLP 은닉층 구조)
* `BATCH_SIZE`: 128
* `EPOCHS`: 20 (Early Stopping 적용)
* `LR`: 1e-4 (학습률)
* `DROPOUT_RATE`: 0.3
* `PATIENCE`: 3 (Early Stopping patience)

### 6.2 평가 지표
* `TOP_K`: 10 (NDCG@10, Recall@10, Precision@10)
* Negative Sampling을 통한 평가 데이터 구성

## 7. 주요 결과

### 7.1 조합 방식 비교
* Addition vs Concatenation 방식 성능 비교
* 각 방식에서 최적 Side Information 조합 선정

### 7.2 최적화 효과
* 가중치 기반 조합의 성능 향상
* 차원 할당 전략에 따른 성능 변화
* 최종 최적 모델 구성

## 8. 문서 구조

### 8.1 보고서
* NCF_보고서.pdf
  * 실험 설계 및 방법론
  * 실험 결과 분석
  * 결론 및 향후 연구 방향

### 8.2 참고 코드
* NCF_base_참고.ipynb: 기본 NCF 모델 구현
* negative_sampling_참고.ipynb: 네거티브 샘플링 구현

### 8.3 실험 코드
* 실험1_Addition조합.ipynb: Addition 방식 조합 실험
* 실험2_Concat조합.ipynb: Concatenation 방식 조합 실험
* 실험3_Addition최적화.ipynb: Addition 방식 최적화 실험
* 실험4_Concat참여전략.ipynb: Concatenation 차원 전략 실험

