from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from database.connection import get_db
from crud import course as crud_course
from schemas.course import CourseCreate, CourseUpdate, CourseResponse

router = APIRouter()

@router.get("/", response_model=List[CourseResponse])
def read_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return crud_course.get_courses(db, skip=skip, limit=limit)

@router.get("/{course_id}", response_model=CourseResponse)
def read_course(course_id: str, db: Session = Depends(get_db)):
    db_course = crud_course.get_course(db, course_id=course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy học phần '{course_id}'")
    return db_course

@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    if crud_course.get_course(db, course_id=course.course_id):
        raise HTTPException(status_code=400, detail=f"Mã học phần '{course.course_id}' đã tồn tại")
    return crud_course.create_course(db, course=course)

@router.put("/{course_id}", response_model=CourseResponse)
def update_course(course_id: str, course_update: CourseUpdate, db: Session = Depends(get_db)):
    db_course = crud_course.get_course(db, course_id=course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy học phần '{course_id}'")
    return crud_course.update_course(db, db_course=db_course, course_update=course_update)

@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: str, db: Session = Depends(get_db)):
    db_course = crud_course.get_course(db, course_id=course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy học phần '{course_id}'")
    crud_course.delete_course(db, db_course=db_course)