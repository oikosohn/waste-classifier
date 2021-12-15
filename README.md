# “초”경량 이미지 분류기

## 환경 설정

- OCR은 다른 가상환경 이름으로 대체 가능
```
conda create -n OCR
conda activate OCR
pip install -r requirements.txt
```

## Streamlit, FastAPI 실행
리눅스
```
make -j 2 run_app
```

윈도우 
```
# FastAPI 백그라운드 실행
start /b python -m app

# Streamlit 포그라운드 실행
streamlit run app/frontend.py

```
