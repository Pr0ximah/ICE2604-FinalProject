from fastapi import FastAPI
import uvicorn
from api_port import app_get
import json
from api_port import search

"""写的异常处理报告，未完善，待测试"""
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import RequestValidationError
# from fastapi.exceptions import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import ValidationError


app = FastAPI()

@app.exception_handler(StarletteHTTPException)#重写HTTPException的异常处理
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

@app.exception_handler(RequestValidationError)#重写请求异常验证处理器
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=exc.status_code)

app.include_router(app_get, prefix='/api_port', tags=["一些get的请求接口"])      #给与对应的位置和名称

# @app.get("/search/content={content}&type={type}")
# def read_all_data(type: str, content: str):
#     data = json.loads(search.get_result(type, content))
#     return {"data": data}

if __name__ == "__main__":
    uvicorn.run('api:app', host='127.0.0.1', port=8000, reload=True, workers=8)