# model/risk.py
# Model: Đánh giá rủi ro bảo mật

class Risk:
    _id_counter = 1

    # Các loại rủi ro
    RISK_CATEGORIES = [
        "Cybersecurity",
        "Data Breach",
        "System Failure",
        "Human Error",
        "Natural Disaster",
        "Third-party Risk",
        "Compliance",
        "Financial Fraud"
    ]

    # Mức độ tác động (Impact)
    IMPACT_LEVELS = {
        "Very High": 5,
        "High": 4,
        "Medium": 3,
        "Low": 2,
        "Very Low": 1
    }

    # Mức độ xác suất (Probability)
    PROBABILITY_LEVELS = {
        "Almost Certain": 5,
        "Likely": 4,
        "Possible": 3,
        "Unlikely": 2,
        "Rare": 1
    }

    # Trạng thái xử lý
    RISK_STATUS = [
        "Identified",   # Đã xác định
        "Analyzed",     # Đã phân tích
        "Mitigating",   # Đang xử lý
        "Mitigated",    # Đã xử lý
        "Accepted",     # Chấp nhận rủi ro
        "Transferred"   # Chuyển giao rủi ro
    ]

    def __init__(self, name: str, category: str, asset_id: int,
                 impact: str, probability: str, description: str = "",
                 mitigation: str = "", owner: str = ""):
        self.id = Risk._id_counter
        Risk._id_counter += 1

        self.name = name
        self.category = category
        self.asset_id = asset_id  # Liên kết với Asset
        self.impact = impact      # Very High, High, Medium, Low, Very Low
        self.probability = probability  # Almost Certain, Likely, Possible, Unlikely, Rare
        self.description = description
        self.mitigation = mitigation
        self.owner = owner
        self.status = "Identified"
        self.created_date = None  # Sẽ set khi lưu

    def get_risk_score(self) -> int:
        """Tính điểm rủi ro = Impact * Probability"""
        impact_score = self.IMPACT_LEVELS.get(self.impact, 1)
        prob_score = self.PROBABILITY_LEVELS.get(self.probability, 1)
        return impact_score * prob_score

    def get_risk_level(self) -> str:
        """Xác định mức độ rủi ro dựa trên điểm số"""
        score = self.get_risk_score()
        if score >= 20:
            return "Critical"
        elif score >= 12:
            return "High"
        elif score >= 6:
            return "Medium"
        else:
            return "Low"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "asset_id": self.asset_id,
            "impact": self.impact,
            "probability": self.probability,
            "risk_score": self.get_risk_score(),
            "risk_level": self.get_risk_level(),
            "description": self.description,
            "mitigation": self.mitigation,
            "owner": self.owner,
            "status": self.status
        }

    @staticmethod
    def from_dict(data: dict) -> "Risk":
        risk = Risk.__new__(Risk)
        risk.id = data["id"]
        risk.name = data["name"]
        risk.category = data["category"]
        risk.asset_id = data["asset_id"]
        risk.impact = data["impact"]
        risk.probability = data["probability"]
        risk.description = data.get("description", "")
        risk.mitigation = data.get("mitigation", "")
        risk.owner = data.get("owner", "")
        risk.status = data.get("status", "Identified")
        return risk