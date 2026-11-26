import os
import shutil
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
LC_PATH = os.path.join(DATA_DIR, "lecturer_course.xlsx")
BACKUP_PATH = os.path.join(DATA_DIR, "lecturer_course.bak.xlsx")

def normalize_lecturer_id(series: pd.Series) -> pd.Series:
    return series.astype(str).str.replace("#", "", regex=False).str.strip()

def normalize_code(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip()

def main():
    # Tạo bản sao lưu trước khi chỉnh sửa
    shutil.copy2(LC_PATH, BACKUP_PATH)

    df_class = pd.read_excel(os.path.join(DATA_DIR, "class.xlsx"))
    df_cl = pd.read_excel(os.path.join(DATA_DIR, "class_lecturer.xlsx"))
    df_lc = pd.read_excel(LC_PATH)

    # Chuẩn hóa đồng nhất ở tất cả các bảng
    df_class["Class_Id"] = normalize_code(df_class["Class_Id"])
    df_class["Course_Id"] = normalize_code(df_class["Course_Id"])
    df_class["Term"] = normalize_code(df_class["Term"])

    df_cl["Class_Id"] = normalize_code(df_cl["Class_Id"])
    df_cl["Lecturer_ID"] = normalize_lecturer_id(df_cl["Lecturer_ID"])

    df_lc["Course_Id"] = normalize_code(df_lc["Course_Id"])
    df_lc["Lecturer_ID"] = normalize_lecturer_id(df_lc["Lecturer_ID"])

    # Ghép dữ liệu và đếm số kỳ không trùng lặp
    df_merged = pd.merge(
        df_cl,
        df_class[["Class_Id", "Course_Id", "Term"]],
        on="Class_Id",
        how="inner",
    )
    df_count = (
        df_merged.groupby(["Lecturer_ID", "Course_Id"])["Term"]
        .nunique()
        .reset_index(name="Teaching_Count_New")
    )

    df_lc = df_lc.drop(columns=["Teaching_Count"], errors="ignore")
    df_final = pd.merge(df_lc, df_count, on=["Lecturer_ID", "Course_Id"], how="left")
    df_final["Teaching_Count"] = df_final["Teaching_Count_New"].fillna(0).astype(int)
    df_final = df_final.drop(columns=["Teaching_Count_New"])

    df_final.to_excel(LC_PATH, index=False)
    print(f"Đã cập nhật Teaching_Count thành công (File gốc sao lưu tại: {BACKUP_PATH}).")

if __name__ == "__main__":
    main()