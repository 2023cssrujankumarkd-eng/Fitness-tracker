from app import db
from datetime import datetime

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)  # Add name field
    type = db.Column(db.String(20), nullable=False)  # weight_loss, muscle_gain, endurance
    target_value = db.Column(db.Float, nullable=False)
    current_value = db.Column(db.Float, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)

    user = db.relationship('User', back_populates='goals')

    def __init__(self, **kwargs):
        super(Goal, self).__init__(**kwargs)
        # Validate name
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError('Goal name is required')
        
        # Validate goal type
        valid_types = ['weight_loss', 'muscle_gain', 'endurance']
        if self.type not in valid_types:
            raise ValueError(f'Invalid goal type. Must be one of: {", ".join(valid_types)}')
        
        # Validate values
        if self.target_value <= 0 or self.current_value <= 0:
            raise ValueError('Target and current values must be positive numbers')
        
        # Validate deadline
        if self.deadline < datetime.utcnow():
            raise ValueError('Deadline must be a future date')

    @property
    def progress(self):
        if self.type == 'weight_loss':
            # For weight loss, progress is based on how much weight has been lost
            total_to_lose = self.current_value - self.target_value
            if total_to_lose <= 0:
                return 0
            current_lost = self.current_value - self.target_value
            return min(100, max(0, (current_lost / total_to_lose * 100)))
        else:
            # For other goals, progress is based on current value relative to target
            if self.target_value <= 0:
                return 0
            return min(100, max(0, (self.current_value / self.target_value * 100)))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'target_value': self.target_value,
            'current_value': self.current_value,
            'deadline': self.deadline.isoformat(),
            'created_at': self.created_at.isoformat(),
            'progress': self.progress
        }

    @staticmethod
    def get_overall_progress(user_id):
        goals = Goal.query.filter_by(user_id=user_id).all()
        if not goals:
            return 0
        
        total_progress = 0
        for goal in goals:
            progress = (goal.current_value / goal.target_value) * 100
            total_progress += min(progress, 100)  # Cap at 100%
        
        return round(total_progress / len(goals))