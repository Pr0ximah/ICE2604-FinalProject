from fastapi import APIRouter, Path, Query, Cookie, Header,Form
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field
import json
from api_port import search

app_get = APIRouter()

def GetYear(data):
    Year_number = {}
    for i in data:
        year = i["_source"]["year"]
        if year in Year_number:
            Year_number[year] += 1
        else:
            Year_number[year] = 1
    year_list = [{"year": i, "num": j} for i, j in Year_number.items()]
    sorted_year_list = sorted(year_list, key=lambda x: x["year"])
    return sorted_year_list

@app_get.get("/search/content={content}&type={type}")
def read_all_data(type:str, content:str):
    data = []
    if type == "Title":
        data = json.loads(search.get_json(search.search_title(content)))
    elif type == "Year":
        data = json.loads(search.get_json(search.search_year(content)))
    elif type == "Author":
        data = json.loads(search.get_json(search.search_author(content)))
    elif type == "Keywords":
        data = json.loads(search.get_json(search.search_keywords(content)))
    year_number = GetYear(data)
    return {"data" : data, "year_list": year_number}

@app_get.get("/search_yearnumber/content={content}&type={type}")
def get_year_number(type:str, content:str):
    data = []
    if type == "Title":
        data = json.loads(search.get_json(search.search_title(content)))
    elif type == "Year":
        data = json.loads(search.get_json(search.search_year(content)))
    elif type == "Author":
        data = json.loads(search.get_json(search.search_author(content)))
    elif type == "Keywords":
        data = json.loads(search.get_json(search.search_keywords(content)))
    year_number = GetYear(data)
    return {"year_list" : year_number}

@app_get.get("/search/year/content={content}")
def get_year(content: str):
    data = []
    data = json.loads(search.get_json(search.search_year(content)))
    year_number = GetYear(data)
    return {"data" : data, "year_list": year_number}

@app_get.get("/search/title/content={content}")
def get_title(content: str):
    data = []
    data = json.loads(search.get_json(search.search_title(content)))
    year_number = GetYear(data)
    return {"data" : data, "year_list": year_number}

@app_get.get("/search/author/content={content}")
def get_author(content: str):
    data = []
    data = json.loads(search.get_json(search.search_author(content)))
    year_number = GetYear(data)
    return {"data" : data, "year_list": year_number}

@app_get.get("/search/keywords/content={content}")
def get_keywords(content: str):
    data = []
    data = json.loads(search.get_json(search.search_keywords(content)))
    year_number = GetYear(data)
    return {"data" : data, "year_list": year_number}

if __name__ == '__main__':
    print(get_keywords("Sm"))