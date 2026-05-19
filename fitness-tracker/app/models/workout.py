from app import db
from datetime import datetime, timedelta
from sqlalchemy import func
import json

class Workout(db.Model):
    __tablename__ = 'workouts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # strength, hiit, cardio, yoga
    duration = db.Column(db.Integer, nullable=False)  # in minutes
    difficulty = db.Column(db.String(20), nullable=False)  # beginner, intermediate, advanced
    description = db.Column(db.Text)
    calories_burned = db.Column(db.Integer, default=0)
    equipment_needed = db.Column(db.String(200))  # comma-separated list
    target_muscle_groups = db.Column(db.String(200))  # comma-separated list
    is_template = db.Column(db.Boolean, default=False)  # for saving workout templates
    is_public = db.Column(db.Boolean, default=False)  # for sharing workouts
    likes = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)
    rating_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    
    # Relationships
    user = db.relationship('User', back_populates='workouts')
    exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')
    sessions = db.relationship('WorkoutSession', back_populates='workout', cascade='all, delete-orphan')
    
    def get_equipment_list(self):
        return [e.strip() for e in self.equipment_needed.split(',')] if self.equipment_needed else []
    
    def get_muscle_groups(self):
        return [m.strip() for m in self.target_muscle_groups.split(',')] if self.target_muscle_groups else []
    
    def update_rating(self, new_rating):
        total_rating = (self.rating * self.rating_count) + new_rating
        self.rating_count += 1
        self.rating = total_rating / self.rating_count
        db.session.commit()
    
    @staticmethod
    def get_workouts_this_week(user_id):
        """Get the number of workouts completed this week."""
        start_of_week = datetime.utcnow() - timedelta(days=datetime.utcnow().weekday())
        return WorkoutSession.query.filter(
            WorkoutSession.user_id == user_id,
            WorkoutSession.completed_at >= start_of_week
        ).count()
    
    @staticmethod
    def compare_workouts(user_id):
        """Compare workouts this week with last week."""
        now = datetime.utcnow()
        start_of_week = now - timedelta(days=now.weekday())
        start_of_last_week = start_of_week - timedelta(days=7)
        
        this_week = WorkoutSession.query.filter(
            WorkoutSession.user_id == user_id,
            WorkoutSession.completed_at >= start_of_week
        ).count()
        
        last_week = WorkoutSession.query.filter(
            WorkoutSession.user_id == user_id,
            WorkoutSession.completed_at >= start_of_last_week,
            WorkoutSession.completed_at < start_of_week
        ).count()
        
        return this_week - last_week
    
    @staticmethod
    def get_total_time(user_id):
        """Get total workout time in hours for the current month."""
        start_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        total_minutes = db.session.query(func.sum(WorkoutSession.duration)).filter(
            WorkoutSession.user_id == user_id,
            WorkoutSession.completed_at >= start_of_month
        ).scalar() or 0
        
        return round(total_minutes / 60, 1)  # Convert to hours
    
    @staticmethod
    def get_calories_burned(user_id):
        """Get total calories burned for the current month."""
        start_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return db.session.query(func.sum(Workout.calories_burned)).filter(
            Workout.user_id == user_id,
            Workout.timestamp >= start_of_month
        ).scalar() or 0

    @staticmethod
    def get_workouts_increase(user_id):
        """Calculate the percentage increase in workouts between current and previous weeks."""
        now = datetime.utcnow()
        current_week_start = now - timedelta(days=now.weekday())
        current_week_end = current_week_start + timedelta(days=7)
        previous_week_start = current_week_start - timedelta(days=7)
        previous_week_end = current_week_start
        
        # Get workout counts from completed sessions
        current_week_count = WorkoutSession.query.filter(
            WorkoutSession.user_id == user_id,
            WorkoutSession.completed_at >= current_week_start,
            WorkoutSession.completed_at < current_week_end
        ).count()
        
        previous_week_count = WorkoutSession.query.filter(
            WorkoutSession.user_id == user_id,
            WorkoutSession.completed_at >= previous_week_start,
            WorkoutSession.completed_at < previous_week_end
        ).count()
        
        # Calculate percentage increase
        if previous_week_count == 0:
            return 100 if current_week_count > 0 else 0
        return ((current_week_count - previous_week_count) / previous_week_count) * 100

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'duration': self.duration,
            'difficulty': self.difficulty,
            'description': self.description,
            'calories_burned': self.calories_burned,
            'equipment_needed': self.get_equipment_list(),
            'target_muscle_groups': self.get_muscle_groups(),
            'is_template': self.is_template,
            'is_public': self.is_public,
            'likes': self.likes,
            'views': self.views,
            'rating': self.rating,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'notes': self.notes
        }

