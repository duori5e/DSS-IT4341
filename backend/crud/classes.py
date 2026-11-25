from typing import Optional
from sqlalchemy.orm import Session
from database import models
from schemas.classes import ClassCreate, ClassUpdate

def get_classes(
    db: Session,
    term: Optional[str] = None,
    course_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
):
    query = db.query(models.ClassSection)
    if term:
        query = query.filter(models.ClassSection.term == term)
    if course_id:
        query = query.filter(models.ClassSection.course_id == course_id)
    return query.offset(skip).limit(limit).all()

def get_class(db: Session, class_id: str):
    return db.query(models.ClassSection).filter(models.ClassSection.class_id == class_id).first()

def create_class(db: Session, class_in: ClassCreate):
    db_class = models.ClassSection(**class_in.model_dump())
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class

def update_class(db: Session, db_class: models.ClassSection, class_update: ClassUpdate):
    update_data = class_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_class, key, value)
    db.commit()
    db.refresh(db_class)
    return db_class

def delete_class(db: Session, db_class: models.ClassSection):
    db.delete(db_class)
    db.commit()