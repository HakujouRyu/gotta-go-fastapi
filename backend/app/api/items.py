from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.database import get_db
from app.common.models import Item
from app.common.schemas import Item as ItemSchema
from app.common.schemas import ItemCreate

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[ItemSchema])
def list_items(db: Session = Depends(get_db)):  # noqa: B008
    return db.query(Item).all()


@router.post("", response_model=ItemSchema)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):  # noqa: B008
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/{item_id}", response_model=ItemSchema)
def get_item(item_id: int, db: Session = Depends(get_db)):  # noqa: B008
    return db.query(Item).filter(Item.id == item_id).first()
