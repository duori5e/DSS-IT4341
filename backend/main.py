from fastapi import FastAPI
from database.connection import engine, Base

# Import chuẩn tên file và tên Class
from models.course import Course
from models.lecturer import Lecturer
from models.class_model import ClassModel
from models.lecturer_course import LecturerCourse
from models.assignment import ClassLecture

# Bắn lệnh tạo bảng vào PostgreSQL
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SoICT Scheduler API")

@app.get("/")
def read_root():
    return {"message": "Database DSS đã kết nối và tạo bảng thành công!"}