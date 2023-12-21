from fastapi import (
    APIRouter,
    Path,
    Query,
    Cookie,
    Header,
    status,
    Form,
    File,
    UploadFile,
    HTTPException,
)
from fastapi.responses import FileResponse
from typing import Optional, List
from pydantic import BaseModel, Field
import json
from api_port import search
from api_port.db_tool import sql_tool
import hashlib
import os
from datetime import datetime


class login_item(BaseModel):
    user: str = ""
    key: str = ""


class login_time(BaseModel):
    user: str = ""


class confirm_password(BaseModel):
    user: str = ""
    password: str = ""


class name_paperid(BaseModel):
    user: str = ""
    paper_id: str = ""


class user_name(BaseModel):
    user: str = ""


class get_id_model(BaseModel):
    id: str = ""


app_post = APIRouter()


def generate_sha256_hash(input_string):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_string.encode("utf-8"))
    hashed_value = sha256_hash.hexdigest()
    return hashed_value


@app_post.post("/signup")
async def Signup(item: login_item):
    user = item.user
    key = item.key
    datadepot = sql_tool("ADMINROOT", "ice2604_final_project", "users")
    content = datadepot.fetch_specific("user_name", user)
    if content:
        return False
    successsignin = False
    key_db = generate_sha256_hash(key)
    datadepot.insert([f"{user}", f"{key_db}", None, None])
    datadepot.save()
    content = datadepot.fetch_specific("user_name", user)
    if not content:
        return False
    time = datetime.now()
    time_str = time.strftime("%Y-%m-%d %H:%M:%S")
    password = user + time_str
    key_db = generate_sha256_hash(password)
    datadepot.insert_column_by_username("login_time", key_db, user)
    datadepot.save()
    content = datadepot.fetch_specific("user_name", user)
    return key_db


@app_post.post("/login")
async def Login(item: login_item):
    user = item.user
    key = item.key
    datadepot = sql_tool("ADMINROOT", "ice2604_final_project", "users")
    content = datadepot.fetch_specific("user_name", user)
    successlogin = False
    if not content:
        return False
    key_db = content[0][1]
    key_login = generate_sha256_hash(key)
    if key_db != key_login:
        return False
    content = datadepot.fetch_specific("user_name", user)
    time = datetime.now()
    time_str = time.strftime("%Y-%m-%d %H:%M:%S")
    password = user + time_str
    key_db = generate_sha256_hash(password)
    datadepot.insert_column_by_username("login_time", key_db, user)
    datadepot.save()
    content = datadepot.fetch_specific("user_name", user)
    return key_db


# 登录的接口，返回password
@app_post.post("/login_password")
async def LoginPassword(item: login_time):
    datadepot = sql_tool("ADMINROOT", "ice2604_final_project", "users")
    user = item.user
    content = datadepot.fetch_specific("user_name", user)
    successsigninpassword = False
    time = datetime.now()
    time_str = time.strftime("%Y-%m-%d %H:%M:%S")
    password = user + time_str
    key_db = generate_sha256_hash(password)
    datadepot.insert_column_by_username("login_time", key_db, user)
    datadepot.save()
    content = datadepot.fetch_specific("user_name", user)
    if content:
        successsigninpassword = True
    return key_db
    # return successsigninpassword


# 验证的接口，返回True和False
@app_post.post("/confirm_password")
async def Confiem_Password(item: confirm_password):
    user = item.user
    password = item.password
    datadepot = sql_tool("ADMINROOT", "ice2604_final_project", "users")
    content = datadepot.fetch_specific("user_name", user)
    try:
        password_db = content[0][3]
        if password == password_db:
            return True
        else:
            return False
    except Exception:
        return False


@app_post.post("/collectpaper")
async def Collect(item: name_paperid):
    user = item.user
    paper_id = item.paper_id
    datadepot = sql_tool("ADMINROOT", "ice2604_final_project", "users")
    content = datadepot.fetch_specific("user_name", user)
    oldpaper = content[0][2]
    # return oldpaper
    paper_list = []
    if not oldpaper:
        paper_list.append(paper_id)
        newpaper_dict = {"user": paper_list}
        newpaper = json.dumps(newpaper_dict)
    else:
        # print(oldpaper)
        oldpaper_dict = json.loads(oldpaper)
        paper_list = oldpaper_dict["user"]
        for i in paper_list:
            # print(i)
            if not i:
                paper_list.remove(i)
            if i == paper_id:
                return {"error": "This article has been collected!"}
        paper_list.append(paper_id)
        newpaper_dict = {"user": paper_list}
        newpaper = json.dumps(newpaper_dict)
    datadepot.insert_column_by_username("love_paper", newpaper, user)
    datadepot.save()
    content = datadepot.fetch_specific("user_name", user)
    content = json.loads(content[0][2])
    return True


