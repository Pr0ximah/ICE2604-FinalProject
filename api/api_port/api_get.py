from fastapi import APIRouter, Path, Query, Cookie, Header, status, Form, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from typing import Optional, List
from pydantic import BaseModel, Field
import json
from api_port import search
from api_port.db_tool import sql_tool

app_get = APIRouter()

def Push_Error():
    error_name = search.error_name
    print(error_name)
    if error_name == "ConnectionError":
        print("连接错误:无法连接到Elasticsearch。")
        raise HTTPException(status_code=418, detail="连接错误:无法连接到Elasticsearch。")
    elif error_name == "NameError":     #目前来看有点问题，没有继续往下写
        print("输入错误:根据年份查询需要输入数字")
        raise HTTPException(status_code=423, detail="输入错误:查询年份需要输入数字")
    elif error_name=="":
        return

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


def GetJournal(data):
    Journal_list = {}
    for i in data:
        journal = i["_source"]["journal"]
        if journal == "" or journal is None:
            journal = "Others"
        if journal in Journal_list:
            Journal_list[journal] += 1
        else:
            Journal_list[journal] = 1
    Journal_list = [{"journal": i, "num": j} for i, j in Journal_list.items()]
    sorted_Jounral_list = sorted(Journal_list, key=lambda x: x["num"], reverse=True)
    return sorted_Jounral_list

@app_get.get("/search/content={content}&type={type}")
async def read_all_data(type:str, content:str):
    Push_Error()
    data = []
    if type == "Title":
        data = json.loads(search.get_json(search.search_title(content)))
    elif type == "Year":
        data = json.loads(search.get_json(search.search_year(content)))
        # Push_Error()
    elif type == "Author":
        data = json.loads(search.get_json(search.search_author(content)))
    elif type == "Keywords":
        data = json.loads(search.get_json(search.search_keywords(content)))
    elif type == "All":
        data = json.loads(search.get_json(search.add_search(content)))
        data.sort(key=lambda x: x['_score'], reverse=True)
        data_tmp = []
        id_set = set()
        for i in data:
            id = i["_source"]['paper_id']
            if id in id_set:
                continue
            else:
                id_set.add(id)
                data_tmp.append(i)
        data = data_tmp.copy()
    year_number = GetYear(data)
    journal_list = GetJournal(data)
    return {"data" : data, "year_list": year_number, "journal_list": journal_list}

@app_get.get("/search_yearnumber/content={content}&type={type}")
async def get_year_number(type:str, content:str):
    Push_Error()
    data = []
    if type == "Title":
        data = json.loads(search.get_json(search.search_title(content)))
    elif type == "Year":
        data = json.loads(search.get_json(search.search_year(content)))
        Push_Error()
    elif type == "Author":
        data = json.loads(search.get_json(search.search_author(content)))
    elif type == "Keywords":
        data = json.loads(search.get_json(search.search_keywords(content)))
    year_number = GetYear(data)
    return {"year_list" : year_number}

@app_get.get("/search/year/content={content}")
async def get_year(content: str):
    Push_Error()
    data = []
    data = json.loads(search.get_json(search.search_year(content)))
    Push_Error()
    year_number = GetYear(data)
    return {"data" : data, "year_list": year_number}

@app_get.get("/search/title/content={content}")
async def get_title(content: str):
    Push_Error()
    data = []
    data = json.loads(search.get_json(search.search_title(content)))
    year_number = GetYear(data)
    return {"data" : data, "year_list": year_number}

@app_get.get("/search/author/content={content}")
async def get_author(content: str):
    Push_Error()
    data = []
    data = json.loads(search.get_json(search.search_author(content)))
    year_number = GetYear(data)
    return {"data" : data, "year_list": year_number}

@app_get.get("/search/keywords/content={content}")
async def get_keywords(content: str):
    Push_Error()
    data = []
    data = json.loads(search.get_json(search.search_keywords(content)))
    year_number = GetYear(data)
    return {"data" : data, "year_list": year_number}


@app_get.get("/file/{paper_id}")
async def getfile(paper_id :str):
    return f"/file/{paper_id}.pdf"

if __name__ == '__main__':
    print(get_keywords("Sm"))