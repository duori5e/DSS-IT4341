from sqlalchemy.orm import Session
from database import models

def get_all_classes(db: Session):
    return db.query(models.ClassSection).all()