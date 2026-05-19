from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from flask_wtf.csrf import CSRFProtect
from app import db
from app.models.activity import Activity
from datetime import datetime

bp = Blueprint('activities', __name__)
csrf = CSRFProtect()

@bp.route('/activities')
@login_required
def activity_index():
    activities = Activity.query.filter_by(user_id=current_user.id)\
        .order_by(Activity.timestamp.desc())\
        .all()
    return render_template('activities/index.html', activities=activities)

@bp.route('/activities/create', methods=['GET', 'POST'])
@login_required
def create_activity():
    if request.method == 'POST':
        try:
            if request.is_json:
                data = request.get_json()
                name = data.get('name')
                type = data.get('type')
                duration = int(data.get('duration'))
                calories = int(data.get('calories'))
                notes = data.get('details')
                timestamp = datetime.fromisoformat(data.get('date').replace('Z', '+00:00'))
            else:
                name = request.form.get('name')
                type = request.form.get('type')
                duration = int(request.form.get('duration'))
                calories = int(request.form.get('calories'))
                notes = request.form.get('details')
                timestamp = datetime.strptime(request.form.get('date'), '%Y-%m-%dT%H:%M')

            activity = Activity(
                name=name,
                type=type,
                duration=duration,
                calories=calories,
                notes=notes,
                timestamp=timestamp,
                user_id=current_user.id
            )

            db.session.add(activity)
            db.session.commit()

            if request.is_json:
                return jsonify({'message': 'Activity added successfully!'}), 201
            else:
                flash('Activity added successfully!', 'success')
                return redirect(url_for('activities.activity_index'))

        except ValueError as e:
            db.session.rollback()
            if request.is_json:
                return jsonify({'message': 'Invalid input values. Please check your input.'}), 400
            else:
                flash('Invalid input values. Please check your input.', 'error')
                return redirect(url_for('activities.create_activity'))
        except Exception as e:
            db.session.rollback()
            if request.is_json:
                return jsonify({'message': f'Error adding activity: {str(e)}'}), 400
            else:
                flash(f'Error adding activity: {str(e)}', 'error')
                return redirect(url_for('activities.create_activity'))

    return render_template('activities/create.html')

@bp.route('/activities/<int:activity_id>')
@login_required
def activity_detail(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    if activity.user_id != current_user.id:
        flash('You do not have permission to view this activity.', 'error')
        return redirect(url_for('activities.activity_index'))
    return render_template('activities/detail.html', activity=activity)

@bp.route('/activities/<int:activity_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    if activity.user_id != current_user.id:
        flash('You do not have permission to edit this activity.', 'error')
        return redirect(url_for('activities.activity_index'))

    if request.method == 'POST':
        try:
            if request.is_json:
                data = request.get_json()
                activity.name = data.get('name')
                activity.type = data.get('type')
                activity.duration = data.get('duration')
                activity.calories = data.get('calories')
                activity.notes = data.get('details')
                activity.timestamp = datetime.fromisoformat(data.get('date').replace('Z', '+00:00'))
            else:
                activity.name = request.form.get('name')
                activity.type = request.form.get('type')
                activity.duration = request.form.get('duration')
                activity.calories = request.form.get('calories')
                activity.notes = request.form.get('details')
                activity.timestamp = datetime.strptime(request.form.get('date'), '%Y-%m-%dT%H:%M')

            db.session.commit()
            
            if request.is_json:
                return jsonify({'message': 'Activity updated successfully!'})
            else:
                flash('Activity updated successfully!', 'success')
                return redirect(url_for('activities.activity_detail', activity_id=activity.id))

        except Exception as e:
            db.session.rollback()
            if request.is_json:
                return jsonify({'message': f'Error updating activity: {str(e)}'}), 400
            else:
                flash(f'Error updating activity: {str(e)}', 'error')
                return redirect(url_for('activities.edit_activity', activity_id=activity.id))

    return render_template('activities/edit.html', activity=activity)

@bp.route('/activities/<int:activity_id>/delete', methods=['POST'])
@login_required
def delete_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    if activity.user_id != current_user.id:
        if request.is_json:
            return jsonify({'message': 'You do not have permission to delete this activity.'}), 403
        flash('You do not have permission to delete this activity.', 'error')
        return redirect(url_for('activities.activity_index'))

    try:
        db.session.delete(activity)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'message': 'Activity deleted successfully!'})
        else:
            flash('Activity deleted successfully!', 'success')
            return redirect(url_for('activities.activity_index'))
            
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'message': f'Error deleting activity: {str(e)}'}), 400
        else:
            flash(f'Error deleting activity: {str(e)}', 'error')
            return redirect(url_for('activities.activity_index'))