@app_post.post("/removepaper")
async def Removepaper(item: name_paperid):
    user = item.user
    paper_id = item.paper_id
    datadepot = sql_tool("ADMINROOT", "ice2604_final_project", "users")
    content = datadepot.fetch_specific("user_name", user)
    oldpaper = content[0][2]
    if not oldpaper:
        return {"error": "This user hasn't collect article!"}
    oldpaper_dict = json.loads(oldpaper)
    paper_list = oldpaper_dict["user"]
    if paper_id in paper_list:
        paper_list.remove(paper_id)
    else:
        return {"error": "This is article is not collected by this user!"}
    newpaper_dict = {"user": paper_list}
    newpaper = json.dumps(newpaper_dict)
    datadepot.insert_column_by_username("love_paper", newpaper, user)
    datadepot.save()
    return True


@app_post.post("/get_collected_paper")
async def GetCollectedPaper(item: user_name):
    user = item.user
    if not user:
        return ""
    datadepot = sql_tool("ADMINROOT", "ice2604_final_project", "users")
    datadepot_pdf = sql_tool("ADMINROOT", "ice2604_final_project", "100_pdf_metadata")
    content_paper = datadepot.fetch_specific("user_name", user)
    content_paper_list_json = content_paper[0][2]
    if not content_paper_list_json:
        # return {"error":"This user hasn't collect article!"}
        return ""
    paper_dict = json.loads(content_paper_list_json)
    paper_list = paper_dict["user"]
    if not paper_list:
        # return {"error":"This user hasn't collect article!"}
        return ""
    return_dict = {}
    print(paper_list)
    for paper_id in paper_list:
        content_pdf = datadepot_pdf.fetch_specific(
            "paper_id", paper_id
        )  # 在储存pdf的数据库中读取
        # return(content_pdf)
        content_list = content_pdf[0]
        return_list = {}
        return_list["DOI"] = content_list[18]
        return_list["Year"] = content_list[4]
        return_list["Journal"] = content_list[14]
        if content_list[6]:
            return_list["Authors"] = content_list[6].split(",")
        if content_list[3]:
            return_list["Keywords"] = content_list[3].split(",")
        return_list["Abstract"] = content_list[9]
        return_list["Title"] = content_list[10]
        return_list["Link"] = content_list[8]
        return_list["ID"] = content_list[11]
        return_dict[f"{paper_id}"] = return_list
    return return_dict


@app_post.post("/get_img")
async def get_img(item: get_id_model):
    paper_id = item.id
    base = "./api/api_port/IMG_pdf/"
    tar_loc = os.path.join(base, paper_id)
    if os.path.exists(tar_loc):
        filenames = os.listdir(tar_loc)
        if filenames:
            return [f"{os.path.join('/IMG_pdf', paper_id, i)}" for i in filenames]
        else:
            return False
    else:
        return False


testdata = [
    {
        "data": [
            {
                "date": "2016-05-03",
                "name": "Tom",
                "address": "No. 189, Grove St, Los Angeles",
            },
            {
                "date": "2016-05-02",
                "name": "Tom",
                "address": "No. 189, Grove St, Los Angeles",
            },
            {
                "date": "2018-05-02",
                "name": "Jack",
                "address": "No. 190, Grove St, Los Angeles",
            },
        ],
        "head": [
            "date",
            "name",
            "address",
        ],
    },
]


@app_post.post("/get_table")
async def get_table(item: get_id_model):
    paper_id = item.id
    return testdata
    # base = './api/api_port/IMG_pdf/'
    # tar_loc = os.path.join(base, paper_id)
    # if (os.path.exists(tar_loc)):
    #     filenames = os.listdir(tar_loc)
    #     if (filenames):
    #         return [f"{os.path.join('/IMG_pdf', paper_id, i)}" for i in filenames]
    #     else:
    #         return False
    # else:
    #     return False
