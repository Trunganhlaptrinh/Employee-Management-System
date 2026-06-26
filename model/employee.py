# model/employee.py
class Employee:
    def __init__(self, id=None, username=None, password=None, 
                 name=None, position=None, department=None, 
                 base_salary=0):
        self.id = id
        self.username = username
        self.password = password  # Trong thực tế nên hash password
        self.name = name
        self.position = position
        self.department = department
        self.base_salary = base_salary

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'position': self.position,
            'department': self.department,
            'base_salary': self.base_salary
        }