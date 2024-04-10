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
    base_url = "https://e.khanbank.com/v1/omni/user/custom/operativeaccounts/5429348172/transactions"
    token = db.query(Token).order_by(Token.created_at.desc()).first()
    print('hello',token.id)
    access_token = crawl.refresh_token(db)['access_token']
    
    
    if token:
        # access_token = token.access_token
        
        base_url = "https://e.khanbank.com/v1/omni/user/custom/operativeaccounts/5429348172/transactions"
        
        # JSON data
        json_data = {
            "transactionValue": 0,
            "transactionDate": {
                "lt": "2024-04-10T00:00:00",
                "gt": "2024-04-10T00:00:00"
            },
            "amount": {
                "lt": "0",
                "gt": "0"
            },
            "transactionCategoryId": "",
            "transactionRemarks": "",
            "customerName": "ДАМБА БАДАМГАРАВ",
            "transactionCurrency": "MNT",
            "branchCode": "5029"
        }
        
        # Construct the query parameters from the JSON data
        query_params = {}
        for key, value in json_data.items():
            if isinstance(value, dict):
                query_params[key] = json.dumps(value)
            else:
                query_params[key] = value
        
        # Encode the query parameters
        encoded_params = urllib.parse.urlencode(query_params)
        
        # Construct the complete request URL
        url = f"{base_url}?{encoded_params}"
        
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'mn-MN',
            'Authorization': f'Bearer {access_token}',
            'Connection': 'keep-alive',
            'Referer': 'https://e.khanbank.com/account/statement/5429348172/MNT/OPR',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }
        
        response = httpx.get(url, headers=headers)
        print(response.text)
        
        return {"message": "API request successful", "response": response.json()}
    
    else:
        return {"message": "No access token found in the database"}
    
