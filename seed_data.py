"""
Seed data script to populate the database with common foods and exercises.
Run this after starting the application to have a pre-populated database.
"""
import sys
sys.path.insert(0, '/app')

from app.database import SessionLocal, FoodDatabase, ExerciseLibrary, ExerciseCategory
from sqlalchemy.exc import IntegrityError

def seed_foods():
    db = SessionLocal()
    
    common_foods = [
        # Proteins
        {"name": "Chicken Breast", "brand": None, "serving_size": 100, "serving_unit": "grams", "calories": 165, "protein_g": 31, "carbs_g": 0, "fats_g": 3.6, "fiber_g": 0},
        {"name": "Eggs", "brand": None, "serving_size": 1, "serving_unit": "large egg", "calories": 70, "protein_g": 6, "carbs_g": 0.5, "fats_g": 5, "fiber_g": 0},
        {"name": "Salmon", "brand": None, "serving_size": 100, "serving_unit": "grams", "calories": 208, "protein_g": 20, "carbs_g": 0, "fats_g": 13, "fiber_g": 0},
        {"name": "Greek Yogurt", "brand": None, "serving_size": 170, "serving_unit": "grams", "calories": 100, "protein_g": 17, "carbs_g": 6, "fats_g": 0, "fiber_g": 0},
        {"name": "Tofu", "brand": None, "serving_size": 100, "serving_unit": "grams", "calories": 76, "protein_g": 8, "carbs_g": 2, "fats_g": 4.8, "fiber_g": 0.3},
        
        # Carbs
        {"name": "Brown Rice", "brand": None, "serving_size": 100, "serving_unit": "grams cooked", "calories": 111, "protein_g": 2.6, "carbs_g": 23, "fats_g": 0.9, "fiber_g": 1.8},
        {"name": "Oatmeal", "brand": None, "serving_size": 100, "serving_unit": "grams", "calories": 389, "protein_g": 16.9, "carbs_g": 66, "fats_g": 6.9, "fiber_g": 10.6},
        {"name": "Whole Wheat Bread", "brand": None, "serving_size": 1, "serving_unit": "slice", "calories": 80, "protein_g": 4, "carbs_g": 13, "fats_g": 1, "fiber_g": 2},
        {"name": "Sweet Potato", "brand": None, "serving_size": 100, "serving_unit": "grams", "calories": 86, "protein_g": 1.6, "carbs_g": 20, "fats_g": 0.1, "fiber_g": 3},
        {"name": "Quinoa", "brand": None, "serving_size": 100, "serving_unit": "grams cooked", "calories": 120, "protein_g": 4.4, "carbs_g": 21, "fats_g": 1.9, "fiber_g": 2.8},
        
        # Fruits
        {"name": "Banana", "brand": None, "serving_size": 1, "serving_unit": "medium", "calories": 105, "protein_g": 1.3, "carbs_g": 27, "fats_g": 0.4, "fiber_g": 3.1},
        {"name": "Apple", "brand": None, "serving_size": 1, "serving_unit": "medium", "calories": 95, "protein_g": 0.5, "carbs_g": 25, "fats_g": 0.3, "fiber_g": 4.4},
        {"name": "Blueberries", "brand": None, "serving_size": 100, "serving_unit": "grams", "calories": 57, "protein_g": 0.7, "carbs_g": 14, "fats_g": 0.3, "fiber_g": 2.4},
        {"name": "Orange", "brand": None, "serving_size": 1, "serving_unit": "medium", "calories": 62, "protein_g": 1.2, "carbs_g": 15, "fats_g": 0.2, "fiber_g": 3.1},
        
        # Vegetables
        {"name": "Broccoli", "brand": None, "serving_size": 100, "serving_unit": "grams", "calories": 34, "protein_g": 2.8, "carbs_g": 7, "fats_g": 0.4, "fiber_g": 2.6},
        {"name": "Spinach", "brand": None, "serving_size": 100, "serving_unit": "grams", "calories": 23, "protein_g": 2.9, "carbs_g": 3.6, "fats_g": 0.4, "fiber_g": 2.2},
        {"name": "Carrots", "brand": None, "serving_size": 100, "serving_unit": "grams", "calories": 41, "protein_g": 0.9, "carbs_g": 10, "fats_g": 0.2, "fiber_g": 2.8},
        
        # Fats & Others
        {"name": "Almonds", "brand": None, "serving_size": 28, "serving_unit": "grams (1 oz)", "calories": 164, "protein_g": 6, "carbs_g": 6, "fats_g": 14, "fiber_g": 3.5},
        {"name": "Avocado", "brand": None, "serving_size": 100, "serving_unit": "grams", "calories": 160, "protein_g": 2, "carbs_g": 9, "fats_g": 15, "fiber_g": 7},
        {"name": "Olive Oil", "brand": None, "serving_size": 1, "serving_unit": "tablespoon", "calories": 119, "protein_g": 0, "carbs_g": 0, "fats_g": 13.5, "fiber_g": 0},
        {"name": "Peanut Butter", "brand": None, "serving_size": 2, "serving_unit": "tablespoons", "calories": 188, "protein_g": 8, "carbs_g": 7, "fats_g": 16, "fiber_g": 2},
        
        # Beverages/Misc
        {"name": "Protein Shake", "brand": "Generic", "serving_size": 1, "serving_unit": "scoop (30g)", "calories": 120, "protein_g": 24, "carbs_g": 3, "fats_g": 1, "fiber_g": 0},
        {"name": "Milk", "brand": None, "serving_size": 240, "serving_unit": "ml (1 cup)", "calories": 149, "protein_g": 8, "carbs_g": 12, "fats_g": 8, "fiber_g": 0},
    ]
    
    added = 0
    for food_data in common_foods:
        existing = db.query(FoodDatabase).filter(FoodDatabase.name == food_data["name"]).first()
        if not existing:
            food = FoodDatabase(**food_data, is_custom=False)
            db.add(food)
            added += 1
    
    try:
        db.commit()
        print(f"✅ Added {added} foods to database!")
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding foods: {e}")
    finally:
        db.close()


