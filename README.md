# SoICT Scheduler API (Backend)

Hệ thống quản lý và hỗ trợ xếp lịch học cho Viện CNTT&TT (SoICT). Dự án sử dụng FastAPI để xây dựng API và PostgreSQL làm cơ sở dữ liệu, tích hợp công cụ tự động làm sạch và nạp dữ liệu trực tiếp từ file Excel.

## Yêu cầu hệ thống
* [Miniconda](https://docs.conda.io/en/latest/miniconda.html) hoặc Python 3.11+
* PostgreSQL & pgAdmin (phiên bản mới nhất)

## Hướng dẫn cài đặt và khởi chạy

### 1. Thiết lập môi trường và thư viện
Mở Command Prompt/Terminal và chạy lần lượt các lệnh sau:

```cmd
# Clone dự án về máy (nhớ thay link bằng repo thực tế của bạn)
git clone https://github.com/duori5e/DSS-IT4341
cd DSS-SoICT

# Tạo và kích hoạt môi trường ảo (nếu dùng Conda)
conda create -n course python=3.11
conda activate course

# Cài đặt các thư viện bắt buộc 
pip install fastapi uvicorn sqlalchemy psycopg psycopg-binary pandas openpyxl python-dotenv
```

### 2. Cấu hình Cơ sở dữ liệu
1. Mở **pgAdmin**, tạo một database trống mới và đặt tên là `DSS`.
2. Truy cập vào thư mục `backend`, tìm file `.env.example` và copy/đổi tên nó thành `.env`.
3. Mở file `.env` vừa tạo và cập nhật chuỗi kết nối với tài khoản PostgreSQL trên máy của bạn:
   ```env
   # Thay TEN_DANG_NHAP và MAT_KHAU cho phù hợp với máy của bạn
   DATABASE_URL=postgresql+psycopg://TEN_DANG_NHAP:MAT_KHAU@localhost:5432/DSS
   ```

### 3. Khởi tạo cấu trúc bảng (Migration)
Di chuyển vào thư mục `backend` và khởi chạy server lần đầu tiên. Code sẽ tự động kết nối và tạo toàn bộ 5 bảng cần thiết trong cơ sở dữ liệu:

```cmd
cd backend
uvicorn main:app --reload
```
Khi Terminal hiện dòng chữ `Application startup complete.`, hãy nhấn `Ctrl + C` để tắt server.

### 4. Nạp dữ liệu tự động (Seed Data)
Để đẩy dữ liệu từ các file Excel mẫu vào database, hãy chạy script sau:

```cmd
cd database
python seed_data.py
```
Nếu Terminal thông báo `-> Thành công! Toàn bộ dữ liệu đã nằm trong PostgreSQL.`, bạn đã hoàn tất việc thiết lập cơ sở dữ liệu và có thể bắt đầu phát triển các API tiếp theo.