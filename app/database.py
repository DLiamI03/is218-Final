from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Boolean, Text, ForeignKey, Date, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
import enum

# Database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/app_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Enums
class ActivityLevel(str, enum.Enum):
    SEDENTARY = "sedentary"
    LIGHT = "light"
    MODERATE = "moderate"
    ACTIVE = "active"
    VERY_ACTIVE = "very_active"

class GoalType(str, enum.Enum):
    LOSE_WEIGHT = "lose_weight"
    GAIN_WEIGHT = "gain_weight"
    MAINTAIN = "maintain"
    BUILD_MUSCLE = "build_muscle"

class ExerciseCategory(str, enum.Enum):
    STRENGTH = "strength"
    CARDIO = "cardio"
    FLEXIBILITY = "flexibility"
    SPORTS = "sports"

class MealType(str, enum.Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"

class GoalStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    body_metrics = relationship("BodyMetric", back_populates="user")
    workout_sessions = relationship("WorkoutSession", back_populates="user")
    meal_logs = relationship("MealLog", back_populates="user")
    water_intakes = relationship("WaterIntake", back_populates="user")
    goals = relationship("Goal", back_populates="user")


class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    date_of_birth = Column(Date, nullable=True)
    height_cm = Column(Float, nullable=True)
    current_weight_kg = Column(Float, nullable=True)
    goal_weight_kg = Column(Float, nullable=True)
    activity_level = Column(SQLEnum(ActivityLevel), default=ActivityLevel.MODERATE)
    goal_type = Column(SQLEnum(GoalType), default=GoalType.MAINTAIN)
    daily_calorie_target = Column(Integer, nullable=True)
    
    user = relationship("User", back_populates="profile")


class BodyMetric(Base):
    __tablename__ = "body_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    weight_kg = Column(Float, nullable=False)
    body_fat_percentage = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="body_metrics")


class ExerciseLibrary(Base):
    __tablename__ = "exercise_library"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(SQLEnum(ExerciseCategory), nullable=False)
    muscle_group = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    calories_per_minute = Column(Float, default=5.0)
    is_custom = Column(Boolean, default=False)


class WorkoutSession(Base):
    __tablename__ = "workout_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    duration_minutes = Column(Integer, nullable=True)
    total_calories_burned = Column(Integer, default=0)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="workout_sessions")
    exercises = relationship("WorkoutExercise", back_populates="session")


class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("workout_sessions.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercise_library.id"), nullable=False)
    order = Column(Integer, default=0)
    notes = Column(Text, nullable=True)
    
    session = relationship("WorkoutSession", back_populates="exercises")
    exercise = relationship("ExerciseLibrary")
    sets = relationship("ExerciseSet", back_populates="workout_exercise")


class ExerciseSet(Base):
    __tablename__ = "exercise_sets"
    
    id = Column(Integer, primary_key=True, index=True)
    workout_exercise_id = Column(Integer, ForeignKey("workout_exercises.id"), nullable=False)
    set_number = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=True)
    weight_kg = Column(Float, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    
    workout_exercise = relationship("WorkoutExercise", back_populates="sets")


class FoodDatabase(Base):
    __tablename__ = "food_database"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=True)
    serving_size = Column(Float, nullable=False)
    serving_unit = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
    protein_g = Column(Float, default=0)
    carbs_g = Column(Float, default=0)
    fats_g = Column(Float, default=0)
    fiber_g = Column(Float, default=0)
    is_custom = Column(Boolean, default=False)


class MealLog(Base):
    __tablename__ = "meal_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    meal_type = Column(SQLEnum(MealType), nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="meal_logs")
    foods = relationship("MealFood", back_populates="meal")


class MealFood(Base):
    __tablename__ = "meal_foods"
    
    id = Column(Integer, primary_key=True, index=True)
    meal_id = Column(Integer, ForeignKey("meal_logs.id"), nullable=False)
    food_id = Column(Integer, ForeignKey("food_database.id"), nullable=False)
    servings = Column(Float, default=1.0)
    
    meal = relationship("MealLog", back_populates="foods")
    food = relationship("FoodDatabase")


class WaterIntake(Base):
    __tablename__ = "water_intake"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    amount_ml = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="water_intakes")


class Goal(Base):
    __tablename__ = "goals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    goal_type = Column(String, nullable=False)
    target_value = Column(Float, nullable=False)
    current_value = Column(Float, default=0)
    start_date = Column(Date, nullable=False)
    target_date = Column(Date, nullable=True)
    status = Column(SQLEnum(GoalStatus), default=GoalStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="goals")


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create all tables
def create_tables():
    Base.metadata.create_all(bind=engine)
