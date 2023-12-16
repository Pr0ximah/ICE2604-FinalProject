from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import json
import uvicorn
from api_port import app_get
from api_port import app_post

app = FastAPI()

app.mount(path="/file", app=StaticFiles(directory='api/api_port/file'), name="static")  #挂在静态文件，在主应用程序中， mount将目录中一个独立的应用挂载过来，和应用无关 

app.include_router(app_get, prefix='/api_port', tags=["一些get的请求接口"])      #给与对应的位置和名称
app.include_router(app_post, prefix='/api_port', tags=["一些post的请求接口"])      #给与对应的位置和名称

if __name__ == "__main__":
    uvicorn.run('api:app', host='127.0.0.1', port=8000, reload=True, workers=8)