def seed_exercises():
    db = SessionLocal()
    
    common_exercises = [
        # Strength - Upper Body
        {"name": "Push-ups", "category": ExerciseCategory.STRENGTH, "muscle_group": "chest", "description": "Classic bodyweight chest exercise", "calories_per_minute": 7.0},
        {"name": "Pull-ups", "category": ExerciseCategory.STRENGTH, "muscle_group": "back", "description": "Bodyweight back exercise", "calories_per_minute": 8.0},
        {"name": "Bench Press", "category": ExerciseCategory.STRENGTH, "muscle_group": "chest", "description": "Barbell chest press", "calories_per_minute": 6.0},
        {"name": "Dumbbell Rows", "category": ExerciseCategory.STRENGTH, "muscle_group": "back", "description": "Single arm dumbbell row", "calories_per_minute": 5.5},
        {"name": "Shoulder Press", "category": ExerciseCategory.STRENGTH, "muscle_group": "shoulders", "description": "Overhead press", "calories_per_minute": 5.0},
        {"name": "Bicep Curls", "category": ExerciseCategory.STRENGTH, "muscle_group": "arms", "description": "Dumbbell bicep curls", "calories_per_minute": 4.0},
        {"name": "Tricep Dips", "category": ExerciseCategory.STRENGTH, "muscle_group": "arms", "description": "Bodyweight tricep exercise", "calories_per_minute": 5.5},
        
        # Strength - Lower Body
        {"name": "Squats", "category": ExerciseCategory.STRENGTH, "muscle_group": "legs", "description": "Barbell back squat", "calories_per_minute": 8.0},
        {"name": "Deadlifts", "category": ExerciseCategory.STRENGTH, "muscle_group": "legs", "description": "Conventional deadlift", "calories_per_minute": 9.0},
        {"name": "Lunges", "category": ExerciseCategory.STRENGTH, "muscle_group": "legs", "description": "Walking or stationary lunges", "calories_per_minute": 6.0},
        {"name": "Leg Press", "category": ExerciseCategory.STRENGTH, "muscle_group": "legs", "description": "Machine leg press", "calories_per_minute": 6.5},
        {"name": "Calf Raises", "category": ExerciseCategory.STRENGTH, "muscle_group": "calves", "description": "Standing calf raises", "calories_per_minute": 4.0},
        
        # Strength - Core
        {"name": "Plank", "category": ExerciseCategory.STRENGTH, "muscle_group": "core", "description": "Isometric core hold", "calories_per_minute": 5.0},
        {"name": "Crunches", "category": ExerciseCategory.STRENGTH, "muscle_group": "abs", "description": "Basic ab crunches", "calories_per_minute": 4.5},
        {"name": "Russian Twists", "category": ExerciseCategory.STRENGTH, "muscle_group": "obliques", "description": "Seated twisting ab exercise", "calories_per_minute": 5.0},
        
        # Cardio
        {"name": "Running", "category": ExerciseCategory.CARDIO, "muscle_group": None, "description": "Outdoor or treadmill running", "calories_per_minute": 11.0},
        {"name": "Cycling", "category": ExerciseCategory.CARDIO, "muscle_group": None, "description": "Outdoor or stationary bike", "calories_per_minute": 8.0},
        {"name": "Swimming", "category": ExerciseCategory.CARDIO, "muscle_group": None, "description": "Lap swimming", "calories_per_minute": 10.0},
        {"name": "Jumping Jacks", "category": ExerciseCategory.CARDIO, "muscle_group": None, "description": "Full body cardio", "calories_per_minute": 8.0},
        {"name": "Jump Rope", "category": ExerciseCategory.CARDIO, "muscle_group": None, "description": "Skipping rope", "calories_per_minute": 12.0},
        {"name": "Burpees", "category": ExerciseCategory.CARDIO, "muscle_group": None, "description": "Full body explosive movement", "calories_per_minute": 10.0},
        {"name": "Rowing Machine", "category": ExerciseCategory.CARDIO, "muscle_group": None, "description": "Indoor rowing", "calories_per_minute": 9.0},
        
        # Flexibility
        {"name": "Yoga Flow", "category": ExerciseCategory.FLEXIBILITY, "muscle_group": None, "description": "Vinyasa yoga", "calories_per_minute": 4.0},
        {"name": "Static Stretching", "category": ExerciseCategory.FLEXIBILITY, "muscle_group": None, "description": "Hold stretches", "calories_per_minute": 2.5},
        
        # Sports
        {"name": "Basketball", "category": ExerciseCategory.SPORTS, "muscle_group": None, "description": "Recreational basketball", "calories_per_minute": 8.0},
        {"name": "Soccer", "category": ExerciseCategory.SPORTS, "muscle_group": None, "description": "Recreational soccer", "calories_per_minute": 9.0},
        {"name": "Tennis", "category": ExerciseCategory.SPORTS, "muscle_group": None, "description": "Singles or doubles tennis", "calories_per_minute": 7.0},
    ]
    
    added = 0
    for exercise_data in common_exercises:
        existing = db.query(ExerciseLibrary).filter(ExerciseLibrary.name == exercise_data["name"]).first()
        if not existing:
            exercise = ExerciseLibrary(**exercise_data, is_custom=False)
            db.add(exercise)
            added += 1
    
    try:
        db.commit()
        print(f"✅ Added {added} exercises to database!")
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding exercises: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    print("🌱 Seeding database with common foods and exercises...")
    seed_foods()
    seed_exercises()
    print("✅ Database seeding complete!")
