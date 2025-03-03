import streamlit as st


def sidebar():

    st.sidebar.image("./static/axel.jpeg", width=100)
    st.sidebar.header("Settings")

    # Load the API key environment variable or user input
    st.sidebar.title("OpenAI API Key")
    open_api_key = st.sidebar.text_input("Enter your OpenAI API Key")

    # Choose a image analysis model
    st.sidebar.title("Image analysis model")
    image_analysis_model = st.sidebar.selectbox(
        "Select an image analysis model",
        [
            "gpt-4o-mini",
            "gpt-4",
            "gpt-4-davinci",
            "gpt-4-davinci-instruct",
            "gpt-4-davinci-codex",
            "gpt-4-davinci-codex-instruct",
        ],
    )

    # Image Analysis Prompt
    st.sidebar.title("Image Analysis Prompt")
    image_prompt = st.sidebar.text_area(
        "Enter an image analysis prompt",
        value=st.session_state.image_analysis_prompt,
        height=150,
    )

    # Choose chat model
    st.sidebar.title("Chat model")
    chat_model = st.sidebar.selectbox(
        "Select a model",
        [
            "gpt-4o-mini",
            "gpt-4",
            "gpt-4-davinci",
            "gpt-4-davinci-instruct",
            "gpt-4-davinci-codex",
            "gpt-4-davinci-codex-instruct",
        ],
    )

    # Prompt Template
    st.sidebar.title("Prompt Template")
    prompt_template = st.sidebar.text_area(
        "Enter a prompt template",
        value=st.session_state.chat_prompt,
        height=150,
    )

    # Update the session state
    if chat_model:
        st.session_state.model = chat_model
    if image_analysis_model:
        st.session_state.image_model = image_analysis_model
    if prompt_template:
        st.session_state.prompt_template = prompt_template
    if image_prompt:
        st.session_state.image_analysis_prompt = image_prompt
    if open_api_key:
        st.session_state.open_api_key = open_api_key
