from app import create_app, db
from app.models.user import User
from app.models.physician import Physician

def cleanup_doctors():
    app = create_app()
    with app.app_context():
        # First, delete duplicate entries (keeping the first one for each specialty)
        specialties = ['Sports Medicine', 'Nutrition', 'Physical Therapy', 'Exercise Physiology']
        for specialty in specialties:
            physicians = Physician.query.filter_by(specialty=specialty).all()
            if len(physicians) > 1:
                # Keep the first one, delete the rest
                for physician in physicians[1:]:
                    db.session.delete(physician)
        
        # Update the remaining physicians with proper names
        doctor_updates = {
            'smith': {
                'name': 'Dr. John Smith',
                'specialty': 'Sports Medicine',
                'bio': 'Dr. Smith specializes in sports medicine and has over 15 years of experience helping athletes achieve their fitness goals.'
            },
            'johnson': {
                'name': 'Dr. Sarah Johnson',
                'specialty': 'Nutrition',
                'bio': 'Dr. Johnson is a nutrition expert with a focus on sports nutrition and dietary planning for optimal performance.'
            },
            'williams': {
                'name': 'Dr. Michael Williams',
                'specialty': 'Physical Therapy',
                'bio': 'Dr. Williams specializes in physical therapy and rehabilitation, helping patients recover from injuries and improve mobility.'
            },
            'brown': {
                'name': 'Dr. Emily Brown',
                'specialty': 'Exercise Physiology',
                'bio': 'Dr. Brown is an exercise physiologist with expertise in designing personalized workout programs for various fitness levels.'
            }
        }

        for username, data in doctor_updates.items():
            user = User.query.filter_by(username=username).first()
            if user:
                physician = Physician.query.filter_by(user_id=user.id).first()
                if physician:
                    physician.name = data['name']
                    physician.specialty = data['specialty']
                    physician.bio = data['bio']

        try:
            db.session.commit()
            print("Doctors cleaned up successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error cleaning up doctors: {str(e)}")

if __name__ == '__main__':
    cleanup_doctors() 