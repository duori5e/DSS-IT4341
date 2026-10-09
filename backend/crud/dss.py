from sqlalchemy.orm import Session
from database import models

def get_dss_inputs(db: Session):
    # 1. Lấy toàn bộ lớp học và điều kiện dạy
    classes = db.query(models.ClassSection).all()
    lecturer_courses = db.query(models.LecturerCourse).all()
    
    # 2. Gom nhóm giảng viên theo môn học (tạo Dictionary để tra cứu siêu tốc)
    course_to_lecturers = {}
    for lc in lecturer_courses:
        if lc.course_id not in course_to_lecturers:
            course_to_lecturers[lc.course_id] = []
        course_to_lecturers[lc.course_id].append(lc.lecturer_id)
        
    # 3. Chuẩn bị dữ liệu đầu ra cho từng lớp
    result = []
    for c in classes:
        # Tìm danh sách giảng viên dạy được môn của lớp này
        eligible = course_to_lecturers.get(c.course_id, [])
        result.append({
            "class_id": c.class_id,
            "course_id": c.course_id,
            "day": c.day,
            "time": c.time,
            "period": c.period,
            "room": c.room,
            "eligible_lecturers": eligible
        })
        
    return result