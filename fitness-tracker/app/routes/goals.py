from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models.goal import Goal
from app import db
from datetime import datetime
from flask_wtf.csrf import CSRFProtect

bp = Blueprint('goals', __name__, url_prefix='/goals')
csrf = CSRFProtect()

@bp.route('/')
@login_required
def goal_index():
    goals = Goal.query.filter_by(user_id=current_user.id).all()
    completed_goals = sum(1 for goal in goals if goal.progress >= 100)
    success_rate = round((completed_goals / len(goals) * 100) if goals else 0)
    return render_template('goals/index.html', 
                         goals=goals,
                         completed_goals=completed_goals,
                         success_rate=success_rate,
                         now=datetime.utcnow())

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_goal():
    if request.method == 'POST':
        goal = Goal(
            user_id=current_user.id,
            name=request.form['name'],
            type=request.form['type'],
            target_value=float(request.form['target_value']),
            current_value=float(request.form['current_value']),
            deadline=datetime.strptime(request.form['deadline'], '%Y-%m-%d')
        )
        db.session.add(goal)
        db.session.commit()
        flash('Goal created successfully!', 'success')
        return redirect(url_for('goals.goal_index'))
    return render_template('goals/create.html')

@bp.route('/<int:goal_id>')
@login_required
def goal_detail(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if goal.user_id != current_user.id:
        flash('You do not have permission to view this goal.', 'error')
        return redirect(url_for('goals.goal_index'))
    return render_template('goals/detail.html', goal=goal)

@bp.route('/api/goals', methods=['GET'])
@login_required
def get_goals():
    try:
        goals = Goal.query.filter_by(user_id=current_user.id).all()
        return jsonify([goal.to_dict() for goal in goals])
    except Exception as e:
        print("Error fetching goals:", str(e))
        return jsonify({'message': 'Error fetching goals'}), 500

@bp.route('/api/goals', methods=['POST'])
@login_required
def add_goal():
    try:
        print("=== Starting goal creation ===")
        print("Request method:", request.method)
        print("Request headers:", dict(request.headers))
        print("Request data:", request.get_data())
        
        data = request.get_json()
        print("Parsed JSON data:", data)
        
        # Validate required fields
        required_fields = ['name', 'type', 'target_value', 'current_value', 'deadline']
        for field in required_fields:
            if field not in data:
                print(f"Missing required field: {field}")
                return jsonify({'message': f'Missing required field: {field}'}), 400
        
        # Validate name
        if not data['name'] or len(data['name'].strip()) == 0:
            print("Invalid name: name is required")
            return jsonify({'message': 'Goal name is required'}), 400
        
        # Validate data types and values
        try:
            target_value = float(data['target_value'])
            current_value = float(data['current_value'])
            if target_value <= 0 or current_value <= 0:
                print("Invalid values: target_value or current_value must be positive")
                return jsonify({'message': 'Target and current values must be positive numbers'}), 400
        except ValueError as e:
            print(f"Value error: {str(e)}")
            return jsonify({'message': 'Target and current values must be valid numbers'}), 400

        try:
            deadline = datetime.fromisoformat(data['deadline'])
            if deadline < datetime.utcnow():
                print("Invalid deadline: must be a future date")
                return jsonify({'message': 'Deadline must be a future date'}), 400
        except ValueError as e:
            print(f"Date parsing error: {str(e)}")
            return jsonify({'message': 'Invalid deadline format. Use YYYY-MM-DD'}), 400

        # Validate goal type
        valid_types = ['weight_loss', 'muscle_gain', 'endurance']
        if data['type'] not in valid_types:
            print(f"Invalid goal type: {data['type']}")
            return jsonify({'message': f'Invalid goal type. Must be one of: {", ".join(valid_types)}'}), 400
        
        print("Creating goal object...")
        # Create goal object
        goal = Goal(
            user_id=current_user.id,
            name=data['name'],
            type=data['type'],
            target_value=target_value,
            current_value=current_value,
            deadline=deadline
        )
        print("Goal object created:", goal.__dict__)
        
        print("Saving to database...")
        # Save to database
        db.session.add(goal)
        db.session.commit()
        print("Goal saved successfully")
        
        response_data = {
            'message': 'Goal added successfully',
            'goal': goal.to_dict()
        }
        print("Sending response:", response_data)
        return jsonify(response_data), 201
        
    except Exception as e:
        print("=== Error in goal creation ===")
        print("Error type:", type(e).__name__)
        print("Error message:", str(e))
        db.session.rollback()  # Roll back the session in case of an error
        return jsonify({'message': f'Error adding goal: {str(e)}'}), 400

@bp.route('/api/goals/<int:goal_id>', methods=['GET'])
@login_required
def get_goal(goal_id):
    try:
        goal = Goal.query.filter_by(id=goal_id, user_id=current_user.id).first()
        if not goal:
            return jsonify({'message': 'Goal not found'}), 404
        return jsonify(goal.to_dict())
    except Exception as e:
        print(f"Error fetching goal {goal_id}: {str(e)}")
        return jsonify({'message': 'Error fetching goal'}), 500

@bp.route('/api/goals/<int:goal_id>', methods=['PUT'])
@login_required
def update_goal(goal_id):
    goal = Goal.query.filter_by(id=goal_id, user_id=current_user.id).first_or_404()
    data = request.get_json()
    
    goal.type = data.get('type', goal.type)
    goal.target_value = data.get('target_value', goal.target_value)
    goal.current_value = data.get('current_value', goal.current_value)
    if 'deadline' in data:
        goal.deadline = datetime.fromisoformat(data['deadline'])
    
    db.session.commit()
    return jsonify({'message': 'Goal updated successfully'})

@bp.route('/api/goals/<int:goal_id>', methods=['DELETE'])
@login_required
def delete_goal(goal_id):
    try:
        print(f"Attempting to delete goal {goal_id}")
        goal = Goal.query.filter_by(id=goal_id, user_id=current_user.id).first()
        
        if not goal:
            print(f"Goal {goal_id} not found or doesn't belong to user {current_user.id}")
            return jsonify({'message': 'Goal not found'}), 404
            
        print(f"Found goal: {goal.to_dict()}")
        db.session.delete(goal)
        db.session.commit()
        print(f"Successfully deleted goal {goal_id}")
        return jsonify({'message': 'Goal deleted successfully'})
        
    except Exception as e:
        print(f"Error deleting goal {goal_id}: {str(e)}")
        db.session.rollback()
        return jsonify({'message': f'Error deleting goal: {str(e)}'}), 500

@bp.route('/api/goals/<int:goal_id>/complete', methods=['POST'])
@login_required
def complete_goal(goal_id):
    try:
        goal = Goal.query.filter_by(id=goal_id, user_id=current_user.id).first()
        if not goal:
            return jsonify({'message': 'Goal not found'}), 404
            
        # Set current value to target value to mark as completed
        goal.current_value = goal.target_value
        db.session.commit()
        
        return jsonify({
            'message': 'Goal marked as completed',
            'goal': goal.to_dict()
        })
    except Exception as e:
        print(f"Error completing goal {goal_id}: {str(e)}")
        db.session.rollback()
        return jsonify({'message': f'Error completing goal: {str(e)}'}), 500