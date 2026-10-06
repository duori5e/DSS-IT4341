from sqlalchemy import Column, String
from database.connection import Base

class Lecturer(Base):
    __tablename__ = "lecturers"

    lecturer_id = Column(String, primary_key=True, index=True)
    staff_id = Column(String, unique=True, index=True)
    lecture_name = Column(String, nullable=False)
    email = Column(String)
    position = Column(String)
    degree = Column(String)
    seniority = Column(String)