Cài đặt
1. Tải dự án
bash
git clone https://github.com/yourusername/employee-management.git
cd employee-management
Hoặc tải file ZIP và giải nén.

2. Cài đặt thư viện
Mở terminal (Command Prompt / PowerShell) trong thư mục dự án và chạy:

bash
pip install -r requirements.txt
File requirements.txt bao gồm:

text
flask==3.0.3
flask-cors==4.0.1
gunicorn==21.2.0
3. Cấu trúc thư mục
Sau khi tải về, cấu trúc thư mục như sau:

text
employee-management/
├── app.py                    # File chính
├── requirements.txt          # Thư viện cần cài
├── controller/               # Xử lý logic
├── model/                    # Định nghĩa dữ liệu
├── util/                     # Tiện ích
├── view/                     # Giao diện (HTML, CSS, JS)
├── data/                     # Dữ liệu (JSON)
└── image/                    # Hình ảnh
Chạy ứng dụng
Chạy local
bash
python app.py
Truy cập
Mở trình duyệt và truy cập: http://localhost:5000

Dừng ứng dụng
Nhấn Ctrl + C trong terminal.