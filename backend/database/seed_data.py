import os
import re
import sys
import pandas as pd
from sqlalchemy import inspect

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import engine

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

def parse_weight(val) -> float:
    if pd.isna(val):
        return 0.0
    match = re.match(r"^(\d+(?:\.\d+)?)", str(val).strip())
    return float(match.group(1)) if match else 0.0

def clean_lecturer_id(series: pd.Series) -> pd.Series:
    return series.astype(str).str.replace("#", "", regex=False).str.strip()

def clean_str(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip()

def seed_database():
    print("Đang kiểm tra trạng thái schema trong PostgreSQL...")
    inspector = inspect(engine)
    required_tables = {"courses", "lecturers", "classes", "lecturer_courses", "class_lectures"}
    existing_tables = set(inspector.get_table_names())

    if not required_tables.issubset(existing_tables):
        missing = required_tables - existing_tables
        raise RuntimeError(
            f"Thiếu các bảng trong database: {', '.join(missing)}. "
            "Vui lòng chạy 'alembic upgrade head' tại thư mục backend/ trước khi chạy seed_data.py!"
        )

    # 1. Nạp Courses
    print("1/5: Đang nạp bảng Courses...")
    df_course = pd.read_excel(os.path.join(DATA_DIR, "course.xlsx"))
    df_course["Course_Id"] = clean_str(df_course["Course_Id"])
    df_course.drop_duplicates(subset=["Course_Id"], inplace=True)
    df_course.rename(columns={
        "Course_Id": "course_id",
        "Course_name": "course_name",
        "Weight": "weight",
        "LT+BT": "lt_bt",
        "BT": "bt",
        "TN": "tn",
    }, inplace=True)
    df_course["weight"] = df_course["weight"].apply(parse_weight)
    for col in ["lt_bt", "bt", "tn"]:
        df_course[col] = pd.to_numeric(df_course.get(col, 0), errors="coerce").fillna(0).astype(int)

    valid_courses = df_course["course_id"].unique()
    existing_courses = pd.read_sql("SELECT course_id FROM courses", engine)["course_id"]
    new_courses = df_course[~df_course["course_id"].isin(existing_courses)]
    new_courses.to_sql("courses", con=engine, if_exists="append", index=False)

    # 2. Nạp Lecturers
    print("2/5: Đang nạp bảng Lecturers...")
    df_lec = pd.read_excel(os.path.join(DATA_DIR, "lecturer.xlsx"))
    df_lec["Lecturer_ID"] = clean_lecturer_id(df_lec["Lecturer_ID"])
    df_lec.drop_duplicates(subset=["Lecturer_ID"], inplace=True)
    df_lec.rename(columns={
        "Lecturer_ID": "lecturer_id",
        "staffID": "staff_id",
        "Lecture_name": "lecture_name",
        "Email": "email",
        "Position": "position",
        "Degree": "degree",
        "Seniority": "seniority",
    }, inplace=True)
    df_lec["seniority"] = pd.to_numeric(df_lec["seniority"], errors="coerce").fillna(0.0).astype(float)

    valid_lecturers = df_lec["lecturer_id"].unique()
    existing_lecs = pd.read_sql("SELECT lecturer_id FROM lecturers", engine)["lecturer_id"]
    new_lecs = df_lec[~df_lec["lecturer_id"].isin(existing_lecs)]
    new_lecs.to_sql("lecturers", con=engine, if_exists="append", index=False)

    # 3. Nạp Classes
    print("3/5: Đang nạp bảng Classes...")
    df_class = pd.read_excel(os.path.join(DATA_DIR, "class.xlsx"))
    df_class["Class_Id"] = clean_str(df_class["Class_Id"])
    df_class["Course_Id"] = clean_str(df_class["Course_Id"])
    df_class.drop_duplicates(subset=["Class_Id"], inplace=True)
    df_class.rename(columns={
        "Class_Id": "class_id",
        "Term": "term",
        "Course_Id": "course_id",
        "Notes": "notes",
        "Session_No": "session_no",
        "Day": "day",
        "Time": "time",
        "Period": "period",
        "Weeks": "weeks",
        "Room": "room",
        "Requires_Lab": "requires_lab",
        "Registered_Count": "registered_count",
        "Max": "max_capacity",
        "Status": "status",
        "Class_Type": "class_type",
        "Management_Code": "management_code",
    }, inplace=True)
    df_class["session_no"] = pd.to_numeric(df_class["session_no"], errors="coerce").astype("Int64")
    df_class["period"] = pd.to_numeric(df_class["period"], errors="coerce").astype("Int64")
    df_class["registered_count"] = pd.to_numeric(df_class["registered_count"], errors="coerce").fillna(0).astype(int)
    df_class["max_capacity"] = pd.to_numeric(df_class["max_capacity"], errors="coerce").fillna(0).astype(int)

    df_class = df_class[df_class["course_id"].isin(valid_courses)]
    valid_classes = df_class["class_id"].unique()
    existing_classes = pd.read_sql("SELECT class_id FROM classes", engine)["class_id"]
    new_classes = df_class[~df_class["class_id"].isin(existing_classes)]
    new_classes.to_sql("classes", con=engine, if_exists="append", index=False)

    # 4. Nạp Lecturer_Courses
    print("4/5: Đang nạp bảng Lecturer_Courses...")
    df_lc = pd.read_excel(os.path.join(DATA_DIR, "lecturer_course.xlsx"))
    df_lc["Lecturer_ID"] = clean_lecturer_id(df_lc["Lecturer_ID"])
    df_lc["Course_Id"] = clean_str(df_lc["Course_Id"])
    df_lc.drop_duplicates(subset=["Lecturer_ID", "Course_Id"], inplace=True)
    df_lc.rename(columns={
        "Lecturer_ID": "lecturer_id",
        "Course_Id": "course_id",
        "Teaching_Count": "teaching_count",
    }, inplace=True)
    df_lc["teaching_count"] = pd.to_numeric(df_lc.get("teaching_count", 0), errors="coerce").fillna(0).astype(int)
    df_lc = df_lc[df_lc["lecturer_id"].isin(valid_lecturers) & df_lc["course_id"].isin(valid_courses)]

    existing_lc = pd.read_sql("SELECT lecturer_id, course_id FROM lecturer_courses", engine)
    if not existing_lc.empty:
        df_lc = df_lc.merge(existing_lc, on=["lecturer_id", "course_id"], how="left", indicator=True)
        df_lc = df_lc[df_lc["_merge"] == "left_only"].drop(columns=["_merge"])
    df_lc.to_sql("lecturer_courses", con=engine, if_exists="append", index=False)

    # 5. Nạp Class_Lectures
    print("5/5: Đang nạp bảng Class_Lectures...")
    df_cl = pd.read_excel(os.path.join(DATA_DIR, "class_lecturer.xlsx"))
    df_cl["Class_Id"] = clean_str(df_cl["Class_Id"])
    df_cl["Lecturer_ID"] = clean_lecturer_id(df_cl["Lecturer_ID"])
    df_cl.drop_duplicates(subset=["Class_Id", "Lecturer_ID"], inplace=True)
    df_cl.rename(columns={"Class_Id": "class_id", "Lecturer_ID": "lecturer_id"}, inplace=True)
    df_cl = df_cl[df_cl["class_id"].isin(valid_classes) & df_cl["lecturer_id"].isin(valid_lecturers)]

    existing_cl = pd.read_sql("SELECT class_id, lecturer_id FROM class_lectures", engine)
    if not existing_cl.empty:
        df_cl = df_cl.merge(existing_cl, on=["class_id", "lecturer_id"], how="left", indicator=True)
        df_cl = df_cl[df_cl["_merge"] == "left_only"].drop(columns=["_merge"])
    df_cl.to_sql("class_lectures", con=engine, if_exists="append", index=False)

    print("-> Hoàn tất đồng bộ dữ liệu vào PostgreSQL!")

if __name__ == "__main__":
    seed_database()