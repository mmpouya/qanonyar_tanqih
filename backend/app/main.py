from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import json
import os

from app.core.database import SessionLocal, engine, Base
from app.models import User, SectionData
from app.core.security import verify_token, create_access_token, get_password_hash, verify_password

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Legal Sections Analysis API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# Pydantic models
class UserRegister(BaseModel):
    username: str
    password: str
    email: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class SectionDataCreate(BaseModel):
    data: List[dict]  # List of section objects

class SectionDataResponse(BaseModel):
    id: int
    user_id: int
    data: List[dict]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to get current user
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    username = payload.get("sub")
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user

# Routes
@app.get("/")
def read_root():
    return {"message": "Legal Sections Analysis API"}

@app.post("/api/register", response_model=dict)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully", "user_id": new_user.id}

@app.post("/api/login", response_model=dict)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username
    }

@app.get("/api/sample-data", response_model=dict)
def get_sample_data(current_user: User = Depends(get_current_user)):
    # Load sample data from file
    sample_file_path = os.path.join(os.path.dirname(__file__), "..", "new_sample.json")
    try:
        with open(sample_file_path, "r", encoding="utf-8") as f:
            sample_data = json.load(f)
        return {"data": sample_data}
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sample data file not found"
        )

@app.post("/api/save-data", response_model=dict)
def save_data(
    section_data: SectionDataCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if user already has saved data
    existing_data = db.query(SectionData).filter(
        SectionData.user_id == current_user.id
    ).first()
    
    if existing_data:
        # Update existing data
        existing_data.data = section_data.data
        existing_data.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(existing_data)
        return {
            "message": "Data updated successfully",
            "data_id": existing_data.id,
            "updated_at": existing_data.updated_at
        }
    else:
        # Create new data entry
        new_data = SectionData(
            user_id=current_user.id,
            data=section_data.data
        )
        db.add(new_data)
        db.commit()
        db.refresh(new_data)
        return {
            "message": "Data saved successfully",
            "data_id": new_data.id,
            "created_at": new_data.created_at
        }

@app.get("/api/get-data", response_model=dict)
def get_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_data = db.query(SectionData).filter(
        SectionData.user_id == current_user.id
    ).first()
    
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No saved data found for this user"
        )
    
    return {
        "data": user_data.data,
        "updated_at": user_data.updated_at
    }

@app.get("/api/user/me", response_model=dict)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "created_at": current_user.created_at
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

