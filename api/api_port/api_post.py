from fastapi import APIRouter, Path, Query, Cookie, Header, status, Form, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from typing import Optional, List
from pydantic import BaseModel, Field
import json
from api_port import search
from api_port.db_tool import sql_tool
import hashlib

app_post = APIRouter()

def generate_sha256_hash(input_string):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_string.encode('utf-8'))
    hashed_value = sha256_hash.hexdigest()
    return hashed_value

@app_post.post("/signin/{user}&{key}")
async def Signin(user :str, key :str):
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

@app_post.post("/login/{user}&{key}")
async def Login(user :str, key :str):
    datadepot = sql_tool("shan", "finalproject", "users")
    content = datadepot.fetch_specific("user_name", user)
    successlogin = False
    if not content: return False
    key_db = content[0][1]
    key_login = generate_sha256_hash(key)
    if key_db == key_login: successlogin=True
    return successlogin