# util/validation.py
import re
from datetime import datetime

class Validation:
    @staticmethod
    def is_empty(value):
        return not value or str(value).strip() == ''
    
    @staticmethod
    def validate_username(username):
        if Validation.is_empty(username):
            return False, "Username cannot be empty"
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        return True, ""
    
    @staticmethod
    def validate_password(password):
        if Validation.is_empty(password):
            return False, "Password cannot be empty"
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        return True, ""
    
    @staticmethod
    def validate_name(name):
        if Validation.is_empty(name):
            return False, "Name cannot be empty"
        if not re.match(r'^[A-Za-z\s]+$', name):
            return False, "Name must contain only letters and spaces"
        return True, ""
    
    @staticmethod
    def validate_date(date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True, ""
        except ValueError:
            return False, "Invalid date format (YYYY-MM-DD)"
    
    @staticmethod
    def validate_month(month_str):
        try:
            datetime.strptime(month_str, '%Y-%m')
            return True, ""
        except ValueError:
            return False, "Invalid month format (YYYY-MM)"
    
    @staticmethod
    def validate_position(position):
        valid_positions = ['Manager', 'Team Lead', 'Developer', 'Tester', 'Designer', 'HR']
        if position not in valid_positions:
            return False, f"Position must be one of: {', '.join(valid_positions)}"
        return True, ""