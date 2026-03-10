"""
Seed Vietnamese data for Bookstore Microservices.
Gửi dữ liệu mẫu tiếng Việt qua API Gateway (http://localhost:8000).
Đồng bộ đầy đủ dữ liệu từ database — chỉ cần chạy file này sau khi clone dự án.
"""
import requests, json, time, sys

BASE = "http://localhost:8000/api"

def post(path, data):
    r = requests.post(f"{BASE}{path}", json=data, timeout=10)
    if r.status_code in (200, 201):
        result = r.json()
        print(f"  ✓ POST {path} -> {result.get('id','ok')}")
        return result
    else:
        print(f"  ✗ POST {path} -> {r.status_code}: {r.text[:200]}")
        return None

# Chờ API Gateway sẵn sàng
print("Đang kiểm tra API Gateway...")
for i in range(30):
    try:
        r = requests.get(f"{BASE}/books/", timeout=5)
        if r.status_code == 200:
            print("API Gateway sẵn sàng!")
            break
    except Exception:
        pass
    time.sleep(2)
else:
    print("API Gateway không phản hồi. Hủy bỏ.")
    sys.exit(1)

# ═══════════════════════════════════════
# 1. STAFF & MANAGER
# ═══════════════════════════════════════
print("\n══ 1. NHÂN VIÊN & QUẢN LÝ ══")
staff_list = [
    {"username": "admin", "email": "admin@bookstore.vn", "password": "admin123", "full_name": "Nguyễn Văn An", "phone_number": "0901234567", "gender": "male", "role": "admin", "employee_code": "MGR001", "department": "Ban Giám đốc", "position": "Giám đốc", "hire_date": "2020-01-15", "salary": 30000000},
    {"username": "staffthu", "email": "thu@bookstore.vn", "password": "staff123", "full_name": "Trần Thị Thu", "phone_number": "0912345678", "gender": "female", "role": "staff", "employee_code": "STF001", "department": "Phòng Kinh doanh", "position": "Nhân viên bán hàng", "hire_date": "2022-03-01", "salary": 12000000},
    {"username": "staffminh", "email": "minh@bookstore.vn", "password": "staff123", "full_name": "Lê Hoàng Minh", "phone_number": "0923456789", "gender": "male", "role": "staff", "employee_code": "STF002", "department": "Phòng Kho vận", "position": "Nhân viên kho", "hire_date": "2022-06-15", "salary": 11000000},
    {"username": "staffhoa", "email": "hoa@bookstore.vn", "password": "staff123", "full_name": "Phạm Thị Hoa", "phone_number": "0934567890", "gender": "female", "role": "staff", "employee_code": "STF003", "department": "Phòng Chăm sóc KH", "position": "Nhân viên CSKH", "hire_date": "2023-01-10", "salary": 11500000},
    {"username": "staffduc", "email": "duc@bookstore.vn", "password": "staff123", "full_name": "Võ Quốc Đức", "phone_number": "0945678901", "gender": "male", "role": "staff", "employee_code": "STF004", "department": "Phòng IT", "position": "Quản trị hệ thống", "hire_date": "2021-08-20", "salary": 15000000},
]
for s in staff_list:
    post("/staff/", s)

managers = [
    {"username": "admin", "email": "admin@bookstore.vn", "password": "admin123", "full_name": "Nguyễn Văn An", "phone_number": "0901234567", "gender": "male", "employee_code": "MGR001", "department": "Ban Giám đốc", "access_level": 10},
]
for m in managers:
    post("/manager/", m)

# ═══════════════════════════════════════
# 2. CUSTOMERS
# ═══════════════════════════════════════
print("\n══ 2. KHÁCH HÀNG ══")
customers = [
    {"username": "ngoclinh", "email": "linh@gmail.com", "password": "cust123", "full_name": "Nguyễn Ngọc Linh", "phone_number": "0961111111", "date_of_birth": "1995-05-20", "gender": "female", "membership_level": "Gold", "loyalty_points": 1250, "total_spent": 2500000},
    {"username": "thanhtung", "email": "tung@gmail.com", "password": "cust123", "full_name": "Trần Thanh Tùng", "phone_number": "0962222222", "date_of_birth": "1990-11-03", "gender": "male", "membership_level": "Silver", "loyalty_points": 800, "total_spent": 1600000},
    {"username": "maitrang", "email": "trang@gmail.com", "password": "cust123", "full_name": "Lê Mai Trang", "phone_number": "0963333333", "date_of_birth": "1998-08-15", "gender": "female", "membership_level": "Bronze", "loyalty_points": 350, "total_spent": 700000},
    {"username": "quanghuy", "email": "huy@gmail.com", "password": "cust123", "full_name": "Phạm Quang Huy", "phone_number": "0964444444", "date_of_birth": "1992-02-28", "gender": "male", "membership_level": "Gold", "loyalty_points": 2100, "total_spent": 4200000},
    {"username": "thuyduong", "email": "duong@gmail.com", "password": "cust123", "full_name": "Hoàng Thùy Dương", "phone_number": "0965555555", "date_of_birth": "1997-12-10", "gender": "female", "membership_level": "Silver", "loyalty_points": 600, "total_spent": 1200000},
    {"username": "ducnam", "email": "nam@gmail.com", "password": "cust123", "full_name": "Vũ Đức Nam", "phone_number": "0966666666", "date_of_birth": "1988-07-04", "gender": "male", "membership_level": "Bronze", "loyalty_points": 150, "total_spent": 300000},
    {"username": "thuha", "email": "ha@gmail.com", "password": "cust123", "full_name": "Đinh Thu Hà", "phone_number": "0967777777", "date_of_birth": "2000-01-25", "gender": "female", "membership_level": "Bronze", "loyalty_points": 200, "total_spent": 400000},
    {"username": "minhquan", "email": "quan@gmail.com", "password": "cust123", "full_name": "Bùi Minh Quân", "phone_number": "0968888888", "date_of_birth": "1993-09-18", "gender": "male", "membership_level": "Silver", "loyalty_points": 950, "total_spent": 1900000},
]
for c in customers:
    post("/customers/", c)

