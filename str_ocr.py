import os
import base64
from PIL import Image
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st
from io import BytesIO


# Load environment variables
load_dotenv()

# # Get API keys from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

st.title("携帯OCRアプリ")
uploaded_file = st.file_uploader("文字を読み取る写真をアップロードしてください", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_byte = buffered.getvalue()
    encoded_image = base64.b64encode(img_byte).decode("utf-8")

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an excellent secretary who responds in Japanese."},
            {"role": "user",
            "content": [
                {"type": "text", "text": """\
            ## 命令
            この画像に表示されている文字を教えて下さい。
            書かれている文字以外は応答しないでください。

            ## Output
            """},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{encoded_image}"
                            },
                        },
                    ],
                    }
                ]
            )

    st.write(completion.choices[0].message.content)