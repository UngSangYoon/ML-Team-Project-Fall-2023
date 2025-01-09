# 축구 경기 결과 예측 프로젝트

Player stat(성적)에 기반하여 축구 경기 결과를 예측하는 모델입니다. numpy로 구현된 Logistic Regression, Artificial Neural Network 모델로 이루어져 있습니다.

### Player stat 에 기반한 축구 경기 결과 예측  
**팀원:** 김동희, 윤웅상, 유준상, 정진홍  

---

## 프로젝트 개요  
- **목표:** 경기 시작 전 선발 명단만으로 유의미한 경기 결과 예측  
- **구현 환경:**  
  - Integrated Development Environment: Visual Studio Code  
  - Python 3.11.4  
  - Numpy 패키지 사용  

---

## Data  
- **Input Features:**  
  - 팀 스탯: 8개  
  - 골키퍼 스탯: 5개  
  - 필드 플레이어 스탯: 14개  
  - 총 153개 feature (홈 팀, 어웨이 팀 각각 포함)  
  - Input Size: 306 (153 x 2)  
  - Data Type: float  
  - 학습 전 Normalization 적용  
- **Output:**  
  - 홈 팀 득점수  
  - 어웨이 팀 득점수  

---

## Data 출처  
- **FBREF 사이트:** Stats 크롤링  
- **Kaggle:** Match line-up 데이터  
- 선수 이름으로 매핑하여 match 별 player stat 데이터 생성  
- **시즌 범위:** 2017/18~2021/22 (총 1892개 데이터 이용)  
- **Reference Links:**  
  - Line-up 데이터: [Kaggle Dataset](https://www.kaggle.com/datasets/josephvm/english-premier-league-game-events-and-results?select=matches.csv)  
  - 시즌별 Stats: [FBREF](https://fbref.com/en/comps/9/history/Premier-League-Seasons)  

---

## Models  

### 다항 로지스틱 회귀  
- **Target Data 전처리:**  
  - 득점 4 이상은 Clipping (총 25개 Class 생성)  
  - Class: `(X:Y)` 형태를 Integer Data로 Embedding  
    - 예: 2:4 → `14 = 2 * 5 + 4`  
- **학습 과정:**  
  - Random 추출된 Batch 학습 (Optimizer: SGD, Loss Function: Cross-Entropy Loss)  
  - Iteration마다 Cost 계산 및 그래프화  

#### 결과 평가  
- Learning Rate: `0.00001`  
- Step: `5000`  
- Batch Size: `200`  
- **Accuracy:**  
  - 득점 예측 정확도: `6.91%`  
  - 승부 예측 정확도: `37.76%`  

---

### Neural Network  
- **Utils & Layers 구현:**  
  - Optimizers: SGD, Adam  
  - Loss Functions: Mean Squared Error Loss  
  - Activation Functions: ReLU, LeakyReLU, SiLU, tanh  

#### Adam Optimizer  
- Momentum과 RMSProp 결합  
- Gradient의 First & Second Moment 계산  

#### Shallow Neural Network  
- **설정:**  
  - Weight Initialization: He Initialization  
  - Activation Function: LeakyReLU  
  - Loss Function: Mean Squared Error Loss  
  - Hyperparameters:  
    - Hidden Layer Size: 50  
    - Learning Rate: 0.002  
    - Iterations: 10000  
    - Batch Size: 200  

#### Deep Neural Network  
- **설정:**  
  - Hidden Layer: 2개  
  - Dropout Rate: 0.5  
  - Learning Rate Decay 적용  

#### 결과 평가  
- 득점 예측 정확도: `~10%`  
- 승부 예측 정확도: `~50%`  

---

## 결론  
- **성과:**  
  - 다양한 데이터 전처리 및 모델 적용  
  - Overfitting 방지를 위한 최신 기법 적용 (Dropout, Learning Rate Decay)  
  - 다양한 Layer 구현으로 최적 모델 탐색 가능  
- **제약:**  
  - 데이터 수의 제한  
  - 경기 내용의 다양성으로 인한 과적합 발생 가능  

---

## 팀 기여  
- **정진홍:** Neural Network 모델 세부 Layer 및 Optimizer 구현  
- **유준상:** Logistic Regression 모델 제작  
- **윤웅상:** 데이터 크롤링 및 전처리, Neural Network 모델 제작  
- **김동희:** 데이터 전처리, 최적 Hyperparameter 탐색  

## Getting Started

```
python run.py
```