# ═══════════════════════════════════════
# 2b. ĐỊA CHỈ GIAO HÀNG
# ═══════════════════════════════════════
print("\n══ 2b. ĐỊA CHỈ GIAO HÀNG ══")
addresses = [
    {"customer": 1, "recipient_name": "Ngọc Linh", "phone_number": "1234577", "address_line1": "Ngõ 3", "ward": "Yên Xá", "district": "Thanh Trì", "city": "Hà Nội", "country": "Vietnam", "is_default": True, "address_type": "home"},
]
for a in addresses:
    post("/customers/addresses/", a)

# ═══════════════════════════════════════
# 3. PUBLISHERS (NXB)
# ═══════════════════════════════════════
print("\n══ 3. NHÀ XUẤT BẢN ══")
publishers = [
    {"name": "NXB Kim Đồng", "description": "Nhà xuất bản sách thiếu nhi và truyện tranh hàng đầu Việt Nam", "address": "55 Quang Trung, Nguyễn Du", "city": "Hà Nội", "country": "Việt Nam", "phone_number": "024-39434730", "email": "info@nxbkimdong.com.vn"},
    {"name": "NXB Trẻ", "description": "Nhà xuất bản sách đa dạng thể loại, phục vụ bạn đọc trẻ", "address": "161B Lý Chính Thắng, Quận 3", "city": "TP. Hồ Chí Minh", "country": "Việt Nam", "phone_number": "028-39316289", "email": "hopthubandoc@nxbtre.com.vn"},
    {"name": "NXB Tổng hợp TP.HCM", "description": "Nhà xuất bản tổng hợp đa lĩnh vực tại TP.HCM", "address": "62 Nguyễn Thị Minh Khai, Quận 1", "city": "TP. Hồ Chí Minh", "country": "Việt Nam", "phone_number": "028-38225340", "email": "tonghop@nxbhcm.com.vn"},
    {"name": "NXB Phụ Nữ Việt Nam", "description": "Nhà xuất bản chuyên sách về phụ nữ, gia đình và xã hội", "address": "39 Hàng Chuối", "city": "Hà Nội", "country": "Việt Nam", "phone_number": "024-39717979", "email": "info@nxbphunu.com.vn"},
    {"name": "NXB Văn Học", "description": "Nhà xuất bản chuyên về văn học Việt Nam và thế giới", "address": "18 Nguyễn Trường Tộ", "city": "Hà Nội", "country": "Việt Nam", "phone_number": "024-38293765", "email": "info@nxbvanhoc.com.vn"},
    {"name": "NXB Giáo Dục Việt Nam", "description": "Nhà xuất bản sách giáo khoa và tài liệu giáo dục", "address": "81 Trần Hưng Đạo, Hoàn Kiếm", "city": "Hà Nội", "country": "Việt Nam", "phone_number": "024-38220801", "email": "info@nxbgd.vn"},
    {"name": "NXB Lao Động", "description": "Sách kinh tế, quản trị, kỹ năng và phát triển bản thân", "address": "175 Giảng Võ", "city": "Hà Nội", "country": "Việt Nam", "phone_number": "024-38515380", "email": "info@nxblaodong.com.vn"},
    {"name": "NXB Hội Nhà Văn", "description": "Nhà xuất bản của Hội Nhà văn Việt Nam", "address": "65 Nguyễn Du", "city": "Hà Nội", "country": "Việt Nam", "phone_number": "024-38222135", "email": "info@nxbhoinhavan.com.vn"},
]
for p in publishers:
    post("/catalog/publishers/", p)

# ═══════════════════════════════════════
# 4. AUTHORS
# ═══════════════════════════════════════
print("\n══ 4. TÁC GIẢ ══")
authors = [
    {"name": "Nguyễn Nhật Ánh", "biography": "Nhà văn nổi tiếng với nhiều tác phẩm văn học thiếu nhi và tuổi mới lớn. Tác giả của Mắt biếc, Tôi thấy hoa vàng trên cỏ xanh.", "birth_date": "1955-05-07", "nationality": "Việt Nam"},
    {"name": "Nam Cao", "biography": "Nhà văn hiện thực xuất sắc của văn học Việt Nam với các tác phẩm Chí Phèo, Lão Hạc, Sống mòn.", "birth_date": "1915-10-29", "death_date": "1951-11-30", "nationality": "Việt Nam"},
    {"name": "Tô Hoài", "biography": "Nhà văn lớn của Việt Nam, tác giả Dế mèn phiêu lưu ký, Vợ chồng A Phủ.", "birth_date": "1920-09-27", "death_date": "2014-07-06", "nationality": "Việt Nam"},
    {"name": "Nguyễn Du", "biography": "Đại thi hào dân tộc Việt Nam, tác giả Truyện Kiều - kiệt tác văn học cổ điển.", "birth_date": "1766-01-03", "death_date": "1820-09-16", "nationality": "Việt Nam"},
    {"name": "Hồ Chí Minh", "biography": "Chủ tịch Hồ Chí Minh - nhà thơ, nhà văn lớn với Nhật ký trong tù, Tuyên ngôn Độc lập.", "birth_date": "1890-05-19", "death_date": "1969-09-02", "nationality": "Việt Nam"},
    {"name": "Nguyễn Ngọc Tư", "biography": "Nhà văn nữ miền Tây Nam Bộ, tác giả Cánh đồng bất tận, Gió lẻ.", "birth_date": "1976-01-01", "nationality": "Việt Nam"},
    {"name": "Nguyễn Phong Việt", "biography": "Nhà thơ trẻ nổi tiếng với các tập thơ Đi qua thương nhớ, Sinh ra là để cô đơn.", "birth_date": "1980-12-25", "nationality": "Việt Nam"},
    {"name": "Dale Carnegie", "biography": "Tác giả người Mỹ nổi tiếng với các sách kỹ năng sống: Đắc nhân tâm, Quẳng gánh lo đi.", "birth_date": "1888-11-24", "death_date": "1955-11-01", "nationality": "Mỹ"},
    {"name": "Paulo Coelho", "biography": "Nhà văn Brazil nổi tiếng với Nhà giả kim, Mười một phút, Brida.", "birth_date": "1947-08-24", "nationality": "Brazil"},
    {"name": "Yuval Noah Harari", "biography": "Tác giả Israel viết về lịch sử nhân loại: Sapiens, Homo Deus, 21 bài học cho thế kỷ 21.", "birth_date": "1976-02-24", "nationality": "Israel"},
    {"name": "Thích Nhất Hạnh", "biography": "Thiền sư, nhà văn, nhà hoạt động hòa bình Việt Nam. Tác giả của Phép lạ của sự tỉnh thức.", "birth_date": "1926-10-11", "death_date": "2022-01-22", "nationality": "Việt Nam"},
    {"name": "Trần Đăng Khoa", "biography": "Nhà thơ thần đồng Việt Nam, nổi tiếng từ nhỏ với Góc sân và khoảng trời.", "birth_date": "1958-04-26", "nationality": "Việt Nam"},
]
for a in authors:
    post("/catalog/authors/", a)

