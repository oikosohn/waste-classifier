
import io
import os
import time
from pathlib import Path

from PIL import Image

import streamlit as st

import requests

# SETTING PAGE CONFIG TO WIDE MODE
ASSETS_SRC_PATH = os.path.join(Path(__file__).parent.parent, "src")
ASSETS_MODEL_PATH = os.path.join(Path(__file__).parent.parent, "model")

st.set_page_config(layout="wide")

def main():
    st.title("Light weight model for recycle")

    st.write("재활용 쓰레기 이미지를 업로드해주세요!")

    start = time.time()
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg","png"])

    if uploaded_file:
        image_bytes = uploaded_file.getvalue()
        image = Image.open(io.BytesIO(image_bytes))

        st.image(image, caption='업로드한 이미지')

        # 추론 시작
        st.write("분류 중....")
        files = [
            ('files', (uploaded_file.name, image_bytes,
                       uploaded_file.type))
        ]
        response = requests.post("http://localhost:8001/cls", files=files)
        label = response.json()["products"][0]["result"]

        end = time.time()

        # 추론 결과 반영
        st.write("="*30)
        st.write("분류 완료")
        st.write(f'이 쓰레기는 {label[0]} 입니다.')
        st.write(f'이미지 업로드부터 분류 완료까지 {end-start} 초가 걸립니다.')


main()