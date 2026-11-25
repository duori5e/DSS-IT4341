from sqlalchemy.orm import Session
from database import models
from schemas.lecturer import LecturerCreate, LecturerUpdate

def get_lecturers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Lecturer).offset(skip).limit(limit).all()

def get_lecturer(db: Session, lecturer_id: str):
    return db.query(models.Lecturer).filter(models.Lecturer.lecturer_id == lecturer_id).first()

def create_lecturer(db: Session, lecturer: LecturerCreate):
    db_lecturer = models.Lecturer(**lecturer.model_dump())
    db.add(db_lecturer)
    db.commit()
    db.refresh(db_lecturer)
    return db_lecturer

def update_lecturer(db: Session, db_lecturer: models.Lecturer, lecturer_update: LecturerUpdate):
    update_data = lecturer_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_lecturer, key, value)
    db.commit()
    db.refresh(db_lecturer)
    return db_lecturer

def delete_lecturer(db: Session, db_lecturer: models.Lecturer):
    db.delete(db_lecturer)
    db.commit()