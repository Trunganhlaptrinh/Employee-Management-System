# app.py
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from controller.employee_controller import EmployeeController
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Nên đổi thành secret key riêng

controller = EmployeeController()

# === ROUTES ===

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        success, message = controller.login(username, password)
        if success:
            user = controller.get_current_user()
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['name'] = user['name']
            session['position'] = user['position']
            session['department'] = user['department']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error=message)
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    controller.logout()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    today = datetime.now().strftime('%Y-%m-%d')
    month = datetime.now().strftime('%Y-%m')
    
    # Get today's attendance
    attendance = controller.get_today_attendance(user_id)
    
    # Get attendance history for this month
    attendances = controller.get_attendance_history(user_id, month)
    work_days = sum(1 for a in attendances if a[5] == 'present')
    total_days = len(attendances)
    
    # Get leaves
    leaves = controller.get_my_leaves(user_id)
    approved_leaves = sum(1 for l in leaves if l[5] == 'approved')
    pending_leaves = sum(1 for l in leaves if l[5] == 'pending')
    
    # Get salary
    salary_data = None
    salary = controller.db.get_salary_history(user_id)
    if salary:
        latest = salary[0]
        salary_data = f"{latest[6]:,.0f}"  # total column
    
    return render_template('dashboard.html',
                         user=session,
                         today=today,
                         attendance=attendance,
                         work_days=work_days,
                         total_days=total_days or 1,
                         approved_leaves=approved_leaves,
                         pending_leaves=pending_leaves,
                         salary=salary_data)

@app.route('/attendance')
def attendance():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    month = request.args.get('month', datetime.now().strftime('%Y-%m'))
    
    attendances = controller.get_attendance_history(user_id, month)
    
    return render_template('attendance.html',
                         attendances=attendances,
                         month=month)

@app.route('/attendance/check-in', methods=['POST'])
def check_in():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    success, message = controller.check_in(session['user_id'])
    if success:
        return render_template('attendance.html',
                             attendances=controller.get_attendance_history(session['user_id']),
                             month=datetime.now().strftime('%Y-%m'),
                             success=message)
    else:
        return render_template('attendance.html',
                             attendances=controller.get_attendance_history(session['user_id']),
                             month=datetime.now().strftime('%Y-%m'),
                             error=message)

@app.route('/attendance/check-out', methods=['POST'])
def check_out():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    success, message = controller.check_out(session['user_id'])
    return render_template('attendance.html',
                         attendances=controller.get_attendance_history(session['user_id']),
                         month=datetime.now().strftime('%Y-%m'),
                         success=message)

@app.route('/leave')
def leave():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    leaves = controller.get_my_leaves(session['user_id'])
    return render_template('leave.html', leaves=leaves)

@app.route('/leave/request', methods=['POST'])
def request_leave():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    from_date = request.form.get('from_date')
    to_date = request.form.get('to_date')
    reason = request.form.get('reason')
    
    success, message = controller.request_leave(session['user_id'], from_date, to_date, reason)
    leaves = controller.get_my_leaves(session['user_id'])
    
    if success:
        return render_template('leave.html', leaves=leaves, success=message)
    else:
        return render_template('leave.html', leaves=leaves, error=message)

@app.route('/salary')
def salary():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    month = request.args.get('month', datetime.now().strftime('%Y-%m'))
    
    # Get salary data
    salary_rows = controller.db.get_salary_history(user_id)
    salary_data = None
    
    # Find salary for current month
    for row in salary_rows:
        if row[2] == month:
            salary_data = {
                'base_salary': row[3],
                'bonus': row[4],
                'deduction': row[5],
                'total': row[6],
                'work_days': 0,  # Will be calculated
                'leave_days': 0
            }
            break
    
    if salary_data:
        # Get work days
        attendances = controller.get_attendance_history(user_id, month)
        salary_data['work_days'] = sum(1 for a in attendances if a[5] == 'present')
        leaves = controller.get_my_leaves(user_id)
        salary_data['leave_days'] = sum(1 for l in leaves if l[5] == 'approved' and l[2].startswith(month))
    
    return render_template('salary.html',
                         month=month,
                         salary=salary_data,
                         history=salary_rows)

@app.route('/salary/calculate', methods=['POST'])
def calculate_salary():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    month = request.form.get('month', datetime.now().strftime('%Y-%m'))
    success, result = controller.calculate_salary(session['user_id'], month)
    
    if success:
        return redirect(url_for('salary', month=month))
    else:
        return render_template('salary.html',
                             month=month,
                             error=result,
                             history=controller.db.get_salary_history(session['user_id']))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)