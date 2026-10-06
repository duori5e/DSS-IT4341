from sqlalchemy import Column, String, Integer, ForeignKey
from database.connection import Base

class ClassModel(Base):
    __tablename__ = "classes"

    class_id = Column(String, primary_key=True, index=True)
    term = Column(String)
    course_id = Column(String, ForeignKey("courses.course_id"))
    notes = Column(String)
    session_no = Column(String)
    day = Column(String)
    time = Column(String)
    period = Column(String)
    weeks = Column(String)
    room = Column(String)
    requires_lab = Column(String)
    registered_count = Column(Integer)
    max_capacity = Column(Integer) 
    status = Column(String)
    class_type = Column(String)
    management_code = Column(String)