from sqlalchemy import Column, String, ForeignKey
from database.connection import Base

class LecturerCourse(Base):
    __tablename__ = "lecturer_courses"

    lecturer_id = Column(String, ForeignKey("lecturers.lecturer_id"), primary_key=True)
    course_id = Column(String, ForeignKey("courses.course_id"), primary_key=True)