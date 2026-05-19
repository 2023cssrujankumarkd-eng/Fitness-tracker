from app import db
from datetime import datetime

class FoodItem(db.Model):
    __tablename__ = 'food_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    barcode = db.Column(db.String(50), unique=True)
    calories = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    serving_size = db.Column(db.Float, nullable=False)
    serving_unit = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'calories': self.calories,
            'protein': self.protein,
            'carbs': self.carbs,
            'fat': self.fat,
            'serving_size': self.serving_size,
            'serving_unit': self.serving_unit,
            'barcode': self.barcode,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class MealPlan(db.Model):
    __tablename__ = 'meal_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='meal_plans')
    meals = db.relationship('Meal', back_populates='meal_plan', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'meals': [meal.to_dict() for meal in self.meals]
        }

class Meal(db.Model):
    __tablename__ = 'meals'
    
    id = db.Column(db.Integer, primary_key=True)
    meal_plan_id = db.Column(db.Integer, db.ForeignKey('meal_plans.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)  # e.g., "Breakfast", "Lunch"
    time = db.Column(db.Time, nullable=False)
    
    # Relationships
    meal_plan = db.relationship('MealPlan', back_populates='meals')
    food_items = db.relationship('MealFoodItem', back_populates='meal', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'meal_plan_id': self.meal_plan_id,
            'name': self.name,
            'time': self.time.isoformat() if self.time else None,
            'food_items': [item.to_dict() for item in self.food_items]
        }

class MealFoodItem(db.Model):
    __tablename__ = 'meal_food_items'
    
    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)
    food_item_id = db.Column(db.Integer, db.ForeignKey('food_items.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)  # number of servings
    
    # Relationships
    meal = db.relationship('Meal', back_populates='food_items')
    food_item = db.relationship('FoodItem')
    
    def to_dict(self):
        return {
            'id': self.id,
            'meal_id': self.meal_id,
            'food_item_id': self.food_item_id,
            'quantity': self.quantity,
            'food_item': self.food_item.to_dict() if self.food_item else None
        }

class NutritionLog(db.Model):
    __tablename__ = 'nutrition_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    food_item_id = db.Column(db.Integer, db.ForeignKey('food_items.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)  # number of servings
    meal_type = db.Column(db.String(20), nullable=False)  # e.g., "Breakfast", "Lunch"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='nutrition_logs')
    food_item = db.relationship('FoodItem')
    
    def __repr__(self):
        return f'<NutritionLog {self.food_item.name if self.food_item else "Unknown"}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date.isoformat() if self.date else None,
            'food_item_id': self.food_item_id,
            'quantity': self.quantity,
            'meal_type': self.meal_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'food_item': self.food_item.to_dict() if self.food_item else None
        }

class MealEntry(db.Model):
    __tablename__ = 'meal_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    food_item_id = db.Column(db.Integer, db.ForeignKey('food_items.id'), nullable=False)
    meal_type = db.Column(db.String(20), nullable=False)  # breakfast, lunch, dinner, snack
    servings = db.Column(db.Float, nullable=False, default=1.0)
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='meal_entries')
    food_item = db.relationship('FoodItem', backref='meal_entries')

class WaterIntake(db.Model):
    __tablename__ = 'water_intakes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    glasses = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='water_intakes')
    
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'glasses': self.glasses
        }