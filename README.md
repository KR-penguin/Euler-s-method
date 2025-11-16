# 오일러 적분 근사 실험

오일러 방법을 이용한 수치 적분 근사와 실제값 비교 분석 프로그램입니다.

## 📋 프로젝트 개요

이 프로젝트는 오일러 방법(Euler Method)을 사용하여 다양한 함수의 정적분을 근사하고, 실제 적분값과 비교하여 근사의 정확도를 분석합니다.

## 🎯 주요 기능

- **다양한 함수 타입 지원**
  - 선형 함수 (Linear): `ax + b`
  - 이차 함수 (Quadratic): `ax² + bx + c`
  - 삼각 함수 (Sine): `A·sin(kx)`
  - 지수 함수 (Exponential): `A·e^(kx)`

- **자동 실험 생성**
  - 100개의 랜덤 적분 문제 자동 생성
  - 다양한 스텝 크기 (h = 0.05, 0.1, 0.25, 0.5)
  - 적분 구간 [a, b] 랜덤 설정

- **데이터 분석**
  - 실제 적분값 vs 오일러 근사값 계산
  - 절대 오차 및 상대 오차 계산
  - CSV 파일로 결과 저장

- **시각화**
  - 문제 번호별 실제값과 근사값 비교 그래프
  - matplotlib 기반 고해상도 이미지 생성

## 📦 필요 패키지

```bash
pip install matplotlib pandas numpy
```

## 🚀 사용 방법

### 1. 실험 데이터 생성

```python
python main.py
```

기본적으로 `generate_experiments()` 함수가 주석 처리되어 있으므로, 새로운 데이터를 생성하려면:

```python
if __name__ == "__main__":
    generate_experiments()  # 주석 해제
    visualize_data()
```

### 2. 데이터 시각화

CSV 파일이 이미 존재하는 경우:

```python
if __name__ == "__main__":
    visualize_data()
```

## 📊 출력 파일

- `euler_integration_experiments.csv`: 100개 실험 결과 데이터
- `euler_integration_visualization.png`: 시각화 그래프

## 📈 CSV 데이터 구조

| 컬럼명 | 설명 |
|--------|------|
| id | 문제 번호 (1-100) |
| func_type | 함수 타입 (linear, quadratic, sin, exp) |
| func_expr | 함수 표현식 |
| a | 적분 시작점 |
| b | 적분 끝점 |
| h | 스텝 크기 |
| true_value | 실제 적분값 (해석적 해) |
| euler_value | 오일러 근사값 |
| abs_error | 절대 오차 |
| rel_error | 상대 오차 |

## 🔬 오일러 적분 방법

오일러 방법은 미분방정식 `y'(x) = f(x)`를 수치적으로 풀어 적분을 근사합니다:

```
y(b) ≈ Σ f(x_i) · h
```

이는 좌측 리만합(Left Riemann Sum)과 동일한 방식입니다.

## 📝 주요 함수

### `make_function(kind)`
지정된 타입의 함수와 그 원시함수를 생성합니다.

### `euler_integral(f, a, b, h)`
오일러 방법으로 정적분을 근사 계산합니다.

### `generate_experiments(num_problems, filename)`
지정된 개수의 적분 문제를 생성하고 CSV로 저장합니다.

### `visualize_data(filename)`
CSV 데이터를 읽어 matplotlib로 시각화합니다.

## 🎨 시각화 특징

- X축: 문제 번호 (1-100)
- Y축: 적분값
- 파란색 선: 실제 적분값
- 자주색 선: 오일러 근사값
- 한글 폰트 지원 (Malgun Gothic/NanumGothic)

## 📌 참고사항

- `random.seed(42)` 설정으로 재현 가능한 결과 생성
- 스텝 크기가 작을수록 근사 정확도 향상
- 지수 함수는 큰 값으로 인해 상대적으로 큰 오차 발생 가능

## 📄 라이센스

이 프로젝트는 학교 수학 심화 탐구 과제용으로 제작되었습니다.
