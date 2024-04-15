from fastapi import FastAPI, Request, Depends

from pydantic import BaseModel
from khan import crawl
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import engine, get_db
from .models.token import Base, Token
import urllib.parse
import httpx
import json

Base.metadata.create_all(bind=engine)
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
def khan(otp: Otp, request: Request, db: Session = Depends(get_db)):
    request_id = request.app.state.request_id
    username = request.app.state.username
    response = crawl.login(otp.password, request_id, username)
    access_token = response['access_token']
    refresh_token = response['refresh_token']
    token = Token(access_token=access_token, refresh_token=refresh_token)
    db.add(token)
    db.commit()
    db.refresh(token)
    return {"message": "Token created successfully", "token_id": token.id}
    

@app.get('/transactions')
def transactions(db: Session = Depends(get_db)):
    return crawl.get_transaction(db)
    
@app.get('/refresh_token')
def refresh_token(db: Session = Depends(get_db)):
    crawl.get_token(db)
    return {'success': "hello"}