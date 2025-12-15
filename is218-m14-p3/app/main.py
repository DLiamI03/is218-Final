from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
import os
import traceback

from app.database import get_db, create_tables, User, Calculation
from app.schemas import (
    UserCreate, UserResponse, Token,
    CalculationCreate, CalculationUpdate, CalculationResponse
)
from app.auth import (
    get_password_hash, authenticate_user, create_access_token,
    get_current_user, get_user_by_username, get_user_by_email,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

# Create FastAPI app
app = FastAPI(title="Calculations API", version="1.0.0")

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
    """Register a new user."""
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
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
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


# ===== BREAD ENDPOINTS FOR CALCULATIONS =====

def calculate_result(operation: str, operand1: float, operand2: float) -> float:
    """Perform calculation based on operation."""
    if operation == "add":
        return operand1 + operand2
    elif operation == "subtract":
        return operand1 - operand2
    elif operation == "multiply":
        return operand1 * operand2
    elif operation == "divide":
        if operand2 == 0:
            raise ValueError("Cannot divide by zero")
        return operand1 / operand2
    else:
        raise ValueError(f"Invalid operation: {operation}")


# Browse - GET all calculations for current user
@app.get("/calculations", response_model=List[CalculationResponse])
def browse_calculations(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve all calculations belonging to the logged-in user.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    """
    calculations = db.query(Calculation).filter(
        Calculation.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return calculations


# Read - GET a specific calculation by ID
@app.get("/calculations/{calculation_id}", response_model=CalculationResponse)
def read_calculation(
    calculation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve details of a specific calculation by its ID.
    
    - **calculation_id**: The ID of the calculation to retrieve
    """
    calculation = db.query(Calculation).filter(
        Calculation.id == calculation_id,
        Calculation.user_id == current_user.id
    ).first()
    
    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found"
        )
    
    return calculation


# Add - POST a new calculation
@app.post("/calculations", response_model=CalculationResponse, status_code=status.HTTP_201_CREATED)
def add_calculation(
    calculation: CalculationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new calculation by specifying the operation and operands.
    
    - **operation**: The operation to perform (add, subtract, multiply, divide)
    - **operand1**: The first operand
    - **operand2**: The second operand
    """
    try:
        # Calculate the result
        result = calculate_result(
            calculation.operation,
            calculation.operand1,
            calculation.operand2
        )
        
        # Create new calculation
        db_calculation = Calculation(
            operation=calculation.operation,
            operand1=calculation.operand1,
            operand2=calculation.operand2,
            result=result,
            user_id=current_user.id
        )
        
        db.add(db_calculation)
        db.commit()
        db.refresh(db_calculation)
        return db_calculation
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# Edit - PUT/PATCH update an existing calculation
@app.put("/calculations/{calculation_id}", response_model=CalculationResponse)
@app.patch("/calculations/{calculation_id}", response_model=CalculationResponse)
def edit_calculation(
    calculation_id: int,
    calculation_update: CalculationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update fields of an existing calculation.
    
    - **calculation_id**: The ID of the calculation to update
    - **operation**: (optional) New operation
    - **operand1**: (optional) New first operand
    - **operand2**: (optional) New second operand
    """
    # Get the calculation
    db_calculation = db.query(Calculation).filter(
        Calculation.id == calculation_id,
        Calculation.user_id == current_user.id
    ).first()
    
    if not db_calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found"
        )
    
    # Update fields if provided
    update_data = calculation_update.dict(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    for field, value in update_data.items():
        setattr(db_calculation, field, value)
    
    # Recalculate result
    try:
        db_calculation.result = calculate_result(
            db_calculation.operation,
            db_calculation.operand1,
            db_calculation.operand2
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    db.commit()
    db.refresh(db_calculation)
    return db_calculation


# Delete - DELETE a calculation
@app.delete("/calculations/{calculation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calculation(
    calculation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Remove a calculation by its ID.
    
    - **calculation_id**: The ID of the calculation to delete
    """
    db_calculation = db.query(Calculation).filter(
        Calculation.id == calculation_id,
        Calculation.user_id == current_user.id
    ).first()
    
    if not db_calculation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found"
        )
    
    db.delete(db_calculation)
    db.commit()
    return None


# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
