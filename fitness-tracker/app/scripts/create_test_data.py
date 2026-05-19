from app import create_app, db
from app.models.user import User
from app.models.consultation import Consultation

def create_test_data():
    app = create_app()
    with app.app_context():
        # Create test patient
        patient_data = {
            'username': 'test_patient',
            'email': 'patient@test.com',
            'password': 'password123'
        }

        # Check if patient exists
        patient = User.query.filter_by(username=patient_data['username']).first()
        if not patient:
            patient = User(
                username=patient_data['username'],
                email=patient_data['email']
            )
            patient.set_password(patient_data['password'])
            db.session.add(patient)
            db.session.flush()

        # Get Dr. Smith
        doctor = User.query.filter_by(username='smith').first()
        if not doctor:
            print("Dr. Smith not found!")
            return

        # Create test consultation
        consultation = Consultation(
            patient_id=patient.id,
            doctor_id=doctor.id,
            notes="I need advice on proper warm-up exercises for running.",
            status='pending'
        )
        db.session.add(consultation)

        try:
            db.session.commit()
            print("Test data created successfully!")
            print(f"Created consultation from {patient.username} to Dr. {doctor.username}")
        except Exception as e:
            db.session.rollback()
            print(f"Error creating test data: {str(e)}")

if __name__ == '__main__':
    create_test_data() 