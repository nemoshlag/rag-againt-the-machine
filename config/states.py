import os

import streamlit as st


def set_default_state(key, value):
    if key not in st.session_state:
        st.session_state[key] = value


def set_initial_state():
    set_default_state("open_api_key", os.environ.get("OPENAI_API_KEY", ""))
    set_default_state("model", "gpt-4o-mini")
    set_default_state("image_model", "gpt-4o-mini")
    set_default_state(
        "chat_prompt",
        "You are a professional car repair assistant. Use the provided context to diagnose issues and provide solutions.",
    )
    set_default_state(
        "image_analysis_prompt",
        "You are an expert car repair assistant. Analyze the image for any potential malfunctions, damages, or abnormalities related to car parts.",
    )
