# Signora Backend

**Signora** là nền tảng học ngôn ngữ ký hiệu thích ứng, hỗ trợ người học tiếp cận và luyện tập ngôn ngữ ký hiệu thông qua các bài học có cấu trúc, video minh họa, nhận diện ký hiệu bằng AI và hệ thống phản hồi cá nhân hóa.

Repository này chứa mã nguồn Backend của hệ thống Signora, được xây dựng bằng **FastAPI**, cung cấp các RESTful API phục vụ quản lý người dùng, phiên bản học tập, nội dung bài học, tiến độ học tập, lượt luyện tập và phản hồi thích ứng.

---

## 1. Giới thiệu

Signora hướng đến việc xây dựng trải nghiệm học ngôn ngữ ký hiệu trực quan, tương tác và phù hợp với khả năng của từng người học.

Backend chịu trách nhiệm quản lý dữ liệu và xử lý các nghiệp vụ chính của hệ thống, bao gồm:

- Quản lý hồ sơ người dùng.
- Quản lý các phiên bản và nội dung bài học.
- Lưu trữ thông tin các ký hiệu và hướng dẫn thực hiện.
- Theo dõi tiến độ học tập của người dùng.
- Quản lý các lượt luyện tập và kết quả nhận diện.
- Cung cấp phản hồi dựa trên kết quả luyện tập.
- Hỗ trợ cơ chế học tập thích ứng thông qua việc ghi nhận lỗi sai.

### Luồng hoạt động chính

1. Người dùng chọn hồ sơ học tập.
2. Người dùng lựa chọn phiên bản học tập.
3. Hệ thống hiển thị danh sách bài học và tiến độ tương ứng.
4. Người dùng truy cập bài học, xem video minh họa và hướng dẫn thực hiện ký hiệu.
5. Người dùng thực hành thông qua hệ thống nhận diện ngôn ngữ ký hiệu.
6. Backend tiếp nhận và lưu kết quả luyện tập, các lỗi sai.
7. Hệ thống cung cấp phản hồi và cập nhật tiến độ học tập.

---

## 2. Chức năng chính

### 2.1. Quản lý người dùng
- Tạo hồ sơ người dùng.
- Lấy thông tin người dùng.
- Lựa chọn hồ sơ đã tồn tại.

### 2.2. Quản lý phiên bản và bài học
- Lấy danh sách các phiên bản học tập.
- Lấy danh sách bài học theo từng phiên bản.
- Tạo bài học mới cùng danh sách ký hiệu bên trong.
- Lấy thông tin chi tiết bài học.
- Lấy thông tin chi tiết từng ký hiệu.
- Kiểm tra trạng thái khả dụng của bài học.
- Quản lý cấu hình phản hồi cho từng bài học.

### 2.3. Quản lý tiến độ học tập
- Theo dõi số lượng bài học đã hoàn thành.
- Tính tỷ lệ hoàn thành bài học.
- Lưu điểm số cao nhất và điểm số gần nhất.
- Thống kê tiến độ tổng quan.
- Theo dõi tiến độ theo phiên bản và từng bài học.

### 2.4. Quản lý lượt luyện tập
- Tạo và quản lý các lượt luyện tập.
- Lưu kết quả và điểm số.
- Ghi nhận các lỗi sai trong quá trình thực hành.
- Lưu lịch sử luyện tập của người dùng.

### 2.5. Phản hồi thích ứng
- Cung cấp phản hồi dựa trên kết quả luyện tập.
- Hỗ trợ phản hồi cố định và phản hồi thích ứng.
- Ghi nhận các lỗi sai lặp lại để hỗ trợ cá nhân hóa quá trình học tập.

### 2.6. Thu thập dữ liệu
- Lưu trữ các mẫu dữ liệu được thu thập trong quá trình học tập.
- Hỗ trợ quản lý dữ liệu phục vụ phân tích và cải thiện hệ thống.

---

## 3. Công nghệ sử dụng

| Công nghệ | Vai trò |
|---|---|
| Python 3.9.9 | Ngôn ngữ lập trình |
| FastAPI | Framework xây dựng Backend API |
| SQLAlchemy 2.0 | ORM và tương tác với cơ sở dữ liệu |
| SQLAlchemy Async | Hỗ trợ truy vấn cơ sở dữ liệu bất đồng bộ |
| SQL Server | Hệ quản trị cơ sở dữ liệu |
| Pydantic | Kiểm tra và xác thực dữ liệu |
| Alembic | Quản lý phiên bản và migration cơ sở dữ liệu |
| PyODBC | Kết nối Python với SQL Server |
| Uvicorn | ASGI Server chạy ứng dụng |

---

## 4. Kiến trúc hệ thống

