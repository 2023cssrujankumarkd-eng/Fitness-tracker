import os
from dotenv import load_dotenv
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

class Config:
    # Basic Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f"sqlite:///{os.path.join(basedir, 'fitness_tracker.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security settings
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() in ('true', '1', 'yes')
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Mail settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', True)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/static/uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Admin settings
    ADMIN_USERNAME = 'admin'
    ADMIN_EMAIL = 'admin@example.com'
    
    # API settings
    API_RATE_LIMIT = '100 per minute'
    API_RATE_LIMIT_STORAGE_URL = 'memory://'
    
    # Socket.IO settings
    SOCKETIO_MESSAGE_QUEUE = os.environ.get('SOCKETIO_MESSAGE_QUEUE', 'redis://')
    
    # Logging settings
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    # Feature flags
    ENABLE_EMAIL_VERIFICATION = True
    ENABLE_SOCIAL_LOGIN = False
    ENABLE_WORKOUT_SHARING = True
    ENABLE_WORKOUT_TEMPLATES = True
    ENABLE_EXERCISE_LIBRARY = True
    ENABLE_PROGRESS_TRACKING = True
    ENABLE_GOAL_SETTING = True
    ENABLE_NUTRITION_TRACKING = True
    ENABLE_CONSULTATIONS = True