# ═══════════════════════════════════════
# 5. CATEGORIES
# ═══════════════════════════════════════
print("\n══ 5. THỂ LOẠI ══")
categories = [
    {"name": "Văn học Việt Nam", "slug": "van-hoc-viet-nam", "description": "Tiểu thuyết, truyện ngắn, thơ của các tác giả Việt Nam", "display_order": 1},
    {"name": "Văn học nước ngoài", "slug": "van-hoc-nuoc-ngoai", "description": "Tác phẩm văn học dịch từ các ngôn ngữ khác", "display_order": 2},
    {"name": "Kỹ năng sống", "slug": "ky-nang-song", "description": "Sách phát triển bản thân, kỹ năng mềm, giao tiếp", "display_order": 3},
    {"name": "Kinh tế - Quản trị", "slug": "kinh-te-quan-tri", "description": "Sách về kinh doanh, quản lý, đầu tư, tài chính", "display_order": 4},
    {"name": "Thiếu nhi", "slug": "thieu-nhi", "description": "Sách dành cho trẻ em và thiếu niên", "display_order": 5},
    {"name": "Khoa học - Công nghệ", "slug": "khoa-hoc-cong-nghe", "description": "Sách khoa học, lập trình, AI, công nghệ thông tin", "display_order": 6},
    {"name": "Lịch sử - Địa lý", "slug": "lich-su-dia-ly", "description": "Sách về lịch sử Việt Nam, thế giới và địa lý", "display_order": 7},
    {"name": "Tâm lý - Triết học", "slug": "tam-ly-triet-hoc", "description": "Sách tâm lý học, triết học, tư duy", "display_order": 8},
    {"name": "Sách giáo khoa", "slug": "sach-giao-khoa", "description": "Sách giáo khoa các cấp và tài liệu tham khảo", "display_order": 9},
    {"name": "Manga - Comic", "slug": "manga-comic", "description": "Truyện tranh manga Nhật Bản và comic quốc tế", "display_order": 10},
]
for c in categories:
    post("/catalog/categories/", c)