Backend được tổ chức theo mô hình phân tầng (Layered Architecture), giúp tách biệt trách nhiệm giữa các thành phần và hỗ trợ việc mở rộng, bảo trì hệ thống.

```text
Frontend (React + TypeScript)
              |
              | HTTP / REST API
              v
         FastAPI
              |
              v
          API Layer
       (Routers / Endpoints)
              |
              v
         Service Layer
        (Business Logic)
              |
              v
       Repository Layer
         (Data Access)
              |
              v
        SQLAlchemy ORM
              |
              v
          SQL Server
```

### Trách nhiệm các tầng

- **API Layer:** Tiếp nhận HTTP Request, kiểm tra dữ liệu đầu vào và trả về Response.
- **Schema Layer:** Định nghĩa cấu trúc dữ liệu Request và Response bằng Pydantic.
- **Service Layer:** Xử lý nghiệp vụ và điều phối các hoạt động của hệ thống.
- **Repository Layer:** Thực hiện các thao tác truy vấn và tương tác với cơ sở dữ liệu.
- **Model Layer:** Định nghĩa các bảng và mối quan hệ trong cơ sở dữ liệu bằng SQLAlchemy.

---

## 5. Cấu trúc thư mục

```text
backend/
│
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── users.py
│   │       ├── versions.py
│   │       ├── lessons.py
│   │       ├── progress.py
│   │       ├── attempts.py
│   │       └── feedback.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── version.py
│   │   ├── lesson.py
│   │   ├── lesson_item.py
│   │   ├── user_lesson_progress.py
│   │   ├── attempt.py
│   │   ├── attempt_error.py
│   │   ├── feedback.py
│   │   ├── app_settings.py
│   │   └── collector_sample.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── version.py
│   │   ├── lesson.py
│   │   ├── progress.py
│   │   ├── attempt.py
│   │   └── feedback.py
│   │
│   ├── repositories/
│   │   ├── user_repository.py
│   │   ├── lesson_repository.py
│   │   └── ...
│   │
│   ├── services/
│   │   ├── user_service.py
│   │   ├── lesson_service.py
│   │   └── ...
│   │
│   └── main.py
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── .env.example
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md
```

*Lưu ý: Cấu trúc trên mang tính tham khảo theo định hướng tổ chức dự án. Cần điều chỉnh tên file và module theo mã nguồn thực tế.*

---

## 6. Thiết kế cơ sở dữ liệu

Hệ thống sử dụng SQL Server để quản lý và lưu trữ dữ liệu.

Các bảng chính:

| Bảng | Mô tả |
|---|---|
| `users` | Lưu thông tin và hồ sơ người dùng |
| `versions` | Lưu thông tin các phiên bản học tập |
| `lessons` | Lưu danh sách bài học thuộc từng phiên bản |
| `lesson_items` | Lưu thông tin các ký hiệu trong bài học |
| `user_lesson_progress` | Theo dõi tiến độ học tập của người dùng |
| `attempts` | Lưu các lượt luyện tập và kết quả |
| `attempt_errors` | Ghi nhận các lỗi sai trong quá trình luyện tập |
| `feedbacks` | Lưu thông tin phản hồi |
| `app_settings` | Lưu cấu hình ứng dụng |
| `collector_samples` | Lưu các mẫu dữ liệu thu thập được |

### Mối quan hệ giữa các thực thể

```text
users
  |
  +---- user_lesson_progress
  |
  +---- attempts
           |
           +---- attempt_errors

versions
  |
  +---- lessons
           |
           +---- lesson_items
           |
           +---- user_lesson_progress
           |
           +---- attempts

feedbacks
app_settings
collector_samples
```

---

## 7. Danh sách API

Các API được phân chia theo từng nhóm chức năng.

### 7.1. Lesson API

| Method | Endpoint | Mô tả |
|---|---|---|
| GET | `/versions/{version_id}/lessons` | Lấy danh sách bài học theo phiên bản, có thể kèm tiến độ người dùng |
| GET | `/lessons/{lesson_id}` | Lấy chi tiết bài học và danh sách ký hiệu |
| POST | `/versions/{version_id}/lessons` | Tạo bài học mới cùng danh sách ký hiệu |
| GET | `/lesson-items/{lesson_item_id}` | Lấy chi tiết một ký hiệu |
| GET | `/lessons/{lesson_id}/feedback-config` | Lấy cấu hình phản hồi của bài học |
| GET | `/lessons/{lesson_id}/availability` | Kiểm tra khả năng truy cập và luyện tập bài học |

### 7.2. Progress API

| Method | Endpoint | Mô tả |
|---|---|---|
| GET | `/users/{user_id}/progress` | Lấy tiến độ học tập tổng quan |
| GET | `/users/{user_id}/progress/versions/{version_id}` | Lấy tiến độ theo phiên bản |
| GET | `/users/{user_id}/progress/lessons/{lesson_id}` | Lấy tiến độ của một bài học |

