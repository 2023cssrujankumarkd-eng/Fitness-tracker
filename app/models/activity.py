from app import db
from datetime import datetime, timedelta

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # in minutes
    calories = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.Text)

    user = db.relationship('User', back_populates='activities')

    @staticmethod
    def get_calories_burned_today(user_id):
        today = datetime.utcnow().date()
        activities = Activity.query.filter(
            Activity.user_id == user_id,
            db.func.date(Activity.timestamp) == today
        ).all()
        return sum(activity.calories for activity in activities)

    @staticmethod
    def get_calories_increase(user_id):
        today = datetime.utcnow().date()
        yesterday = today - timedelta(days=1)
        
        today_calories = Activity.get_calories_burned_today(user_id)
        yesterday_calories = sum(
            activity.calories for activity in Activity.query.filter(
                Activity.user_id == user_id,
                db.func.date(Activity.timestamp) == yesterday
            ).all()
        )
        
        return today_calories - yesterday_calories

    @staticmethod
    def get_active_minutes_today(user_id):
        today = datetime.utcnow().date()
        activities = Activity.query.filter(
            Activity.user_id == user_id,
            db.func.date(Activity.timestamp) == today
        ).all()
        return sum(activity.duration for activity in activities)

    @staticmethod
    def get_minutes_increase(user_id):
        today = datetime.utcnow().date()
        yesterday = today - timedelta(days=1)
        
        today_minutes = Activity.get_active_minutes_today(user_id)
        yesterday_minutes = sum(
            activity.duration for activity in Activity.query.filter(
                Activity.user_id == user_id,
                db.func.date(Activity.timestamp) == yesterday
            ).all()
        )
        
        return today_minutes - yesterday_minutes

    @staticmethod
    def get_recent_activities(user_id, limit=3):
        return Activity.query.filter_by(user_id=user_id)\
            .order_by(Activity.timestamp.desc())\
            .limit(limit)\
            .all()

    def __repr__(self):
        return f'<Activity {self.name}>'