# ═══════════════════════════════════════
# 6. BOOKS (25 cuốn)
# ═══════════════════════════════════════
print("\n══ 6. SÁCH ══")
books = [
    {"isbn": "978-604-1-21001", "title": "Mắt Biếc", "description": "Câu chuyện tình yêu đơn phương đẹp và buồn của Ngạn dành cho Hà Lan, từ thuở học trò đến khi trưởng thành.", "price": 110000, "discount_price": 88000, "stock": 50, "published_date": "2019-01-15", "language": "Tiếng Việt", "pages": 232, "format": "paperback", "cover_image": "https://m.media-amazon.com/images/S/compressed.photo.goodreads.com/books/1691147319i/11273677.jpg", "publisher_id": 1, "author_ids": [1], "category_ids": [1]},
    {"isbn": "978-604-1-21002", "title": "Tôi Thấy Hoa Vàng Trên Cỏ Xanh", "description": "Câu chuyện giản dị về tuổi thơ hồn nhiên ở một vùng quê nghèo, nơi tình bạn và lòng nhân hậu tỏa sáng.", "price": 125000, "discount_price": 99000, "stock": 45, "published_date": "2018-06-01", "language": "Tiếng Việt", "pages": 378, "format": "paperback", "cover_image": "https://www.nxbtre.com.vn/Images/Book/NXBTreStoryFull_08352010_033550.jpg", "publisher_id": 1, "author_ids": [1], "category_ids": [1]},
    {"isbn": "978-604-1-21003", "title": "Cho Tôi Xin Một Vé Đi Tuổi Thơ", "description": "Cuốn sách đưa người đọc trở về tuổi thơ trong sáng, với những trò chơi và ước mơ trẻ thơ.", "price": 95000, "discount_price": 76000, "stock": 60, "published_date": "2020-03-10", "language": "Tiếng Việt", "pages": 216, "format": "paperback", "cover_image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTypVeemU3zMELBFSUVTcyacuZsLICuGtZEww&s", "publisher_id": 2, "author_ids": [1], "category_ids": [1, 5]},
    {"isbn": "978-604-1-21004", "title": "Ngồi Khóc Trên Cây", "description": "Câu chuyện tình yêu lãng mạn và cảm động giữa cô gái kỳ lạ Rùa và chàng trai Đông.", "price": 105000, "discount_price": 84000, "stock": 35, "published_date": "2021-08-20", "language": "Tiếng Việt", "pages": 300, "format": "paperback", "cover_image": "https://www.netabooks.vn/Data/Sites/1/Product/77924/ngoi-khoc-tren-cay-kho-nho.jpg", "publisher_id": 1, "author_ids": [1], "category_ids": [1]},
    {"isbn": "978-604-1-21005", "title": "Chí Phèo (Tuyển tập Nam Cao)", "description": "Tuyển tập truyện ngắn xuất sắc nhất của Nam Cao: Chí Phèo, Lão Hạc, Đời thừa, Sống mòn.", "price": 89000, "discount_price": 71000, "stock": 40, "published_date": "2020-05-15", "language": "Tiếng Việt", "pages": 420, "format": "paperback", "cover_image": "https://cdn1.fahasa.com/media/catalog/product/v/n/vn-11134207-7ra0g-m6nr4tgwi1k706_1.jpg", "publisher_id": 5, "author_ids": [2], "category_ids": [1]},
    {"isbn": "978-604-1-21006", "title": "Dế Mèn Phiêu Lưu Ký", "description": "Cuộc phiêu lưu kỳ thú của chú Dế Mèn qua nhiều vùng đất, gặp gỡ nhiều loài vật thú vị.", "price": 75000, "discount_price": 60000, "stock": 80, "published_date": "2019-09-01", "language": "Tiếng Việt", "pages": 180, "format": "paperback", "cover_image": "https://dtv-ebook.com.vn/images/truyen-online/ebook-de-men-phieu-luu-ky-prc-pdf-epub.jpg", "publisher_id": 1, "author_ids": [3], "category_ids": [1, 5]},
    {"isbn": "978-604-1-21007", "title": "Truyện Kiều", "description": "Kiệt tác văn học cổ điển Việt Nam, kể về cuộc đời đầy sóng gió của nàng Kiều - Thúy Kiều.", "price": 68000, "discount_price": 54000, "stock": 100, "published_date": "2018-01-01", "language": "Tiếng Việt", "pages": 320, "format": "hardcover", "cover_image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT25qr58jmX-WF7PsRZRtDjO3txVY0u4YO5yw&s", "publisher_id": 5, "author_ids": [4], "category_ids": [1]},
    {"isbn": "978-604-1-21008", "title": "Đắc Nhân Tâm", "description": "Cuốn sách kinh điển về nghệ thuật giao tiếp và thu phục lòng người, bán chạy nhất mọi thời đại.", "price": 86000, "discount_price": 69000, "stock": 120, "published_date": "2021-01-01", "language": "Tiếng Việt", "pages": 320, "format": "paperback", "cover_image": "https://covers.openlibrary.org/b/isbn/9780671027032-L.jpg", "publisher_id": 2, "author_ids": [8], "category_ids": [2, 3]},
    {"isbn": "978-604-1-21009", "title": "Nhà Giả Kim", "description": "Câu chuyện về chàng chăn cừu Santiago theo đuổi giấc mơ tìm kho báu ở Kim tự tháp Ai Cập.", "price": 79000, "discount_price": 63000, "stock": 90, "published_date": "2020-06-15", "language": "Tiếng Việt", "pages": 228, "format": "paperback", "cover_image": "https://covers.openlibrary.org/b/isbn/9780062315007-L.jpg", "publisher_id": 3, "author_ids": [9], "category_ids": [2]},
    {"isbn": "978-604-1-21010", "title": "Sapiens: Lược Sử Loài Người", "description": "Hành trình lịch sử 70.000 năm của loài người từ thời Đồ Đá đến thế kỷ 21.", "price": 199000, "discount_price": 159000, "stock": 30, "published_date": "2022-03-01", "language": "Tiếng Việt", "pages": 560, "format": "paperback", "cover_image": "https://covers.openlibrary.org/b/isbn/9780062316097-L.jpg", "publisher_id": 3, "author_ids": [10], "category_ids": [2, 7]},
    {"isbn": "978-604-1-21011", "title": "Quẳng Gánh Lo Đi Và Vui Sống", "description": "Bí quyết để có cuộc sống vui vẻ, hạnh phúc và thoát khỏi lo âu.", "price": 95000, "discount_price": 76000, "stock": 55, "published_date": "2021-05-10", "language": "Tiếng Việt", "pages": 360, "format": "paperback", "cover_image": "https://covers.openlibrary.org/b/isbn/9780671733353-L.jpg", "publisher_id": 2, "author_ids": [8], "category_ids": [3]},
    {"isbn": "978-604-1-21012", "title": "Phép Lạ Của Sự Tỉnh Thức", "description": "Hướng dẫn thực hành chánh niệm trong đời sống hàng ngày của Thiền sư Thích Nhất Hạnh.", "price": 85000, "discount_price": 68000, "stock": 40, "published_date": "2020-11-01", "language": "Tiếng Việt", "pages": 180, "format": "paperback", "cover_image": "https://covers.openlibrary.org/b/isbn/9780807012390-L.jpg", "publisher_id": 4, "author_ids": [11], "category_ids": [3, 8]},
    {"isbn": "978-604-1-21013", "title": "Nghĩ Giàu Làm Giàu", "description": "13 nguyên tắc vàng để đạt được thành công và giàu có do Napoleon Hill tổng kết.", "price": 115000, "discount_price": 92000, "stock": 35, "published_date": "2021-08-01", "language": "Tiếng Việt", "pages": 400, "format": "paperback", "cover_image": "https://covers.openlibrary.org/b/isbn/9781585424337-L.jpg", "publisher_id": 7, "author_ids": [], "category_ids": [3, 4]},
    {"isbn": "978-604-1-21014", "title": "Cha Giàu Cha Nghèo", "description": "Bài học tài chính cá nhân qua câu chuyện hai người cha - Robert Kiyosaki.", "price": 135000, "discount_price": 108000, "stock": 25, "published_date": "2022-01-15", "language": "Tiếng Việt", "pages": 350, "format": "paperback", "cover_image": "https://covers.openlibrary.org/b/isbn/9781612680194-L.jpg", "publisher_id": 2, "author_ids": [], "category_ids": [4]},
    {"isbn": "978-604-1-21015", "title": "Khởi Nghiệp Tinh Gọn", "description": "Phương pháp khởi nghiệp hiện đại, giảm rủi ro và tăng tốc phát triển sản phẩm.", "price": 149000, "discount_price": 119000, "stock": 20, "published_date": "2022-06-01", "language": "Tiếng Việt", "pages": 290, "format": "paperback", "cover_image": "https://covers.openlibrary.org/b/isbn/9780307887894-L.jpg", "publisher_id": 7, "author_ids": [], "category_ids": [4]},
    {"isbn": "978-604-1-21016", "title": "Doraemon (Tập 1)", "description": "Tập 1 bộ truyện tranh Doraemon của Fujiko F. Fujio, chú mèo máy đến từ tương lai.", "price": 25000, "discount_price": 20000, "stock": 200, "published_date": "2019-04-01", "language": "Tiếng Việt", "pages": 192, "format": "paperback", "cover_image": "https://books.google.com/books/content?id=TOTEEAAAQBAJ&printsec=frontcover&img=1&zoom=2&source=gbs_api", "publisher_id": 1, "author_ids": [], "category_ids": [5, 10]},
    {"isbn": "978-604-1-21017", "title": "Conan - Thám Tử Lừng Danh (Tập 1)", "description": "Tập 1 bộ truyện trinh thám nổi tiếng về cậu bé thám tử Conan.", "price": 25000, "discount_price": 20000, "stock": 180, "published_date": "2019-05-01", "language": "Tiếng Việt", "pages": 186, "format": "paperback", "cover_image": "https://books.google.com/books/content?id=_S3yAQAAQBAJ&printsec=frontcover&img=1&zoom=2&source=gbs_api", "publisher_id": 1, "author_ids": [], "category_ids": [5, 10]},
    {"isbn": "978-604-1-21018", "title": "Lược Sử Thời Gian", "description": "Từ vụ nổ Big Bang đến hố đen - hành trình khám phá vũ trụ của Stephen Hawking.", "price": 125000, "discount_price": 100000, "stock": 30, "published_date": "2021-03-01", "language": "Tiếng Việt", "pages": 250, "format": "paperback", "cover_image": "https://covers.openlibrary.org/b/isbn/9780553380163-L.jpg", "publisher_id": 3, "author_ids": [], "category_ids": [6]},
    {"isbn": "978-604-1-21019", "title": "Python Cơ Bản Cho Người Mới", "description": "Hướng dẫn lập trình Python từ zero, phù hợp cho người mới bắt đầu học lập trình.", "price": 189000, "discount_price": 151000, "stock": 25, "published_date": "2023-01-10", "language": "Tiếng Việt", "pages": 480, "format": "paperback", "cover_image": "https://covers.openlibrary.org/b/isbn/9781593279288-L.jpg", "publisher_id": 6, "author_ids": [], "category_ids": [6]},
    {"isbn": "978-604-1-21020", "title": "Lịch Sử Việt Nam Bằng Tranh (Tập 1)", "description": "Từ thuở hồng hoang đến thời đại Hùng Vương - lịch sử Việt Nam qua tranh vẽ.", "price": 45000, "discount_price": 36000, "stock": 70, "published_date": "2020-09-01", "language": "Tiếng Việt", "pages": 100, "format": "paperback", "cover_image": "https://salt.tikicdn.com/cache/750x750/ts/product/59/bd/22/04b047c3206bd0aaac3552b689ec3df1.jpg.webp", "publisher_id": 1, "author_ids": [], "category_ids": [7, 5]},
    {"isbn": "978-604-1-21021", "title": "Đại Việt Sử Ký Toàn Thư", "description": "Bộ quốc sử cổ nhất của Việt Nam, ghi chép lịch sử từ thời Hồng Bàng đến thời Lê.", "price": 350000, "discount_price": 280000, "stock": 15, "published_date": "2020-01-01", "language": "Tiếng Việt", "pages": 1200, "format": "hardcover", "cover_image": "https://quangduc.com/images/file/rRAEINTd1AgBAeQP/dai-viet-su-ky-toan-thu.gif", "publisher_id": 5, "author_ids": [], "category_ids": [7]},
    {"isbn": "978-604-1-21022", "title": "Đi Qua Thương Nhớ", "description": "Tập thơ best-seller của Nguyễn Phong Việt về tình yêu, nỗi nhớ và cuộc sống.", "price": 75000, "discount_price": 60000, "stock": 45, "published_date": "2021-02-14", "language": "Tiếng Việt", "pages": 160, "format": "paperback", "cover_image": "https://cdn1.fahasa.com/media/catalog/product/8/9/8936071850911.jpg", "publisher_id": 2, "author_ids": [7], "category_ids": [1]},
    {"isbn": "978-604-1-21023", "title": "Nhật Ký Trong Tù", "description": "Tập thơ bất hủ của Chủ tịch Hồ Chí Minh viết trong nhà tù Tưởng Giới Thạch.", "price": 55000, "discount_price": 44000, "stock": 60, "published_date": "2019-05-19", "language": "Tiếng Việt", "pages": 200, "format": "paperback", "cover_image": "https://file3.qdnd.vn/data/images/0/2023/05/12/hoanghoang/a.jpg?dpi=150&quality=100&w=870", "publisher_id": 5, "author_ids": [5], "category_ids": [1]},
    {"isbn": "978-604-1-21024", "title": "Góc Sân Và Khoảng Trời", "description": "Tập thơ thiếu nhi kinh điển của thần đồng thơ Trần Đăng Khoa.", "price": 45000, "discount_price": 36000, "stock": 55, "published_date": "2019-06-01", "language": "Tiếng Việt", "pages": 120, "format": "paperback", "cover_image": "https://upload.wikimedia.org/wikipedia/vi/b/b1/Goc_san_va_khoang_troi.jpg", "publisher_id": 1, "author_ids": [12], "category_ids": [1, 5]},
    {"isbn": "978-604-1-21025", "title": "Cánh Đồng Bất Tận", "description": "Tuyển tập truyện ngắn đặc sắc của Nguyễn Ngọc Tư về cuộc sống miền Tây sông nước.", "price": 98000, "discount_price": 78000, "stock": 30, "published_date": "2020-08-01", "language": "Tiếng Việt", "pages": 240, "format": "paperback", "cover_image": "https://books.google.com/books/content?id=c_9XCQAAQBAJ&printsec=frontcover&img=1&zoom=2&source=gbs_api", "publisher_id": 2, "author_ids": [6], "category_ids": [1]},
]
for b in books:
    post("/books/", b)

