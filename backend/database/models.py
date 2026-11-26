from sqlalchemy import Column, String, Integer, Float, ForeignKey
from database.connection import Base

class Course(Base):
    __tablename__ = "courses"

    course_id = Column(String, primary_key=True, index=True)
    course_name = Column(String)
    weight = Column(Float, default=0.0)
    lt_bt = Column(Integer, default=0)
    bt = Column(Integer, default=0)
    tn = Column(Integer, default=0)


class Lecturer(Base):
    __tablename__ = "lecturers"

    lecturer_id = Column(String, primary_key=True, index=True)
    staff_id = Column(String)
    lecture_name = Column(String)
    email = Column(String)
    position = Column(String)
    degree = Column(String)
    seniority = Column(Float, default=0.0)


class ClassSection(Base):
    __tablename__ = "classes"

    class_id = Column(String, primary_key=True, index=True)
    term = Column(String, index=True)
    course_id = Column(String, ForeignKey("courses.course_id", ondelete="CASCADE"), index=True)
    notes = Column(String)
    session_no = Column(Integer)
    day = Column(String)
    time = Column(String)
    period = Column(Integer, nullable=True)
    weeks = Column(String)
    room = Column(String)
    requires_lab = Column(String)
    registered_count = Column(Integer, default=0)
    max_capacity = Column(Integer, default=0)
    status = Column(String)
    class_type = Column(String)
    management_code = Column(String)


class LecturerCourse(Base):
    __tablename__ = "lecturer_courses"

    lecturer_id = Column(String, ForeignKey("lecturers.lecturer_id", ondelete="CASCADE"), primary_key=True)
    course_id = Column(String, ForeignKey("courses.course_id", ondelete="CASCADE"), primary_key=True)
    teaching_count = Column(Integer, default=0)


class ClassLecture(Base):
    __tablename__ = "class_lectures"

    class_id = Column(String, ForeignKey("classes.class_id", ondelete="CASCADE"), primary_key=True)
    lecturer_id = Column(String, ForeignKey("lecturers.lecturer_id", ondelete="CASCADE"), primary_key=True)