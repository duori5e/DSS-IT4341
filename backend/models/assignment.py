from sqlalchemy import Column, String, ForeignKey
from database.connection import Base

class ClassLecture(Base):
    __tablename__ = "class_lectures"

    class_id = Column(String, ForeignKey("classes.class_id"), primary_key=True)
    lecturer_id = Column(String, ForeignKey("lecturers.lecturer_id"), primary_key=True)