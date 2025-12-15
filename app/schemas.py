from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


# Enums (matching database enums)
class ActivityLevel(str, Enum):
    SEDENTARY = "sedentary"
    LIGHT = "light"
    MODERATE = "moderate"
    ACTIVE = "active"
    VERY_ACTIVE = "very_active"

class GoalType(str, Enum):
    LOSE_WEIGHT = "lose_weight"
    GAIN_WEIGHT = "gain_weight"
    MAINTAIN = "maintain"
    BUILD_MUSCLE = "build_muscle"

class MealType(str, Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"

class ExerciseCategory(str, Enum):
    STRENGTH = "strength"
    CARDIO = "cardio"
    FLEXIBILITY = "flexibility"
    SPORTS = "sports"


# User Schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserResponse(UserBase):
    id: int
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# Profile Schemas
class UserProfileCreate(BaseModel):
    date_of_birth: Optional[date] = None
    height_cm: Optional[float] = Field(None, gt=0, le=300)
    current_weight_kg: Optional[float] = Field(None, gt=0, le=500)
    goal_weight_kg: Optional[float] = Field(None, gt=0, le=500)
    activity_level: ActivityLevel = ActivityLevel.MODERATE
    goal_type: GoalType = GoalType.MAINTAIN
    daily_calorie_target: Optional[int] = Field(None, gt=0, le=10000)


class UserProfileUpdate(BaseModel):
    date_of_birth: Optional[date] = None
    height_cm: Optional[float] = Field(None, gt=0, le=300)
    current_weight_kg: Optional[float] = Field(None, gt=0, le=500)
    goal_weight_kg: Optional[float] = Field(None, gt=0, le=500)
    activity_level: Optional[ActivityLevel] = None
    goal_type: Optional[GoalType] = None
    daily_calorie_target: Optional[int] = Field(None, gt=0, le=10000)


class UserProfileResponse(BaseModel):
    id: int
    user_id: int
    date_of_birth: Optional[date]
    height_cm: Optional[float]
    current_weight_kg: Optional[float]
    goal_weight_kg: Optional[float]
    activity_level: ActivityLevel
    goal_type: GoalType
    daily_calorie_target: Optional[int]
    
    class Config:
        from_attributes = True


# Body Metrics Schemas
class BodyMetricCreate(BaseModel):
    date: date
    weight_kg: float = Field(..., gt=0, le=500)
    body_fat_percentage: Optional[float] = Field(None, ge=0, le=100)
    notes: Optional[str] = None


class BodyMetricResponse(BaseModel):
    id: int
    user_id: int
    date: date
    weight_kg: float
    body_fat_percentage: Optional[float]
    notes: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# Food Schemas
class FoodDatabaseCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    brand: Optional[str] = Field(None, max_length=100)
    serving_size: float = Field(..., gt=0)
    serving_unit: str = Field(..., min_length=1, max_length=50)
    calories: int = Field(..., ge=0)
    protein_g: float = Field(0, ge=0)
    carbs_g: float = Field(0, ge=0)
    fats_g: float = Field(0, ge=0)
    fiber_g: float = Field(0, ge=0)
    is_custom: bool = False


class FoodDatabaseResponse(BaseModel):
    id: int
    name: str
    brand: Optional[str]
    serving_size: float
    serving_unit: str
    calories: int
    protein_g: float
    carbs_g: float
    fats_g: float
    fiber_g: float
    is_custom: bool
    
    class Config:
        from_attributes = True


# Meal Schemas
class MealFoodItem(BaseModel):
    food_id: int
    servings: float = Field(1.0, gt=0)


class MealLogCreate(BaseModel):
    date: date
    meal_type: MealType
    notes: Optional[str] = None
    foods: List[MealFoodItem] = []


class MealFoodResponse(BaseModel):
    id: int
    food_id: int
    servings: float
    food: FoodDatabaseResponse
    
    class Config:
        from_attributes = True


class MealLogResponse(BaseModel):
    id: int
    user_id: int
    date: date
    meal_type: MealType
    notes: Optional[str]
    created_at: datetime
    foods: List[MealFoodResponse]
    
    class Config:
        from_attributes = True


# Exercise Schemas
class ExerciseLibraryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    category: ExerciseCategory
    muscle_group: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    calories_per_minute: float = Field(5.0, ge=0)
    is_custom: bool = False


class ExerciseLibraryResponse(BaseModel):
    id: int
    name: str
    category: ExerciseCategory
    muscle_group: Optional[str]
    description: Optional[str]
    calories_per_minute: float
    is_custom: bool
    
    class Config:
        from_attributes = True


# Workout Schemas
class ExerciseSetCreate(BaseModel):
    set_number: int = Field(..., gt=0)
    reps: Optional[int] = Field(None, ge=0)
    weight_kg: Optional[float] = Field(None, ge=0)
    duration_seconds: Optional[int] = Field(None, ge=0)


class WorkoutExerciseCreate(BaseModel):
    exercise_id: int
    order: int = 0
    notes: Optional[str] = None
    sets: List[ExerciseSetCreate] = []


class WorkoutSessionCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    date: date
    duration_minutes: Optional[int] = Field(None, ge=0)
    total_calories_burned: int = Field(0, ge=0)
    notes: Optional[str] = None
    exercises: List[WorkoutExerciseCreate] = []


class ExerciseSetResponse(BaseModel):
    id: int
    set_number: int
    reps: Optional[int]
    weight_kg: Optional[float]
    duration_seconds: Optional[int]
    
    class Config:
        from_attributes = True


class WorkoutExerciseResponse(BaseModel):
    id: int
    exercise_id: int
    order: int
    notes: Optional[str]
    exercise: ExerciseLibraryResponse
    sets: List[ExerciseSetResponse]
    
    class Config:
        from_attributes = True


class WorkoutSessionResponse(BaseModel):
    id: int
    user_id: int
    name: str
    date: date
    duration_minutes: Optional[int]
    total_calories_burned: int
    notes: Optional[str]
    created_at: datetime
    exercises: List[WorkoutExerciseResponse]
    
    class Config:
        from_attributes = True


# Water Intake Schemas
class WaterIntakeCreate(BaseModel):
    date: date
    amount_ml: int = Field(..., gt=0, le=10000)


class WaterIntakeResponse(BaseModel):
    id: int
    user_id: int
    date: date
    amount_ml: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Goal Schemas
class GoalCreate(BaseModel):
    goal_type: str = Field(..., min_length=1, max_length=100)
    target_value: float
    current_value: float = 0
    start_date: date
    target_date: Optional[date] = None


class GoalResponse(BaseModel):
    id: int
    user_id: int
    goal_type: str
    target_value: float
    current_value: float
    start_date: date
    target_date: Optional[date]
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# AI Parsing Schemas
class AIParseFoodRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)


class AIParseFoodResponse(BaseModel):
    food_items: List[FoodDatabaseCreate]


class AIParseWorkoutRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)


class AIParseWorkoutResponse(BaseModel):
    exercises: List[dict]  # Simplified for MVP


# Dashboard Summary Schema
class DashboardSummary(BaseModel):
    total_calories_today: int
    total_protein_today: float
    total_carbs_today: float
    total_fats_today: float
    total_water_today: int
    workouts_this_week: int
    current_weight: Optional[float]
    goal_weight: Optional[float]
    calories_target: Optional[int]
