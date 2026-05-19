from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app.models.goal import Goal
from app import db
from flask_wtf.csrf import CSRFProtect

bp = Blueprint('auth', __name__)
csrf = CSRFProtect()

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            data = request.form
            if User.query.filter_by(username=data['username']).first():
                flash('Username already exists')
                return redirect(url_for('auth.register'))
                
            if User.query.filter_by(email=data['email']).first():
                flash('Email already exists')
                return redirect(url_for('auth.register'))
            
            user = User(
                username=data['username'],
                email=data['email'],
            )
            user.set_password(data['password'])
            
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please login.')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error during registration: {str(e)}')
            return redirect(url_for('auth.register'))
    
    return render_template('register.html', title='Register')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            data = request.form
            user = User.query.filter_by(username=data['username']).first()
            
            if user and user.check_password(data['password']):
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('main.dashboard'))
            
            flash('Invalid username or password')
        except Exception as e:
            flash(f'Error during login: {str(e)}')
    
    return render_template('login.html', title='Login')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@bp.route('/add_goal', methods=['POST'])
@login_required
def add_goal():
    try:
        data = request.form
        user = current_user  # Assuming you have current_user from flask_login

        # Create a new goal
        goal = Goal(
            user_id=user.id,
            goal_type=data['goal_type'],
            target=data['target'],
            deadline=data['deadline']
        )

        db.session.add(goal)
        db.session.commit()

        flash('Goal added successfully!')
        return redirect(url_for('main.dashboard'))
    except Exception as e:
        db.session.rollback()  # Roll back the session in case of an error
        flash(f'Error adding goal: {str(e)}')
        return redirect(url_for('main.dashboard'))