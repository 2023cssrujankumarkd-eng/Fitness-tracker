from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from app import db
from app.models.consultation import Consultation
from app.models.physician import Physician
from app.models.user import User
from datetime import datetime
from sqlalchemy import desc, text
import traceback

bp = Blueprint('consultations', __name__)

@bp.route('/consultations')
@login_required
def consultation_index():
    # Initialize is_physician
    is_physician = False
    
    try:
        # Log current user info
        current_app.logger.info(f"Current user: {current_user.id}, username: {current_user.username}")
        
        # Check if user is a physician
        physician = Physician.query.filter_by(user_id=current_user.id).first()
        is_physician = physician is not None
        current_app.logger.info(f"User is physician: {is_physician}")
        
        # Log all consultations first
        all_consultations = Consultation.query.all()
        current_app.logger.info(f"Total consultations in database: {len(all_consultations)}")
        for c in all_consultations:
            current_app.logger.info(
                f"All consultations - ID: {c.id}, "
                f"User: {c.user_id}, "
                f"Physician: {c.physician_id}, "
                f"Status: {c.status}"
            )
        
        # Filtered query
        try:
            if is_physician:
                current_app.logger.info(f"User is a doctor with ID: {current_user.id}")
                consultations = db.session.query(Consultation)\
                    .filter(Consultation.physician_id == current_user.id)\
                    .order_by(desc(Consultation.created_at))\
                    .all()
                
                # Log raw SQL query
                query = db.session.query(Consultation)\
                    .filter(Consultation.physician_id == current_user.id)\
                    .order_by(desc(Consultation.created_at))
                current_app.logger.info(f"SQL Query: {query}")
                
            else:
                current_app.logger.info("User is a patient")
                consultations = db.session.query(Consultation)\
                    .filter(Consultation.user_id == current_user.id)\
                    .order_by(desc(Consultation.created_at))\
                    .all()
            
            current_app.logger.info(f"Filtered query found {len(consultations)} consultations")
            
            # Log each consultation
            for c in consultations:
                current_app.logger.info(
                    f"Filtered consultation {c.id}: "
                    f"user_id={c.user_id}, "
                    f"physician_id={c.physician_id}, "
                    f"status={c.status}"
                )
            
            return render_template('consultations/index.html', consultations=consultations, is_physician=is_physician)
            
        except Exception as e:
            current_app.logger.error(f"Error in filtered query: {str(e)}")
            current_app.logger.error(f"Error type: {type(e)}")
            current_app.logger.error(f"Traceback: {traceback.format_exc()}")
            flash('An error occurred while loading consultations.', 'error')
            return render_template('consultations/index.html', consultations=[], is_physician=is_physician)
            
    except Exception as e:
        current_app.logger.error(f"Error in consultation_index: {str(e)}")
        current_app.logger.error(f"Error type: {type(e)}")
        current_app.logger.error(f"Error args: {e.args}")
        current_app.logger.error(f"Traceback: {traceback.format_exc()}")
        flash('An error occurred while loading consultations.', 'error')
        return render_template('consultations/index.html', consultations=[], is_physician=is_physician)

@bp.route('/consultations/create', methods=['GET', 'POST'])
@login_required
def create_consultation():
    if request.method == 'POST':
        consultation = Consultation(
            user_id=current_user.id,
            physician_id=request.form.get('doctor_id'),
            notes=request.form.get('notes', ''),
            status='pending'
        )
        db.session.add(consultation)
        db.session.commit()
        flash('Consultation requested successfully!', 'success')
        return redirect(url_for('consultations.consultation_index'))
    
    # Get all doctors with their user information
    doctors = db.session.query(Physician, User).join(User).filter(Physician.is_active == True).all()
    return render_template('consultations/create.html', doctors=doctors)

@bp.route('/consultations/<int:consultation_id>')
@login_required
def consultation_detail(consultation_id):
    consultation = Consultation.query.get_or_404(consultation_id)
    if consultation.user_id != current_user.id and consultation.physician_id != current_user.id:
        flash('You do not have permission to view this consultation.', 'error')
        return redirect(url_for('consultations.consultation_index'))
    
    # Check if user is a physician
    is_physician = Physician.query.filter_by(user_id=current_user.id).first() is not None
    return render_template('consultations/detail.html', consultation=consultation, is_physician=is_physician)

@bp.route('/consultations/<int:consultation_id>/update', methods=['POST'])
@login_required
def update_consultation(consultation_id):
    consultation = Consultation.query.get_or_404(consultation_id)
    
    # Check if user is the assigned doctor
    if consultation.physician_id != current_user.id:
        flash('You do not have permission to update this consultation.', 'error')
        return redirect(url_for('consultations.consultation_index'))
    
    action = request.form.get('action')
    if action == 'approve':
        consultation.status = 'approved'
        flash('Consultation approved successfully!', 'success')
    elif action == 'reject':
        consultation.status = 'rejected'
        flash('Consultation rejected.', 'info')
    elif action == 'complete':
        consultation.status = 'completed'
        consultation.completed_at = datetime.utcnow()
        consultation.recommendation = request.form.get('recommendation', '')
        flash('Consultation marked as completed!', 'success')
    
    db.session.commit()
    return redirect(url_for('consultations.consultation_detail', consultation_id=consultation.id))