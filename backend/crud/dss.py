from sqlalchemy.orm import Session
from database import models

def get_dss_inputs(db: Session):
    classes = db.query(models.ClassSection).all()
    lecturer_courses = db.query(models.LecturerCourse).all()
    
    course_to_lecturers = {}
    for lc in lecturer_courses:
        if lc.course_id not in course_to_lecturers:
            course_to_lecturers[lc.course_id] = []
        # Lưu cả ID và số lần dạy thay vì chỉ lưu ID
        course_to_lecturers[lc.course_id].append({
            "lecturer_id": lc.lecturer_id,
            "teaching_count": lc.teaching_count
        })
        
    result = []
    for c in classes:
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