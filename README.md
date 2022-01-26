# “초”경량 재활용쓰레기 이미지 분류기

[model-optimization-level3-cv-18](https://github.com/boostcampaitech2/model-optimization-level3-cv-18)의 Best model을 이용한 프로토타이핑

## 시연 영상
![streamlit-frontend-2022-01-26-10-01-91](https://user-images.githubusercontent.com/59533593/151091010-06d0804e-e59e-40f1-8d34-a4d874dc84a1.gif)


## 실행 방법

### 가상환경 설정
```
conda create -n OCR
conda activate OCR
pip install -r requirements.txt
```
- OCR 대신 다른 이름으로 대체 가능

### Streamlit, FastAPI 실행
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

## Reference
`src` in this repo is based on Kindle(by JeiKeiLim)
