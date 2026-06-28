# model/asset.py
# Model: Quản lý tài sản CNTT của doanh nghiệp

class Asset:
    _id_counter = 1

    # Các loại tài sản
    ASSET_TYPES = [
        "Server",
        "Database",
        "Application",
        "Network Device",
        "Data Storage",
        "API Service",
        "Website",
        "Employee Device",
        "Cloud Service",
        "Other"
    ]

    # Mức độ quan trọng
    CRITICALITY_LEVELS = [
        "Critical",    # Rất quan trọng - ngừng hoạt động ảnh hưởng toàn công ty
        "High",        # Quan trọng - ảnh hưởng lớn đến hoạt động
        "Medium",      # Trung bình - ảnh hưởng vừa phải
        "Low"          # Thấp - ít ảnh hưởng
    ]

    def __init__(self, name: str, asset_type: str, criticality: str, 
                 description: str = "", owner: str = "", location: str = ""):
        self.id = Asset._id_counter
        Asset._id_counter += 1

        self.name = name
        self.asset_type = asset_type
        self.criticality = criticality
        self.description = description
        self.owner = owner
        self.location = location
        self.status = "active"  # active | inactive | retired

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "asset_type": self.asset_type,
            "criticality": self.criticality,
            "description": self.description,
            "owner": self.owner,
            "location": self.location,
            "status": self.status
        }

    @staticmethod
    def from_dict(data: dict) -> "Asset":
        asset = Asset.__new__(Asset)
        asset.id = data["id"]
        asset.name = data["name"]
        asset.asset_type = data["asset_type"]
        asset.criticality = data["criticality"]
        asset.description = data.get("description", "")
        asset.owner = data.get("owner", "")
        asset.location = data.get("location", "")
        asset.status = data.get("status", "active")
        return asset