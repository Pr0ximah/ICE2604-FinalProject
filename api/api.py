from fastapi import FastAPI
import json
import uvicorn
from api_port import app_get

app = FastAPI()

app.include_router(app_get, prefix='/api_port', tags=["一些get的请求接口"])      #给与对应的位置和名称

if __name__ == "__main__":
    uvicorn.run('api:app', host='127.0.0.1', port=8000, reload=True, workers=8)