from fastapi import APIRouter, Path, Query, Cookie, Header, status, Form, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from typing import Optional, List
from pydantic import BaseModel, Field
import json
from api_port import search
from api_port.db_tool import sql_tool
import hashlib
from datetime import datetime

app_post = APIRouter()

def generate_sha256_hash(input_string):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_string.encode('utf-8'))
    hashed_value = sha256_hash.hexdigest()
    return hashed_value

@app_post.post("/signup")
async def Signup(user :str, key :str):
    datadepot = sql_tool("shan", "finalproject", "users")
    content = datadepot.fetch_specific("user_name", user)
    if content: return False
    successsignin = False
    key_db=generate_sha256_hash(key)
    datadepot.insert([f"{user}", f"{key_db}"])
    datadepot.save()
    content = datadepot.fetch_specific("user_name", user)
    if content: successsignin = True
    return successsignin

@app_post.post("/login")
async def Login(user :str, key :str):
    datadepot = sql_tool("shan", "finalproject", "users")
    content = datadepot.fetch_specific("user_name", user)
    successlogin = False
    if not content: return False
    key_db = content[0][1]
    key_login = generate_sha256_hash(key)
    if key_db == key_login: successlogin=True
    return successlogin

# 登录的接口，返回password
@app_post.post("/login_password")
async def LoginPassword(user:str, time: datetime):
    datadepot = sql_tool("shan", "finalproject", "users")
    content = datadepot.fetch_specific("user_name", user)
    successsigninpassword = False
    time_str = time.strftime("%Y-%m-%d %H:%M:%S")
    password=user+time_str
    key_db=generate_sha256_hash(password)
    datadepot.insert_column_by_username("login_time", key_db, user)
    datadepot.save()
    content = datadepot.fetch_specific("user_name", user)
    if content: successsigninpassword = True
    return key_db
    # return successsigninpassword

# 验证的接口，返回True和False
@app_post.post("/confirm_password")
async def Confiem_Password(user : str, password : str):
    datadepot = sql_tool("shan", "finalproject", "users")
    content = datadepot.fetch_specific("user_name", user)
    password_db = content[0][3]
    if password == password_db: return True
    else: return False

# 收集能力没写完
@app_post.post("/collectpaper")
async def Collect(user: str, paper_id :str):
    datadepot = sql_tool("shan", "finalproject", "users")
    datadepot_pdf = sql_tool("shan", "finalproject", "users")
    content = datadepot_pdf.fetch_specific("paper_id", paper_id)  #在储存pdf的数据库中读取
    '''根据content进行更改'''
    title = content
    author = content

    content_user = datadepot.fetch_specific("user_name", user)
    oldpaper = content_user[0][2]
    oldpaper_dict=json.loads(oldpaper)
    oldpaper_dict[f"{paper_id}"] = [f"{title}", f"{author}"]
    newpaper= json.dumps(oldpaper_dict)
    datadepot.insert_column()
    return content