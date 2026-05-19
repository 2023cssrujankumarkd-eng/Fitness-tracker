from app import create_app, db
from app.models.nutrition import FoodItem

def create_sample_food():
    app = create_app()
    with app.app_context():
        # Clear existing food items
        FoodItem.query.delete()
        
        # Create sample food items
        sample_foods = [
            FoodItem(
                name='Chicken Breast',
                calories=165,
                protein=31,
                carbs=0,
                fat=3.6,
                serving_size=100,
                serving_unit='g'
            ),
            FoodItem(
                name='Brown Rice',
                calories=112,
                protein=2.6,
                carbs=23.5,
                fat=0.9,
                serving_size=100,
                serving_unit='g'
            ),
            FoodItem(
                name='Salmon',
                calories=208,
                protein=22,
                carbs=0,
                fat=13,
                serving_size=100,
                serving_unit='g'
            ),
            FoodItem(
                name='Broccoli',
                calories=34,
                protein=2.8,
                carbs=6.6,
                fat=0.4,
                serving_size=100,
                serving_unit='g'
            ),
            FoodItem(
                name='Greek Yogurt',
                calories=59,
                protein=10,
                carbs=3.6,
                fat=0.4,
                serving_size=100,
                serving_unit='g'
            ),
            FoodItem(
                name='Oatmeal',
                calories=307,
                protein=13,
                carbs=55,
                fat=5,
                serving_size=100,
                serving_unit='g'
            ),
            FoodItem(
                name='Banana',
                calories=89,
                protein=1.1,
                carbs=22.8,
                fat=0.3,
                serving_size=100,
                serving_unit='g'
            ),
            FoodItem(
                name='Eggs',
                calories=155,
                protein=12.6,
                carbs=1.1,
                fat=11.3,
                serving_size=100,
                serving_unit='g'
            ),
            FoodItem(
                name='Sweet Potato',
                calories=86,
                protein=1.6,
                carbs=20.1,
                fat=0.1,
                serving_size=100,
                serving_unit='g'
            ),
            FoodItem(
                name='Quinoa',
                calories=120,
                protein=4.4,
                carbs=21.3,
                fat=1.9,
                serving_size=100,
                serving_unit='g'
            )
        ]
        
        try:
            # Add to database
            for food in sample_foods:
                db.session.add(food)
            
            db.session.commit()
            print("Sample food items created successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error creating food items: {str(e)}")

if __name__ == '__main__':
    create_sample_food() 