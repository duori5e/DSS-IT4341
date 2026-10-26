import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

# 1. Đọc dữ liệu từ các file
df_class = pd.read_excel(f"{DATA_DIR}/class.xlsx")
df_cl = pd.read_excel(f"{DATA_DIR}/class_lecturer.xlsx")
df_lc = pd.read_excel(f"{DATA_DIR}/lecturer_course.xlsx")

# 2. Xử lý dữ liệu và làm sạch khoảng trắng
df_class['Class_Id'] = df_class['Class_Id'].astype(str).str.strip()
df_class['Course_Id'] = df_class['Course_Id'].astype(str).str.strip()
df_class['Term'] = df_class['Term'].astype(str).str.strip() # Lấy thêm cột Term

df_cl['Class_Id'] = df_cl['Class_Id'].astype(str).str.strip()
df_cl['Lecturer_ID'] = df_cl['Lecturer_ID'].astype(str).str.replace('#', '', regex=False).str.strip()

df_lc['Course_Id'] = df_lc['Course_Id'].astype(str).str.strip()
df_lc['Lecturer_ID'] = df_lc['Lecturer_ID'].astype(str).str.strip()

# 3. Nối dữ liệu để lấy cột Term cho từng lớp
df_merged = pd.merge(df_cl, df_class[['Class_Id', 'Course_Id', 'Term']], on='Class_Id', how='inner')

# 4. Đếm số Kỳ học (Term) không trùng lặp cho mỗi cặp Giảng viên - Môn học
df_count = df_merged.groupby(['Lecturer_ID', 'Course_Id'])['Term'].nunique().reset_index(name='Teaching_Count_New')

# 5. Cập nhật vào bảng gốc
if 'Teaching_Count' in df_lc.columns:
    df_lc = df_lc.drop(columns=['Teaching_Count'])
    
df_final = pd.merge(df_lc, df_count, on=['Lecturer_ID', 'Course_Id'], how='left')
df_final['Teaching_Count'] = df_final['Teaching_Count_New'].fillna(0).astype(int)
df_final = df_final.drop(columns=['Teaching_Count_New'])

# 6. Lưu lại file Excel
df_final.to_excel(f"{DATA_DIR}/lecturer_course.xlsx", index=False)
print("Đã đếm thành công: Mỗi kỳ chỉ tính 1 lần!")