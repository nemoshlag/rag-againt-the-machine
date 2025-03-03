import os

import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
import base64
import tempfile

import faiss
import pytesseract
from PIL import Image
from sentence_transformers import SentenceTransformer

from components.sidebar import sidebar
from config.states import set_initial_state

#  Set the initial state
set_initial_state()
sidebar()

# Load Sentence Transformer Model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Set OpenAI API Key


# Function to create FAISS index
def create_faiss_index(chunks):
    embeddings = model.encode(chunks)
    d = embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)
    return index, embeddings


# Function to query FAISS index
def query_faiss_index(index, chunks, query, top_k=3):
    query_embedding = model.encode([query])
    D, I = index.search(query_embedding, top_k)
    return [chunks[i] for i in I[0]]


# Function to extract text from images
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text


# Function to describe image using OpenAI
def describe_image_with_llm(image_path):
    image = Image.open(image_path)
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        response = client.chat.completions.create(
            model=st.session_state.image_model,
            messages=[
                {
                    "role": "system",
                    "content": st.session_state.image_analysis_prompt,
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            },
                        }
                    ],
                },
            ],
        )
    return response.choices[0].message.content


# Streamlit UI
st.title("Car Repair AI Assistant")

uploaded_file = st.file_uploader(
    "Upload a car part image or repair treatment data",
    type=["txt", "png", "jpg", "jpeg"],
)
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    if uploaded_file.type in ["image/png", "image/jpeg"]:
        extracted_text = extract_text_from_image(temp_path)
        image_description = describe_image_with_llm(temp_path)
        document_text = f"Extracted Text:\n{extracted_text}\n\nCar Part Analysis:\n{image_description}"
    else:
        with open(temp_path, "r", encoding="utf-8") as f:
            document_text = f.read()

    os.remove(temp_path)

    # Split document into chunks
    chunks = document_text.split("\n\n")

    # Create FAISS Index
    index, _ = create_faiss_index(chunks)
    st.success("Data uploaded and indexed successfully!")

    query = st.text_input("Ask about car parts or repair data:")
    if query:
        relevant_chunks = query_faiss_index(index, chunks, query)
        context = "\n".join(relevant_chunks)

        # Query OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": st.session_state.chat_prompt,
                },
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"},
            ],
        )

        st.write("### Answer:")
        st.write(response.choices[0].message.content)
