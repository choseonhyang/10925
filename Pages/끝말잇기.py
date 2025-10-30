import streamlit as st

# --- 초기 설정 및 세션 상태 관리 ---
# st.session_state를 사용하여 게임 상태 저장

if 'game_words' not in st.session_state:
    st.session_state.game_words = [] # 사용된 단어 목록
    st.session_state.last_char = None  # 마지막 글자
    st.session_state.message = "게임을 시작합니다! 아무 단어나 입력하세요."
    st.session_state.game_over = False

def initialize_game():
    """게임 상태를 초기화합니다."""
    st.session_state.game_words = []
    st.session_state.last_char = None
    st.session_state.message = "게임을 시작합니다! 아무 단어나 입력하세요."
    st.session_state.game_over = False

def check_word(new_word):
    """새로 입력된 단어의 유효성을 검사합니다."""
    
    # 1. 빈 문자열 또는 공백 검사
    if not new_word.strip():
        st.session_state.message = "🚨 단어를 입력해 주세요!"
        return False
        
    # 2. 한 글자 단어 검사 (일반적으로 끝말잇기 규칙)
    if len(new_word) <= 1:
        st.session_state.message = "🚨 한 글자 단어는 사용할 수 없습니다. 다시 입력해 주세요."
        return False

    # 3. 중복 단어 검사
    if new_word in st.session_state.game_words:
        st.session_state.message = f"❌ '{new_word}'은(는) 이미 사용된 단어입니다. 게임 오버!"
        st.session_state.game_over = True
        return False

    # 4. 끝말잇기 규칙 검사 (첫 단어가 아닐 때)
    if st.session_state.last_char is not None:
        if new_word[0] != st.session_state.last_char:
            st.session_state.message = f"❌ '{st.session_state.last_char}'로 시작해야 합니다. '{new_word}' (은)는 규칙 위반! 게임 오버!"
            st.session_state.game_over = True
            return False

    # 모든 검사를 통과하면 유효한 단어입니다.
    return True

def process_word():
    """입력된 단어를 처리하고 게임 상태를 업데이트합니다."""
    
    new_word = st.session_state.input_word.strip()

    if st.session_state.game_over:
        st.session_state.message = "게임이 끝났습니다. '새 게임 시작' 버튼을 눌러주세요."
        st.session_state.input_word = "" # 입력창 비우기
        return

    if check_word(new_word):
        # 단어 추가 및 상태 업데이트
        st.session_state.game_words.append(new_word)
        st.session_state.last_char = new_word[-1]
        st.session_state.message = f"✅ 성공! 다음은 '{st.session_state.last_char}'로 시작하는 단어를 입력하세요."
        st.session_state.input_word = "" # 입력창 비우기
    else:
        # 단어가 유효하지 않은 경우, 입력창은 비우지 않아 사용자가 다시 시도 가능하도록 할 수도 있습니다.
        # 여기서는 비워서 다음 입력을 유도합니다.
        st.session_state.input_word = ""
        

# --- Streamlit UI 구성 ---

st.title("🔗 끝말잇기 게임")
st.markdown("---")

# 현재 게임 상태 표시
col1, col2 = st.columns(2)

with col1:
    if st.session_state.last_char:
        st.metric(label="마지막 단어의 끝 글자", value=f"'{st.session_state.last_char}'")
    else:
        st.metric(label="마지막 단어의 끝 글자", value="없음")

with col2:
    st.metric(label="현재 단어 개수", value=len(st.session_state.game_words))

st.markdown("---")

# 메시지 출력 (성공/실패/안내)
if st.session_state.game_over:
    st.error(st.session_state.message)
    st.balloons()
else:
    st.info(st.session_state.message)

# 사용자 입력
st.text_input(
    label="단어를 입력하세요:", 
    key="input_word", 
    on_change=process_word, # 입력 후 엔터를 누르거나 포커스를 잃으면 process_word 함수 실행
    disabled=st.session_state.game_over,
    placeholder=f"'{st.session_state.last_char}'로 시작하는 단어" if st.session_state.last_char else "아무 단어나 입력"
)

# 게임 재시작 버튼
st.button("🔄 새 게임 시작", on_click=initialize_game)

st.markdown("---")

# 사용된 단어 목록
st.subheader("📝 사용된 단어 목록")
if st.session_state.game_words:
    # 단어를 줄 바꿈으로 구분하여 표시
    st.text_area(
        label="기록", 
        value="\n".join(st.session_state.game_words), 
        height=200, 
        disabled=True
    )
else:
    st.write("아직 사용된 단어가 없습니다.")
