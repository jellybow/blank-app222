import streamlit as st
import random
import time

st.title("나누기 연습 - 과일 나누기 놀이")
st.markdown("---")
st.subheader("문제를 풀고, 이모지가 한 개씩 이동하는 과정을 지켜봐요!")

# 과일 선택
fruit_option = st.selectbox("어떤 과일로 연습할래요?", ("🍎 사과", "🍌 바나나", "🍊 오렌지"))
emoji = fruit_option.split()[0]

# 난이도 선택(최대 과일 개수)
difficulty = st.selectbox("난이도", ("쉬움 (최대 10)", "보통 (최대 20)", "어려움 (최대 30)"))
max_val = {"쉬움 (최대 10)": 10, "보통 (최대 20)": 20, "어려움 (최대 30)": 30}[difficulty]

if "problem" not in st.session_state:
    st.session_state.problem = None

col_gen, _ = st.columns([1, 3])
with col_gen:
    if st.button("새 문제 내기"):
        # divisor는 2~min(6, max_val)
        divisor = random.randint(2, min(6, max_val))
        dividend = random.randint(divisor, max_val)
        st.session_state.problem = {"dividend": dividend, "divisor": divisor, "emoji": emoji}
        st.session_state.answered = False
        st.session_state.animate_done = False
        # 초기 애니메이션 상태
        st.session_state.groups = [""] * divisor
        st.session_state.remaining = dividend
        st.session_state.next_idx = 0

if st.session_state.problem is None:
    st.info("먼저 '새 문제 내기' 버튼을 눌러 문제를 받아보세요.")
    st.stop()

dividend = st.session_state.problem["dividend"]
divisor = st.session_state.problem["divisor"]
emoji = st.session_state.problem["emoji"]

st.markdown(f"### 문제: {dividend}{emoji}를 {divisor}명에게 나눌게요. 한 사람당 몇 개? 남는 개수는 몇 개일까요?")

col1, col2 = st.columns(2)
with col1:
    user_q = st.number_input("한 사람당 개수", min_value=0, value=dividend // divisor, step=1, key="user_q")
with col2:
    user_r = st.number_input("남는 개수", min_value=0, value=dividend % divisor, step=1, key="user_r")

if st.button("정답 제출"):
    st.session_state.answered = True
    st.session_state.user_q = int(user_q)
    st.session_state.user_r = int(user_r)
    # reset groups & remaining (in case user changed inputs before)
    st.session_state.groups = [""] * divisor
    st.session_state.remaining = dividend
    st.session_state.next_idx = 0
    st.session_state.animate_done = False

if st.session_state.get("answered"):
    # 자리 표시자 준비
    cols = st.columns(divisor)
    placeholders = [c.empty() for c in cols]
    rem_ph = st.empty()

    # 초기 렌더
    for i in range(divisor):
        placeholders[i].markdown(f"**친구 {i+1}**\n\n{st.session_state['groups'][i] or ' '}")
    rem_ph.markdown(f"남은 과일: {st.session_state['remaining']}{emoji}")

    # 애니메이션 실행 (한 번만)
    if not st.session_state.animate_done:
        while st.session_state.remaining > 0:
            idx = st.session_state.next_idx
            st.session_state.groups[idx] += emoji
            st.session_state.remaining -= 1
            st.session_state.next_idx = (idx + 1) % divisor

            # 업데이트
            for i in range(divisor):
                placeholders[i].markdown(f"**친구 {i+1}**\n\n{st.session_state['groups'][i]}")
            rem_ph.markdown(f"남은 과일: {st.session_state['remaining']}{emoji}")
            time.sleep(0.25)

        st.session_state.animate_done = True

    # 최종 정답 확인
    final_q = dividend // divisor
    final_r = dividend % divisor
    st.markdown("---")
    if st.session_state.user_q == final_q and st.session_state.user_r == final_r:
        st.success(f"정답이에요! 한 사람당 {final_q}{emoji}, 남는 개수 {final_r}{emoji}입니다.")
    else:
        st.error(f"틀렸어요. 정답은 한 사람당 {final_q}{emoji}, 남는 개수 {final_r}{emoji}입니다.")

    if st.button("다시 풀기"):
        # 초기화
        st.session_state.problem = None
        st.session_state.answered = False
        st.session_state.animate_done = False
        st.experimental_rerun()
