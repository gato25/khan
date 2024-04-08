from fastapi import FastAPI, Request
from pydantic import BaseModel
from khan import crawl

app = FastAPI()


class Auth(BaseModel):
    username: str
    password: str

class Otp(BaseModel):
    password: str

@app.post('/get_otp')
def get_otp(auth: Auth, request: Request):
    global request_id
    response =  crawl.get_otp(auth.password) 
    request.app.state.request_id = response['unique_id']
    return response

@app.post('/login')
def khan(otp: Otp, request: Request):
    request_id = request.app.state.request_id
    return crawl.login(otp.password, request_id)