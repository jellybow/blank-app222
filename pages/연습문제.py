import streamlit as st
import random

# ----------------------
# 1. 문제 생성 함수 정의 (단일 문제 및 제한 조건 적용)
# ----------------------
def generate_single_division_problem(difficulty):
    """
    몫(1~9)이 한 자리 수이고, 피제수가 최대 30인 나눗셈 문제를 1개 생성합니다.
    (피제수, 제수, 몫, 나머지) 튜플을 반환합니다.
    """
    
    max_attempts = 50 # 무한 루프 방지를 위한 최대 시도 횟수
    attempts = 0
    
    while attempts < max_attempts:
        divisor = random.randint(2, 9) 
        quotient = random.randint(1, 9)
        remainder_max = divisor - 1
        
        # 난이도에 따라 나머지 설정
        if difficulty == 1: # 쉬움: 나머지가 없는 문제
            remainder = 0
        else: # 보통: 나머지가 있을 수 있는 문제 (0 포함)
            remainder = random.randint(0, remainder_max)
        
        # 피제수 계산
        dividend = divisor * quotient + remainder
        
        # 제약 조건 확인: 피제수 <= 30 AND 몫 <= 9
        if dividend <= 30 and quotient <= 9:
            # 최종 유효한 문제 반환
            return dividend, divisor, quotient, remainder
        
        attempts += 1
    
    # 만약 50번 시도 후에도 적절한 문제를 찾지 못했다면 기본값 반환 (매우 드문 경우)
    return 10, 2, 5, 0 # 예시로 쉬운 문제 반환

# ----------------------
# 2. Streamlit 앱 인터페이스
# ----------------------
st.title("➗ 초등 나눗셈 연습 문제 생성기")
st.markdown("---")

# 🎈 사용자 입력 (난이도 선택)
st.header("난이도를 선택해 주세요 👇")
selected_difficulty = st.selectbox(
    "난이도 선택:",
    options=[1, 2],
    format_func=lambda x: f"난이도 {x}",
    label_visibility="collapsed" # 레이블 숨김
)

st.markdown("---")
# 3. 문제 생성 및 출력 — 세션에 문제 저장하고 사용자가 답을 입력하도록 변경
if "current_problem" not in st.session_state:
    st.session_state.current_problem = None
    st.session_state.submitted_q = None
    st.session_state.submitted_r = None

if st.button(f"난이도 {selected_difficulty} 문제 생성하기"):
    # 문제 생성
    dividend, divisor, quotient, remainder = generate_single_division_problem(selected_difficulty)
    st.session_state.current_problem = {
        "dividend": dividend,
        "divisor": divisor,
        "quotient": quotient,
        "remainder": remainder,
    }
    # 제출값 초기화
    st.session_state.submitted_q = None
    st.session_state.submitted_r = None

if st.session_state.current_problem is None:
    st.info("먼저 문제를 생성하세요. '난이도 X 문제 생성하기' 버튼을 누르면 문제를 만들어줍니다.")
    st.stop()

problem = st.session_state.current_problem
dividend = problem["dividend"]
divisor = problem["divisor"]
quotient = problem["quotient"]
remainder = problem["remainder"]

st.subheader("💡 오늘의 나눗셈 문제")
problem_string = f"$$ {dividend} \\div {divisor} = \\text{{[ ]}} $$"
st.markdown(problem_string)

# 사용자 입력: 몫과 나머지
col1, col2 = st.columns(2)
with col1:
    user_q = st.number_input("몫 (한 사람당 몇 개?)", min_value=0, value=0, step=1, key="user_q")
with col2:
    user_r = st.number_input("나머지 (남는 개수)", min_value=0, value=0, step=1, key="user_r")

if st.button("정답 확인"):
    st.session_state.submitted_q = int(user_q)
    st.session_state.submitted_r = int(user_r)
    # 결과 피드백
    if st.session_state.submitted_q == quotient and st.session_state.submitted_r == remainder:
        st.success(f"정답이에요! 몫 = {quotient}, 나머지 = {remainder}")
    else:
        st.error(f"틀렸어요. 정답은 몫 = {quotient}, 나머지 = {remainder} 입니다.")
        with st.expander("정답 보기 (펼치기)"):
            st.write(f"**몫:** {quotient}")
            st.write(f"**나머지:** {remainder}")

    # 작은 안내
    st.markdown("---")