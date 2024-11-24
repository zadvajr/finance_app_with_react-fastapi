"""main fastapi app"""
from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine
import models
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

class TransactionBase(BaseModel):
    amount: float
    category: str
    description: str
    is_income: bool
    date: str

class TransactionModel(TransactionBase):
    id: int

    class Config:
        from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

models.Base.metadata.create_all(bind=engine)

@app.post("/transactions/", response_model=TransactionModel, status_code=201)
async def create_transaction(transaction: TransactionBase, db: db_dependency):
    db_transaction = models.Transactions(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    
    return db_transaction

@app.get("/transactions/", response_model=list[TransactionModel])
async def read_transactions(db: db_dependency, skip: int=0, limit:int=100):
    transactions = db.query(models.Transactions).offset(skip).limit(limit).all()
    return transactions
