# backend/schemas/lecturer.py
from pydantic import BaseModel
from typing import Optional

class LecturerBase(BaseModel):
    lecturer_id: str
    staff_id: Optional[str] = None
    lecture_name: Optional[str] = None
    email: Optional[str] = None
    position: Optional[str] = None
    degree: Optional[str] = None
    seniority: Optional[str] = None

class LecturerResponse(LecturerBase):
    class Config:
        from_attributes = True