import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 앱 제목 ---
st.title("📘 유리함수의 그래프 탐구 디지털 교과서")
st.markdown("### 주제: $y = \\frac{a}{x}$ 의 그래프와 성질을 탐구해봅시다.")
st.write("---")

# 1️⃣ y = a/x 그래프 그리기
st.header("1. y = a/x 의 그래프 그리기")
a1 = st.slider("a 값을 선택하세요 (1단계)", -5.0, 5.0, 1.0, 0.5, key="a1")

x = np.linspace(-10, 10, 400)
x = x[x != 0]  # 0은 정의되지 않음
y1 = a1 / x

fig1, ax1 = plt.subplots()
ax1.plot(x, y1, color='blue', label=f"y = {a1}/x")
ax1.axhline(0, color='black', linewidth=1)
ax1.axvline(0, color='black', linewidth=1)
ax1.set_title(f"y = {a1}/x 의 그래프")
ax1.set_xlabel("x")
ax1.set_ylabel("y")
ax1.legend()
ax1.grid(True)
st.pyplot(fig1)

st.markdown("""
- 분모가 0인 x=0에서는 그래프가 존재하지 않습니다.  
- y = a/x 는 원점을 중심으로 하는 쌍곡선 형태의 그래프입니다.
""")

st.write("---")

# 2️⃣ a값의 변화에 따른 그래프 모양
st.header("2. a 값의 변화에 따른 그래프 모양")
a_values = st.multiselect(
    "비교할 a 값을 선택하세요 (2단계)", [-3, -2, -1, 1, 2, 3], default=[-2, 1]
)

fig2, ax2 = plt.subplots()
for a in a_values:
    ax2.plot(x, a / x, label=f"a = {a}")
ax2.axhline(0, color='black', linewidth=1)
ax2.axvline(0, color='black', linewidth=1)
ax2.set_title("a 값의 변화에 따른 그래프 모양 비교")
ax2.legend()
ax2.grid(True)
st.pyplot(fig2)

st.markdown("""
- a의 절댓값이 커질수록 그래프는 축에 가까워집니다.  
- a가 **양수**이면 제1,3사분면 / **음수**이면 제2,4사분면에 그래프가 그려집니다.
""")

st.write("---")

# 3️⃣ 사분면 위치와 대칭성
st.header("3. 사분면 위치와 대칭성 탐구")
a3 = st.slider("a 값을 선택하세요 (3단계)", -5.0, 5.0, 1.0, 0.5, key="a3")
y3 = a3 / x

fig3, ax3 = plt.subplots()
ax3.plot(x, y3, color='blue', label=f"y = {a3}/x")
ax3.axhline(0, color='black', linewidth=1)
ax3.axvline(0, color='black', linewidth=1)
ax3.grid(True)
ax3.legend()
st.pyplot(fig3)

# --- 대칭성 설명 ---
if a3 > 0:
    st.markdown("""
    ✅ **a > 0일 때:** 그래프는 제1사분면과 제3사분면에 위치합니다.  
    ➡️ 원점을 중심으로 **y = -x** 에 대칭입니다.
    """)
elif a3 < 0:
    st.markdown("""
    ✅ **a < 0일 때:** 그래프는 제2사분면과 제4사분면에 위치합니다.  
    ➡️ 원점을 중심으로 **y = x** 에 대칭입니다.
    """)
else:
    st.markdown("a = 0이면 y = 0, 즉 x축과 일치합니다.")

st.write("---")
st.caption("© 2025 수학 디지털교과서 프로젝트 | 작성자: 조선향")