# ═══════════════════════════════════════
# 7. ORDERS (10 đơn hàng — lưu order_number để dùng cho shipments/payments)
# ═══════════════════════════════════════
print("\n══ 7. ĐƠN HÀNG ══")
orders_data = [
    {"customer_id": 1, "status": "delivered", "subtotal": 187000, "shipping_fee": 30000, "discount": 10000, "final_amount": 207000, "payment_method": "cod", "notes": "Giao giờ hành chính", "items": [{"book_id": 1, "book_title": "Mắt Biếc", "quantity": 1, "unit_price": 88000, "subtotal": 88000}, {"book_id": 9, "book_title": "Nhà Giả Kim", "quantity": 1, "unit_price": 63000, "subtotal": 63000}, {"book_id": 7, "book_title": "Truyện Kiều", "quantity": 1, "unit_price": 54000, "subtotal": 54000}]},
    {"customer_id": 2, "status": "shipped", "subtotal": 328000, "shipping_fee": 25000, "discount": 0, "final_amount": 353000, "payment_method": "bank_transfer", "notes": "", "items": [{"book_id": 10, "book_title": "Sapiens", "quantity": 1, "unit_price": 159000, "subtotal": 159000}, {"book_id": 8, "book_title": "Đắc Nhân Tâm", "quantity": 1, "unit_price": 69000, "subtotal": 69000}, {"book_id": 2, "book_title": "Tôi Thấy Hoa Vàng Trên Cỏ Xanh", "quantity": 1, "unit_price": 99000, "subtotal": 99000}]},
    {"customer_id": 3, "status": "pending", "subtotal": 156000, "shipping_fee": 30000, "discount": 0, "final_amount": 186000, "payment_method": "e_wallet", "notes": "Gọi trước khi giao", "items": [{"book_id": 3, "book_title": "Cho Tôi Xin Một Vé Đi Tuổi Thơ", "quantity": 1, "unit_price": 76000, "subtotal": 76000}, {"book_id": 6, "book_title": "Dế Mèn Phiêu Lưu Ký", "quantity": 1, "unit_price": 60000, "subtotal": 60000}]},
    {"customer_id": 4, "status": "delivered", "subtotal": 543000, "shipping_fee": 0, "discount": 50000, "final_amount": 493000, "payment_method": "credit_card", "notes": "", "items": [{"book_id": 14, "book_title": "Cha Giàu Cha Nghèo", "quantity": 1, "unit_price": 108000, "subtotal": 108000}, {"book_id": 15, "book_title": "Khởi Nghiệp Tinh Gọn", "quantity": 1, "unit_price": 119000, "subtotal": 119000}, {"book_id": 10, "book_title": "Sapiens", "quantity": 1, "unit_price": 159000, "subtotal": 159000}, {"book_id": 19, "book_title": "Python Cơ Bản Cho Người Mới", "quantity": 1, "unit_price": 151000, "subtotal": 151000}]},
    {"customer_id": 5, "status": "confirmed", "subtotal": 175000, "shipping_fee": 20000, "discount": 0, "final_amount": 195000, "payment_method": "cod", "notes": "Giao cuối tuần", "items": [{"book_id": 12, "book_title": "Phép Lạ Của Sự Tỉnh Thức", "quantity": 1, "unit_price": 68000, "subtotal": 68000}, {"book_id": 11, "book_title": "Quẳng Gánh Lo Đi Và Vui Sống", "quantity": 1, "unit_price": 76000, "subtotal": 76000}]},
    {"customer_id": 1, "status": "processing", "subtotal": 371000, "shipping_fee": 0, "discount": 20000, "final_amount": 351000, "payment_method": "bank_transfer", "notes": "", "items": [{"book_id": 18, "book_title": "Lược Sử Thời Gian", "quantity": 1, "unit_price": 100000, "subtotal": 100000}, {"book_id": 21, "book_title": "Đại Việt Sử Ký Toàn Thư", "quantity": 1, "unit_price": 280000, "subtotal": 280000}]},
    {"customer_id": 6, "status": "delivered", "subtotal": 40000, "shipping_fee": 15000, "discount": 0, "final_amount": 55000, "payment_method": "cod", "notes": "", "items": [{"book_id": 16, "book_title": "Doraemon (Tập 1)", "quantity": 1, "unit_price": 20000, "subtotal": 20000}, {"book_id": 17, "book_title": "Conan - Thám Tử Lừng Danh (Tập 1)", "quantity": 1, "unit_price": 20000, "subtotal": 20000}]},
    {"customer_id": 8, "status": "delivered", "subtotal": 230000, "shipping_fee": 25000, "discount": 15000, "final_amount": 240000, "payment_method": "credit_card", "notes": "Bọc quà tặng", "items": [{"book_id": 1, "book_title": "Mắt Biếc", "quantity": 1, "unit_price": 88000, "subtotal": 88000}, {"book_id": 5, "book_title": "Chí Phèo (Tuyển tập Nam Cao)", "quantity": 1, "unit_price": 71000, "subtotal": 71000}, {"book_id": 22, "book_title": "Đi Qua Thương Nhớ", "quantity": 1, "unit_price": 60000, "subtotal": 60000}]},
    {"customer_id": 1, "status": "cancelled", "subtotal": 114000, "shipping_fee": 0, "discount": 0, "final_amount": 114000, "payment_method": "cod", "carrier_code": "GHN", "shipping_address_id": 1, "notes": "", "items": [{"book_id": 24, "book_title": "Góc Sân Và Khoảng Trời", "quantity": 1, "unit_price": 36000, "subtotal": 36000}, {"book_id": 25, "book_title": "Cánh Đồng Bất Tận", "quantity": 1, "unit_price": 78000, "subtotal": 78000}]},
    {"customer_id": 1, "status": "cancelled", "subtotal": 36000, "shipping_fee": 0, "discount": 0, "final_amount": 36000, "payment_method": "cod", "carrier_code": "GHN", "shipping_address_id": 1, "notes": "", "items": [{"book_id": 24, "book_title": "Góc Sân Và Khoảng Trời", "quantity": 1, "unit_price": 36000, "subtotal": 36000}]},
]

