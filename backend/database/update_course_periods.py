import os
import shutil
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
COURSE_PATH = os.path.join(DATA_DIR, "course.xlsx")
BACKUP_PATH = os.path.join(DATA_DIR, "course.bak.xlsx")

def calc_periods(time_str) -> int:
    if pd.isna(time_str) or "-" not in str(time_str):
        return 0
    start, end = str(time_str).strip().split("-", 1)
    if len(start) != 4 or len(end) != 4:
        return 0
    try:
        h1, m1 = int(start[:2]), int(start[2:])
        h2, m2 = int(end[:2]), int(end[2:])
        duration = (h2 * 60 + m2) - (h1 * 60 + m1)
        return max(0, round(duration / 50))
    except ValueError:
        return 0

def main():
    shutil.copy2(COURSE_PATH, BACKUP_PATH)

    df_class = pd.read_excel(os.path.join(DATA_DIR, "class.xlsx"))
    df_course = pd.read_excel(COURSE_PATH)

    df_class["Course_Id"] = df_class["Course_Id"].astype(str).str.strip()
    df_class["Class_Type"] = df_class["Class_Type"].astype(str).str.strip()
    df_course["Course_Id"] = df_course["Course_Id"].astype(str).str.strip()

    df_class["Periods"] = df_class["Time"].apply(calc_periods)
    course_periods = (
        df_class.groupby(["Course_Id", "Class_Type"])["Periods"]
        .max()
        .unstack(fill_value=0)
    )

    target_cols = ["LT+BT", "BT", "TN"]
    for col in target_cols:
        if col not in course_periods.columns:
            course_periods[col] = 0

    # Xóa các cột cũ nếu đã tồn tại để tránh tạo cột _x, _y khi merge lại
    df_course = df_course.drop(columns=target_cols, errors="ignore")
    df_course = df_course.merge(
        course_periods[target_cols],
        left_on="Course_Id",
        right_index=True,
        how="left",
    )

    for col in target_cols:
        df_course[col] = df_course[col].fillna(0).astype(int)

    df_course.to_excel(COURSE_PATH, index=False)
    print(f"Đã cập nhật LT+BT, BT, TN thành công (File gốc sao lưu tại: {BACKUP_PATH}).")

if __name__ == "__main__":
    main()