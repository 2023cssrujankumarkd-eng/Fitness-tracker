from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from flask_wtf import CSRFProtect
from sqlalchemy import text
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_socketio import SocketIO
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()
bcrypt = Bcrypt()
flask_admin = Admin(name='Fitness Tracker Admin', template_mode='bootstrap4')
socketio = SocketIO()
cors = CORS()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    flask_admin.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    cors.init_app(app)
    
    # Configure logging
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/fitness_tracker.log',
                                         maxBytes=10240,
                                         backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Fitness Tracker startup')
    
    # Import models to ensure they are registered with SQLAlchemy
    from app.models.user import User
    from app.models.workout import Workout, Exercise, WorkoutExercise, WorkoutSession
    from app.models.activity import Activity
    from app.models.goal import Goal
    from app.models.nutrition import NutritionLog
    
    # Register blueprints
    from app.routes.auth import bp as auth_bp
    from app.routes.main import bp as main_bp
    from app.routes.activities import bp as activities_bp
    from app.routes.workout import bp as workout_bp
    from app.routes.nutrition import bp as nutrition_bp
    from app.routes.goals import bp as goals_bp
    from app.routes.consultations import bp as consultations_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(activities_bp)
    app.register_blueprint(workout_bp)
    app.register_blueprint(nutrition_bp)
    app.register_blueprint(goals_bp)
    app.register_blueprint(consultations_bp)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Create database tables
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Create admin user if it doesn't exist
        if not User.query.filter_by(username='admin').first():
            admin_user = User(
                username='admin',
                email='admin@example.com',
                is_admin=True,
                first_name='Admin',
                last_name='User',
                is_active=True,
                email_verified=True
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            
            # Create some default exercises
            exercises = [
                Exercise(
                    name='Push-ups',
                    description='A classic bodyweight exercise that targets the chest, shoulders, and triceps.',
                    duration=60,
                    rest_duration=30,
                    muscle_groups='chest,shoulders,triceps',
                    equipment='none',
                    difficulty='beginner',
                    calories_per_minute=8.0,
                    form_tips='Keep your body straight and lower your chest to the ground.'
                ),
                Exercise(
                    name='Squats',
                    description='A fundamental lower body exercise that targets the quadriceps, hamstrings, and glutes.',
                    duration=60,
                    rest_duration=45,
                    muscle_groups='quadriceps,hamstrings,glutes',
                    equipment='none',
                    difficulty='beginner',
                    calories_per_minute=7.0,
                    form_tips='Keep your back straight and knees aligned with your toes.'
                ),
                Exercise(
                    name='Plank',
                    description='An isometric core exercise that improves stability and posture.',
                    duration=45,
                    rest_duration=30,
                    muscle_groups='core,shoulders',
                    equipment='none',
                    difficulty='beginner',
                    calories_per_minute=4.0,
                    form_tips='Maintain a straight line from head to heels.'
                )
            ]
            db.session.add_all(exercises)
            db.session.commit()
    
    return app