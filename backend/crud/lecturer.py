# backend/crud/lecturer.py
from sqlalchemy.orm import Session
from database import models

def get_all_lecturers(db: Session):
    return db.query(models.Lecturer).all()