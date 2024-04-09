from fastapi import FastAPI, Request
from pydantic import BaseModel
from khan import crawl
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Auth(BaseModel):
    username: str
    password: str

class Otp(BaseModel):
    password: str

@app.post('/get_otp')
def get_otp(auth: Auth, request: Request):
    response =  crawl.get_otp(auth.username, auth.password) 
    request.app.state.request_id = response['unique_id']
    request.app.state.username = auth.username
    return response

@app.post('/login')
def khan(otp: Otp, request: Request):
    request_id = request.app.state.request_id
    username = request.app.state.username
    return crawl.login(otp.password, request_id, username)