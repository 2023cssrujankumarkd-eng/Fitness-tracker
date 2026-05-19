from flask import render_template, Blueprint, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.goal import Goal
from app.models.activity import Activity
from app.models.nutrition import NutritionLog
from app.models.workout import Workout
from datetime import datetime, timedelta

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@bp.route('/dashboard')
@login_required
def dashboard():
    # Get stats for the current user
    stats = {
        'workouts_this_week': Workout.get_workouts_this_week(current_user.id),
        'workouts_increase': Workout.get_workouts_increase(current_user.id),
        'calories_burned': Activity.get_calories_burned_today(current_user.id),
        'calories_increase': Activity.get_calories_increase(current_user.id),
        'active_minutes': Activity.get_active_minutes_today(current_user.id),
        'minutes_increase': Activity.get_minutes_increase(current_user.id),
        'goals_progress': Goal.get_overall_progress(current_user.id)
    }

    # Get recent activities
    recent_activities = Activity.get_recent_activities(current_user.id, limit=3)
    
    return render_template('dashboard.html',
                         stats=stats,
                         recent_activities=recent_activities)

@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        # Handle profile updates
        if request.form.get('username') != current_user.username:
            if User.query.filter_by(username=request.form['username']).first():
                flash('Username already exists', 'error')
                return redirect(url_for('main.settings'))
            current_user.username = request.form['username']
        
        if request.form.get('email') != current_user.email:
            if User.query.filter_by(email=request.form['email']).first():
                flash('Email already exists', 'error')
                return redirect(url_for('main.settings'))
            current_user.email = request.form['email']
        
        # Handle password change
        if request.form.get('current_password'):
            if not current_user.check_password(request.form['current_password']):
                flash('Current password is incorrect', 'error')
                return redirect(url_for('main.settings'))
            
            if request.form['new_password'] != request.form['confirm_password']:
                flash('New passwords do not match', 'error')
                return redirect(url_for('main.settings'))
            
            current_user.set_password(request.form['new_password'])
        
        db.session.commit()
        flash('Settings updated successfully', 'success')
        return redirect(url_for('main.settings'))
    
    return render_template('settings.html', title='Settings')
