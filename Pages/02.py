import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 앱 제목 ---
st.title("📘 유리함수의 그래프 탐구 디지털 교과서")
st.markdown("### 주제: $y = \\frac{a}{x}$ 의 그래프와 성질을 탐구해봅시다.")

# --- 목차 ---
st.sidebar.title("📚 목차")
menu = st.sidebar.radio(
    "탐구할 내용을 선택하세요",
    ("1. y=a/x의 그래프 그리기", "2. a값의 변화에 따른 그래프 모양", "3. 사분면 위치와 대칭성")
)

# --- 1단계: y=a/x의 기본 그래프 ---
if menu == "1. y=a/x의 그래프 그리기":
    st.subheader("1️⃣ y = a/x 의 그래프를 그려봅시다")

    a = st.slider("a 값을 선택하세요", -5.0, 5.0, 1.0, 0.5)
    x = np.linspace(-10, 10, 400)
    x = x[x != 0]  # 0은 정의되지 않으므로 제거
    y = a / x

    fig, ax = plt.subplots()
    ax.plot(x, y, label=f"y = {a}/x", color='blue')
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.set_title(f"y = {a}/x 의 그래프")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)
    st.markdown("- 분모가 0이 될 수 없기 때문에, x=0에서는 그래프가 존재하지 않습니다.")
    st.markdown("- y = a/x 는 원점을 중심으로 한 쌍곡선 형태입니다.")

# --- 2단계: a값의 변화에 따른 그래프 ---
elif menu == "2. a값의 변화에 따른 그래프 모양":
    st.subheader("2️⃣ a값의 변화에 따른 그래프 모양 관찰")

    x = np.linspace(-10, 10, 400)
    x = x[x != 0]

    a_values = st.multiselect(
        "비교할 a 값을 선택하세요 (여러 개 선택 가능)",
        [-3, -2, -1, 1, 2, 3],
        default=[-2, 1]
    )

    fig, ax = plt.subplots()
    for a in a_values:
        y = a / x
        ax.plot(x, y, label=f"a={a}")
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.set_title("a 값의 변화에 따른 그래프 모양 비교")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)
    st.markdown("""
    - a의 절댓값이 커질수록 그래프는 축에 더 가까워지며, 기울기가 가파릅니다.  
    - a가 양수이면 1,3사분면에 / a가 음수이면 2,4사분면에 그래프가 위치합니다.
    """)

# --- 3단계: 사분면 위치와 대칭성 ---
elif menu == "3. 사분면 위치와 대칭성":
    st.subheader("3️⃣ 사분면 위치와 대칭성 탐구")

    a = st.slider("a 값을 선택하세요", -5.0, 5.0, 1.0, 0.5)
    x = np.linspace(-10, 10, 400)
    x = x[x != 0]
    y = a / x

    fig, ax = plt.subplots()
    ax.plot(x, y, label=f"y = {a}/x", color='blue')
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.grid(True)
    ax.legend()

    st.pyplot(fig)

    if a > 0:
        st.markdown("✅ **a > 0일 때:** 그래프는 제1사분면과 제3사분면에 위치합니다.")
        st.markdown("➡️ 원점을 중심으로 **y = -x** 에 대칭입니다.")
    elif a < 0:
        st.markdown("✅ **a < 0일 때:** 그래프는 제2사분면과 제4사분면에 위치합니다.")
        st.markdown("➡️ 원점을 중심으로 **y = x** 에 대칭입니다.")
    else:
        st.markdown("a = 0이면 y = 0, 즉 x축과 일치합니다.")

# --- 푸터 ---
st.markdown("---")
st.caption("© 2025 수학 디지털교과서 프로젝트 | 작성자: 조선향")
