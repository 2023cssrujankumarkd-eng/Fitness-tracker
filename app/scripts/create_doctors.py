from app import create_app, db
from app.models.user import User
from app.models.physician import Physician

def create_doctors():
    app = create_app()
    with app.app_context():
        # Create doctors
        doctors = [
            {
                'username': 'dr.smith',
                'email': 'smith@fitness.com',
                'password': 'password123',
                'name': 'Dr. John Smith',
                'specialty': 'Sports Medicine',
                'bio': 'Dr. Smith specializes in sports medicine and has over 15 years of experience helping athletes achieve their fitness goals.'
            },
            {
                'username': 'dr.johnson',
                'email': 'johnson@fitness.com',
                'password': 'password123',
                'name': 'Dr. Sarah Johnson',
                'specialty': 'Nutrition',
                'bio': 'Dr. Johnson is a nutrition expert with a focus on sports nutrition and dietary planning for optimal performance.'
            },
            {
                'username': 'dr.williams',
                'email': 'williams@fitness.com',
                'password': 'password123',
                'name': 'Dr. Michael Williams',
                'specialty': 'Physical Therapy',
                'bio': 'Dr. Williams specializes in physical therapy and rehabilitation, helping patients recover from injuries and improve mobility.'
            },
            {
                'username': 'dr.brown',
                'email': 'brown@fitness.com',
                'password': 'password123',
                'name': 'Dr. Emily Brown',
                'specialty': 'Exercise Physiology',
                'bio': 'Dr. Brown is an exercise physiologist with expertise in designing personalized workout programs for various fitness levels.'
            }
        ]

        for doctor_data in doctors:
            # Check if user already exists
            if User.query.filter_by(username=doctor_data['username']).first():
                print(f"Doctor {doctor_data['username']} already exists")
                continue

            # Create user
            user = User(
                username=doctor_data['username'],
                email=doctor_data['email'],
                is_active=True,
                email_verified=True
            )
            user.set_password(doctor_data['password'])
            db.session.add(user)
            db.session.flush()  # Get the user ID

            # Create physician profile
            physician = Physician(
                user_id=user.id,
                name=doctor_data['name'],
                specialty=doctor_data['specialty'],
                bio=doctor_data['bio']
            )
            db.session.add(physician)

        try:
            db.session.commit()
            print("Doctors created successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error creating doctors: {str(e)}")

if __name__ == '__main__':
    create_doctors() 