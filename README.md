# SoICT Scheduler API (Backend)

Hệ thống quản lý và hỗ trợ xếp lịch học cho Viện CNTT&TT (SoICT). Dự án sử dụng FastAPI để xây dựng API và PostgreSQL làm cơ sở dữ liệu, tích hợp công cụ tự động làm sạch và nạp dữ liệu trực tiếp từ file Excel.

## Yêu cầu hệ thống

* [Miniconda](https://docs.conda.io/en/latest/miniconda.html) hoặc Python 3.11+
* PostgreSQL và pgAdmin (phiên bản mới nhất)

## Hướng dẫn cài đặt và khởi chạy

### 1. Thiết lập môi trường và thư viện

Mở Command Prompt/Terminal và chạy lần lượt các lệnh sau:

```cmd
# Clone dự án về máy
git clone https://github.com/Tên_Của_Bạn/DSS-SoICT.git
cd DSS-SoICT

# Tạo và kích hoạt môi trường ảo (nếu dùng Conda)
conda create -n course python=3.11
conda activate course

# Cài đặt các thư viện bắt buộc
pip install fastapi uvicorn sqlalchemy psycopg psycopg-binary pandas openpyxl
```

### 2. Cấu hình cơ sở dữ liệu

Mở pgAdmin, tạo một database trống mới và đặt tên là `DSS`.

Trong dự án, mở file `backend/database/connection.py`. Thay thế chuỗi kết nối mặc định bằng thông tin tài khoản PostgreSQL trên máy của bạn:

```python
# Thay 'postgres' và 'MAT_KHAU_CUA_BAN' cho phù hợp
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg://postgres:MAT_KHAU_CUA_BAN@localhost:5432/DSS"
```

### 3. Khởi tạo cấu trúc bảng (Migration)

Di chuyển vào thư mục `backend` và khởi chạy server lần đầu tiên. Code sẽ tự động kết nối và tạo toàn bộ 5 bảng cần thiết trong cơ sở dữ liệu:

```dos
cd backend
uvicorn main:app --reload
```

Khi Terminal hiện dòng chữ `Application startup complete.`, hãy nhấn `Ctrl + C` để tắt server.

### 4. Nạp dữ liệu tự động (Seed Data)

Để đẩy dữ liệu từ các file Excel mẫu vào database (có bao gồm tự động xử lý trùng lặp và loại bỏ dữ liệu mồ côi), hãy chạy script sau:

```dos
cd database
python seed_data.py
```

Nếu Terminal thông báo `-> Thành công! Toàn bộ dữ liệu đã nằm trong PostgreSQL.`, bạn đã hoàn tất việc thiết lập cơ sở dữ liệu và có thể bắt đầu phát triển các API tiếp theo.

---

**Lưu ý:** Ở dòng lệnh clone dự án (`git clone ...`), hãy thay `Tên_Của_Bạn` bằng tên người dùng GitHub thực tế của bạn hoặc cập nhật URL thành địa chỉ repository.