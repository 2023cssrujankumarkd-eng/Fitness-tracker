from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import jwt
from time import time
from flask import current_app

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    email_verified = db.Column(db.Boolean, default=False)
    profile_picture = db.Column(db.String(200))
    bio = db.Column(db.Text)
    height = db.Column(db.Float)  # in cm
    weight = db.Column(db.Float)  # in kg
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    fitness_level = db.Column(db.String(20))  # beginner, intermediate, advanced
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    last_seen = db.Column(db.DateTime)
    
    # Relationships
    workouts = db.relationship('Workout', back_populates='user')
    activities = db.relationship('Activity', back_populates='user')
    goals = db.relationship('Goal', back_populates='user')
    nutrition_logs = db.relationship('NutritionLog', back_populates='user')
    consultations = db.relationship('Consultation', back_populates='user')
    meal_plans = db.relationship('MealPlan', back_populates='user')
    workout_sessions = db.relationship('WorkoutSession', back_populates='user')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                          algorithms=['HS256'])['reset_password']
        except:
            return None
        return User.query.get(id)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.username

    def get_bmi(self):
        if self.height and self.weight:
            height_m = self.height / 100
            return round(self.weight / (height_m * height_m), 2)
        return None

    def get_age(self):
        if self.date_of_birth:
            today = datetime.utcnow().date()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None

    def update_last_seen(self):
        self.last_seen = datetime.utcnow()
        db.session.commit()

    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
