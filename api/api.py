from fastapi import FastAPI
import json
import search

app = FastAPI()

@app.get("/search/content={content}&type={type}")
def read_all_data(type: str, content: str):
    data = json.loads(search.get_result(type, content))
    return {"data": data}