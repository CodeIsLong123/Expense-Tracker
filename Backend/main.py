from enum import Enum
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from Database_actions import db_actions

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Category(str, Enum):
    income = "income"
    expense = "expense"

class Item(BaseModel):
    name: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)
    category: Category
    id: Optional[int] = None

class QueryResult(BaseModel):
    items: List[Item]

db = db_actions.DatabseActions()

@app.get("/", response_model=QueryResult)
def index():
    transactions = db.show_all_entries()
    return {"items": transactions}

@app.get("/transaction/{id}", response_model=Item)
def get_transaction(id: int):
    transaction = db.get_transaction_by_id(id)
    if not transaction:
        raise HTTPException(status_code=404, detail=f"Transaction {id} not found")
    return transaction

@app.delete("/transaction/{id}")
def delete_transaction(id: int):
    transaction = db.get_transaction_by_id(id)
    if not transaction:
        raise HTTPException(status_code=404, detail=f"Transaction {id} not found")
    db.delete_from_id(id)
    return {"message": f"Transaction {id} deleted"}

@app.post("/items", response_model=Item)
def add_transaction(item: Item):
    try:
        new_id = db.insert_into_table(item.name, item.amount, item.category.value)
        item.id = new_id
        return item
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    
    dh = db_actions.DatabseActions()

    print(dh.show_all_entries())    