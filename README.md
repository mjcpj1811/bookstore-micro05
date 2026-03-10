# 📚 Bookstore Microservices

Hệ thống quản lý nhà sách trực tuyến xây dựng theo kiến trúc **Microservices**, sử dụng **Django REST Framework** + **MySQL** + **Docker**.

## Kiến trúc hệ thống

```
                         ┌──────────────┐
                         │  API Gateway │ :8000
                         │  (Django)    │
                         └──────┬───────┘
                                │
        ┌───────┬───────┬───────┼───────┬───────┬───────┐
        ▼       ▼       ▼       ▼       ▼       ▼       ▼
   ┌────────┐┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐
   │ Staff  ││Mngr  ││Cust  ││Book  ││Cart  ││Order ││ ...  │
   │ :8001  ││:8002 ││:8003 ││:8005 ││:8006 ││:8007 ││      │
   └────┬───┘└──┬───┘└──┬───┘└──┬───┘└──┬───┘└──┬───┘└──┬───┘
        └───────┴───────┴───────┼───────┴───────┴───────┘
                                ▼
                         ┌──────────────┐
                         │   MySQL 8.0  │ :3307
                         └──────────────┘
```

| Service | Port | Mô tả |
|---------|------|-------|
| API Gateway | 8000 | Proxy + giao diện web (Customer, Staff, Manager) |
| Staff Service | 8001 | Quản lý nhân viên |
| Manager Service | 8002 | Quản lý quản lý viên |
| Customer Service | 8003 | Quản lý khách hàng, địa chỉ |
| Catalog Service | 8004 | NXB, tác giả, danh mục |
| Book Service | 8005 | Quản lý sách |
| Cart Service | 8006 | Giỏ hàng |
| Order Service | 8007 | Đơn hàng, checkout |
| Ship Service | 8008 | Vận chuyển, hãng vận chuyển |
| Pay Service | 8009 | Thanh toán, phương thức thanh toán |
| Comment & Rate Service | 8010 | Đánh giá, bình luận sách |
| Recommender AI Service | 8011 | Gợi ý sách (AI collaborative filtering) |
| MySQL | 3307 | Cơ sở dữ liệu (11 databases) |

## Yêu cầu

- **Docker Desktop** (bao gồm Docker Compose)
- **Python 3.10+** (để chạy seed data)
- **pip** (Python package manager)

## Khởi tạo dự án

### Bước 1: Clone repository

```bash
git clone <repository-url>
cd bookstore-micro05
```

### Bước 2: Build và khởi chạy Docker containers

```bash
docker compose up --build -d
```

Lệnh này sẽ:
- Tạo MySQL container + 11 databases
- Build và chạy 11 microservices + API Gateway
- Tự động chạy migrations cho tất cả services

> ⏳ Lần đầu build sẽ mất vài phút. Đợi tất cả services healthy trước khi tiếp tục.

Kiểm tra trạng thái:

```bash
docker compose ps
```

Đảm bảo tất cả containers có trạng thái `Up`.

### Bước 3: Seed dữ liệu mẫu

Cài thư viện `requests` (nếu chưa có):

```bash
pip install requests
```

Chạy seed data:

```bash
python seed_data.py
```

Script sẽ tự động đợi API Gateway sẵn sàng, sau đó tạo:
- 5 nhân viên, 1 quản lý, 8 khách hàng
- 8 NXB, 12 tác giả, 10 danh mục, 25 cuốn sách (có ảnh bìa)
- 10 đơn hàng, 7 vận đơn, 10 thanh toán
- 6 hãng vận chuyển, 4 phương thức thanh toán
- 14 đánh giá sách, 9 gợi ý sách
- 3 giỏ hàng có sản phẩm

### Bước 4: Truy cập ứng dụng

| Trang | URL |
|-------|-----|
| **Trang chủ (Khách hàng)** | http://localhost:8000/ |
| **Đăng nhập** | http://localhost:8000/login/ |
| **Staff Portal** | http://localhost:8000/staff/ |
| **Manager Portal** | http://localhost:8000/manager/ |
| **API Root** | http://localhost:8000/api/ |
| **Health Check** | http://localhost:8000/api/health/ |

### Tài khoản mẫu

| Vai trò | Username | Password |
|---------|----------|----------|
| Manager | `admin` | `admin123` |
| Staff | `staffthu`, `staffminh`, `staffhoa`, `staffduc` | `staff123` |
| Customer | `ngoclinh`, `thanhtung`, `maitrang`, `quanghuy`, ... | `cust123` |

## Các lệnh hữu ích

```bash
# Khởi chạy
docker compose up -d

# Dừng
docker compose down

# Dừng + xóa dữ liệu (reset hoàn toàn)
docker compose down -v

# Xem logs
docker compose logs -f api-gateway
docker compose logs -f book-service

# Rebuild một service
docker compose up --build -d book-service

# Truy cập shell của một service
docker exec -it bookstore-micro05-book-service-1 python manage.py shell
```

## Chạy local (không Docker)

> Yêu cầu: MySQL đang chạy trên localhost:3306, đã tạo 11 databases.

```bash
# Tạo virtual environment
python -m venv .venv

# Kích hoạt (Windows)
.venv\Scripts\activate

# Cài dependencies
pip install -r requirements.txt

# Chạy migrations
python run_migrations.py

# Chạy tất cả services
python run_all.py

# Seed dữ liệu
python seed_data.py
```

## Cấu trúc thư mục

```
bookstore-micro05/
├── docker-compose.yml        # Docker orchestration
├── entrypoint.sh             # Container entrypoint (migrations + start)
├── init-databases.sql        # Tạo 11 databases
├── requirements.txt          # Python dependencies
├── run_all.py                # Chạy tất cả services (local)
├── run_migrations.py         # Chạy migrations (local)
├── seed_data.py              # Seed dữ liệu mẫu
├── api_gateway/              # API Gateway + Web UI
│   ├── gateway/              #   Proxy views + template views
│   └── templates/            #   HTML templates (customer, staff, manager)
├── staff_service/            # Staff microservice
├── manager_service/          # Manager microservice
├── customer_service/         # Customer microservice
├── catalog_service/          # Catalog (NXB, tác giả, danh mục)
├── book_service/             # Book microservice
├── cart_service/             # Cart microservice
├── order_service/            # Order microservice
├── ship_service/             # Shipping microservice
├── pay_service/              # Payment microservice
├── comment_rate_service/     # Review & Rating microservice
└── recommender_ai_service/   # AI Recommendation microservice
```

## Tech Stack

- **Backend:** Django 4.2, Django REST Framework
- **Database:** MySQL 8.0
- **Containerization:** Docker, Docker Compose
- **Frontend:** HTML, Bootstrap 5, JavaScript (fetch API)
- **AI:** Collaborative Filtering (popularity-based recommendation)
