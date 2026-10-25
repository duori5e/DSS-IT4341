from pydantic import BaseModel
from typing import List, Optional

# Thêm class này để định nghĩa chi tiết giảng viên
class EligibleLecturer(BaseModel):
    lecturer_id: str
    teaching_count: int

class ClassInputDSS(BaseModel):
    class_id: str
    course_id: Optional[str] = None
    day: Optional[str] = None
    time: Optional[str] = None
    period: Optional[str] = None
    room: Optional[str] = None
    # Đổi kiểu dữ liệu ở đây
    eligible_lecturers: List[EligibleLecturer] = []

class ScenarioInputResponse(BaseModel):
    scenario_name: str
    total_classes: int
    data: List[ClassInputDSS]