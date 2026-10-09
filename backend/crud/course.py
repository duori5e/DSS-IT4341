# backend/crud/course.py
from sqlalchemy.orm import Session
from database import models

def get_all_courses(db: Session):
    return db.query(models.Course).all()