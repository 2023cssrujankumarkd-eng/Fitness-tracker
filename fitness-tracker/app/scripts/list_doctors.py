from app import create_app, db
from app.models.user import User
from app.models.physician import Physician

def list_doctors():
    app = create_app()
    with app.app_context():
        # Get all users with usernames starting with 'dr.'
        doctors = User.query.filter(User.username.like('dr.%')).all()
        
        print("\nDoctors in database:")
        print("-" * 50)
        for doctor in doctors:
            physician = Physician.query.filter_by(user_id=doctor.id).first()
            print(f"Username: {doctor.username}")
            print(f"Email: {doctor.email}")
            if physician:
                print(f"Specialty: {physician.specialty}")
                print(f"Bio: {physician.bio}")
            print("-" * 50)

if __name__ == '__main__':
    list_doctors() 