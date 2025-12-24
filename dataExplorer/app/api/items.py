from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import SessionLocal
from models.models import Customers
from schemas.item import ItemCreate, ItemOut

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ItemOut)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Customers(name=item.name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