order_numbers = {}
for i, o in enumerate(orders_data, 1):
    result = post("/orders/", o)
    if result:
        order_numbers[i] = result.get("order_number", f"ORD-{i:03d}")

# ═══════════════════════════════════════
# 8. CARRIERS & SHIPMENTS
# ═══════════════════════════════════════
print("\n══ 8. ĐƠN VỊ VẬN CHUYỂN ══")
carriers = [
    {"name": "Giao Hàng Nhanh (GHN)", "code": "GHN", "contact_number": "1900636677", "website": "https://ghn.vn"},
    {"name": "Giao Hàng Tiết Kiệm (GHTK)", "code": "GHTK", "contact_number": "1900545436", "website": "https://ghtk.vn"},
    {"name": "VNPost - Bưu Điện Việt Nam", "code": "VNPOST", "contact_number": "1900545499", "website": "https://vnpost.vn"},
    {"name": "J&T Express", "code": "JT", "contact_number": "1900100168", "website": "https://jtexpress.vn"},
    {"name": "Viettel Post", "code": "VTP", "contact_number": "1900636009", "website": "https://viettelpost.com.vn"},
    {"name": "Shopee Express", "code": "SP"},
]
for c in carriers:
    post("/shipments/carriers/", c)

print("\n══ 8b. VẬN ĐƠN ══")
shipments = [
    {"order_id": 1, "order_number": order_numbers.get(1, ""), "customer_id": 1, "carrier_code": "GHN", "tracking_number": "GHN12345678", "status": "delivered", "shipping_cost": 30000},
    {"order_id": 2, "order_number": order_numbers.get(2, ""), "customer_id": 2, "carrier_code": "GHTK", "tracking_number": "GHTK87654321", "status": "in_transit", "shipping_cost": 25000},
    {"order_id": 4, "order_number": order_numbers.get(4, ""), "customer_id": 4, "carrier_code": "GHN", "tracking_number": "GHN11112222", "status": "delivered", "shipping_cost": 0},
    {"order_id": 7, "order_number": order_numbers.get(7, ""), "customer_id": 6, "carrier_code": "VNPOST", "tracking_number": "VNP99998888", "status": "delivered", "shipping_cost": 15000},
    {"order_id": 8, "order_number": order_numbers.get(8, ""), "customer_id": 8, "carrier_code": "JT", "tracking_number": "JT33334444", "status": "delivered", "shipping_cost": 25000},
    {"order_id": 9, "order_number": order_numbers.get(9, ""), "customer_id": 1, "carrier_code": "GHN", "status": "pending", "shipping_cost": 0, "shipping_address_id": 1},
    {"order_id": 10, "order_number": order_numbers.get(10, ""), "customer_id": 1, "carrier_code": "GHN", "status": "pending", "shipping_cost": 0, "shipping_address_id": 1},
]
for s in shipments:
    post("/shipments/", s)

