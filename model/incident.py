# model/incident.py
# Model: Ghi nhận sự cố bảo mật

from datetime import datetime

class Incident:
    _id_counter = 1

    # Loại sự cố
    INCIDENT_TYPES = [
        "Phishing Attack",
        "Malware Infection",
        "Data Breach",
        "Unauthorized Access",
        "DDoS Attack",
        "System Outage",
        "Human Error",
        "Third-party Incident",
        "Physical Security",
        "Other"
    ]

    # Mức độ nghiêm trọng
    SEVERITY_LEVELS = [
        "Critical",    # Ảnh hưởng toàn công ty
        "High",        # Ảnh hưởng lớn
        "Medium",      # Ảnh hưởng vừa
        "Low"          # Ảnh hưởng nhỏ
    ]

    # Trạng thái xử lý
    INCIDENT_STATUS = [
        "Open",          # Mới phát hiện
        "Investigating", # Đang điều tra
        "Containing",    # Đang ngăn chặn
        "Resolved",      # Đã xử lý
        "Closed"         # Đã đóng
    ]

    def __init__(self, title: str, incident_type: str, severity: str,
                 description: str = "", affected_assets: list = None,
                 reported_by: str = "", assigned_to: str = ""):
        self.id = Incident._id_counter
        Incident._id_counter += 1

        self.title = title
        self.incident_type = incident_type
        self.severity = severity
        self.description = description
        self.affected_assets = affected_assets or []
        self.reported_by = reported_by
        self.assigned_to = assigned_to
        self.status = "Open"
        self.reported_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.resolved_date = None
        self.root_cause = ""
        self.lessons_learned = ""

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "incident_type": self.incident_type,
            "severity": self.severity,
            "description": self.description,
            "affected_assets": self.affected_assets,
            "reported_by": self.reported_by,
            "assigned_to": self.assigned_to,
            "status": self.status,
            "reported_date": self.reported_date,
            "resolved_date": self.resolved_date,
            "root_cause": self.root_cause,
            "lessons_learned": self.lessons_learned
        }

    @staticmethod
    def from_dict(data: dict) -> "Incident":
        incident = Incident.__new__(Incident)
        incident.id = data["id"]
        incident.title = data["title"]
        incident.incident_type = data["incident_type"]
        incident.severity = data["severity"]
        incident.description = data.get("description", "")
        incident.affected_assets = data.get("affected_assets", [])
        incident.reported_by = data.get("reported_by", "")
        incident.assigned_to = data.get("assigned_to", "")
        incident.status = data.get("status", "Open")
        incident.reported_date = data.get("reported_date", "")
        incident.resolved_date = data.get("resolved_date")
        incident.root_cause = data.get("root_cause", "")
        incident.lessons_learned = data.get("lessons_learned", "")
        return incident