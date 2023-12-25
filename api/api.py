from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import json
import uvicorn
from api_port import app_get
from api_port import app_post
from api_port.db_tool import sql_tool

dict_all = {}

def get_json_data():
    datadepot = sql_tool("ADMINROOT", "ice2604_final_project", "100_pdf_metadata")
    s = datadepot.fetch_all()
    for i in s:
        dict_elem = {}
        dict_elem["date"]=i[0]
        if i[1]:
            dict_elem["ref_paper"]=i[1].split(",")
        else:
            dict_elem["ref_paper"]=[]
        if i[2]:
            dict_elem["conference"]=i[2]
        else:
            dict_elem["conference"]=""
        if i[3]:
            dict_elem["keywords"]=i[3].split(",")
        else:
            dict_elem["keywords"]=[]
        dict_elem["year"]=int(i[4])
        if i[5]:
            dict_elem["author"]={"affiliation":i[5].split(","), "name":i[6].split(",")}
        else:
            dict_elem["author"] = {"affiliation": "", "name": ""}
        dict_elem["last_page"]=i[7]
        dict_elem["link"]=i[8]
        dict_elem["abstract"]=i[9]
        dict_elem["title"]=i[10]
        dict_elem["paper_id"]=i[11]
        if i[12] is not None:
            dict_elem["volume"]=int(i[12])
        dict_elem["update_time"]=i[13]
        dict_elem["journal"]=i[14]
        dict_elem["issn"]=i[15]
        dict_elem["first_page"]=i[16]
        dict_elem["publisher"]=i[17]
        dict_elem["doi"]=i[18]
        dict_all[i[11]]=dict_elem

get_json_data()


app = FastAPI()

# app.mount(path="/file", app=StaticFiles(directory='api/api_port/file'), name="static")  #挂在静态文件，在主应用程序中， mount将目录中一个独立的应用挂载过来，和应用无关 
app.mount(path="/api_port/IMG_pdf", app=StaticFiles(directory='./api/api_port/IMG_pdf/'), name="static")  #挂在静态文件，在主应用程序中， mount将目录中一个独立的应用挂载过来，和应用无关 

app.include_router(app_get, prefix='/api_port', tags=["一些get的请求接口"])      #给与对应的位置和名称
app.include_router(app_post, prefix='/api_port', tags=["一些post的请求接口"])      #给与对应的位置和名称

if __name__ == "__main__":
    uvicorn.run('api:app', host='127.0.0.1', port=8000, reload=True, workers=8)