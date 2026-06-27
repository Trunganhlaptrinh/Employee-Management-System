# controller/salary_controller.py
# controller: xử lý logic lương thưởng

from flask import Blueprint, request, jsonify, session
from model.salary     import Salary
from util.file_helper  import FileHelper
from util.validation   import Validation

salary_bp = Blueprint("salary", __name__)

# ========================
# TẠO BẢNG LƯƠNG (chỉ admin)
# POST /api/salary
# ========================
@salary_bp.route("", methods=["POST"])
def create_salary():
    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "Không có quyền"}), 403

    data = request.get_json()
    try:
        employee_id = int(data.get("employee_id", 0))
        month       = Validation.check_month(data.get("month", ""))
        bonus       = Validation.check_money(data.get("bonus", 0),     "Thưởng")
        deduction   = Validation.check_money(data.get("deduction", 0), "Khấu trừ")
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400

    # lấy lương cơ bản từ employee
    employees = FileHelper.read_all("employees")
    emp = next((e for e in employees if e["id"] == employee_id), None)
    if not emp:
        return jsonify({"success": False, "message": "Không tìm thấy nhân viên"}), 404

    # kiểm tra đã tạo bảng lương tháng này chưa
    all_salaries = FileHelper.read_all("salaries")
    already = any(
        s["employee_id"] == employee_id and s["month"] == month
        for s in all_salaries
    )
    if already:
        return jsonify({"success": False, "message": "Đã có bảng lương tháng này"}), 409

    sal = Salary(
        employee_id = employee_id,
        month       = month,
        base        = emp["base_salary"],
        bonus       = bonus,
        deduction   = deduction
    )
    FileHelper.append_item("salaries", sal.to_dict())
    return jsonify({"success": True, "message": "Tạo bảng lương thành công", "total": sal.total}), 201

# ========================
# XEM BẢNG LƯƠNG
# GET /api/salary?employee_id=&month=
# ========================
@salary_bp.route("", methods=["GET"])
def get_salaries():
    if "employee_id" not in session:
        return jsonify({"success": False, "message": "Chưa đăng nhập"}), 401

    all_salaries = FileHelper.read_all("salaries")
    result = all_salaries

    if session["role"] != "admin":
        result = [s for s in result if s["employee_id"] == session["employee_id"]]
    else:
        emp_id_filter = request.args.get("employee_id")
        if emp_id_filter:
            result = [s for s in result if s["employee_id"] == int(emp_id_filter)]

    month_filter = request.args.get("month")
    if month_filter:
        result = [s for s in result if s["month"] == month_filter]

    return jsonify({"success": True, "data": result})

# ========================
# CẬP NHẬT BẢNG LƯƠNG (chỉ admin)
# PUT /api/salary/<id>
# ========================
@salary_bp.route("/<int:salary_id>", methods=["PUT"])
def update_salary(salary_id):
    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "Không có quyền"}), 403

    data = request.get_json()
    try:
        bonus     = Validation.check_money(data.get("bonus", 0),     "Thưởng")
        deduction = Validation.check_money(data.get("deduction", 0), "Khấu trừ")
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400

    all_salaries = FileHelper.read_all("salaries")
    for i, s in enumerate(all_salaries):
        if s["id"] == salary_id:
            all_salaries[i]["bonus"]     = bonus
            all_salaries[i]["deduction"] = deduction
            all_salaries[i]["total"]     = s["base"] + bonus - deduction
            FileHelper.write_all("salaries", all_salaries)
            return jsonify({"success": True, "message": "Cập nhật thành công", "total": all_salaries[i]["total"]})

    return jsonify({"success": False, "message": "Không tìm thấy bảng lương"}), 404

@salary_bp.route("/<int:salary_id>", methods=["DELETE"])
def delete_salary(salary_id):
    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "Không có quyền"}), 403

    ok = FileHelper.delete_item("salaries", salary_id)
    if not ok:
        return jsonify({"success": False, "message": "Không tìm thấy bảng lương"}), 404
    return jsonify({"success": True, "message": "Đã xóa bảng lương"})
