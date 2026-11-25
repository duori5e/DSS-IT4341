from pydantic import BaseModel
from typing import Optional

class CourseBase(BaseModel):
    course_id: str
    course_name: Optional[str] = None
    weight: Optional[float] = 0.0
    lt_bt: Optional[int] = 0
    bt: Optional[int] = 0
    tn: Optional[int] = 0

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    class Config:
        from_attributes = True

class CourseUpdate(BaseModel):
    course_name: Optional[str] = None
    weight: Optional[float] = None
    lt_bt: Optional[int] = None
    bt: Optional[int] = None
    tn: Optional[int] = None