# ═══════════════════════════════════════
# 9. PAYMENT METHODS & PAYMENTS
# ═══════════════════════════════════════
print("\n══ 9. PHƯƠNG THỨC THANH TOÁN ══")
methods = [
    {"name": "Thanh toán khi nhận hàng", "code": "cod", "description": "Trả tiền mặt khi nhận hàng", "processing_fee": 0, "display_order": 1},
    {"name": "Chuyển khoản ngân hàng", "code": "bank_transfer", "description": "Chuyển khoản qua tài khoản ngân hàng", "processing_fee": 0, "display_order": 2},
    {"name": "Thẻ tín dụng / ghi nợ", "code": "credit_card", "description": "Visa, Mastercard, JCB", "processing_fee": 15000, "display_order": 3},
    {"name": "Ví điện tử", "code": "e_wallet", "description": "MoMo, ZaloPay, VNPay", "processing_fee": 0, "display_order": 4},
]
for m in methods:
    post("/payments/methods/", m)

print("\n══ 9b. HOÁ ĐƠN THANH TOÁN ══")
payments = [
    {"order_id": 1, "order_number": order_numbers.get(1, ""), "customer_id": 1, "payment_method": "cod", "amount": 207000, "status": "completed"},
    {"order_id": 2, "order_number": order_numbers.get(2, ""), "customer_id": 2, "payment_method": "bank_transfer", "amount": 353000, "status": "completed"},
    {"order_id": 4, "order_number": order_numbers.get(4, ""), "customer_id": 4, "payment_method": "credit_card", "amount": 493000, "status": "completed"},
    {"order_id": 7, "order_number": order_numbers.get(7, ""), "customer_id": 6, "payment_method": "cod", "amount": 55000, "status": "completed"},
    {"order_id": 8, "order_number": order_numbers.get(8, ""), "customer_id": 8, "payment_method": "credit_card", "amount": 240000, "status": "completed"},
    {"order_id": 3, "order_number": order_numbers.get(3, ""), "customer_id": 3, "payment_method": "e_wallet", "amount": 186000, "status": "pending"},
    {"order_id": 5, "order_number": order_numbers.get(5, ""), "customer_id": 5, "payment_method": "cod", "amount": 195000, "status": "pending"},
    {"order_id": 6, "order_number": order_numbers.get(6, ""), "customer_id": 1, "payment_method": "bank_transfer", "amount": 351000, "status": "processing"},
    {"order_id": 9, "order_number": order_numbers.get(9, ""), "customer_id": 1, "payment_method": "cod", "amount": 114000, "status": "pending"},
    {"order_id": 10, "order_number": order_numbers.get(10, ""), "customer_id": 1, "payment_method": "cod", "amount": 36000, "status": "pending"},
]
for p in payments:
    post("/payments/", p)

# ═══════════════════════════════════════
# 10. REVIEWS (14 đánh giá)
# ═══════════════════════════════════════
print("\n══ 10. ĐÁNH GIÁ ══")
reviews = [
    {"book_id": 8, "customer_id": 1, "rating": 5, "title": "Rất bổ ích", "comment": "Đắc Nhân Tâm giúp tôi thay đổi cách giao tiếp rất nhiều. Ai cũng nên đọc cuốn này.", "is_verified": True},
    {"book_id": 10, "customer_id": 2, "rating": 4, "title": "Đáng đọc", "comment": "Sapiens mang đến góc nhìn mới về lịch sử loài người. Hơi dài nhưng rất hấp dẫn.", "is_verified": True},
    {"book_id": 2, "customer_id": 2, "rating": 5, "title": "Tuổi thơ dữ dội", "comment": "Nguyễn Nhật Ánh viết hay quá! Đọc xong nhớ tuổi thơ vô cùng.", "is_verified": True},
    {"book_id": 9, "customer_id": 3, "rating": 4, "title": "Sách hay", "comment": "Nhà Giả Kim truyền cảm hứng theo đuổi ước mơ. Phù hợp cho mọi lứa tuổi.", "is_verified": False},
    {"book_id": 6, "customer_id": 3, "rating": 5, "title": "Kinh điển!", "comment": "Con trai tôi rất thích Dế Mèn. Sách in đẹp, giấy tốt.", "is_verified": False},
    {"book_id": 14, "customer_id": 4, "rating": 4, "title": "Thay đổi tư duy tài chính", "comment": "Cha Giàu Cha Nghèo giúp tôi hiểu về tiền bạc và đầu tư. Nên đọc sớm.", "is_verified": True},
    {"book_id": 19, "customer_id": 4, "rating": 3, "title": "Khá cơ bản", "comment": "Cuốn Python này phù hợp cho người hoàn toàn mới. Nếu đã biết lập trình thì hơi dễ.", "is_verified": True},
    {"book_id": 12, "customer_id": 5, "rating": 5, "title": "Bình yên", "comment": "Đọc sách của Thầy Nhất Hạnh giúp tâm an lạc. Rất cần thiết trong cuộc sống hiện đại.", "is_verified": True},
    {"book_id": 1, "customer_id": 8, "rating": 5, "title": "Mắt Biếc tuyệt vời", "comment": "Đọc lần thứ 3 vẫn thấy hay và cảm động. Cảm ơn Nguyễn Nhật Ánh!", "is_verified": True},
    {"book_id": 5, "customer_id": 8, "rating": 4, "title": "Văn học kinh điển", "comment": "Tuyển tập Nam Cao rất đáng đọc. Chí Phèo là tác phẩm bất hủ.", "is_verified": True},
    {"book_id": 16, "customer_id": 6, "rating": 5, "title": "Con thích lắm!", "comment": "Mua cho con đọc, bé rất thích Doraemon. Sách in màu đẹp.", "is_verified": True},
    {"book_id": 7, "customer_id": 4, "rating": 5, "title": "Kiệt tác", "comment": "Truyện Kiều là niềm tự hào của văn học Việt Nam. Bản in rất đẹp.", "is_verified": True},
    {"book_id": 22, "customer_id": 8, "rating": 4, "title": "Thơ hay xúc động", "comment": "Tập thơ Đi Qua Thương Nhớ đọc rất xúc động, phù hợp cho những ai đang yêu.", "is_verified": True},
    {"book_id": 1, "customer_id": 1, "rating": 5, "title": "Quá hay", "comment": "Tôi đã mua và thấy rất hay.", "is_verified": False},
]
for r in reviews:
    post("/reviews/", r)

