from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext

from app.core.database import get_db
from app.models.models import User, UserProfile

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Pydantic schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str]

    class Config:
        from_attributes = True


class UserProfileCreate(BaseModel):
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    skills: List[str]
    experience_years: int
    current_job_title: Optional[str] = None
    current_company: Optional[str] = None
    education: Optional[List[dict]] = None
    certifications: Optional[List[str]] = None
    resume_text: Optional[str] = None
    professional_summary: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    desired_job_titles: Optional[List[str]] = None
    desired_locations: Optional[List[str]] = None
    desired_salary_min: Optional[float] = None
    remote_preference: Optional[str] = "any"

class UserProfileResponse(BaseModel):
    id: int
    user_id: int
    phone: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip_code: Optional[str]
    skills: str
    experience_years: int
    current_job_title: Optional[str]
    current_company: Optional[str]
    education: Optional[str]
    certifications: Optional[str]
    resume_text: Optional[str]
    professional_summary: Optional[str]
    linkedin_url: Optional[str]
    github_url: Optional[str]
    portfolio_url: Optional[str]
    desired_job_titles: Optional[str]
    desired_locations: Optional[str]
    desired_salary_min: Optional[float]
    remote_preference: Optional[str]

    class Config:
        from_attributes = True


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password
    hashed_password = pwd_context.hash(user.password)

    # Create user
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/{user_id}/profile", response_model=UserProfileResponse)
def create_user_profile(
    user_id: int,
    profile: UserProfileCreate,
    db: Session = Depends(get_db)
):
    """Create or update user profile"""
    import json

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if profile already exists
    existing_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    skills_str = json.dumps(profile.skills)
    education_str = json.dumps(profile.education) if profile.education else None
    certifications_str = json.dumps(profile.certifications) if profile.certifications else None
    desired_titles_str = json.dumps(profile.desired_job_titles) if profile.desired_job_titles else None
    desired_locations_str = json.dumps(profile.desired_locations) if profile.desired_locations else None

    if existing_profile:
        # Update existing profile
        existing_profile.phone = profile.phone
        existing_profile.address = profile.address
        existing_profile.city = profile.city
        existing_profile.state = profile.state
        existing_profile.zip_code = profile.zip_code
        existing_profile.skills = skills_str
        existing_profile.experience_years = profile.experience_years
        existing_profile.current_job_title = profile.current_job_title
        existing_profile.current_company = profile.current_company
        existing_profile.education = education_str
        existing_profile.certifications = certifications_str
        existing_profile.resume_text = profile.resume_text
        existing_profile.professional_summary = profile.professional_summary
        existing_profile.linkedin_url = profile.linkedin_url
        existing_profile.github_url = profile.github_url
        existing_profile.portfolio_url = profile.portfolio_url
        existing_profile.desired_job_titles = desired_titles_str
        existing_profile.desired_locations = desired_locations_str
        existing_profile.desired_salary_min = profile.desired_salary_min
        existing_profile.remote_preference = profile.remote_preference
        db.commit()
        db.refresh(existing_profile)
        return existing_profile
    else:
        # Create new profile
        db_profile = UserProfile(
            user_id=user_id,
            phone=profile.phone,
            address=profile.address,
            city=profile.city,
            state=profile.state,
            zip_code=profile.zip_code,
            skills=skills_str,
            experience_years=profile.experience_years,
            current_job_title=profile.current_job_title,
            current_company=profile.current_company,
            education=education_str,
            certifications=certifications_str,
            resume_text=profile.resume_text,
            professional_summary=profile.professional_summary,
            linkedin_url=profile.linkedin_url,
            github_url=profile.github_url,
            portfolio_url=profile.portfolio_url,
            desired_job_titles=desired_titles_str,
            desired_locations=desired_locations_str,
            desired_salary_min=profile.desired_salary_min,
            remote_preference=profile.remote_preference
        )
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        return db_profile


@router.get("/{user_id}/profile", response_model=UserProfileResponse)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    """Get user profile"""
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
