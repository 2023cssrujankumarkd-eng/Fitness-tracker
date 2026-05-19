from app import create_app, db
from app.models.nutrition import FoodItem, MealPlan, Meal, MealFoodItem, NutritionLog
from app.models.user import User
from app.models.goal import Goal
from app.models.activity import Activity
from app.models.workout import Workout, Exercise, WorkoutExercise, WorkoutSession
from app.models.consultation import Consultation
from sqlalchemy import text

app = create_app()

def create_tables():
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Created all tables")
        
        # Verify tables were created
        with db.engine.connect() as conn:
            tables = conn.execute(text("SHOW TABLES")).fetchall()
            print("\nCreated tables:")
            for table in tables:
                print(f"- {table[0]}")

if __name__ == '__main__':
    create_tables()
    