# ═══════════════════════════════════════
# 11. RECOMMENDATIONS
# ═══════════════════════════════════════
print("\n══ 11. GỢI Ý ══")
recs = [
    {"customer_id": 1, "book_id": 4, "score": 0.95, "reason": "Dựa trên sách của Nguyễn Nhật Ánh bạn đã mua"},
    {"customer_id": 1, "book_id": 25, "score": 0.88, "reason": "Bạn thích văn học Việt Nam"},
    {"customer_id": 2, "book_id": 13, "score": 0.91, "reason": "Bạn quan tâm đến sách kỹ năng sống"},
    {"customer_id": 2, "book_id": 18, "score": 0.85, "reason": "Dựa trên Sapiens bạn đã mua"},
    {"customer_id": 3, "book_id": 1, "score": 0.93, "reason": "Sách bán chạy nhất phù hợp với bạn"},
    {"customer_id": 4, "book_id": 10, "score": 0.89, "reason": "Bạn thích sách kinh tế và lịch sử"},
    {"customer_id": 5, "book_id": 23, "score": 0.87, "reason": "Dựa trên sở thích tâm linh của bạn"},
    {"customer_id": 6, "book_id": 24, "score": 0.90, "reason": "Sách thiếu nhi phù hợp cho con bạn"},
    {"customer_id": 8, "book_id": 9, "score": 0.86, "reason": "Bạn thích văn học nước ngoài"},
]
for r in recs:
    post("/recommendations/", r)

# ═══════════════════════════════════════
# 12. CARTS (giỏ hàng)
# ═══════════════════════════════════════
print("\n══ 12. GIỎ HÀNG ══")
carts = [
    {"customer_id": 3, "items": [{"book_id": 1, "book_title": "Mắt Biếc", "quantity": 1, "price": 88000}, {"book_id": 11, "book_title": "Quẳng Gánh Lo Đi Và Vui Sống", "quantity": 1, "price": 76000}]},
    {"customer_id": 7, "items": [{"book_id": 8, "book_title": "Đắc Nhân Tâm", "quantity": 2, "price": 69000}, {"book_id": 25, "book_title": "Cánh Đồng Bất Tận", "quantity": 1, "price": 78000}]},
    {"customer_id": 5, "items": [{"book_id": 21, "book_title": "Đại Việt Sử Ký Toàn Thư", "quantity": 1, "price": 280000}]},
]
for c in carts:
    post("/carts/", c)

# ═══════════════════════════════════════
# 13. USER BEHAVIORS (dữ liệu hành vi cho gợi ý AI)
# ═══════════════════════════════════════
print("\n══ 13. HÀNH VI NGƯỜI DÙNG ══")
behaviors = [
    {"customer_id": 1, "book_id": 23, "action_type": "view"},
    {"customer_id": 1, "book_id": 20, "action_type": "view"},
    {"customer_id": 1, "book_id": 11, "action_type": "add_to_cart"},
    {"customer_id": 1, "book_id": 7, "action_type": "add_to_cart"},
    {"customer_id": 1, "book_id": 9, "action_type": "add_to_cart"},
    {"customer_id": 1, "book_id": 8, "action_type": "view"},
    {"customer_id": 1, "book_id": 9, "action_type": "view"},
    {"customer_id": 1, "book_id": 12, "action_type": "view"},
    {"customer_id": 1, "book_id": 16, "action_type": "view"},
]
for b in behaviors:
    post("/recommendations/behaviors/", b)

print("\n" + "="*50)
print("✅ HOÀN TẤT THÊM DỮ LIỆU!")
print("="*50)
print("""
📊 Tổng kết:
  • 5 nhân viên (1 admin + 4 staff)
  • 1 quản lý (admin, access_level 10)
  • 8 khách hàng + 1 địa chỉ giao hàng
  • 8 nhà xuất bản
  • 12 tác giả
  • 10 thể loại
  • 25 cuốn sách
  • 10 đơn hàng (8 gốc + 2 đã hủy)
  • 6 đơn vị vận chuyển + 7 vận đơn
  • 4 phương thức thanh toán + 10 hóa đơn
  • 14 đánh giá
  • 9 gợi ý sách
  • 3 giỏ hàng (có sản phẩm)
  • 9 hành vi người dùng

🔑 Tài khoản đăng nhập:
  Manager: admin / admin123
  Staff:   staffthu / staff123
  Staff:   staffminh / staff123
  KH:      ngoclinh / cust123
  KH:      thanhtung / cust123
""")
