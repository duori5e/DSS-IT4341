# backend/database/models.py
from sqlalchemy import Column, String
from database.connection import Base

class Course(Base):
    __tablename__ = "courses"

    course_id = Column(String, primary_key=True, index=True)
    course_name = Column(String)
    weight = Column(String)

# Cập nhật thêm vào cuối file backend/database/models.py
class Lecturer(Base):
    __tablename__ = "lecturers"

    lecturer_id = Column(String, primary_key=True, index=True)
    staff_id = Column(String)
    lecture_name = Column(String)
    email = Column(String)
    position = Column(String)
    degree = Column(String)
    seniority = Column(String)

class ClassSection(Base):
    __tablename__ = "classes"

    class_id = Column(String, primary_key=True, index=True)
    term = Column(String)
    course_id = Column(String)
    notes = Column(String)
    session_no = Column(String)
    day = Column(String)
    time = Column(String)
    period = Column(String)
    weeks = Column(String)
    room = Column(String)
    requires_lab = Column(String)
    registered_count = Column(String)
    max_capacity = Column(String)
    status = Column(String)
    class_type = Column(String)
    management_code = Column(String)

class LecturerCourse(Base):
    __tablename__ = "lecturer_courses"
    lecturer_id = Column(String, primary_key=True)
    course_id = Column(String, primary_key=True)

class ClassLecture(Base):
    __tablename__ = "class_lectures"
    class_id = Column(String, primary_key=True)
    lecturer_id = Column(String, primary_key=True)