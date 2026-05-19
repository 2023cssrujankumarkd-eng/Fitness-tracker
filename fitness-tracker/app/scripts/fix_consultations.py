from app import create_app, db
from app.models.user import User
from app.models.physician import Physician
from app.models.consultation import Consultation

def fix_consultations():
    app = create_app()
    with app.app_context():
        # Get all consultations
        consultations = Consultation.query.all()
        print(f"Found {len(consultations)} consultations")
        
        # Get doctor mappings
        doctor_mappings = {
            'dr.smith': 2,  # Dr. John Smith
            'dr.johnson': 3,  # Dr. Sarah Johnson
            'dr.williams': 4,  # Dr. Michael Williams
            'dr.brown': 5   # Dr. Emily Brown
        }
        
        # Print all users for verification
        users = User.query.all()
        print("\nAll users in database:")
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}")
        
        # Update consultations
        for consultation in consultations:
            # Get the doctor's username
            doctor = User.query.get(consultation.doctor_id)
            if doctor:
                print(f"\nProcessing consultation {consultation.id}:")
                print(f"Current doctor_id: {consultation.doctor_id}")
                print(f"Doctor username: {doctor.username}")
                
                # Update to the correct doctor_id
                if doctor.username in doctor_mappings:
                    old_id = consultation.doctor_id
                    consultation.doctor_id = doctor_mappings[doctor.username]
                    print(f"Updated consultation {consultation.id} from doctor_id {old_id} to {consultation.doctor_id}")
                else:
                    print(f"Warning: Doctor username {doctor.username} not found in mappings")
            else:
                print(f"Warning: No doctor found for consultation {consultation.id} with doctor_id {consultation.doctor_id}")
        
        try:
            db.session.commit()
            print("\nConsultations updated successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error updating consultations: {str(e)}")

if __name__ == '__main__':
    fix_consultations() 