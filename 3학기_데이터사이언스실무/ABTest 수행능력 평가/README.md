# 웹 UI 개선을 위한 A/B/C 테스트 분석

* 산출물 : 
  * final_exam_abtest.ipynb
  * final_exam_abtest.html

## 1. 프로젝트 개요

### 1.1 목적
* 국민대학교 대학원 데이터사이언스 실무 과목 기말 과제 수행
* 웹사이트 개편을 위한 신규 디자인 효과성 검증
* 3가지 디자인 안 중 최적 디자인 선정을 위한 A/B/C 테스트 수행


## 2. 프로젝트 내용

### 2.1 연구 주제
웹 UI 개선을 위한 A/B/C 테스트 분석

### 2.2 주요 연구 내용
* ABTEST 적정 규모(기간, 샘플 사이즈) 설계
* MVT(Multi-Variate Test) 설계
* 데이터 전처리 및 로그 할당 오류 점검
* 모수/비모수, 연속형/이산형 검정 수행
* ABT Pair-wise 비교 및 사후검정법 적용
* 최종 디자인 선정 및 해석

### 2.3 기술 스택
* 데이터 처리: pandas, numpy
* 통계 분석: scipy.stats, statsmodels
* 시각화: matplotlib, seaborn, plotly
* 검정력 분석: statsmodels.stats.power
* 개발 환경: Jupyter Notebook

## 3. 데이터 구조

### 3.1 데이터셋
* final_exam_dataset.csv: AB테스트 로그 데이터 (585,652건)

### 3.2 주요 변수
| 변수명 | 데이터타입 | 설명 |
|--------|-----------|------|
| uno | 범주형 | 사용자 고유번호 |
| created_at | 날짜형 | 로그 생성 시간 |
| variation | 범주형 | 변형 그룹 (A, B, C) |
| release | 범주형 | 디자인 버전 (legacy_design, new_design_001, new_design_002, new_design_003) |
| clicked | 이산형 | 클릭 여부 (0: 미클릭, 1: 클릭) |
| purchase_amount | 연속형 | 구매 금액 |

## 4. 분석 과정

### 4.1 데이터 전처리
* 결측치 확인 및 처리
* 로그 할당 오류 점검 (사용자 중복 체크)
  * 다중 그룹 할당 사용자 제거 (1,998명)
  * 오류 데이터 정리
* 날짜별 로그 수 확인 및 이상치 검출

### 4.2 AB Test 설계
* 검정력 분석 (Power Analysis)
  * 유의수준 (α): 0.05
  * 검정력 (1-β): 0.8
  * MDE: 5% 향상
* 샘플 사이즈 계산
  * 모수 검정: NormalIndPower, TTestIndPower
  * 비모수 검정: Mann-Whitney U test
  * 범주형 검정: GofChisquarePower

### 4.3 통계 검정 수행
* **모수 검정**
  * 독립 표본 t-검정 (연속형 변수: 매출)
  * Z-검정 (이산형 변수: 클릭률)
* **비모수 검정**
  * Mann-Whitney U 검정 (매출 분포 비교)
  * 카이제곱 검정 (클릭률 독립성 검정)
* **Pair-wise 비교**
  * 각 디자인 간 쌍별 비교 분석
* **사후검정법**
  * 다중 비교 보정 (Multiple Comparison Correction)

## 5. 주요 결과

### 5.1 데이터 품질
* 초기 데이터: 585,652건
* 전처리 후: 581,656건 (다중 그룹 할당 사용자 제거)
* 오류 데이터 제거: 3,893건

### 5.2 검정 결과
* 클릭률: 디자인별 통계적으로 유의한 차이 확인
* 매출: 디자인별 비교 분석 수행
* 최종 디자인 선정 및 근거 제시
