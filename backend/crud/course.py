from sqlalchemy.orm import Session
from database import models
from schemas.course import CourseCreate, CourseUpdate

def get_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Course).offset(skip).limit(limit).all()

def get_course(db: Session, course_id: str):
    return db.query(models.Course).filter(models.Course.course_id == course_id).first()

def create_course(db: Session, course: CourseCreate):
    db_course = models.Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def update_course(db: Session, db_course: models.Course, course_update: CourseUpdate):
    update_data = course_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_course, key, value)
    db.commit()
    db.refresh(db_course)
    return db_course

def delete_course(db: Session, db_course: models.Course):
    db.delete(db_course)
    db.commit()