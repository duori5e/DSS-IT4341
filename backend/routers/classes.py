from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import get_db
from crud import classes as crud_classes
from schemas import classes as schema_classes

router = APIRouter(
    prefix="/api/classes",
    tags=["Classes"]
)

@router.get("/", response_model=list[schema_classes.ClassResponse])
def read_classes(db: Session = Depends(get_db)):
    return crud_classes.get_all_classes(db)