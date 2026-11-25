from pydantic import BaseModel
from typing import Optional

class ClassBase(BaseModel):
    class_id: str
    term: Optional[str] = None
    course_id: Optional[str] = None
    notes: Optional[str] = None
    session_no: Optional[int] = None
    day: Optional[str] = None
    time: Optional[str] = None
    period: Optional[int] = None
    weeks: Optional[str] = None
    room: Optional[str] = None
    requires_lab: Optional[str] = None
    registered_count: Optional[int] = 0
    max_capacity: Optional[int] = 0
    status: Optional[str] = None
    class_type: Optional[str] = None
    management_code: Optional[str] = None

class ClassCreate(ClassBase):
    pass

class ClassResponse(ClassBase):
    class Config:
        from_attributes = True

class ClassUpdate(BaseModel):
    term: Optional[str] = None
    course_id: Optional[str] = None
    notes: Optional[str] = None
    session_no: Optional[int] = None
    day: Optional[str] = None
    time: Optional[str] = None
    period: Optional[str] = None
    weeks: Optional[str] = None
    room: Optional[str] = None
    requires_lab: Optional[str] = None
    registered_count: Optional[int] = None
    max_capacity: Optional[int] = None
    status: Optional[str] = None
    class_type: Optional[str] = None
    management_code: Optional[str] = None