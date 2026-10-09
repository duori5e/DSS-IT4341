# backend/schemas/course.py
from pydantic import BaseModel
from typing import Optional

class CourseBase(BaseModel):
    course_id: str
    course_name: str
    weight: Optional[str] = None

class CourseResponse(CourseBase):
    class Config:
        from_attributes = True