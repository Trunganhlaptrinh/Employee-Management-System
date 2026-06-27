# controller/auth_controller.py
# controller: xử lý logic đăng nhập, đăng xuất, quản lý nhân viên
# tương tự StudentManagement.java — nhưng trả về JSON thay vì in ra console

from flask import Blueprint, request, jsonify, session
from model.employee   import Employee
from util.file_helper import FileHelper
from util.auth_helper import AuthHelper
from util.validation  import Validation

# Blueprint = nhóm các route liên quan đến auth
# tương tự: class StudentManagement trong Java
auth_bp = Blueprint("auth", __name__)

# ========================
# ĐĂNG NHẬP
# POST /api/auth/login
# ========================
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    # kiểm tra input
    try:
        username = Validation.check_username(data.get("username", ""))
        password = Validation.check_password(data.get("password", ""))
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400

    # tìm nhân viên theo username trong file JSON
    employees = FileHelper.read_all("employees")
    found = None
    for emp_dict in employees:
        if emp_dict["username"] == username:
            found = emp_dict
            break

    # kiểm tra tồn tại và mật khẩu
    if not found or not AuthHelper.check_password(password, found["password_hash"]):
        return jsonify({"success": False, "message": "Sai username hoặc mật khẩu"}), 401

    # lưu thông tin vào session (giữ đăng nhập)
    session["employee_id"] = found["id"]
    session["role"]        = found["role"]
    session["name"]        = found["name"]

    return jsonify({
        "success": True,
        "message": "Đăng nhập thành công",
        "employee": {
            "id":         found["id"],
            "name":       found["name"],
            "role":       found["role"],
            "department": found["department"]
        }
    })

# ========================
# ĐĂNG XUẤT
# POST /api/auth/logout
# ========================
@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": True, "message": "Đã đăng xuất"})

# ========================
# KIỂM TRA SESSION
# GET /api/auth/me
# ========================
@auth_bp.route("/me", methods=["GET"])
def me():
    if "employee_id" not in session:
        return jsonify({"success": False, "message": "Chưa đăng nhập"}), 401
    return jsonify({
        "success":     True,
        "employee_id": session["employee_id"],
        "role":        session["role"],
        "name":        session["name"]
    })

# ========================
# LẤY DANH SÁCH NHÂN VIÊN (chỉ admin)
# GET /api/auth/employees
# ========================
@auth_bp.route("/employees", methods=["GET"])
def get_employees():
    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "Không có quyền"}), 403

    employees = FileHelper.read_all("employees")
    # không trả về password_hash ra ngoài
    safe = [{k: v for k, v in e.items() if k != "password_hash"} for e in employees]
    return jsonify({"success": True, "data": safe})

# ========================
# THÊM NHÂN VIÊN (chỉ admin)
# POST /api/auth/employees
# ========================
@auth_bp.route("/employees", methods=["POST"])
def add_employee():
    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "Không có quyền"}), 403

    data = request.get_json()
    try:
        username   = Validation.check_username(data.get("username", ""))
        password   = Validation.check_password(data.get("password", ""))
        name       = Validation.check_name(data.get("name", ""))
        role       = Validation.check_role(data.get("role", ""))
        department = Validation.check_not_empty(data.get("department", ""), "Phòng ban")
        base_salary = Validation.check_money(data.get("base_salary", 0), "Lương cơ bản")
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400

    # kiểm tra username trùng
    employees = FileHelper.read_all("employees")
    if any(e["username"] == username for e in employees):
        return jsonify({"success": False, "message": "Username đã tồn tại"}), 409

    emp = Employee(
        username      = username,
        password_hash = AuthHelper.hash_password(password),
        name          = name,
        role          = role,
        department    = department,
        base_salary   = base_salary
    )
    FileHelper.append_item("employees", emp.to_dict())
    return jsonify({"success": True, "message": "Thêm nhân viên thành công", "id": emp.id}), 201

# ========================
# XÓA NHÂN VIÊN (chỉ admin)
# DELETE /api/auth/employees/<id>
# ========================
@auth_bp.route("/employees/<int:emp_id>", methods=["DELETE"])
def delete_employee(emp_id):
    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "Không có quyền"}), 403
    if emp_id == session.get("employee_id"):
        return jsonify({"success": False, "message": "Không thể xóa chính mình"}), 400

    ok = FileHelper.delete_item("employees", emp_id)
    if not ok:
        return jsonify({"success": False, "message": "Không tìm thấy nhân viên"}), 404
    return jsonify({"success": True, "message": "Đã xóa nhân viên"})
