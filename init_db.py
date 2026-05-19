from app import create_app, db
from app.models.user import User
from app.models.goal import Goal
from app.models.activity import Activity
from app.models.nutrition import FoodItem, MealPlan, Meal, MealFoodItem, NutritionLog
from app.models.workout import Workout, Exercise, WorkoutExercise, WorkoutSession
from app.models.consultation import Consultation
from app.models.physician import Physician
from sqlalchemy import text

app = create_app()

def init_db():
    with app.app_context():
        print("Initializing database...")
        
        # Disable foreign key checks
        db.session.execute(text('SET FOREIGN_KEY_CHECKS=0'))
        
        # Drop all tables
        print("Dropping all tables...")
        db.drop_all()
        
        # Create all tables
        print("Creating all tables...")
        db.create_all()
        
        # Re-enable foreign key checks
        db.session.execute(text('SET FOREIGN_KEY_CHECKS=1'))
        
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()