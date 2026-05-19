from app import db
from datetime import datetime

class Consultation(db.Model):
    __tablename__ = 'consultations'  # This matches the relationship in Physician model
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    physician_id = db.Column(db.Integer, db.ForeignKey('physicians.id'), nullable=False)
    notes = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, completed, cancelled
    scheduled_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    feedback = db.Column(db.Text)
    rating = db.Column(db.Integer)  # 1-5 stars
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='consultations')
    physician = db.relationship('Physician', back_populates='consultations')
    
    def __repr__(self):
        return f'<Consultation {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'physician_id': self.physician_id,
            'notes': self.notes,
            'status': self.status,
            'scheduled_at': self.scheduled_at.isoformat() if self.scheduled_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'feedback': self.feedback,
            'rating': self.rating,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'physician': self.physician.to_dict() if self.physician else None
        }