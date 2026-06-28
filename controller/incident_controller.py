# controller/incident_controller.py
# Controller: Quản lý sự cố bảo mật

from flask import Blueprint, request, jsonify, session
from model.incident import Incident
from util.file_helper import FileHelper
from util.validation import Validation
from datetime import datetime

incident_bp = Blueprint("incident", __name__)

# ========================
# LẤY DANH SÁCH SỰ CỐ
# GET /api/incidents
# ========================
@incident_bp.route("", methods=["GET"])
def get_incidents():
    if "employee_id" not in session:
        return jsonify({"success": False, "message": "Chưa đăng nhập"}), 401

    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "Không có quyền"}), 403

    incidents = FileHelper.read_all("incidents")
    
    # Lọc theo status
    status = request.args.get("status")
    if status:
        incidents = [i for i in incidents if i["status"] == status]

    # Lọc theo severity
    severity = request.args.get("severity")
    if severity:
        incidents = [i for i in incidents if i["severity"] == severity]

    # Sắp xếp theo ngày báo cáo mới nhất
    incidents.sort(key=lambda x: x.get("reported_date", ""), reverse=True)

    return jsonify({"success": True, "data": incidents})

# ========================
# THÊM SỰ CỐ MỚI
# POST /api/incidents
# ========================
@incident_bp.route("", methods=["POST"])
def add_incident():
    if "employee_id" not in session:
        return jsonify({"success": False, "message": "Chưa đăng nhập"}), 401

    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "Không có quyền"}), 403

    data = request.get_json()
    try:
        title = Validation.check_not_empty(data.get("title", ""), "Tiêu đề")
        incident_type = Validation.check_in_list(data.get("incident_type", ""),
                                                  Incident.INCIDENT_TYPES, "Loại sự cố")
        severity = Validation.check_in_list(data.get("severity", ""),
                                            Incident.SEVERITY_LEVELS, "Mức độ")
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400

    incident = Incident(
        title=title,
        incident_type=incident_type,
        severity=severity,
        description=data.get("description", ""),
        affected_assets=data.get("affected_assets", []),
        reported_by=data.get("reported_by", ""),
        assigned_to=data.get("assigned_to", "")
    )

    FileHelper.append_item("incidents", incident.to_dict())
    return jsonify({"success": True, "message": "Thêm sự cố thành công", "id": incident.id}), 201

# ========================
# CẬP NHẬT SỰ CỐ
# PUT /api/incidents/<id>
# ========================
@incident_bp.route("/<int:incident_id>", methods=["PUT"])
def update_incident(incident_id):
    if "employee_id" not in session:
        return jsonify({"success": False, "message": "Chưa đăng nhập"}), 401

    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "Không có quyền"}), 403

    data = request.get_json()
    incidents = FileHelper.read_all("incidents")
    
    for i, inc in enumerate(incidents):
        if inc["id"] == incident_id:
            # Cập nhật các trường
            if "title" in data:
                incidents[i]["title"] = data["title"]
            if "incident_type" in data:
                incidents[i]["incident_type"] = data["incident_type"]
            if "severity" in data:
                incidents[i]["severity"] = data["severity"]
            if "description" in data:
                incidents[i]["description"] = data["description"]
            if "affected_assets" in data:
                incidents[i]["affected_assets"] = data["affected_assets"]
            if "assigned_to" in data:
                incidents[i]["assigned_to"] = data["assigned_to"]
            if "status" in data:
                incidents[i]["status"] = data["status"]
                if data["status"] == "Resolved" or data["status"] == "Closed":
                    incidents[i]["resolved_date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            if "root_cause" in data:
                incidents[i]["root_cause"] = data["root_cause"]
            if "lessons_learned" in data:
                incidents[i]["lessons_learned"] = data["lessons_learned"]

            FileHelper.write_all("incidents", incidents)
            return jsonify({"success": True, "message": "Cập nhật thành công"})

    return jsonify({"success": False, "message": "Không tìm thấy sự cố"}), 404

# ========================
# XÓA SỰ CỐ
# DELETE /api/incidents/<id>
# ========================
@incident_bp.route("/<int:incident_id>", methods=["DELETE"])
def delete_incident(incident_id):
    if "employee_id" not in session:
        return jsonify({"success": False, "message": "Chưa đăng nhập"}), 401

    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "Không có quyền"}), 403

    ok = FileHelper.delete_item("incidents", incident_id)
    if not ok:
        return jsonify({"success": False, "message": "Không tìm thấy sự cố"}), 404

    return jsonify({"success": True, "message": "Đã xóa sự cố"})