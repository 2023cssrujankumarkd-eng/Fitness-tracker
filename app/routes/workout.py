from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from app.models.workout import Workout, Exercise, WorkoutSession
from app import db
from datetime import datetime

bp = Blueprint('workout', __name__)

@bp.route('/workout')
@login_required
def workout_index():
    return render_template('workout.html')

@bp.route('/api/workouts', methods=['POST'])
@login_required
def create_workout():
    try:
        data = request.get_json()
        
        # Create workout
        workout = Workout(
            user_id=current_user.id,
            name=data.get('name', 'Upper Body Strength'),
            type=data.get('type', 'strength'),
            duration=data.get('duration', 45),  # 45 minutes
            calories_burned=data.get('calories_burned', 0),
            notes=data.get('notes', '')
        )
        
        db.session.add(workout)
        db.session.flush()  # Get workout ID without committing
        
        # Create workout session
        session = WorkoutSession(
            user_id=current_user.id,
            workout_id=workout.id,
            started_at=datetime.utcnow()
        )
        
        db.session.add(session)
        db.session.commit()
        
        return jsonify({
            'message': 'Workout created successfully',
            'workout_id': workout.id,
            'session_id': session.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error creating workout: {str(e)}'}), 400

@bp.route('/api/workouts/<int:workout_id>/complete', methods=['POST'])
@login_required
def complete_workout(workout_id):
    try:
        session = WorkoutSession.query.filter_by(
            workout_id=workout_id,
            user_id=current_user.id,
            completed_at=None
        ).first_or_404()
        
        session.completed_at = datetime.utcnow()
        session.duration = int((session.completed_at - session.started_at).total_seconds())
        
        db.session.commit()
        return jsonify({'message': 'Workout completed successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error completing workout: {str(e)}'}), 400

@bp.route('/api/workouts')
@login_required
def get_workouts():
    workouts = Workout.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': w.id,
        'name': w.name,
        'type': w.type,
        'duration': w.duration,
        'calories_burned': w.calories_burned,
        'timestamp': w.timestamp.isoformat(),
        'notes': w.notes
    } for w in workouts])

@bp.route('/workout/timer')
@login_required
def workout_timer():
    return render_template('workout/timer.html')

@bp.route('/api/workouts/<int:workout_id>')
@login_required
def get_workout(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    return jsonify({
        'id': workout.id,
        'name': workout.name,
        'description': workout.description,
        'exercises': [{
            'id': e.id,
            'name': e.name,
            'duration': e.duration,
            'rest_duration': e.rest_duration,
            'video_url': e.video_url,
            'form_tips': e.form_tips
        } for e in workout.exercises]
    })
