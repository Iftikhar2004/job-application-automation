from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from app.core.database import get_db
from app.models.models import JobApplication, Job, User
from app.services.cover_letter_service import CoverLetterGenerator

router = APIRouter()
cover_letter_gen = CoverLetterGenerator()


# Pydantic schemas
class ApplicationCreate(BaseModel):
    job_id: int
    user_id: int
    notes: Optional[str] = None


class ApplicationUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None
    cover_letter: Optional[str] = None


class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    job_id: int
    status: str
    cover_letter: Optional[str]
    applied_at: Optional[datetime]
    created_at: datetime
    notes: Optional[str]

    class Config:
        from_attributes = True


class GenerateCoverLetterRequest(BaseModel):
    application_id: int
    tone: str = "professional"


@router.post("/", response_model=ApplicationResponse)
def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db)
):
    """Create a new job application"""
    # Verify job exists
    job = db.query(Job).filter(Job.id == application.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Verify user exists
    user = db.query(User).filter(User.id == application.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if application already exists
    existing = db.query(JobApplication).filter(
        JobApplication.job_id == application.job_id,
        JobApplication.user_id == application.user_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Application already exists for this job")

    # Create application
    db_application = JobApplication(
        user_id=application.user_id,
        job_id=application.job_id,
        status="pending",
        notes=application.notes
    )

    db.add(db_application)
    db.commit()
    db.refresh(db_application)

    return db_application


@router.get("/", response_model=List[ApplicationResponse])
def get_applications(
    user_id: Optional[int] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get list of applications with optional filters"""
    query = db.query(JobApplication)

    if user_id:
        query = query.filter(JobApplication.user_id == user_id)

    if status:
        query = query.filter(JobApplication.status == status)

    applications = query.order_by(JobApplication.created_at.desc()).offset(skip).limit(limit).all()
    return applications


@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(application_id: int, db: Session = Depends(get_db)):
    """Get a specific application by ID"""
    application = db.query(JobApplication).filter(JobApplication.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router.put("/{application_id}", response_model=ApplicationResponse)
def update_application(
    application_id: int,
    application_update: ApplicationUpdate,
    db: Session = Depends(get_db)
):
    """Update an application"""
    application = db.query(JobApplication).filter(JobApplication.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    if application_update.status:
        application.status = application_update.status
        if application_update.status == "applied" and not application.applied_at:
            application.applied_at = datetime.utcnow()

    if application_update.notes is not None:
        application.notes = application_update.notes

    if application_update.cover_letter is not None:
        application.cover_letter = application_update.cover_letter

    application.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(application)

    return application


@router.delete("/{application_id}")
def delete_application(application_id: int, db: Session = Depends(get_db)):
    """Delete an application"""
    application = db.query(JobApplication).filter(JobApplication.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    db.delete(application)
    db.commit()

    return {"message": "Application deleted successfully"}


@router.post("/{application_id}/generate-cover-letter")
def generate_cover_letter(
    application_id: int,
    tone: str = "professional",
    db: Session = Depends(get_db)
):
    """Generate a cover letter for an application using user profile data"""
    import json

    application = db.query(JobApplication).filter(JobApplication.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    # Get job and user details
    job = application.job
    user = application.user
    profile = user.profiles

    if not profile:
        raise HTTPException(
            status_code=400,
            detail="User profile not found. Please create your profile first."
        )

    # Extract user skills
    try:
        user_skills = json.loads(profile.skills) if profile.skills else []
    except:
        user_skills = []

    # Build comprehensive user experience summary from profile
    experience_parts = []

    if profile.current_job_title and profile.current_company:
        experience_parts.append(f"Currently working as {profile.current_job_title} at {profile.current_company}")

    if profile.experience_years:
        experience_parts.append(f"{profile.experience_years} years of professional experience")

    if profile.professional_summary:
        experience_parts.append(profile.professional_summary)

    user_experience = ". ".join(experience_parts) if experience_parts else "Professional with relevant experience"

    # Generate cover letter with full profile context
    cover_letter = cover_letter_gen.generate_cover_letter(
        job_title=job.title,
        company=job.company,
        job_description=job.description,
        user_name=user.full_name or user.email.split('@')[0],
        user_skills=user_skills,
        user_experience=user_experience,
        tone=tone
    )

    # Update application with cover letter
    application.cover_letter = cover_letter
    application.updated_at = datetime.utcnow()
    db.commit()

    return {
        "application_id": application_id,
        "cover_letter": cover_letter
    }


@router.get("/stats/user/{user_id}")
def get_user_application_stats(user_id: int, db: Session = Depends(get_db)):
    """Get application statistics for a user"""
    applications = db.query(JobApplication).filter(JobApplication.user_id == user_id).all()

    stats = {
        "total": len(applications),
        "pending": len([a for a in applications if a.status == "pending"]),
        "applied": len([a for a in applications if a.status == "applied"]),
        "interviewing": len([a for a in applications if a.status == "interviewing"]),
        "rejected": len([a for a in applications if a.status == "rejected"]),
        "accepted": len([a for a in applications if a.status == "accepted"])
    }

    return stats
