import os

import streamlit as st
import requests

st.title("Candidate Discovery")

with st.sidebar:
    inject_info = st.toggle("Search candidate database", value=True)
    if st.button("Re-index candidates"):
        with st.spinner("Indexing candidates from database..."):
            r = requests.post(url=os.getenv("SEARCH_ENDPOINT").replace("/search", "/index"))
            if r.status_code == 200:
                st.success(f"Indexed {r.json()['indexed']} candidates.")
            else:
                st.error(f"Indexing failed: {r.status_code}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Describe the candidate you're looking for..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = requests.post(
        url=os.getenv("LLM_ENDPOINT"),
        json={
            "history": st.session_state.messages,
            "inject_info": inject_info,
        },
    )

    if response.status_code != 200:
        st.error(f"API error: {response.status_code} - {response.text}")
    else:
        assistant_message = response.json()["response"]
        with st.chat_message("assistant"):
            st.markdown(assistant_message)
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
