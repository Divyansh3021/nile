import streamlit as st
import random
import time
import git
import os
from google.api_core.exceptions import InternalServerError

flag = False
repo = st.text_input(label="Paste the .git link of repository.")
btn = st.button(label="Submit")

def clone_repo(repo):
    if os.path.exists("githubCode") and os.path.isdir("githubCode"):
        print("File already exists!!")
        pass
    else:
        print("Cloning repo!!")
        git.Repo.clone_from(repo,"githubCode")
        
if btn and not flag:
    clone_repo(repo=repo)
    flag = True

st.title("Nile")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What's your question ?"):
    from util import ask
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        try:
            response = ask(prompt)
        except InternalServerError as err:
            retry_attempts = 0
            MAX_RETRIES = 2
            if retry_attempts < MAX_RETRIES:
                retry_attempts += 1
                time.sleep(2)
                response = ask(prompt)
            else:
                # If retries are exhausted, log the error for further investigation
                response = "500 An internal error has occurred. Please retry or report in https://developers.generativeai.google/guide/troubleshooting"

        # print(response)
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
