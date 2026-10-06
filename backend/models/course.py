from sqlalchemy import Column, String
from database.connection import Base

class Course(Base):
    __tablename__ = "courses"

    course_id = Column(String, primary_key=True, index=True)
    course_name = Column(String, nullable=False)
    weight = Column(String)  # Đã đổi từ Float sang String