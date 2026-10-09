from pydantic import BaseModel
from typing import Optional, Union

class ClassBase(BaseModel):
    class_id: str
    term: Optional[str] = None
    course_id: Optional[str] = None
    notes: Optional[str] = None
    session_no: Optional[Union[int, str]] = None
    day: Optional[str] = None
    time: Optional[str] = None
    period: Optional[str] = None
    weeks: Optional[str] = None
    room: Optional[str] = None
    requires_lab: Optional[str] = None
    registered_count: Optional[Union[int, float, str]] = None
    max_capacity: Optional[Union[int, float, str]] = None
    status: Optional[str] = None
    class_type: Optional[str] = None
    management_code: Optional[str] = None

class ClassResponse(ClassBase):
    class Config:
        from_attributes = True