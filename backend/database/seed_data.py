import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import engine, Base
from database import models

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

def seed_database():
    print("Đang khởi tạo cấu trúc Database...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    print("Bắt đầu nạp dữ liệu từ Excel vào PostgreSQL...")

    # 1. Nạp Courses
    print("1/5: Đang nạp bảng Courses...")
    df_course = pd.read_excel(f"{DATA_DIR}/course.xlsx")
    # Làm sạch ID
    df_course['Course_Id'] = df_course['Course_Id'].astype(str).str.strip()
    df_course.drop_duplicates(subset=["Course_Id"], inplace=True)
    df_course.rename(columns={
        "Course_Id": "course_id", "Course_name": "course_name", "Weight": "weight",
        "LT+BT": "lt_bt", "BT": "bt", "TN": "tn"
    }, inplace=True)
    df_course.to_sql("courses", con=engine, if_exists="append", index=False)
    valid_courses = df_course['course_id'].unique()

    # 2. Nạp Lecturers
    print("2/5: Đang nạp bảng Lecturers...")
    df_lec = pd.read_excel(f"{DATA_DIR}/lecturer.xlsx")
    # Làm sạch ID (xóa # và khoảng trắng)
    df_lec['Lecturer_ID'] = df_lec['Lecturer_ID'].astype(str).str.replace('#', '', regex=False).str.strip()
    df_lec.drop_duplicates(subset=["Lecturer_ID"], inplace=True)
    df_lec.rename(columns={
        "Lecturer_ID": "lecturer_id", "staffID": "staff_id", "Lecture_name": "lecture_name",
        "Email": "email", "Position": "position", "Degree": "degree", "Seniority": "seniority"
    }, inplace=True)
    df_lec.to_sql("lecturers", con=engine, if_exists="append", index=False)
    valid_lecturers = df_lec['lecturer_id'].unique()

    # 3. Nạp Classes
    print("3/5: Đang nạp bảng Classes...")
    df_class = pd.read_excel(f"{DATA_DIR}/class.xlsx")
    # Làm sạch ID
    df_class['Class_Id'] = df_class['Class_Id'].astype(str).str.strip()
    df_class['Course_Id'] = df_class['Course_Id'].astype(str).str.strip()
    df_class.drop_duplicates(subset=["Class_Id"], inplace=True)
    df_class.rename(columns={
        "Class_Id": "class_id", "Term": "term", "Course_Id": "course_id",
        "Notes": "notes", "Session_No": "session_no", "Day": "day",
        "Time": "time", "Period": "period", "Weeks": "weeks",
        "Room": "room", "Requires_Lab": "requires_lab",
        "Registered_Count": "registered_count", "Max": "max_capacity",
        "Status": "status", "Class_Type": "class_type", "Management_Code": "management_code"
    }, inplace=True)
    df_class = df_class[df_class['course_id'].isin(valid_courses)]
    df_class.to_sql("classes", con=engine, if_exists="append", index=False)
    valid_classes = df_class['class_id'].unique()

    # 4. Nạp Lecturer_Course
    print("4/5: Đang nạp bảng Lecturer_Courses...")
    df_lc = pd.read_excel(f"{DATA_DIR}/lecturer_course.xlsx")
    # Làm sạch ID
    df_lc['Lecturer_ID'] = df_lc['Lecturer_ID'].astype(str).str.replace('#', '', regex=False).str.strip()
    df_lc['Course_Id'] = df_lc['Course_Id'].astype(str).str.strip()
    df_lc.drop_duplicates(inplace=True)
    df_lc.rename(columns={
        "Lecturer_ID": "lecturer_id", 
        "Course_Id": "course_id", 
        "Teaching_Count": "teaching_count"
    }, inplace=True)
    df_lc = df_lc[df_lc['lecturer_id'].isin(valid_lecturers) & df_lc['course_id'].isin(valid_courses)]
    df_lc.to_sql("lecturer_courses", con=engine, if_exists="append", index=False)

    # 5. Nạp Class_Lectures
    print("5/5: Đang nạp bảng Class_Lectures...")
    df_cl = pd.read_excel(f"{DATA_DIR}/class_lecturer.xlsx")
    # Làm sạch ID
    df_cl['Class_Id'] = df_cl['Class_Id'].astype(str).str.strip()
    df_cl['Lecturer_ID'] = df_cl['Lecturer_ID'].astype(str).str.replace('#', '', regex=False).str.strip()
    df_cl.drop_duplicates(inplace=True)
    df_cl.rename(columns={"Class_Id": "class_id", "Lecturer_ID": "lecturer_id"}, inplace=True)
    df_cl = df_cl[df_cl['class_id'].isin(valid_classes) & df_cl['lecturer_id'].isin(valid_lecturers)]
    df_cl.to_sql("class_lectures", con=engine, if_exists="append", index=False)

    print("-> Thành công! Toàn bộ dữ liệu mới đã được cập nhật vào PostgreSQL.")

if __name__ == "__main__":
    seed_database()