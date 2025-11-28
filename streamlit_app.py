import streamlit as st

# 앱 제목 설정
st.title("🍎 똑같이 나눠볼까요? - 나눗셈 시각화 학습")
st.markdown("---")

# 🎈 1. 입력 설정 (초등학생용 쉬운 표현)
st.subheader("나눌 과일 종류와 몇 명에게 나눌지 입력해요.")

# 과일 선택: 사과, 바나나, 오렌지 (이모지 추가)
fruit_option = st.selectbox("어떤 과일로 나눌까요?", ("🍎 사과", "🍌 바나나", "🍊 오렌지"))
item_emoji = fruit_option.split()[0]

col_input_1, col_input_2 = st.columns(2)
with col_input_1:
    dividend = st.number_input("총 과일 개수 (예: 10)", min_value=1, value=10, step=1)
with col_input_2:
    divisor = st.number_input("친구 수 (몇 명에게 나눌까요?)", min_value=1, value=3, step=1)

# 2. 입력 검증: 총 사과 개수는 학생 수(친구 수)보다 같거나 커야 합니다.
if divisor > dividend:
    st.error("총 과일 개수는 친구 수보다 같거나 커야 해요. 과일 수를 늘리거나 친구 수를 줄여주세요.")
    can_divide = False
else:
    can_divide = True

if st.button("나누어 보기! 👩‍🏫"):
    st.markdown("---")

    if not can_divide:
        st.warning("총 과일 개수를 먼저 바꿔주세요. 그 다음에 나눠볼게요!")
    else:
        # 3. 나눗셈 계산
        quotient = dividend // divisor  # 몫
        remainder = dividend % divisor  # 나머지

        # 4. 계산 결과 요약 (초등학생용 문장)
        st.subheader(f"결과: {dividend}개를 {divisor}명에게 나누면 한 사람당 {quotient}개, 남는 개수 {remainder}개예요.")

        if remainder == 0:
            st.success(f"🥳 모두 똑같이 나눠졌어요! 한 사람당 {quotient}{item_emoji}씩 가질 수 있어요.")
        else:
            st.warning(f"⚠️ 조금 남았어요. 한 사람당 {quotient}{item_emoji}씩 주고, {remainder}{item_emoji}가 남아요.")

        st.markdown("---")
        st.subheader(f"단계별 그림: {item_emoji}를 한 개씩 나눠요!")

        # 4. 시각화 구현
        # 각 친구가 가질 과일 리스트 초기화 (몫만큼 가짐)
        groups = [item_emoji * quotient for _ in range(divisor)]

        # 남은 과일 (나머지)
        remaining_emojis = item_emoji * remainder

        # 컬럼 생성 (친구 수만큼)
        cols = st.columns(divisor)

        # 분배된 과일 시각화
        for i in range(divisor):
            with cols[i]:
                st.markdown(f"**친구 {i+1}** 🧑")
                st.markdown(f"## {groups[i]}")
                st.markdown(f"*(총 **{quotient}** 개)*")
                st.markdown("---")

        # 남은 과일 시각화
        st.markdown(f"### 📦 남은 과일 (남은 개수: {remainder}개)")
        if remainder > 0:
            st.markdown(f"## {remaining_emojis}", unsafe_allow_html=True)
            st.info("이 과일들은 모두에게 똑같이 줄 수 없어서 남았어요.")
        else:
            st.markdown("남은 과일이 없어요. 모두 깔끔하게 나눠졌어요! ✨")