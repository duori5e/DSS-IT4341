# backend/schemas/course.py
from pydantic import BaseModel
from typing import Optional

class CourseBase(BaseModel):
    course_id: str
    course_name: str
    weight: Optional[str] = None
    lt_bt: Optional[int] = 0
    bt: Optional[int] = 0
    tn: Optional[int] = 0

class CourseResponse(CourseBase):
    class Config:
        from_attributes = True