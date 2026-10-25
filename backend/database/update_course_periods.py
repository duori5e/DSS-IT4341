import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

# 1. Đọc dữ liệu từ file class.xlsx và course.xlsx
df_class = pd.read_excel(f"{DATA_DIR}/class.xlsx")
df_course = pd.read_excel(f"{DATA_DIR}/course.xlsx")

# 2. Xóa khoảng trắng thừa để tránh lỗi không khớp ID
df_class['Course_Id'] = df_class['Course_Id'].astype(str).str.strip()
df_course['Course_Id'] = df_course['Course_Id'].astype(str).str.strip()
df_class['Class_Type'] = df_class['Class_Type'].astype(str).str.strip()

# 3. Hàm tính số tiết từ chuỗi thời gian (VD: "0645-0910")
def calc_periods(time_str):
    if pd.isna(time_str) or '-' not in str(time_str):
        return 0
    start, end = str(time_str).split('-')
    if len(start) != 4 or len(end) != 4: 
        return 0
    
    try:
        # Tách giờ và phút
        h1, m1 = int(start[:2]), int(start[2:])
        h2, m2 = int(end[:2]), int(end[2:])
        
        # Tính tổng thời gian bằng phút
        duration = (h2 * 60 + m2) - (h1 * 60 + m1)
        
        # 1 tiết khoảng 45p + 5p nghỉ = 50p/chu kỳ. Chia lấy tròn.
        return round(duration / 50)
    except:
        return 0

# 4. Áp dụng hàm tính số tiết cho bảng class
df_class['Periods'] = df_class['Time'].apply(calc_periods)

# 5. Gom nhóm theo Môn học và Loại lớp (Lấy số tiết đại diện lớn nhất trong trường hợp có nhiều lớp trùng)
course_periods = df_class.groupby(['Course_Id', 'Class_Type'])['Periods'].max().unstack(fill_value=0)

# 6. Gộp dữ liệu vào bảng course gốc
# Đảm bảo có đủ 3 cột LT+BT, BT, TN, nếu chưa có thì gán mảng 0
for col in ['LT+BT', 'BT', 'TN']:
    if col not in course_periods.columns:
        course_periods[col] = 0

# Cập nhật hoặc ghi đè dữ liệu mới vào bảng course
df_course = df_course.merge(course_periods[['LT+BT', 'BT', 'TN']], left_on='Course_Id', right_index=True, how='left')

# Điền 0 cho những môn không có lịch trong bảng class và ép về kiểu số nguyên
for col in ['LT+BT', 'BT', 'TN']:
    df_course[col] = df_course[col].fillna(0).astype(int)

# 7. Lưu đè lại file course.xlsx
df_course.to_excel(f"{DATA_DIR}/course.xlsx", index=False)
print("Đã cập nhật thành công 3 cột LT+BT, BT, và TN vào bảng course!")