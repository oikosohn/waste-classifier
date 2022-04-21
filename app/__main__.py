if __name__ == "__main__":
    import uvicorn
    # uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
    
    # if you want not use sentry, then comment out below.
    import sentry_sdk
    from sentry_sdk import capture_exception

    sentry_sdk.init(
        "sentry_url 추가",
        traces_sample_rate = 1.0
    )
    
    try:
        # 배포하고 sentry를 사용하기 위해서 아래 명령어를 수정해야 함
        uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
    except Exception as e:
        capture_exception(e)
        raise e
