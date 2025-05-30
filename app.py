import streamlit as st
import google.generativeai as genai

# Streamlit Cloud에서 .streamlit/secrets.toml에 저장된 API 키를 불러옵니다.
# secrets.toml 파일 사용법:
# 1. .streamlit 폴더를 생성합니다 (없는 경우)
# 2. .streamlit/secrets.toml 파일을 생성하고 다음 형식으로 API 키를 저장합니다:
#    GEMINI_API_KEY = "your-api-key-here"
# 3. 이 파일은 절대 GitHub 등에 공개하지 않도록 주의하세요!
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 페이지 설정
st.set_page_config(
    page_title="Gemini 챗봇",
    page_icon="🤖",
    layout="wide"
)

# 세션 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 제목
st.title("🤖 Gemini 챗봇")

# 채팅 인터페이스
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["parts"][0])

# 사용자 입력
user_input = st.chat_input("질문을 입력하세요:")

if user_input:
    # 사용자 메시지 추가
    st.session_state.chat_history.append({
        "role": "user",
        "parts": [user_input]
    })
    
    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.write(user_input)
    
    # Gemini 모델 초기화
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=st.session_state.chat_history)
    
    # 응답 생성
    with st.chat_message("assistant"):
        with st.spinner("생각 중..."):
            response = chat.send_message(user_input)
            st.write(response.text)
    
    # 응답을 대화 이력에 추가
    st.session_state.chat_history.append({
        "role": "model",
        "parts": [response.text]
    })
