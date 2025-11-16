import math
import csv
import random
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

random.seed(42)  # 재현 가능하게 고정 (원하면 지워도 됨)

# ----- 1. 적분 문제를 구성할 함수 패밀리 정의 -----
def make_function(kind):
    """
    kind: 'linear', 'quadratic', 'sin', 'exp'
    return: (f, F, expr_str)
        f(x)  : 적분할 함수
        F(x)  : f(x)의 원시함수(부정적분)
        expr_str : 보고서용 함수 표현 문자열
    """
    if kind == "linear":
        # f(x) = a x + b
        a = random.randint(-3, 3)
        b = random.randint(-3, 3)
        # a, b가 둘 다 0이면 재미 없으니 한 번 더 뽑기
        if a == 0 and b == 0:
            a = 1

        def f(x):
            return a * x + b

        def F(x):
            return a * x**2 / 2 + b * x

        expr = f"{a}*x + {b}"
        return f, F, expr

    elif kind == "quadratic":
        # f(x) = a x^2 + b x + c
        a = random.randint(-2, 2)
        b = random.randint(-3, 3)
        c = random.randint(-3, 3)
        if a == 0 and b == 0 and c == 0:
            a = 1  # 전부 0이면 무의미하니 보정

        def f(x):
            return a * x**2 + b * x + c

        def F(x):
            return a * x**3 / 3 + b * x**2 / 2 + c * x

        expr = f"{a}*x^2 + {b}*x + {c}"
        return f, F, expr

    elif kind == "sin":
        # f(x) = A * sin(kx)
        A = random.randint(1, 3) * random.choice([-1, 1])
        k = random.randint(1, 4)  # 0은 피함

        def f(x):
            return A * math.sin(k * x)

        def F(x):
            # ∫ A sin(kx) dx = -A/k cos(kx)
            return -A / k * math.cos(k * x)

        expr = f"{A}*sin({k}*x)"
        return f, F, expr

    elif kind == "exp":
        # f(x) = A * exp(kx)
        A = random.randint(1, 3) * random.choice([-1, 1])
        k = random.randint(-2, 2)
        if k == 0:
            # k=0이면 f(x) = A, F(x) = A x
            def f(x):
                return A

            def F(x):
                return A * x

            expr = f"{A}"
            return f, F, expr

        def f(x):
            return A * math.exp(k * x)

        def F(x):
            # ∫ A e^{kx} dx = A/k e^{kx}
            return A / k * math.exp(k * x)

        expr = f"{A}*exp({k}*x)"
        return f, F, expr

    else:
        raise ValueError("Unknown function kind")


# ----- 2. 오일러 적분 근사 함수 (좌측 리만합 관점) -----
def euler_integral(f, a, b, h):
    """
    y'(x) = f(x), y(a) = 0 을 오일러 방법으로 적분한다고 생각하면
    y(b) ≈ ∑ f(x_i) * h  (좌측 리만합과 동일)
    """
    n_steps = int((b - a) / h)
    x = a
    y = 0.0
    for _ in range(n_steps):
        y += f(x) * h  # y_{i+1} = y_i + f(x_i)*h
        x += h
    return y


# ----- 3. 적분 문제 100개 생성 + 계산 + CSV로 저장 -----
def generate_experiments(num_problems=100, filename="euler_integration_experiments.csv"):
    kinds = ["linear", "quadratic", "sin", "exp"]

    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # 헤더
        writer.writerow([
            "id",
            "func_type",
            "func_expr",
            "a",
            "b",
            "h",
            "true_value",
            "euler_value",
            "abs_error",
            "rel_error"
        ])

        for i in range(1, num_problems + 1):
            kind = random.choice(kinds)
            f_fun, F_fun, expr = make_function(kind)

            # 적분 구간 [a, b] 설정 (a < b)
            a = random.uniform(0.0, 3.0)
            b = random.uniform(3.0, 6.0)
            if a > b:
                a, b = b, a

            # 스텝 사이즈 h 선택 (너무 크지도 작지도 않게)
            h = random.choice([0.5, 0.25, 0.1, 0.05])

            # 실제 적분값 (해석적 해)
            true_val = F_fun(b) - F_fun(a)

            # 오일러 적분 근사
            euler_val = euler_integral(f_fun, a, b, h)

            # 오차 계산
            abs_error = abs(true_val - euler_val)
            rel_error = abs_error / (abs(true_val) + 1e-12)  # 0으로 나누는 것 방지

            writer.writerow([
                i,
                kind,
                expr,
                a,
                b,
                h,
                true_val,
                euler_val,
                abs_error,
                rel_error
            ])

    print(f"Saved {num_problems} experiments to '{filename}'")


# ----- 4. 데이터 시각화 함수 -----
def visualize_data(filename="euler_integration_experiments.csv"):
    """CSV 파일을 읽어서 matplotlib로 시각화"""
    
    # 데이터 불러오기
    df = pd.read_csv(filename)
    
    # 한글 폰트 설정 (Windows)
    try:
        plt.rcParams['font.family'] = 'Malgun Gothic'
    except:
        try:
            plt.rcParams['font.family'] = 'NanumGothic'
        except:
            pass
    plt.rcParams['axes.unicode_minus'] = False
    
    # Figure 생성
    fig, ax = plt.subplots(figsize=(16, 8))
    
    # 문제 번호 (x축)
    problem_numbers = df['id']
    
    # 실제값과 근사값을 함께 그리기
    ax.plot(problem_numbers, df['true_value'], 
            marker='o', linestyle='-', linewidth=1.5, markersize=4, 
            color='#2E86AB', alpha=0.7, label='실제값')
    
    ax.plot(problem_numbers, df['euler_value'], 
            marker='s', linestyle='-', linewidth=1.5, markersize=4, 
            color='#A23B72', alpha=0.7, label='오일러 근사값')
    
    ax.set_xlabel('문제 번호', fontsize=12)
    ax.set_ylabel('적분값', fontsize=12)
    ax.set_title('오일러 적분 근사: 실제값 vs 근사값 비교', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11, loc='best')
    ax.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig('euler_integration_visualization.png', dpi=300, bbox_inches='tight')
    print("시각화 완료! 'euler_integration_visualization.png' 파일이 저장되었습니다.")
    plt.show()


if __name__ == "__main__":
    # generate_experiments()  # 이미 CSV가 있으면 주석 처리
    visualize_data()
