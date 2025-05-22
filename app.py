import streamlit as st

import chat
import config

st.markdown(config.FOOTER, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"system", "content":chat.INSTRUCTION}]

for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("메시지를 입력하세요...")

if user_input:
    st.session_state.messages.append({"role":"user", "content":user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("메시지 작성 중..."):
            reply = chat.get_reply(user_input)
            st.markdown(reply)
            st.session_state.messages.append({"role":"assistant", "content":reply})