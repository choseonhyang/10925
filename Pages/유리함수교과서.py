import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(page_title="유리함수 마스터", layout="wide")

st.title("📊 유리함수(Rational Function) 학습 가이드")
st.write("유리함수의 기본 성질부터 그래프 시각화까지 한 번에 학습해보세요.")

# 사이드바: 함수 파라미터 입력
st.sidebar.header("함수 설정: $y = \\frac{k}{x-p} + q$")
k = st.sidebar.slider("상수 k (기울기 결정)", -10.0, 10.0, 1.0, 0.5)
p = st.sidebar.number_input("x축 평행이동 (p)", value=0.0)
q = st.sidebar.number_input("y축 평행이동 (q)", value=0.0)

# 레이아웃 나누기
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📌 유리함수의 성질 요약")
    
    # 성질 계산 및 정리
    st.info(f"""
    **1. 점근선의 방정식:**
    - $x = {p}$
    - $y = {q}$
    
    **2. 정의역과 치역:**
    - **정의역:** $\\{{x | x \\neq {p}인 \\text{{ 모든 실수}}\\}} $
    - **치역:** $\\{{y | y \\neq {q}인 \\text{{ 모든 실수}}\\}} $
    
    **3. 대칭성:**
    - 점 대칭: 점 $({p}, {q})$에 대하여 대칭
    - 선 대칭: 기울기가 $\pm 1$이고 $({p}, {q})$를 지나는 두 직선에 대해 대칭
        - $y = (x - {p}) + {q}$
        - $y = -(x - {p}) + {q}$
    """)
    
    if k > 0:
        st.write("💡 **k > 0 일 때:** 그래프는 제 1, 3사분면 방향에 위치합니다.")
    elif k < 0:
        st.write("💡 **k < 0 일 때:** 그래프는 제 2, 4사분면 방향에 위치합니다.")
    else:
        st.warning("k가 0이면 유리함수가 아닌 상수함수(y=q)가 됩니다.")

with col2:
    st.subheader("📈 그래프 시각화")
    
    # 그래프 그리기
    if k != 0:
        fig, ax = plt.subplots(figsize=(6, 6))
        
        # 데이터 생성 (점근선 부근에서 끊기지 않도록 두 구간으로 나눔)
        x1 = np.linspace(p - 10, p - 0.1, 400)
        x2 = np.linspace(p + 0.1, p + 10, 400)
        
        y1 = k / (x1 - p) + q
        y2 = k / (x2 - p) + q
        
        # 함수 그래프
        ax.plot(x1, y1, 'b', label=f'y = {k}/(x-{p}) + {q}')
        ax.plot(x2, y2, 'b')
        
        # 점근선 표시
        ax.axvline(x=p, color='r', linestyle='--', label='Asymptote x')
        ax.axhline(y=q, color='r', linestyle='--', label='Asymptote y')
        
        # 좌표축 설정
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.legend()
        
        # 범위 제한
        ax.set_xlim(p-10, p+10)
        ax.set_ylim(q-10, q+10)
        
        st.pyplot(fig)
    else:
        st.write("k 값을 조절하여 그래프를 확인하세요.")

---

### 📖 활용 및 학습 팁
1. **역함수 구하기:** 유리함수 $y = \frac{ax+b}{cx+d}$의 역함수 공식을 활용해 보세요.
2. **실생활 활용:** 유리함수는 **보일의 법칙**(압력과 부피의 관계)이나 **작업 시간 계산** 등에서 자주 등장합니다.
