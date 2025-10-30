import streamlit as st
import random
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="로또 번호 생성기",
    layout="centered"
)

# 로또 번호 생성 함수
def generate_lotto_numbers():
    """1부터 45 사이의 중복 없는 6개 숫자를 오름차순으로 생성"""
    # range(1, 46)은 1부터 45까지를 의미합니다.
    numbers = random.sample(range(1, 46), 6)
    numbers.sort() # 오름차순 정렬
    return numbers

## 🍀 대한민국 로또 번호 생성기
st.title("🍀 대한민국 로또 번호 생성기")
st.markdown("1부터 45 사이의 숫자 중 **중복 없는 6개**의 숫자를 무작위로 생성합니다.")

---

# 1. 게임 수 입력 (슬라이더)
# st.slider를 사용하여 1부터 10까지의 정수를 입력받습니다.
game_count = st.slider(
    '몇 게임을 생성하시겠어요? (1 ~ 10 게임)',
    min_value=1,
    max_value=10,
    value=5,  # 기본값
    step=1,
    help="생성할 로또 번호 조합의 개수를 선택하세요."
)

# '생성' 버튼
if st.button('🎲 번호 생성'):
    st.subheader(f"✅ {game_count} 게임 추천 번호")
    
    # 생성된 번호를 저장할 리스트
    results = []
    
    # 입력된 게임 수만큼 번호를 생성합니다.
    for i in range(1, game_count + 1):
        lotto_numbers = generate_lotto_numbers()
        # 결과를 딕셔너리 형태로 저장
        results.append({
            "게임": f"게임 {i}",
            "번호": " | ".join([f"{num:02d}" for num in lotto_numbers]),
            "숫자1": lotto_numbers[0],
            "숫자2": lotto_numbers[1],
            "숫자3": lotto_numbers[2],
            "숫자4": lotto_numbers[3],
            "숫자5": lotto_numbers[4],
            "숫자6": lotto_numbers[5]
        })
    
    # 결과를 DataFrame으로 변환
    df = pd.DataFrame(results)
    
    # 보기 쉽게 '게임'과 '번호' 열만 출력
    st.table(df[['게임', '번호']].style.set_properties(**{'font-size': '18px'}))
    
    st.balloons() # 번호 생성 후 풍선 효과!
