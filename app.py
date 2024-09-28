import io
import os
import subprocess
import streamlit as st
from PIL import Image
from huggingface_hub import HfApi, InferenceApi
from app_handler import send_query_get_response_hf  # Modified to use Hugging Face
from chat_gen import generate_html
from main import upload_files_to_hf_repo, attach_files_to_assistant, check_and_upload_files

# Load logos
logo = Image.open('logo.png')
sb_logo = Image.open('sb_logo.png')

# Streamlit UI setup
c1, c2 = st.columns([0.9, 3.2])

with c1:
    st.caption('')
    st.caption('')
    st.image(logo, width=120)

with c2:
    st.title('EduMentor: An AI-Enhanced Tutoring System')

# RAG Function Description
st.markdown("## AI Tutor Description")
rag_description = """
EduMentor leverages Hugging Face's models to provide in-depth, contextually rich answers to educational queries. This AI-driven approach combines knowledge retrieval with dynamic response generation, offering students a deeper, interactive learning experience.
"""
st.markdown(rag_description)

# Hugging Face API Token Input
api_token = st.text_input(label='Enter your Hugging Face API Token', type='password')

if api_token:

    hf_api = HfApi(token=api_token)
    inference = InferenceApi(repo_id="eldestboom/ai_tutor", token=api_token)  # Replace with your Hugging Face model ID


    repo_id = "eldestboom/ai_tutor"
    files_info = check_and_upload_files(hf_api, repo_id)
    st.markdown(f'Number of files uploaded in the assistant: :blue[{len(files_info)}]')
    st.divider()

    # Sidebar for Additional Features
    st.sidebar.header('EduMentor: AI-Tutor')
    st.sidebar.image(logo, width=120)
    st.sidebar.caption('Made by D')

    # Button to delete all files from the Hugging Face repository
    if st.sidebar.button('Delete All Files from Repository'):
        repo_files = hf_api.list_repo_files(repo_id)
        for file_path in repo_files:
            hf_api.delete_file(path_in_repo=file_path, repo_id=repo_id)
            st.sidebar.success(f'Deleted file: {file_path}')

    if st.sidebar.button('Generate Chat History'):
        html_data = generate_html(st.session_state.messages)
        st.sidebar.download_button(label="Download Chat History as HTML",
                                   data=html_data,
                                   file_name="chat_history.html",
                                   mime="text/html")

    # Main Chat Interface
    st.subheader('Q&A record with AI-Tutor 📜')
    st.caption('You can download chat history in PDF or HTML using the sidebar.')

    # Initialize session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    # Capture new user input
    if prompt := st.chat_input("Ask a question to the AI tutor"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI response (Hugging Face model)
        with st.chat_message("assistant", avatar='👨🏻‍🏫'):
            message_placeholder = st.empty()
            with st.spinner('Thinking...'):
                response = send_query_get_response_hf(inference, prompt)  # Hugging Face model interaction
            message_placeholder.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

else:
    # Warning if no API token is provided
    st.warning("Please enter your Hugging Face API Token to use EduMentor.")