### 7.3. Các nhóm API khác

| Nhóm | Chức năng |
|---|---|
| User API | Quản lý hồ sơ người dùng |
| Version API | Quản lý phiên bản học tập |
| Attempt API | Quản lý lượt luyện tập và kết quả |
| Feedback API | Quản lý phản hồi |
| Collector API | Quản lý dữ liệu thu thập |

Danh sách endpoint chi tiết có thể xem trực tiếp trên Swagger UI sau khi khởi chạy Backend.

---

## 8. Hướng dẫn cài đặt và chạy dự án

### 8.1. Yêu cầu môi trường

Cài đặt các công cụ cần thiết:

- Python 3.9.9
- SQL Server LocalDB hoặc SQL Server
- ODBC Driver 18 for SQL Server
- Git

### 8.2. Clone repository

```bash
git clone <repository-url>
cd backend
```

### 8.3. Tạo môi trường ảo

```bash
python -m venv .venv
```

Kích hoạt môi trường ảo trên Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 8.4. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### 8.5. Cấu hình biến môi trường

Tạo file `.env` tại thư mục gốc của dự án:

```env
DATABASE_URL=mssql+pyodbc:///?odbc_connect=DRIVER%3D%7BODBC%20Driver%2018%20for%20SQL%20Server%7D%3BSERVER%3D%28localdb%29%5CMSSQLLocalDB%3BDATABASE%3DSignora%3BTrusted_Connection%3Dyes%3BTrustServerCertificate%3Dyes
```

Đảm bảo cơ sở dữ liệu `Signora` đã được tạo và SQL Server có thể kết nối bình thường.

### 8.6. Khởi tạo cơ sở dữ liệu

Sử dụng Alembic để áp dụng các migration:

```bash
alembic upgrade head
```

### 8.7. Khởi chạy Backend

```bash
uvicorn app.main:app --reload
```

Sau khi khởi chạy thành công, Backend sẽ hoạt động tại:

```text
http://127.0.0.1:8000
```

---

## 9. Quản lý Migration

Dự án sử dụng Alembic để quản lý các thay đổi trong cấu trúc cơ sở dữ liệu.

**Tạo migration mới:**

```bash
alembic revision --autogenerate -m "migration_description"
```

**Áp dụng migration:**

```bash
alembic upgrade head
```

**Kiểm tra phiên bản hiện tại:**

```bash
alembic current
```

**Xem lịch sử migration:**

```bash
alembic history
```

---

## 10. Tài liệu API

FastAPI hỗ trợ tự động tạo tài liệu API thông qua OpenAPI.

Sau khi chạy Backend, truy cập các địa chỉ sau:

| Tài liệu | Đường dẫn |
|---|---|
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |
| OpenAPI JSON | http://127.0.0.1:8000/openapi.json |

Swagger UI hỗ trợ:
- Xem danh sách API theo từng nhóm chức năng.
- Kiểm tra phương thức và endpoint.
- Xem cấu trúc Request và Response.
- Thử nghiệm API trực tiếp trên trình duyệt.

---

## 11. Quy ước phát triển

Để đảm bảo tính nhất quán và khả năng bảo trì, dự án áp dụng một số quy ước:

- Tách biệt SQLAlchemy Models và Pydantic Schemas.
- Đặt các nghiệp vụ xử lý trong Service Layer.
- Sử dụng Repository Layer để quản lý truy vấn dữ liệu.
- Sử dụng Pydantic để xác thực dữ liệu đầu vào.
- Ưu tiên các thao tác bất đồng bộ khi tương tác với cơ sở dữ liệu.
- Sử dụng Alembic để quản lý thay đổi schema.
- Thống nhất cấu trúc Request và Response giữa Backend và Frontend.
- Không lưu trực tiếp video và hình ảnh vào SQL Server.

### Quản lý Media

Các tài nguyên học tập như video minh họa, hình ảnh tham chiếu và video chuyển động chậm được Frontend quản lý dưới dạng static assets.

Backend quản lý thông tin nội dung bài học và các đường dẫn media tương ứng khi cần thiết.

---

## 12. Thông tin dự án

| Thuộc tính | Thông tin |
|---|---|
| Tên dự án | Signora |
| Loại dự án | Nền tảng học ngôn ngữ ký hiệu thích ứng |
| Backend Framework | FastAPI |
| Ngôn ngữ lập trình | Python |
| Cơ sở dữ liệu | SQL Server |
| Kiến trúc | Layered Architecture |
| Môn học | Tương tác người máy (HCI) |

---

**Signora - Để mỗi ký hiệu nở hoa.** 🌱
