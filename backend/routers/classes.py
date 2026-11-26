from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from database.connection import get_db
from crud import classes as crud_classes, course as crud_course
from schemas.classes import ClassCreate, ClassUpdate, ClassResponse

router = APIRouter()

@router.get("/", response_model=List[ClassResponse])
def read_classes(
    term: Optional[str] = Query(None, description="Lọc theo học kỳ (VD: 20241)"),
    course_id: Optional[str] = Query(None, description="Lọc theo mã học phần (VD: IT4341)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return crud_classes.get_classes(db, term=term, course_id=course_id, skip=skip, limit=limit)

@router.get("/{class_id}", response_model=ClassResponse)
def read_class(class_id: str, db: Session = Depends(get_db)):
    db_class = crud_classes.get_class(db, class_id=class_id)
    if not db_class:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy lớp học phần '{class_id}'")
    return db_class

@router.post("/", response_model=ClassResponse, status_code=status.HTTP_201_CREATED)
def create_class(class_in: ClassCreate, db: Session = Depends(get_db)):
    if crud_classes.get_class(db, class_id=class_in.class_id):
        raise HTTPException(status_code=400, detail=f"Mã lớp '{class_in.class_id}' đã tồn tại")
    if class_in.course_id and not crud_course.get_course(db, course_id=class_in.course_id):
        raise HTTPException(status_code=400, detail=f"Mã học phần '{class_in.course_id}' không tồn tại")
    return crud_classes.create_class(db, class_in=class_in)

@router.put("/{class_id}", response_model=ClassResponse)
def update_class(class_id: str, class_update: ClassUpdate, db: Session = Depends(get_db)):
    db_class = crud_classes.get_class(db, class_id=class_id)
    if not db_class:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy lớp học phần '{class_id}'")
    if class_update.course_id and not crud_course.get_course(db, course_id=class_update.course_id):
        raise HTTPException(status_code=400, detail=f"Mã học phần '{class_update.course_id}' không tồn tại")
    return crud_classes.update_class(db, db_class=db_class, class_update=class_update)

@router.delete("/{class_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_class(class_id: str, db: Session = Depends(get_db)):
    db_class = crud_classes.get_class(db, class_id=class_id)
    if not db_class:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy lớp học phần '{class_id}'")
    crud_classes.delete_class(db, db_class=db_class)