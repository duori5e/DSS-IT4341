# backend/routers/lecturer.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import get_db
from crud import lecturer as crud_lecturer
from schemas import lecturer as schema_lecturer

router = APIRouter(
    prefix="/api/lecturers",
    tags=["Lecturers"]
)

@router.get("/", response_model=list[schema_lecturer.LecturerResponse])
def read_lecturers(db: Session = Depends(get_db)):
    return crud_lecturer.get_all_lecturers(db)