class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    duration = db.Column(db.Integer)  # in seconds
    rest_duration = db.Column(db.Integer)  # in seconds
    video_url = db.Column(db.String(200))
    form_tips = db.Column(db.Text)
    muscle_groups = db.Column(db.String(200))  # comma-separated list
    equipment = db.Column(db.String(200))  # comma-separated list
    difficulty = db.Column(db.String(20))  # beginner, intermediate, advanced
    calories_per_minute = db.Column(db.Float)  # estimated calories burned per minute
    is_public = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise')
    
    def get_muscle_groups(self):
        return [m.strip() for m in self.muscle_groups.split(',')] if self.muscle_groups else []
    
    def get_equipment(self):
        return [e.strip() for e in self.equipment.split(',')] if self.equipment else []
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'duration': self.duration,
            'rest_duration': self.rest_duration,
            'video_url': self.video_url,
            'form_tips': self.form_tips,
            'muscle_groups': self.get_muscle_groups(),
            'equipment': self.get_equipment(),
            'difficulty': self.difficulty,
            'calories_per_minute': self.calories_per_minute,
            'is_public': self.is_public,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    duration = db.Column(db.Integer)  # in seconds
    rest_duration = db.Column(db.Integer)  # in seconds
    weight = db.Column(db.Float)  # in kg
    notes = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)
    
    # Relationships
    workout = db.relationship('Workout', back_populates='exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')
    
    def to_dict(self):
        return {
            'id': self.id,
            'workout_id': self.workout_id,
            'exercise_id': self.exercise_id,
            'order': self.order,
            'sets': self.sets,
            'reps': self.reps,
            'duration': self.duration,
            'rest_duration': self.rest_duration,
            'weight': self.weight,
            'notes': self.notes,
            'completed': self.completed,
            'exercise': self.exercise.to_dict() if self.exercise else None
        }

class WorkoutSession(db.Model):
    __tablename__ = 'workout_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    started_at = db.Column(db.DateTime, nullable=False)
    completed_at = db.Column(db.DateTime)
    duration = db.Column(db.Integer)  # in minutes
    calories_burned = db.Column(db.Integer)
    notes = db.Column(db.Text)
    rating = db.Column(db.Integer)  # 1-5 stars
    feedback = db.Column(db.Text)
    mood = db.Column(db.String(20))  # great, good, okay, bad
    energy_level = db.Column(db.Integer)  # 1-10
    difficulty_rating = db.Column(db.Integer)  # 1-10
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='workout_sessions')
    workout = db.relationship('Workout', back_populates='sessions')
    
    def complete_session(self, duration=None, calories_burned=None):
        self.completed_at = datetime.utcnow()
        if duration:
            self.duration = duration
        if calories_burned:
            self.calories_burned = calories_burned
        db.session.commit()
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'workout_id': self.workout_id,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'duration': self.duration,
            'calories_burned': self.calories_burned,
            'notes': self.notes,
            'rating': self.rating,
            'feedback': self.feedback,
            'mood': self.mood,
            'energy_level': self.energy_level,
            'difficulty_rating': self.difficulty_rating,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'workout': self.workout.to_dict() if self.workout else None
        }
