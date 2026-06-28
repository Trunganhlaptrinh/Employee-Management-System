# controller/asset_controller.py
# Controller: Quản lý tài sản CNTT

from flask import Blueprint, request, jsonify, session
from model.asset import Asset
from util.file_helper import FileHelper
from util.validation import Validation

asset_bp = Blueprint("asset", __name__)

# ========================
# LẤY DANH SÁCH TÀI SẢN
# GET /api/assets
# ========================
@asset_bp.route("", methods=["GET"])
def get_assets():
    if "employee_id" not in session:
        return jsonify({"success": False, "message": "Chưa đăng nhập"}), 401

    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "Không có quyền"}), 403

    assets = FileHelper.read_all("assets")
    return jsonify({"success": True, "data": assets})

# ========================
# LẤY THÔNG TIN 1 TÀI SẢN
# GET /api/assets/<id>
# ========================
@asset_bp.route("/<int:asset_id>", methods=["GET"])
def get_asset(asset_id):
    if "employee_id" not in session:
        return jsonify({"success": False, "message": "Chưa đăng nhập"}), 401

    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "Không có quyền"}), 403

    assets = FileHelper.read_all("assets")
    asset = next((a for a in assets if a["id"] == asset_id), None)
    if not asset:
        return jsonify({"success": False, "message": "Không tìm thấy tài sản"}), 404

    return jsonify({"success": True, "data": asset})

# ========================
# THÊM TÀI SẢN MỚI
# POST /api/assets
# ========================
@asset_bp.route("", methods=["POST"])
def add_asset():
    if "employee_id" not in session:
        return jsonify({"success": False, "message": "Chưa đăng nhập"}), 401

    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "Không có quyền"}), 403

    data = request.get_json()
    try:
        name = Validation.check_not_empty(data.get("name", ""), "Tên tài sản")
        asset_type = Validation.check_in_list(data.get("asset_type", ""), 
                                              Asset.ASSET_TYPES, "Loại tài sản")
        criticality = Validation.check_in_list(data.get("criticality", ""),
                                                Asset.CRITICALITY_LEVELS, "Mức độ quan trọng")
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400

    asset = Asset(
        name=name,
        asset_type=asset_type,
        criticality=criticality,
        description=data.get("description", ""),
        owner=data.get("owner", ""),
        location=data.get("location", "")
    )

    FileHelper.append_item("assets", asset.to_dict())
    return jsonify({"success": True, "message": "Thêm tài sản thành công", "id": asset.id}), 201

# ========================
# CẬP NHẬT TÀI SẢN
# PUT /api/assets/<id>
# ========================
@asset_bp.route("/<int:asset_id>", methods=["PUT"])
def update_asset(asset_id):
    if "employee_id" not in session:
        return jsonify({"success": False, "message": "Chưa đăng nhập"}), 401

    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "Không có quyền"}), 403

    data = request.get_json()
    try:
        name = Validation.check_not_empty(data.get("name", ""), "Tên tài sản")
        asset_type = Validation.check_in_list(data.get("asset_type", ""),
                                              Asset.ASSET_TYPES, "Loại tài sản")
        criticality = Validation.check_in_list(data.get("criticality", ""),
                                                Asset.CRITICALITY_LEVELS, "Mức độ quan trọng")
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400

    assets = FileHelper.read_all("assets")
    for i, a in enumerate(assets):
        if a["id"] == asset_id:
            assets[i]["name"] = name
            assets[i]["asset_type"] = asset_type
            assets[i]["criticality"] = criticality
            assets[i]["description"] = data.get("description", "")
            assets[i]["owner"] = data.get("owner", "")
            assets[i]["location"] = data.get("location", "")
            FileHelper.write_all("assets", assets)
            return jsonify({"success": True, "message": "Cập nhật thành công"})

    return jsonify({"success": False, "message": "Không tìm thấy tài sản"}), 404

# ========================
# XÓA TÀI SẢN
# DELETE /api/assets/<id>
# ========================
@asset_bp.route("/<int:asset_id>", methods=["DELETE"])
def delete_asset(asset_id):
    if "employee_id" not in session:
        return jsonify({"success": False, "message": "Chưa đăng nhập"}), 401

    if session.get("role") != "admin":
        return jsonify({"success": False, "message": "Không có quyền"}), 403

    ok = FileHelper.delete_item("assets", asset_id)
    if not ok:
        return jsonify({"success": False, "message": "Không tìm thấy tài sản"}), 404

    return jsonify({"success": True, "message": "Đã xóa tài sản"})