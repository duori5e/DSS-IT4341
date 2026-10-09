# backend/routers/course.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import get_db
from crud import course as crud_course
from schemas import course as schema_course

router = APIRouter(
    prefix="/api/courses",
    tags=["Courses"]
)

@router.get("/", response_model=list[schema_course.CourseResponse])
def read_courses(db: Session = Depends(get_db)):
    courses = crud_course.get_all_courses(db)
    return courses