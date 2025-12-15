"""Unit tests for Pydantic schemas."""
import pytest
from datetime import datetime
from app.schemas import (
    UserCreate, UserResponse, 
    MealLogCreate, WorkoutSessionCreate,
    BodyMetricCreate, GoalCreate
)


def test_user_create_schema():
    """Test UserCreate schema validation."""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    }
    user = UserCreate(**user_data)
    
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.password == "testpass123"


def test_user_create_schema_invalid_email():
    """Test UserCreate schema rejects invalid email."""
    with pytest.raises(Exception):  # Pydantic validation error
        UserCreate(
            username="testuser",
            email="invalid-email",
            password="testpass123"
        )


def test_meal_log_create_schema():
    """Test MealLogCreate schema."""
    meal_data = {
        "meal_type": "breakfast",
        "food_name": "Oatmeal",
        "calories": 150,
        "protein": 5.0,
        "carbs": 27.0,
        "fats": 3.0
    }
    meal = MealLogCreate(**meal_data)
    
    assert meal.meal_type == "breakfast"
    assert meal.food_name == "Oatmeal"
    assert meal.calories == 150


def test_workout_session_create_schema():
    """Test WorkoutSessionCreate schema."""
    workout_data = {
        "exercise_name": "Running",
        "duration_minutes": 30,
        "calories_burned": 300
    }
    workout = WorkoutSessionCreate(**workout_data)
    
    assert workout.exercise_name == "Running"
    assert workout.duration_minutes == 30
    assert workout.calories_burned == 300


def test_body_metric_create_schema():
    """Test BodyMetricCreate schema."""
    metric_data = {
        "weight": 70.5,
        "height": 175.0
    }
    metric = BodyMetricCreate(**metric_data)
    
    assert metric.weight == 70.5
    assert metric.height == 175.0


def test_goal_create_schema():
    """Test GoalCreate schema."""
    goal_data = {
        "title": "Lose Weight",
        "description": "Lose 5kg in 2 months",
        "target_date": "2025-02-14",
        "goal_type": "weight_loss"
    }
    goal = GoalCreate(**goal_data)
    
    assert goal.title == "Lose Weight"
    assert goal.goal_type == "weight_loss"
