from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Calculation Schemas
class CalculationBase(BaseModel):
    operation: str = Field(..., description="Operation: add, subtract, multiply, divide")
    operand1: float = Field(..., description="First operand")
    operand2: float = Field(..., description="Second operand")
    
    @validator('operation')
    def validate_operation(cls, v):
        allowed_operations = ['add', 'subtract', 'multiply', 'divide']
        if v.lower() not in allowed_operations:
            raise ValueError(f'Operation must be one of: {", ".join(allowed_operations)}')
        return v.lower()
    
    @validator('operand2')
    def validate_division_by_zero(cls, v, values):
        if 'operation' in values and values['operation'].lower() == 'divide' and v == 0:
            raise ValueError('Cannot divide by zero')
        return v


class CalculationCreate(CalculationBase):
    pass


class CalculationUpdate(BaseModel):
    operation: Optional[str] = None
    operand1: Optional[float] = None
    operand2: Optional[float] = None
    
    @validator('operation')
    def validate_operation(cls, v):
        if v is not None:
            allowed_operations = ['add', 'subtract', 'multiply', 'divide']
            if v.lower() not in allowed_operations:
                raise ValueError(f'Operation must be one of: {", ".join(allowed_operations)}')
            return v.lower()
        return v


class CalculationResponse(CalculationBase):
    id: int
    result: float
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
