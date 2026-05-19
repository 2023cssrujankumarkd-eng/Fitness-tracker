from flask import Blueprint, request, jsonify, render_template, current_app
from flask_login import login_required, current_user
from app.models.nutrition import FoodItem, MealPlan, Meal, MealFoodItem, NutritionLog, MealEntry, WaterIntake
from app import db
from datetime import datetime, date
import requests
import os

bp = Blueprint('nutrition', __name__)

@bp.route('/nutrition')
@login_required
def nutrition_page():
    return render_template('nutrition/tracker.html')

@bp.route('/nutrition/tracker')
@login_required
def tracker():
    return render_template('nutrition/tracker.html')

@bp.route('/nutrition/meal-plan')
@login_required
def meal_plan():
    return render_template('nutrition/meal_plan.html')

@bp.route('/api/food-items', methods=['GET'])
@login_required
def get_food_items():
    food_items = FoodItem.query.all()
    return jsonify([{
        'id': item.id,
        'name': item.name,
        'calories': item.calories,
        'protein': item.protein,
        'carbs': item.carbs,
        'fat': item.fat,
        'serving_size': item.serving_size,
        'serving_unit': item.serving_unit
    } for item in food_items])

@bp.route('/api/food-items', methods=['POST'])
@login_required
def add_food_item():
    data = request.get_json()
    food_item = FoodItem(
        name=data['name'],
        calories=data['calories'],
        protein=data['protein'],
        carbs=data['carbs'],
        fat=data['fat'],
        serving_size=data['serving_size'],
        serving_unit=data['serving_unit'],
        barcode=data.get('barcode')
    )
    db.session.add(food_item)
    db.session.commit()
    return jsonify({'message': 'Food item added successfully'})

@bp.route('/api/nutrition-log', methods=['POST'])
@login_required
def log_food():
    data = request.get_json()
    log = NutritionLog(
        user_id=current_user.id,
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        food_item_id=data['food_item_id'],
        quantity=data['quantity'],
        meal_type=data['meal_type']
    )
    db.session.add(log)
    db.session.commit()
    return jsonify({'message': 'Food logged successfully'})

@bp.route('/api/nutrition-stats')
@login_required
def get_nutrition_stats():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    logs = NutritionLog.query.filter(
        NutritionLog.user_id == current_user.id,
        NutritionLog.date >= start_date,
        NutritionLog.date <= end_date
    ).all()
    
    stats = {
        'calories': 0,
        'protein': 0,
        'carbs': 0,
        'fat': 0
    }
    
    for log in logs:
        stats['calories'] += log.food_item.calories * log.quantity
        stats['protein'] += log.food_item.protein * log.quantity
        stats['carbs'] += log.food_item.carbs * log.quantity
        stats['fat'] += log.food_item.fat * log.quantity
    
    return jsonify(stats)

@bp.route('/api/food/search')
@login_required
def search_food():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    foods = FoodItem.query.filter(FoodItem.name.ilike(f'%{query}%')).limit(10).all()
    return jsonify([food.to_dict() for food in foods])

@bp.route('/api/food/barcode/<barcode>')
@login_required
def get_food_by_barcode(barcode):
    food = FoodItem.query.filter_by(barcode=barcode).first()
    if food:
        return jsonify(food.to_dict())
    
    # If not in database, try to fetch from Open Food Facts API
    try:
        response = requests.get(f'https://world.openfoodfacts.org/api/v0/product/{barcode}.json')
        data = response.json()
        
        if data['status'] == 1:
            product = data['product']
            food = FoodItem(
                name=product.get('product_name', 'Unknown Product'),
                barcode=barcode,
                calories=float(product.get('nutriments', {}).get('energy-kcal_100g', 0)),
                protein=float(product.get('nutriments', {}).get('proteins_100g', 0)),
                carbs=float(product.get('nutriments', {}).get('carbohydrates_100g', 0)),
                fat=float(product.get('nutriments', {}).get('fat_100g', 0)),
                serving_size=100.0,
                serving_unit='g'
            )
            db.session.add(food)
            db.session.commit()
            return jsonify(food.to_dict())
    except Exception as e:
        current_app.logger.error(f"Error fetching barcode data: {str(e)}")
    
    return jsonify({'error': 'Food not found'}), 404

@bp.route('/api/meals', methods=['GET'])
@login_required
def get_meals():
    date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        selected_date = date.today()
    
    meals = MealEntry.query.filter_by(
        user_id=current_user.id,
        date=selected_date
    ).all()
    
    return jsonify([meal.to_dict() for meal in meals])

@bp.route('/api/meals', methods=['POST'])
@login_required
def add_meal():
    data = request.json
    try:
        meal = MealEntry(
            user_id=current_user.id,
            food_item_id=data['food_item_id'],
            meal_type=data['meal_type'],
            servings=float(data['servings']),
            date=datetime.strptime(data['date'], '%Y-%m-%d').date()
        )
        db.session.add(meal)
        db.session.commit()
        return jsonify(meal.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/api/meals/<int:meal_id>', methods=['DELETE'])
@login_required
def delete_meal(meal_id):
    meal = MealEntry.query.get_or_404(meal_id)
    if meal.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(meal)
    db.session.commit()
    return jsonify({'message': 'Meal deleted successfully'})

@bp.route('/api/water', methods=['GET'])
@login_required
def get_water_intake():
    date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        selected_date = date.today()
    
    water = WaterIntake.query.filter_by(
        user_id=current_user.id,
        date=selected_date
    ).first()
    
    if not water:
        water = WaterIntake(user_id=current_user.id, date=selected_date)
        db.session.add(water)
        db.session.commit()
    
    return jsonify(water.to_dict())

@bp.route('/api/water', methods=['POST'])
@login_required
def update_water_intake():
    data = request.json
    try:
        selected_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        water = WaterIntake.query.filter_by(
            user_id=current_user.id,
            date=selected_date
        ).first()
        
        if not water:
            water = WaterIntake(user_id=current_user.id, date=selected_date)
            db.session.add(water)
        
        water.glasses = data['glasses']
        db.session.commit()
        return jsonify(water.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400