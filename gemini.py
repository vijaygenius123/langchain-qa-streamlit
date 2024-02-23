import os

from dotenv import load_dotenv
import streamlit as st
import vertexai as vertexai

from langchain_google_vertexai import ChatVertexAI
from langchain_core.messages import HumanMessage
import base64

load_dotenv()

st.set_page_config(page_title="Gemini", page_icon="🌟")

vertexai.init(project=os.getenv('PROJECT_ID'), location="europe-west2")

llm = ChatVertexAI(model_name="gemini-1.0-pro-vision-001")

uploaded_file = st.file_uploader('Upload a file', type=['png', 'jpg', 'jpeg'])
st.header('Whats in this image ?')

IMAGE_SAVE_PATH = 'image.png'

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    st.image(bytes_data, caption='Uploaded Image.', use_column_width=True)
    base64_str = base64.b64encode(bytes_data).decode('utf-8')

    image_message = {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{base64_str}"
        },
    }
    text_message = {
        "type": "text",
        "text": "What is shown in this image?",
    }
    message = HumanMessage(content=[text_message, image_message])

    output = llm([message])

    st.success(output)
