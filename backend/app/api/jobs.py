from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.models import Job, User
from app.services.nlp_service import NLPJobAnalyzer
from datetime import datetime

router = APIRouter()
nlp_analyzer = NLPJobAnalyzer()


# Pydantic schemas
from pydantic import BaseModel


class JobCreate(BaseModel):
    title: str
    company: str
    location: str
    description: str
    requirements: Optional[str] = ""
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    job_url: str
    source: str


class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str
    description: str
    requirements: Optional[str]
    salary_min: Optional[float]
    salary_max: Optional[float]
    job_url: str
    source: str
    posted_date: Optional[datetime]
    match_score: Optional[float]
    required_skills: Optional[str]
    experience_required: Optional[int]
    is_active: bool

    class Config:
        from_attributes = True


@router.post("/", response_model=JobResponse)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    """Create a new job posting"""
    # Check if job URL already exists
    existing_job = db.query(Job).filter(Job.job_url == job.job_url).first()
    if existing_job:
        raise HTTPException(status_code=400, detail="Job with this URL already exists")

    # Analyze job with NLP
    full_text = f"{job.description} {job.requirements or ''}"
    analysis = nlp_analyzer.analyze_job(job.description, job.requirements or "")

    # Create job
    db_job = Job(
        title=job.title,
        company=job.company,
        location=job.location,
        description=job.description,
        requirements=job.requirements,
        salary_min=job.salary_min or analysis['salary_range'].get('min'),
        salary_max=job.salary_max or analysis['salary_range'].get('max'),
        job_url=job.job_url,
        source=job.source,
        posted_date=datetime.utcnow(),
        required_skills=str(analysis['required_skills']),
        experience_required=analysis['experience_years']
    )

    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    return db_job


@router.get("/", response_model=List[JobResponse])
def get_jobs(
    skip: int = 0,
    limit: int = 20,
    source: Optional[str] = None,
    company: Optional[str] = None,
    min_match_score: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """Get list of jobs with optional filters"""
    query = db.query(Job).filter(Job.is_active == True)

    if source:
        query = query.filter(Job.source == source)

    if company:
        query = query.filter(Job.company.ilike(f"%{company}%"))

    if min_match_score:
        query = query.filter(Job.match_score >= min_match_score)

    jobs = query.order_by(Job.scraped_at.desc()).offset(skip).limit(limit).all()
    return jobs


@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    """Get a specific job by ID"""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    """Delete a job (soft delete by marking inactive)"""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    job.is_active = False
    db.commit()

    return {"message": "Job deleted successfully"}


@router.post("/{job_id}/calculate-match")
def calculate_match_score(
    job_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Calculate match score between job and user profile"""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get user profile
    if not user.profiles:
        raise HTTPException(status_code=400, detail="User profile not found")

    profile = user.profiles
    user_skills = eval(profile.skills) if profile.skills else []
    user_experience = profile.experience_years or 0

    # Calculate match score
    match_score = nlp_analyzer.calculate_match_score(
        job.description,
        user_skills,
        user_experience
    )

    # Update job with match score
    job.match_score = match_score
    db.commit()

    return {
        "job_id": job_id,
        "user_id": user_id,
        "match_score": match_score
    }


@router.get("/search/skills")
def search_by_skills(
    skills: str = Query(..., description="Comma-separated list of skills"),
    db: Session = Depends(get_db)
):
    """Search jobs by required skills"""
    skill_list = [s.strip().lower() for s in skills.split(",")]

    jobs = db.query(Job).filter(Job.is_active == True).all()

    matching_jobs = []
    for job in jobs:
        job_skills = eval(job.required_skills) if job.required_skills else []
        job_skills_lower = [s.lower() for s in job_skills]

        # Check if any of the user's skills match
        if any(skill in job_skills_lower for skill in skill_list):
            matching_jobs.append(job)

    return matching_jobs[:20]  # Return top 20 matches
