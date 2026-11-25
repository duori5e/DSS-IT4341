# DSS-IT4341 — Hệ thống Hỗ trợ Ra quyết định Phân công Giảng dạy (SoICT Scheduler)

Hệ thống quản lý dữ liệu đào tạo và hỗ trợ xếp lịch giảng dạy cho Viện CNTT&TT (SoICT). Phần Backend sử dụng **FastAPI**, **SQLAlchemy** và **PostgreSQL**, tích hợp công cụ tự động chuẩn hóa và nạp dữ liệu từ Excel.

## Yêu cầu hệ thống
- **Python 3.11+** (khuyến nghị dùng `venv` hoặc [Miniconda](https://docs.conda.io/en/latest/miniconda.html))
- **PostgreSQL** & **pgAdmin**

## Cấu trúc thư mục chính
```text
DSS-IT4341/
├── .env.example          # File mẫu cấu hình biến môi trường
├── requirements.txt      # Danh sách thư viện Python cần thiết
├── README.md
└── backend/
    ├── main.py           # Điểm khởi chạy FastAPI & cấu hình CORS
    ├── data/             # Dữ liệu đầu vào dạng Excel (.xlsx)
    ├── database/         # Kết nối DB, định nghĩa Models & script seed_data.py
    ├── schemas/          # Pydantic schemas kiểm duyệt dữ liệu API
    ├── crud/             # Xử lý truy vấn cơ sở dữ liệu
    ├── routers/          # Định nghĩa các endpoints REST API
    └── dss/              # Module thuật toán tối ưu phân công
```

---

## Hướng dẫn cài đặt & chạy Backend

### 1. Clone dự án và di chuyển vào thư mục gốc
```bash
git clone https://github.com/duori5e/DSS-IT4341.git
cd DSS-IT4341
```

### 2. Tạo môi trường ảo và cài đặt thư viện
Chọn một trong hai cách dưới đây để thiết lập môi trường Python:

* **Cách 1: Dùng Python `venv` (Khuyến nghị)**
  ```bash
  python -m venv venv
  # Windows:
  venv\Scripts\activate
  # macOS / Linux:
  source venv/bin/activate

  pip install -r requirements.txt
  ```

* **Cách 2: Dùng Conda / Miniconda**
  ```bash
  conda create -n course python=3.11
  conda activate course
  pip install -r requirements.txt
  ```

### 3. Cấu hình Cơ sở dữ liệu & Biến môi trường
1. Mở **pgAdmin**, tạo một database trống mới và đặt tên là **`DSS`**.
2. Ngay tại thư mục gốc **`DSS-IT4341/`**, copy file `.env.example` thành file `.env`:
   ```bash
   # Windows (Command Prompt):
   copy .env.example .env
   # macOS / Linux / Git Bash:
   cp .env.example .env
   ```
3. Mở file `.env` vừa tạo và cập nhật chuỗi kết nối PostgreSQL theo tài khoản trên máy:
   ```env
   DATABASE_URL=postgresql+psycopg://TEN_DANG_NHAP:MAT_KHAU@localhost:5432/DSS
   CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
   ```

### 4. Khởi tạo Schema (Migration) và Nạp dữ liệu (Seed Data)
Di chuyển vào thư mục `backend`:
```bash
cd backend
```

* **Trường hợp 1: Thiết lập trên Database mới hoàn toàn (Khuyến nghị)**
  Chạy migration để Alembic tự động khởi tạo toàn bộ cấu trúc bảng và khóa ngoại:
  ```bash
  alembic upgrade head
  ```

* **Trường hợp 2: Database đã có sẵn cấu trúc bảng khớp với `models.py`**
  Đối chiếu cấu trúc bảng hiện tại với `database/models.py`, sau đó đánh dấu mốc baseline để Alembic bắt đầu theo dõi từ phiên bản hiện tại (không tạo lại bảng):
  ```bash
  alembic stamp head
  ```
  *(Lưu ý: Khi thay đổi cột/bảng trong `database/models.py` về sau, chạy `alembic revision --autogenerate -m "mo ta thay doi"` rồi chạy `alembic upgrade head` để cập nhật schema mà không mất dữ liệu).*

* **Nạp dữ liệu mẫu từ Excel vào PostgreSQL:**
  Sau khi hoàn tất bước migration ở trên, chạy script nạp dữ liệu:
  ```bash
  python database/seed_data.py
  ```
  *(Khi Terminal thông báo `-> Hoàn tất đồng bộ dữ liệu vào PostgreSQL!`, quá trình thiết lập dữ liệu đã hoàn tất).*

### 5. Khởi chạy API Server
Tại thư mục `backend`, khởi động server FastAPI:

```bash
uvicorn main:app --reload
```
Khi Terminal hiện dòng `Application startup complete.`, có thể truy cập giao diện kiểm thử API (**Swagger UI**) tại địa chỉ:
- **Swagger UI:** http://127.0.0.1:8000/docs