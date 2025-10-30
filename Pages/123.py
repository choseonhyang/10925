import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(
    page_title="유리함수 그래프 학습 앱",
    layout="wide"
)

# 메인 제목 및 설명
st.title("📊 유리함수 그래프 학습 앱")
st.write("계수 $a, b, c, d$를 입력하여 유리함수 $y = \\frac{ax+b}{cx+d}$의 그래프를 그려보세요.")
st.markdown("---")

# 사이드바에 사용자 입력 받기
with st.sidebar:
    st.header("계수 입력 ($y = \\frac{ax+b}{cx+d}$)")
    # float 타입의 계수 입력 필드
    a = st.number_input("계수 a:", value=1.0, step=0.1)
    b = st.number_input("계수 b:", value=0.0, step=0.1)
    c = st.number_input("계수 c:", value=1.0, step=0.1)
    d = st.number_input("계수 d:", value=0.0, step=0.1)
    
    # 그래프 범위 설정
    st.header("그래프 표시 범위")
    x_min = st.number_input("x축 최소:", value=-10.0, step=1.0)
    x_max = st.number_input("x축 최대:", value=10.0, step=1.0)
    y_min = st.number_input("y축 최소:", value=-10.0, step=1.0)
    y_max = st.number_input("y축 최대:", value=10.0, step=1.0)

# 0으로 나누는 경우 방지
if c == 0 and d == 0:
    st.error("오류: $c$와 $d$ 모두 0일 수 없습니다 (분모가 0이 됩니다).")
elif c == 0 and a != 0:
    st.error("오류: $c=0$이고 $a \\neq 0$이면, 선형 함수가 되거나(a=0인 경우) 상수 함수가 됩니다.")
else:
    # 수직 점근선 계산
    # 분모 $cx+d = 0$이 되는 $x$ 값
    if c != 0:
        vertical_asymptote = -d / c
        # 수평 점근선 계산
        # $y = a/c$
        horizontal_asymptote = a / c
        
        # 그래프 생성
        fig, ax = plt.subplots(figsize=(10, 6))

        # 유리함수 정의
        def rational_function(x):
            return (a * x + b) / (c * x + d)

        # x 값 생성. 점근선 근처에서 불연속성을 처리하기 위해 구간을 나눕니다.
        # 점근선이 범위 안에 있을 때만 분할
        if x_min < vertical_asymptote < x_max:
            # 점근선 주변을 제외한 두 개의 x 배열 생성
            x1 = np.linspace(x_min, vertical_asymptote - 0.01, 500)
            x2 = np.linspace(vertical_asymptote + 0.01, x_max, 500)
            
            # 그래프 그리기
            ax.plot(x1, rational_function(x1), label="$y = \\frac{%.2fx + %.2f}{%.2fx + %.2f}$" % (a, b, c, d), color='blue')
            ax.plot(x2, rational_function(x2), color='blue')
            
            # 수직 점근선 표시
            ax.axvline(vertical_asymptote, color='red', linestyle='--', label=f'수직 점근선 $x = {vertical_asymptote:.2f}$')
        else:
            # 점근선이 범위 밖에 있다면 하나의 x 배열만 생성
            x_vals = np.linspace(x_min, x_max, 1000)
            ax.plot(x_vals, rational_function(x_vals), label="$y = \\frac{%.2fx + %.2f}{%.2fx + %.2f}$" % (a, b, c, d), color='blue')

        # 수평 점근선 표시 (c가 0이 아닐 때만)
        ax.axhline(horizontal_asymptote, color='green', linestyle='--', label=f'수평 점근선 $y = {horizontal_asymptote:.2f}$')
        
        # 교점 표시
        center_x = vertical_asymptote
        center_y = horizontal_asymptote
        
        ax.plot(center_x, center_y, 'o', color='purple', label=f'대칭의 중심 $({center_x:.2f}, {center_y:.2f})$')

        # 그래프 제목 및 레이블 설정
        ax.set_title("유리함수 그래프", fontsize=16)
        ax.set_xlabel("$x$ 축")
        ax.set_ylabel("$y$ 축")
        
        # x, y 축 범위 설정
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        
        # 격자 및 범례 표시
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.legend()
        
        # 그래프 출력
        st.pyplot(fig)
        
        # --- 추가 정보 표시 ---
        st.markdown("## 📚 유리함수의 특징")
        st.write(f"**함수의 식:** $y = \\frac{%.2fx + %.2f}{%.2fx + %.2f}$" % (a, b, c, d))
        st.write(f"**수직 점근선:** 분모가 0이 되는 $x$ 값, $cx+d=0 \\implies x = {vertical_asymptote:.2f}$")
        st.write(f"**수평 점근선:** 계수 $x$의 비, $y = \\frac{a}{c} \\implies y = {horizontal_asymptote:.2f}$")
        st.write(f"**대칭의 중심:** 두 점근선의 교점 $({center_x:.2f}, {center_y:.2f})$")

    else: # c=0이고 d!=0인 경우 (상수 함수 또는 선형 함수)
        if a / d == 0:
            st.warning("경고: 이 함수는 $y = \\frac{b}{d}$인 **상수 함수**입니다 (분자가 $ax+b$에서 $a=0$일 때).")
        else:
            st.warning("경고: 이 함수는 $y = \\frac{a}{d}x + \\frac{b}{d}$인 **선형 함수**입니다 ($c=0$일 때).")
