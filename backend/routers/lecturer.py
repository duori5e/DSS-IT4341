from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from database.connection import get_db
from crud import lecturer as crud_lecturer
from schemas.lecturer import LecturerCreate, LecturerUpdate, LecturerResponse

router = APIRouter()

@router.get("/", response_model=List[LecturerResponse])
def read_lecturers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return crud_lecturer.get_lecturers(db, skip=skip, limit=limit)

@router.get("/{lecturer_id}", response_model=LecturerResponse)
def read_lecturer(lecturer_id: str, db: Session = Depends(get_db)):
    db_lecturer = crud_lecturer.get_lecturer(db, lecturer_id=lecturer_id)
    if not db_lecturer:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy giảng viên '{lecturer_id}'")
    return db_lecturer

@router.post("/", response_model=LecturerResponse, status_code=status.HTTP_201_CREATED)
def create_lecturer(lecturer: LecturerCreate, db: Session = Depends(get_db)):
    if crud_lecturer.get_lecturer(db, lecturer_id=lecturer.lecturer_id):
        raise HTTPException(status_code=400, detail=f"Mã giảng viên '{lecturer.lecturer_id}' đã tồn tại")
    return crud_lecturer.create_lecturer(db, lecturer=lecturer)

@router.put("/{lecturer_id}", response_model=LecturerResponse)
def update_lecturer(lecturer_id: str, lecturer_update: LecturerUpdate, db: Session = Depends(get_db)):
    db_lecturer = crud_lecturer.get_lecturer(db, lecturer_id=lecturer_id)
    if not db_lecturer:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy giảng viên '{lecturer_id}'")
    return crud_lecturer.update_lecturer(db, db_lecturer=db_lecturer, lecturer_update=lecturer_update)

@router.delete("/{lecturer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lecturer(lecturer_id: str, db: Session = Depends(get_db)):
    db_lecturer = crud_lecturer.get_lecturer(db, lecturer_id=lecturer_id)
    if not db_lecturer:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy giảng viên '{lecturer_id}'")
    crud_lecturer.delete_lecturer(db, db_lecturer=db_lecturer)