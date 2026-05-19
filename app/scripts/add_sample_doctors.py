from app import create_app, db
from app.models.user import User
from app.models.physician import Physician

def add_sample_doctors():
    app = create_app()
    with app.app_context():
        # Sample doctors data
        doctors = [
            {
                'username': 'dr.smith',
                'email': 'dr.smith@example.com',
                'password': 'doctor123',
                'specialty': 'Sports Medicine',
                'bio': 'Dr. Smith specializes in sports medicine and has over 15 years of experience helping athletes achieve their fitness goals.'
            },
            {
                'username': 'dr.johnson',
                'email': 'dr.johnson@example.com',
                'password': 'doctor123',
                'specialty': 'Nutrition',
                'bio': 'Dr. Johnson is a nutrition expert with a focus on sports nutrition and dietary planning for optimal performance.'
            },
            {
                'username': 'dr.williams',
                'email': 'dr.williams@example.com',
                'password': 'doctor123',
                'specialty': 'Physical Therapy',
                'bio': 'Dr. Williams specializes in physical therapy and rehabilitation, helping patients recover from injuries and improve mobility.'
            },
            {
                'username': 'dr.brown',
                'email': 'dr.brown@example.com',
                'password': 'doctor123',
                'specialty': 'Exercise Physiology',
                'bio': 'Dr. Brown is an exercise physiologist with expertise in designing personalized workout programs for various fitness levels.'
            }
        ]

        # Add each doctor
        for doctor_data in doctors:
            # Check if user already exists
            if User.query.filter_by(username=doctor_data['username']).first():
                print(f"Doctor {doctor_data['username']} already exists, skipping...")
                continue

            # Create user
            user = User(
                username=doctor_data['username'],
                email=doctor_data['email']
            )
            user.set_password(doctor_data['password'])
            db.session.add(user)
            db.session.flush()  # Get the user ID

            # Create physician profile
            physician = Physician(
                user_id=user.id,
                specialty=doctor_data['specialty'],
                bio=doctor_data['bio']
            )
            db.session.add(physician)

        # Commit all changes
        db.session.commit()
        print("Sample doctors added successfully!")

if __name__ == '__main__':
    add_sample_doctors() 