# controller/risk_controller.py
# Controller: Quản lý đánh giá rủi ro

from flask import Blueprint, request, jsonify, session
from model.risk import Risk
from util.file_helper import FileHelper
from util.validation import Validation

risk_bp = Blueprint("risk", __name__)

# ========================
# LẤY DANH SÁCH RỦI RO
# GET /api/risks
# ========================
@risk_bp.route("", methods=["GET"])
def get_risks():
    if "employee_id" not in session:
        return jsonify({"success": False, "message": "Chưa đăng nhập"}), 401

    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "Không có quyền"}), 403

    risks = FileHelper.read_all("risks")
    
    # Lọc theo asset_id nếu có
    asset_id = request.args.get("asset_id")
    if asset_id:
        risks = [r for r in risks if r["asset_id"] == int(asset_id)]

    return jsonify({"success": True, "data": risks})

# ========================
# THÊM RỦI RO MỚI
# POST /api/risks
# ========================
@risk_bp.route("", methods=["POST"])
def add_risk():
    if "employee_id" not in session:
        return jsonify({"success": False, "message": "Chưa đăng nhập"}), 401

    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "Không có quyền"}), 403

    data = request.get_json()
    try:
        name = Validation.check_not_empty(data.get("name", ""), "Tên rủi ro")
        category = Validation.check_in_list(data.get("category", ""),
                                            Risk.RISK_CATEGORIES, "Loại rủi ro")
        asset_id = int(data.get("asset_id", 0))
        impact = Validation.check_in_list(data.get("impact", ""),
                                          list(Risk.IMPACT_LEVELS.keys()), "Mức độ tác động")
        probability = Validation.check_in_list(data.get("probability", ""),
                                               list(Risk.PROBABILITY_LEVELS.keys()), "Xác suất")
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400

    # Kiểm tra asset tồn tại
    assets = FileHelper.read_all("assets")
    if not any(a["id"] == asset_id for a in assets):
        return jsonify({"success": False, "message": "Tài sản không tồn tại"}), 404

    risk = Risk(
        name=name,
        category=category,
        asset_id=asset_id,
        impact=impact,
        probability=probability,
        description=data.get("description", ""),
        mitigation=data.get("mitigation", ""),
        owner=data.get("owner", "")
    )

    FileHelper.append_item("risks", risk.to_dict())
    return jsonify({"success": True, "message": "Thêm rủi ro thành công", "id": risk.id}), 201

# ========================
# CẬP NHẬT RỦI RO
# PUT /api/risks/<id>
# ========================
@risk_bp.route("/<int:risk_id>", methods=["PUT"])
def update_risk(risk_id):
    if "employee_id" not in session:
        return jsonify({"success": False, "message": "Chưa đăng nhập"}), 401

    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "Không có quyền"}), 403

    data = request.get_json()
    try:
        name = Validation.check_not_empty(data.get("name", ""), "Tên rủi ro")
        category = Validation.check_in_list(data.get("category", ""),
                                            Risk.RISK_CATEGORIES, "Loại rủi ro")
        impact = Validation.check_in_list(data.get("impact", ""),
                                          list(Risk.IMPACT_LEVELS.keys()), "Mức độ tác động")
        probability = Validation.check_in_list(data.get("probability", ""),
                                               list(Risk.PROBABILITY_LEVELS.keys()), "Xác suất")
        status = Validation.check_in_list(data.get("status", ""),
                                          Risk.RISK_STATUS, "Trạng thái")
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400

    risks = FileHelper.read_all("risks")
    for i, r in enumerate(risks):
        if r["id"] == risk_id:
            risks[i]["name"] = name
            risks[i]["category"] = category
            risks[i]["impact"] = impact
            risks[i]["probability"] = probability
            risks[i]["description"] = data.get("description", "")
            risks[i]["mitigation"] = data.get("mitigation", "")
            risks[i]["owner"] = data.get("owner", "")
            risks[i]["status"] = status
            
            # Cập nhật risk_score và risk_level
            temp_risk = Risk.from_dict(risks[i])
            risks[i]["risk_score"] = temp_risk.get_risk_score()
            risks[i]["risk_level"] = temp_risk.get_risk_level()
            
            FileHelper.write_all("risks", risks)
            return jsonify({"success": True, "message": "Cập nhật thành công"})

    return jsonify({"success": False, "message": "Không tìm thấy rủi ro"}), 404

# ========================
# XÓA RỦI RO
# DELETE /api/risks/<id>
# ========================
@risk_bp.route("/<int:risk_id>", methods=["DELETE"])
def delete_risk(risk_id):
    if "employee_id" not in session:
        return jsonify({"success": False, "message": "Chưa đăng nhập"}), 401

    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "Không có quyền"}), 403

    ok = FileHelper.delete_item("risks", risk_id)
    if not ok:
        return jsonify({"success": False, "message": "Không tìm thấy rủi ro"}), 404

    return jsonify({"success": True, "message": "Đã xóa rủi ro"})

# ========================
# LẤY THỐNG KÊ RỦI RO
# GET /api/risks/stats
# ========================
@risk_bp.route("/stats", methods=["GET"])
def get_risk_stats():
    if "employee_id" not in session:
        return jsonify({"success": False, "message": "Chưa đăng nhập"}), 401

    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "Không có quyền"}), 403

    risks = FileHelper.read_all("risks")
    
    stats = {
        "total": len(risks),
        "by_level": {
            "Critical": sum(1 for r in risks if r.get("risk_level") == "Critical"),
            "High": sum(1 for r in risks if r.get("risk_level") == "High"),
            "Medium": sum(1 for r in risks if r.get("risk_level") == "Medium"),
            "Low": sum(1 for r in risks if r.get("risk_level") == "Low")
        },
        "by_status": {
            status: sum(1 for r in risks if r.get("status") == status)
            for status in Risk.RISK_STATUS
        },
        "by_category": {}
    }
    
    # Thống kê theo category
    for risk in risks:
        cat = risk.get("category", "Other")
        stats["by_category"][cat] = stats["by_category"].get(cat, 0) + 1

    return jsonify({"success": True, "data": stats})