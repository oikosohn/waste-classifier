
import io
import os
import time
from pathlib import Path

from PIL import Image

import streamlit as st

import requests

ASSETS_SRC_PATH = os.path.join(Path(__file__).parent.parent, "src")
ASSETS_MODEL_PATH = os.path.join(Path(__file__).parent.parent, "model")

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

def main():

    st.title("Light weight model for recycle")

    rotation = st.sidebar.radio('이미지 회전 :', ['원본', '오른쪽으로 90도 회전','왼쪽으로 90도 회전','180도 회전'])
    
    st.write("재활용 쓰레기 이미지를 업로드해주세요!")
    
    
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg","png"])

    if uploaded_file:
        image_bytes = uploaded_file.getvalue()
        image = Image.open(io.BytesIO(image_bytes))
        
        col1, col2 = st.columns([0.5, 0.5])
        with col1:
            st.markdown('<p style="text-align: center;">Before</p>', unsafe_allow_html=True)
            st.image(image, caption='업로드한 이미지')

        with col2:
            st.markdown('<p style="text-align: center;">After</p>', unsafe_allow_html=True)
            
            if rotation == '원본':
                st.image(image, caption='원본')
            elif rotation == '왼쪽으로 90도 회전':
                image = image.rotate(90)
                st.image(image, caption='왼쪽으로 90도 회전')
            elif rotation == '오른쪽으로 90도 회전':
                image = image.rotate(270)
                st.image(image, caption='오른쪽으로 90도 회전')
            elif rotation == '180도 회전':
                image = image.rotate(180)
                st.image(image, caption='180도 회전')

        submmit = st.sidebar.button(label='제출')

        if submmit:
            start = time.time()
            rotated_image_byte = io.BytesIO()
            image.save(rotated_image_byte, format='PNG')
            rotated_image_byte = rotated_image_byte.getvalue()

            # 추론 시작
            st.write("분류 중....")
            files = [
                ('files', (uploaded_file.name, rotated_image_byte,
                        uploaded_file.type))
            ]
            response = requests.post("http://localhost:8001/cls", files=files)
            label = response.json()["products"][0]["result"]
            end = time.time()

            # 추론 결과 반영
            st.write("="*30)
            st.write("분류 완료")
            st.write(f'이 쓰레기는 {label[0]} 입니다.')
            st.write(f'이미지 제출부터 분류 완료까지 {end-start} 초가 걸립니다.')

main()
