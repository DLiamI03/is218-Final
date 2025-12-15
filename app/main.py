from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from sqlalchemy.orm import Session
from datetime import timedelta
from pydantic import EmailStr
import os
import traceback

from app.database import get_db, create_tables, User
from app.schemas import UserCreate, UserResponse, Token
from app.auth import (
    get_password_hash, authenticate_user, create_access_token,
    get_current_user, get_user_by_username, get_user_by_email,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

# Create FastAPI app
app = FastAPI(title="Application API", version="1.0.0")

# Global exception handler to ensure JSON responses
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions and return JSON."""
    error_detail = str(exc)
    error_traceback = traceback.format_exc()
    print(f"Unhandled exception: {error_detail}")
    print(error_traceback)
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": error_detail
        }
    )

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create database tables on startup
@app.on_event("startup")
def startup_event():
    try:
        print("Creating database tables...")
        create_tables()
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating database tables: {str(e)}")
        raise


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint to verify the application is running."""
    return {"status": "healthy"}


# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main page."""
    return FileResponse("static/index.html")


# User Registration
@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user and send verification email."""
    from app.email_service import generate_verification_token, send_verification_email
    
    # Check if username already exists
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user (not verified yet)
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_verified=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Generate verification token and send email
    verification_token = generate_verification_token(str(db_user.id))
    send_verification_email(db_user.email, db_user.username, verification_token)
    
    return db_user


# User Login
@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login and get access token."""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Get current user
@app.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return current_user


# Email Verification
@app.get("/verify")
def verify_email(token: str, db: Session = Depends(get_db)):
    """Verify user email with token."""
    from app.email_service import verify_token
    
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token"
        )
    
    # Get user and mark as verified
    db_user = db.query(User).filter(User.id == int(user_id)).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if db_user.is_verified:
        return {"message": "Email already verified", "verified": True}
    
    db_user.is_verified = True
    db.commit()
    
    return {"message": "Email verified successfully!", "verified": True}


# Resend Verification Email
@app.post("/resend-verification")
def resend_verification(email: EmailStr, db: Session = Depends(get_db)):
    """Resend verification email to user."""
    from app.email_service import generate_verification_token, send_verification_email
    
    db_user = get_user_by_email(db, email)
    if not db_user:
        # Don't reveal if email exists for security
        return {"message": "If the email exists, a verification link has been sent."}
    
    if db_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already verified"
        )
    
    # Generate new token and send email
    verification_token = generate_verification_token(str(db_user.id))
    send_verification_email(db_user.email, db_user.username, verification_token)
    
    return {"message": "Verification email sent successfully!"}


# ===== FITNESS TRACKER ENDPOINTS =====

from app.schemas import (
    UserProfileCreate, UserProfileUpdate, UserProfileResponse,
    BodyMetricCreate, BodyMetricResponse,
    FoodDatabaseCreate, FoodDatabaseResponse,
    MealLogCreate, MealLogResponse,
    ExerciseLibraryCreate, ExerciseLibraryResponse,
    WorkoutSessionCreate, WorkoutSessionResponse,
    WaterIntakeCreate, WaterIntakeResponse,
    GoalCreate, GoalResponse,
    AIParseFoodRequest, AIParseFoodResponse,
    AIParseWorkoutRequest, DashboardSummary
)
from app.database import (
    UserProfile, BodyMetric, FoodDatabase, MealLog, MealFood,
    ExerciseLibrary, WorkoutSession, WorkoutExercise, ExerciseSet,
    WaterIntake, Goal, MealType
)
from app.ai_service import parse_food_with_ai, parse_workout_with_ai, get_meal_suggestions
from typing import List, Optional
from datetime import date as date_type, datetime, timedelta


