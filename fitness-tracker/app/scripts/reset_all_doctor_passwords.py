from app import create_app, db
from app.models.user import User

def reset_all_doctor_passwords():
    app = create_app()
    with app.app_context():
        # Get all users with usernames starting with 'dr.'
        doctors = User.query.filter(User.username.like('dr.%')).all()
        
        if not doctors:
            print('No doctors found in the database.')
            return
        
        print(f'Found {len(doctors)} doctors:')
        for doctor in doctors:
            doctor.set_password('password123')
            print(f'Reset password for {doctor.username}')
        
        db.session.commit()
        print('\nAll doctor passwords have been reset to: password123')

if __name__ == '__main__':
    reset_all_doctor_passwords() 