# app.py
from flask import Flask, send_from_directory
from flask_cors import CORS
import os

from controller.auth_controller import auth_bp
from controller.attendance_controller import attendance_bp
from controller.leave_controller import leave_bp
from controller.salary_controller import salary_bp
from controller.asset_controller import asset_bp
from controller.risk_controller import risk_bp
from controller.incident_controller import incident_bp

from model.employee import Employee
from model.attendance import Attendance
from model.leave import Leave
from model.salary import Salary
from util.file_helper import FileHelper
from util.auth_helper import AuthHelper

# === ĐỊNH NGHĨA APP TRƯỚC ===
app = Flask(__name__)
app.secret_key = "employee_mgmt_secret_2025"

VIEW_DIR = os.path.join(os.path.dirname(__file__), "view")

CORS(app, supports_credentials=True)

# === ROUTES ===
@app.route("/")
def index():
    return send_from_directory(VIEW_DIR, "index.html")

@app.route("/<path:filename>")
def serve_view(filename):
    return send_from_directory(VIEW_DIR, filename)

# === REGISTER BLUEPRINTS (SAU KHI ĐÃ CÓ APP) ===
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(attendance_bp, url_prefix="/api/attendance")
app.register_blueprint(leave_bp, url_prefix="/api/leave")
app.register_blueprint(salary_bp, url_prefix="/api/salary")
app.register_blueprint(asset_bp, url_prefix="/api/assets")
app.register_blueprint(risk_bp, url_prefix="/api/risks")
app.register_blueprint(incident_bp, url_prefix="/api/incidents")

def sync_id_counters():
    Employee._id_counter = FileHelper.get_max_id("employees") + 1
    Attendance._id_counter = FileHelper.get_max_id("attendance") + 1
    Leave._id_counter = FileHelper.get_max_id("leaves") + 1
    Salary._id_counter = FileHelper.get_max_id("salaries") + 1

def create_default_admin():
    employees = FileHelper.read_all("employees")
    if not employees:
        admin = Employee(
            username="admin",
            password_hash=AuthHelper.hash_password("admin123"),
            name="Administrator",
            role="admin",
            department="Management",
            base_salary=0
        )
        FileHelper.append_item("employees", admin.to_dict())
        print("Đã tạo tài khoản admin mặc định: admin / admin123")

if __name__ == "__main__":
    sync_id_counters()
    create_default_admin()
    app.run(debug=True, port=5000)