# ==== USER PROFILE ENDPOINTS ====
@app.post("/profile", response_model=UserProfileResponse, status_code=status.HTTP_201_CREATED)
def create_user_profile(
    profile_data: UserProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create or update user profile."""
    # Check if profile exists
    existing_profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if existing_profile:
        raise HTTPException(status_code=400, detail="Profile already exists. Use PUT to update.")
    
    profile = UserProfile(user_id=current_user.id, **profile_data.dict())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@app.get("/profile", response_model=UserProfileResponse)
def get_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user profile."""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@app.put("/profile", response_model=UserProfileResponse)
def update_user_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile."""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found. Create one first.")
    
    for key, value in profile_data.dict(exclude_unset=True).items():
        setattr(profile, key, value)
    
    db.commit()
    db.refresh(profile)
    return profile


# ==== BODY METRICS ENDPOINTS ====
@app.post("/body-metrics", response_model=BodyMetricResponse, status_code=status.HTTP_201_CREATED)
def create_body_metric(
    metric: BodyMetricCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log body metrics (weight, body fat %)."""
    db_metric = BodyMetric(user_id=current_user.id, **metric.dict())
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric


@app.get("/body-metrics", response_model=List[BodyMetricResponse])
def get_body_metrics(
    start_date: Optional[date_type] = None,
    end_date: Optional[date_type] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get body metrics history."""
    query = db.query(BodyMetric).filter(BodyMetric.user_id == current_user.id)
    
    if start_date:
        query = query.filter(BodyMetric.date >= start_date)
    if end_date:
        query = query.filter(BodyMetric.date <= end_date)
    
    return query.order_by(BodyMetric.date.desc()).all()


# ==== FOOD DATABASE ENDPOINTS ====
@app.post("/foods", response_model=FoodDatabaseResponse, status_code=status.HTTP_201_CREATED)
def create_food_item(
    food: FoodDatabaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a custom food item."""
    db_food = FoodDatabase(**food.dict(), is_custom=True)
    db.add(db_food)
    db.commit()
    db.refresh(db_food)
    return db_food


@app.get("/foods", response_model=List[FoodDatabaseResponse])
def search_foods(
    search: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search foods in database."""
    query = db.query(FoodDatabase)
    
    if search:
        query = query.filter(FoodDatabase.name.ilike(f"%{search}%"))
    
    return query.limit(limit).all()


# ==== AI PARSING ENDPOINTS ====
@app.post("/ai/parse-food", response_model=AIParseFoodResponse)
def ai_parse_food(
    request: AIParseFoodRequest,
    current_user: User = Depends(get_current_user)
):
    """Parse natural language food description with AI."""
    try:
        food_items = parse_food_with_ai(request.text)
        return {"food_items": food_items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI parsing error: {str(e)}")


@app.post("/ai/parse-workout")
def ai_parse_workout(
    request: AIParseWorkoutRequest,
    current_user: User = Depends(get_current_user)
):
    """Parse natural language workout description with AI."""
    try:
        exercises = parse_workout_with_ai(request.text)
        return {"exercises": exercises}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI parsing error: {str(e)}")


@app.get("/ai/meal-suggestions")
def get_ai_meal_suggestions(
    preferences: Optional[str] = None,
    dietary_restrictions: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Get AI-powered meal suggestions."""
    try:
        suggestions = get_meal_suggestions(preferences, dietary_restrictions)
        return {"suggestions": suggestions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI error: {str(e)}")


# ==== MEAL LOG ENDPOINTS ====
@app.post("/meals", response_model=MealLogResponse, status_code=status.HTTP_201_CREATED)
def create_meal_log(
    meal: MealLogCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log a meal with foods."""
    db_meal = MealLog(
        user_id=current_user.id,
        date=meal.date,
        meal_type=meal.meal_type,
        notes=meal.notes
    )
    db.add(db_meal)
    db.flush()
    
    # Add foods to meal
    for food_item in meal.foods:
        meal_food = MealFood(
            meal_id=db_meal.id,
            food_id=food_item.food_id,
            servings=food_item.servings
        )
        db.add(meal_food)
    
    db.commit()
    db.refresh(db_meal)
    return db_meal


@app.get("/meals", response_model=List[MealLogResponse])
def get_meal_logs(
    start_date: Optional[date_type] = None,
    end_date: Optional[date_type] = None,
    meal_type: Optional[MealType] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get meal history."""
    query = db.query(MealLog).filter(MealLog.user_id == current_user.id)
    
    if start_date:
        query = query.filter(MealLog.date >= start_date)
    if end_date:
        query = query.filter(MealLog.date <= end_date)
    if meal_type:
        query = query.filter(MealLog.meal_type == meal_type)
    
    return query.order_by(MealLog.date.desc()).all()


@app.delete("/meals/{meal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_meal(
    meal_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a meal log."""
    meal = db.query(MealLog).filter(
        MealLog.id == meal_id,
        MealLog.user_id == current_user.id
    ).first()
    
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    
    db.delete(meal)
    db.commit()
    return None


# ==== EXERCISE LIBRARY ENDPOINTS ====
@app.post("/exercises", response_model=ExerciseLibraryResponse, status_code=status.HTTP_201_CREATED)
def create_exercise(
    exercise: ExerciseLibraryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create custom exercise."""
    db_exercise = ExerciseLibrary(**exercise.dict(), is_custom=True)
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise


@app.get("/exercises", response_model=List[ExerciseLibraryResponse])
def search_exercises(
    search: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search exercises in library."""
    query = db.query(ExerciseLibrary)
    
    if search:
        query = query.filter(ExerciseLibrary.name.ilike(f"%{search}%"))
    if category:
        query = query.filter(ExerciseLibrary.category == category)
    
    return query.limit(limit).all()


# ==== WORKOUT SESSION ENDPOINTS ====
@app.post("/workouts", response_model=WorkoutSessionResponse, status_code=status.HTTP_201_CREATED)
def create_workout_session(
    workout: WorkoutSessionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log a workout session."""
    db_workout = WorkoutSession(
        user_id=current_user.id,
        name=workout.name,
        date=workout.date,
        duration_minutes=workout.duration_minutes,
        total_calories_burned=workout.total_calories_burned,
        notes=workout.notes
    )
    db.add(db_workout)
    db.flush()
    
    # Add exercises
    for exercise_data in workout.exercises:
        workout_exercise = WorkoutExercise(
            session_id=db_workout.id,
            exercise_id=exercise_data.exercise_id,
            order=exercise_data.order,
            notes=exercise_data.notes
        )
        db.add(workout_exercise)
        db.flush()
        
        # Add sets
        for set_data in exercise_data.sets:
            exercise_set = ExerciseSet(
                workout_exercise_id=workout_exercise.id,
                **set_data.dict()
            )
            db.add(exercise_set)
    
    db.commit()
    db.refresh(db_workout)
    return db_workout


@app.get("/workouts", response_model=List[WorkoutSessionResponse])
def get_workout_sessions(
    start_date: Optional[date_type] = None,
    end_date: Optional[date_type] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get workout history."""
    query = db.query(WorkoutSession).filter(WorkoutSession.user_id == current_user.id)
    
    if start_date:
        query = query.filter(WorkoutSession.date >= start_date)
    if end_date:
        query = query.filter(WorkoutSession.date <= end_date)
    
    return query.order_by(WorkoutSession.date.desc()).all()


@app.delete("/workouts/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workout(
    workout_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a workout session."""
    workout = db.query(WorkoutSession).filter(
        WorkoutSession.id == workout_id,
        WorkoutSession.user_id == current_user.id
    ).first()
    
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    
    db.delete(workout)
    db.commit()
    return None


# ==== WATER INTAKE ENDPOINTS ====
@app.post("/water", response_model=WaterIntakeResponse, status_code=status.HTTP_201_CREATED)
def log_water_intake(
    water: WaterIntakeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log water intake."""
    db_water = WaterIntake(user_id=current_user.id, **water.dict())
    db.add(db_water)
    db.commit()
    db.refresh(db_water)
    return db_water


@app.get("/water", response_model=List[WaterIntakeResponse])
def get_water_intake(
    start_date: Optional[date_type] = None,
    end_date: Optional[date_type] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get water intake history."""
    query = db.query(WaterIntake).filter(WaterIntake.user_id == current_user.id)
    
    if start_date:
        query = query.filter(WaterIntake.date >= start_date)
    if end_date:
        query = query.filter(WaterIntake.date <= end_date)
    
    return query.order_by(WaterIntake.date.desc()).all()


# ==== GOAL ENDPOINTS ====
@app.post("/goals", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
def create_goal(
    goal: GoalCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a fitness goal."""
    db_goal = Goal(user_id=current_user.id, **goal.dict())
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal


@app.get("/goals", response_model=List[GoalResponse])
def get_goals(
    active_only: bool = True,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user goals."""
    query = db.query(Goal).filter(Goal.user_id == current_user.id)
    
    if active_only:
        query = query.filter(Goal.is_achieved == False)
    
    return query.order_by(Goal.created_at.desc()).all()


# ==== DASHBOARD SUMMARY ENDPOINT ====
@app.get("/dashboard", response_model=DashboardSummary)
def get_dashboard_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dashboard summary with today's stats."""
    today = date_type.today()
    week_ago = today - timedelta(days=7)
    
    # Get today's meals
    today_meals = db.query(MealLog).filter(
        MealLog.user_id == current_user.id,
        MealLog.date == today
    ).all()
    
    # Calculate nutrition totals
    total_calories = 0
    total_protein = 0.0
    total_carbs = 0.0
    total_fats = 0.0
    
    for meal in today_meals:
        for meal_food in meal.foods:
            food = meal_food.food
            servings = meal_food.servings
            total_calories += food.calories * servings
            total_protein += food.protein_g * servings
            total_carbs += food.carbs_g * servings
            total_fats += food.fats_g * servings
    
    # Get today's water intake
    water_today = db.query(WaterIntake).filter(
        WaterIntake.user_id == current_user.id,
        WaterIntake.date == today
    ).all()
    total_water = sum(w.amount_ml for w in water_today)
    
    # Get this week's workouts
    workouts_this_week = db.query(WorkoutSession).filter(
        WorkoutSession.user_id == current_user.id,
        WorkoutSession.date >= week_ago
    ).count()
    
    # Get current profile data
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    
    return {
        "total_calories_today": int(total_calories),
        "total_protein_today": round(total_protein, 1),
        "total_carbs_today": round(total_carbs, 1),
        "total_fats_today": round(total_fats, 1),
        "total_water_today": total_water,
        "workouts_this_week": workouts_this_week,
        "current_weight": profile.current_weight_kg if profile else None,
        "goal_weight": profile.goal_weight_kg if profile else None,
        "calories_target": profile.daily_calorie_target if profile else None
    }
