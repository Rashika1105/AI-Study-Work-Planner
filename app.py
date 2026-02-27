from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from config import Config
import os

# ML Utilities
from utils.predictor import Predictor
from utils.burnout_detector import BurnoutDetector
from utils.suggestions import SuggestionEngine

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    tasks = db.relationship('Task', backref='owner', lazy=True)
    performances = db.relationship('Performance', backref='owner', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(20), nullable=False) # Study or Work
    hours_spent = db.Column(db.Float, default=0.0)
    deadline = db.Column(db.DateTime, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Performance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    predicted_score = db.Column(db.Float)
    burnout_level = db.Column(db.String(20)) # Low, Medium, High
    date_generated = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('auth_login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'warning')
        else:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
    return render_template('auth_register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    predictor = Predictor()
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    
    # Calculate stats for ML
    total_hours = sum(t.hours_spent for t in tasks)
    completed_tasks = sum(1 for t in tasks if t.completed)
    total_tasks = len(tasks)
    missed_deadlines = sum(1 for t in tasks if not t.completed and t.deadline < datetime.utcnow())
    
    avg_daily_hours = total_hours / 7 if total_tasks > 0 else 0
    consistency = (completed_tasks / total_tasks) if total_tasks > 0 else 0
    
    # ML Prediction
    pred_score, confidence = predictor.predict(avg_daily_hours, completed_tasks, missed_deadlines, consistency, 7.5)
    
    # Burnout Check
    burnout_risk, burnout_msg = BurnoutDetector.detect(avg_daily_hours, 7.5, consistency, 5)
    
    # Suggestions
    suggestions = SuggestionEngine.get_suggestions(consistency, avg_daily_hours, (missed_deadlines/total_tasks if total_tasks > 0 else 0), burnout_risk)
    
    return render_template('dashboard.html', 
                          active_page='dashboard',
                          tasks_count=total_tasks,
                          completed_count=completed_tasks,
                          pred_score=pred_score,
                          confidence=confidence,
                          burnout_risk=burnout_risk,
                          burnout_msg=burnout_msg,
                          suggestions=suggestions)

@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        deadline_str = request.form.get('deadline')
        hours = float(request.form.get('hours', 0))
        
        deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
        new_task = Task(user_id=current_user.id, title=title, category=category, deadline=deadline, hours_spent=hours)
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!', 'success')
        
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.deadline.asc()).all()
    return render_template('tasks.html', active_page='tasks', tasks=tasks)

@app.route('/tasks/complete/<int:task_id>')
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id == current_user.id:
        task.completed = True
        db.session.commit()
    return redirect(url_for('tasks'))

@app.route('/analytics')
@login_required
def analytics():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    
    total_tasks = len(tasks)
    completed_tasks = sum(1 for t in tasks if t.completed)
    
    avg_hours = round(sum(t.hours_spent for t in tasks) / total_tasks, 1) if total_tasks > 0 else 0
    completion_rate = round((completed_tasks / total_tasks) * 100, 1) if total_tasks > 0 else 0
    deadlines_met = sum(1 for t in tasks if t.completed and t.deadline >= datetime.utcnow()) # Simple approximation for met deadlines
    
    return render_template('analytics.html', 
                          active_page='analytics',
                          avg_hours=avg_hours,
                          completion_rate=completion_rate,
                          deadlines_met=deadlines_met)

@app.route('/download_report')
@login_required
def download_report():
    from utils.report_generator import ReportGenerator
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    
    # Calculate stats for the report
    total_hours = sum(t.hours_spent for t in tasks)
    completed_tasks = sum(1 for t in tasks if t.completed)
    total_tasks = len(tasks)
    missed_deadlines = sum(1 for t in tasks if not t.completed and t.deadline < datetime.utcnow())
    
    avg_daily_hours = total_hours / 7 if total_tasks > 0 else 0
    consistency = (completed_tasks / total_tasks) if total_tasks > 0 else 0
    
    predictor = Predictor()
    pred_score, _ = predictor.predict(avg_daily_hours, completed_tasks, missed_deadlines, consistency, 7.5)
    burnout_risk, _ = BurnoutDetector.detect(avg_daily_hours, 7.5, consistency, 5)
    suggestions = SuggestionEngine.get_suggestions(consistency, avg_daily_hours, (missed_deadlines/total_tasks if total_tasks > 0 else 0), burnout_risk)
    
    filename = ReportGenerator.generate_pdf(current_user, tasks, pred_score, burnout_risk, suggestions)
    from flask import send_from_directory
    return send_from_directory(os.path.join(app.root_path, 'static', 'reports'), filename)

if __name__ == '__main__':
    with app.app_context():
        # Ensure database directory exists
        db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database')
        if not os.path.exists(db_path):
            os.makedirs(db_path)
        db.create_all()
    app.run(debug=True)
