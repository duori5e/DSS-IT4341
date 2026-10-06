import pandas as pd
import os
from connection import engine

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

def seed_database():
    print("Bắt đầu nạp dữ liệu từ Excel vào PostgreSQL...")

    # 1. Nạp Courses
    print("1/5: Đang nạp bảng Courses...")
    df_course = pd.read_excel(f"{DATA_DIR}/course.xlsx")
    df_course.drop_duplicates(subset=["Course_Id"], inplace=True)
    df_course.rename(columns={
        "Course_Id": "course_id", "Course_name": "course_name", "Weight": "weight"
    }, inplace=True)
    df_course.to_sql("courses", con=engine, if_exists="append", index=False)
    valid_courses = df_course['course_id'].unique() # Lưu lại danh sách ID hợp lệ

    # 2. Nạp Lecturers
    print("2/5: Đang nạp bảng Lecturers...")
    df_lec = pd.read_excel(f"{DATA_DIR}/lecturer.xlsx")
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
    df_class.drop_duplicates(subset=["Class_Id"], inplace=True)
    df_class.rename(columns={
        "Class_Id": "class_id", "Term": "term", "Course_Id": "course_id",
        "Notes": "notes", "Session_No": "session_no", "Day": "day",
        "Time": "time", "Period": "period", "Weeks": "weeks",
        "Room": "room", "Requires_Lab": "requires_lab",
        "Registered_Count": "registered_count", "Max": "max_capacity",
        "Status": "status", "Class_Type": "class_type", "Management_Code": "management_code"
    }, inplace=True)
    # Lọc bỏ các lớp có mã môn học không tồn tại
    df_class = df_class[df_class['course_id'].isin(valid_courses)]
    df_class.to_sql("classes", con=engine, if_exists="append", index=False)
    valid_classes = df_class['class_id'].unique()

    # 4. Nạp Lecturer_Course
    print("4/5: Đang nạp bảng Lecturer_Courses...")
    df_lc = pd.read_excel(f"{DATA_DIR}/lecturer_course.xlsx")
    df_lc.drop_duplicates(inplace=True)
    df_lc.rename(columns={"Lecturer_ID": "lecturer_id", "Course_Id": "course_id"}, inplace=True)
    # Chỉ giữ lại các dòng mà cả Giảng viên và Môn học đều hợp lệ
    df_lc = df_lc[df_lc['lecturer_id'].isin(valid_lecturers) & df_lc['course_id'].isin(valid_courses)]
    df_lc.to_sql("lecturer_courses", con=engine, if_exists="append", index=False)

    # 5. Nạp Class_Lectures
    print("5/5: Đang nạp bảng Class_Lectures...")
    df_cl = pd.read_excel(f"{DATA_DIR}/class_lecturer.xlsx")
    df_cl.drop_duplicates(inplace=True)
    df_cl.rename(columns={"Class_Id": "class_id", "Lecturer_ID": "lecturer_id"}, inplace=True)
    # Chỉ giữ lại các dòng mà cả Lớp và Giảng viên đều hợp lệ
    df_cl = df_cl[df_cl['class_id'].isin(valid_classes) & df_cl['lecturer_id'].isin(valid_lecturers)]
    df_cl.to_sql("class_lectures", con=engine, if_exists="append", index=False)

    print("-> Thành công! Toàn bộ dữ liệu đã nằm trong PostgreSQL.")

if __name__ == "__main__":
    seed_database()