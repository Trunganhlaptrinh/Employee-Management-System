SmartEMS - Employee Management System
Hệ thống quản lý nhân viên với các chức năng: Điểm danh, Nghỉ phép, Lương thưởng, Quản lý hồ sơ.
Giới thiệu
SmartEMS là hệ thống quản lý nhân viên sử dụng Flask và lưu dữ liệu bằng file JSON.
Phân quyền:

* Admin: Quản lý toàn bộ hệ thống

* Nhân viên: Quản lý thông tin cá nhân

Yêu cầu hệ thống

* Python 3.8 trở lên (Tải Python)

* pip (đi kèm với Python)

Lưu ý: Nếu chưa có Python, hãy tải và cài đặt từ trang chủ Python.
Cài đặt
1. Tải dự án
Cách 1 - Dùng Git:
bash

```
git clone https://github.com/yourusername/employee-management.git
cd employee-management
```

Cách 2 - Tải file ZIP:

* Truy cập repository trên GitHub

* Nhấn nút Code → Download ZIP

* Giải nén file ZIP

2. Cài đặt Python (nếu chưa có)
Windows:

1. Tải Python từ: https://www.python.org/downloads/

2. Chạy file cài đặt

3. Quan trọng: Đánh dấu chọn "Add Python to PATH"

4. Nhấn "Install Now"

macOS:
bash

```
# Cài đặt Homebrew trước (nếu chưa có)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Cài đặt Python
brew install python
```

Linux (Ubuntu/Debian):
bash

```
sudo apt update
sudo apt install python3 python3-pip
```

3. Cài đặt thư viện
Mở terminal (Command Prompt / PowerShell) trong thư mục dự án và chạy:
bash

```
pip install -r requirements.txt
```

Nếu gặp lỗi, thử:
bash

```
pip3 install -r requirements.txt
```

File requirements.txt bao gồm:
text

```
flask==3.0.3
flask-cors==4.0.1
gunicorn==21.2.0
```

4. Kiểm tra cài đặt
bash

```
python --version
pip --version
```

Kết quả mong đợi:
text

```
Python 3.8.x
pip 21.x.x
```

5. Cấu trúc thư mục
Sau khi tải về, cấu trúc thư mục như sau:
text

```
employee-management/
├── app.py                    # File chính
├── requirements.txt          # Thư viện cần cài
├── controller/               # Xử lý logic
├── model/                    # Định nghĩa dữ liệu
├── util/                     # Tiện ích
├── view/                     # Giao diện (HTML, CSS, JS)
├── data/                     # Dữ liệu (JSON)
└── image/                    # Hình ảnh
```

Chạy ứng dụng
Chạy local
bash

```
python app.py
```

Hoặc:
bash

```
python3 app.py
```

Truy cập
Mở trình duyệt và truy cập: http://localhost:5000
Dừng ứng dụng
Nhấn Ctrl + C trong terminal.
Tài khoản mặc định
Vai tròUsernamePasswordAdminadminadmin123
Tài khoản admin được tự động tạo khi chạy lần đầu.
Hướng dẫn sử dụng
1. Đăng nhập

1. Mở trình duyệt, truy cập http://localhost:5000

2. Nhập Username và Password

3. Nhấn nút Đăng nhập

2. Dashboard (Trang tổng quan)
Admin:

* Xem tổng số nhân viên, điểm danh hôm nay, đơn nghỉ chờ duyệt, tổng lương

* Các nút truy cập nhanh: Điểm danh, Nghỉ phép, Lương thưởng, Hồ sơ

Nhân viên:

* Xem thông tin cá nhân của mình

* Các nút truy cập nhanh tương tự

3. Điểm danh
Quy tắc:

* Trước 9:00 → Có mặt

* 9:00 - 9:15 → Đi muộn

* Sau 9:15 → Vắng

Admin:

1. Vào tab Điểm danh

2. Chọn nhân viên

3. Chọn trạng thái và ngày

4. Nhấn Điểm danh

Nhân viên:

1. Vào tab Điểm danh

2. Nhấn nút Điểm danh (hệ thống tự động xác định trạng thái)

4. Nghỉ phép
Gửi đơn:

1. Vào tab Nghỉ phép

2. Nhấn Chọn ngày nghỉ

3. Chọn ngày bắt đầu và kết thúc

4. Nhập lý do

5. Nhấn Xác nhận gửi đơn

Admin duyệt đơn:

1. Vào tab Nghỉ phép

2. Chọn đơn cần duyệt

3. Nhấn Duyệt hoặc Từ chối

5. Lương thưởng
Admin:

* Trả lương tháng: Chọn nhân viên → Chọn tháng → Xác nhận

* Chỉnh sửa: Thay đổi lương cơ bản và phòng ban

Nhân viên:

* Xem bảng lương của mình

* Nhấn Xuất Excel để tải file

6. Hồ sơ cá nhân

1. Vào tab Hồ sơ

2. Cập nhật:

   * Ảnh đại diện: Click vào avatar → Chọn ảnh → Cắt ảnh → Xác nhận

   * Ảnh bìa: Click vào ảnh bìa → Chọn ảnh → Cắt ảnh → Xác nhận

   * Thông tin: Sửa ở tab "Chỉnh sửa"

   * Mật khẩu: Sửa ở tab "Đổi mật khẩu"

7. Quản lý nhân viên (Admin)

1. Vào tab Quản lý nhân viên

2. Thêm nhân viên: Nhập thông tin → Nhấn Thêm nhân viên

3. Reset mật khẩu: Nhấn Reset MK

4. Xóa nhân viên: Nhấn Xóa (không xóa được chính mình)

Xử lý lỗi thường gặp
Lỗi: "Python not found"
Nguyên nhân: Chưa cài Python hoặc chưa thêm vào PATH
Cách sửa:

* Cài lại Python và đánh dấu "Add Python to PATH"

* Hoặc thêm thủ công: Hướng dẫn

Lỗi: "pip not found"
Cách sửa:
bash

```
# Windows
python -m pip install --upgrade pip

# macOS/Linux
python3 -m pip install --upgrade pip
```

Lỗi: Module không tìm thấy
Cách sửa:
bash

```
pip install -r requirements.txt
```

Lỗi: Cổng 5000 đã được sử dụng
Cách sửa: Đổi cổng trong file app.py
python

```
app.run(debug=True, port=5001)
```

Lỗi: Không đọc được file JSON
Cách sửa: Tạo thư mục data
bash

```
mkdir data
```

Dữ liệu
Dữ liệu được lưu trong thư mục data/ dưới dạng file JSON:
FileNội dungemployees.jsonThông tin nhân viênattendance.jsonDữ liệu điểm danhleaves.jsonĐơn nghỉ phépsalaries.jsonBảng lương
Backup dữ liệu: Copy toàn bộ thư mục data/
Liên hệ

* Tác giả: TrungAnh

* GitHub: yourusername

License
MIT License
Hướng dẫn tải file README.md:

1. Copy toàn bộ nội dung trên

2. Mở Notepad (hoặc bất kỳ text editor nào)

3. Dán nội dung vào

4. Lưu file với tên README.md

5. Đặt file vào thư mục gốc của dự án

Hoặc bạn có thể tạo file bằng terminal:
Windows (PowerShell):
powershell

```
# Tạo file README.md
New-Item -Path README.md -ItemType File

# Mở file để chỉnh sửa
notepad README.md

# Dán nội dung vào, lưu và thoát
```

macOS/Linux:
bash

```
# Tạo file README.md
touch README.md

# Mở file để chỉnh sửa
nano README.md
# hoặc
vim README.md

# Dán nội dung vào, lưu và thoát
```
