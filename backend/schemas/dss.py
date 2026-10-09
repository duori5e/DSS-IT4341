from pydantic import BaseModel
from typing import List, Optional

class ClassInputDSS(BaseModel):
    class_id: str
    course_id: Optional[str] = None
    day: Optional[str] = None
    time: Optional[str] = None
    period: Optional[str] = None
    room: Optional[str] = None
    # Danh sách các mã giảng viên ĐỦ ĐIỀU KIỆN dạy lớp này
    eligible_lecturers: List[str] = []

class ScenarioInputResponse(BaseModel):
    scenario_name: str
    total_classes: int
    data: List[ClassInputDSS]