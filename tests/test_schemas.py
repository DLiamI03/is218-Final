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
        "date": "2025-12-14",
        "meal_type": "breakfast",
        "notes": "Healthy breakfast"
    }
    meal = MealLogCreate(**meal_data)
    
    assert meal.meal_type == "breakfast"
    assert meal.date.isoformat() == "2025-12-14"
    assert meal.notes == "Healthy breakfast"


def test_workout_session_create_schema():
    """Test WorkoutSessionCreate schema."""
    workout_data = {
        "name": "Morning Run",
        "date": "2025-12-14",
        "duration_minutes": 30,
        "total_calories_burned": 300
    }
    workout = WorkoutSessionCreate(**workout_data)
    
    assert workout.name == "Morning Run"
    assert workout.duration_minutes == 30
    assert workout.total_calories_burned == 300


def test_body_metric_create_schema():
    """Test BodyMetricCreate schema."""
    metric_data = {
        "date": "2025-12-14",
        "weight_kg": 70.5,
        "body_fat_percentage": 15.0
    }
    metric = BodyMetricCreate(**metric_data)
    
    assert metric.weight_kg == 70.5
    assert metric.body_fat_percentage == 15.0


def test_goal_create_schema():
    """Test GoalCreate schema."""
    goal_data = {
        "goal_type": "weight_loss",
        "target_value": 65.0,
        "current_value": 70.0,
        "start_date": "2025-12-14",
        "target_date": "2025-02-14"
    }
    goal = GoalCreate(**goal_data)
    
    assert goal.goal_type == "weight_loss"
    assert goal.target_value == 65.0
    assert goal.current_value == 70.0
