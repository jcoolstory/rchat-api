## 로켓챗 방식의 채팅 서버 

1. fastapi
2. virtualenv
3. mongodb
4. websocket


>설치
```sh
pip install -r requirements.txt
```

>실행

```sh
source venv/bin/activate  # mac venv 실행
uvicorn main:app --reload --host 0.0.0.0  
```


### swagger url

http://0.0.0.0:8000/docs

jwt
pip install 'fastapi-jwt-auth[asymmetric]'