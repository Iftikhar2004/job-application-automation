from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    applications = relationship("JobApplication", back_populates="user")
    profiles = relationship("UserProfile", back_populates="user", uselist=False)


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    # Personal Information
    phone = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)

    # Professional Information
    skills = Column(Text)  # JSON string
    experience_years = Column(Integer)
    current_job_title = Column(String)
    current_company = Column(String)
    education = Column(Text)  # JSON string with degree, institution, year
    certifications = Column(Text)  # JSON string

    # Resume and Summary
    resume_text = Column(Text)
    professional_summary = Column(Text)

    # Links
    linkedin_url = Column(String)
    github_url = Column(String)
    portfolio_url = Column(String)

    # Preferences
    desired_job_titles = Column(Text)  # JSON string
    desired_locations = Column(Text)  # JSON string
    desired_salary_min = Column(Float)
    remote_preference = Column(String)  # remote, hybrid, onsite, any

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="profiles")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String, index=True)
    location = Column(String)
    description = Column(Text)
    requirements = Column(Text)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    job_url = Column(String, unique=True)
    source = Column(String)  # LinkedIn, Indeed, Glassdoor
    posted_date = Column(DateTime)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # NLP Analysis Fields
    match_score = Column(Float, nullable=True)
    required_skills = Column(Text, nullable=True)  # JSON string
    experience_required = Column(Integer, nullable=True)

    # Relationships
    applications = relationship("JobApplication", back_populates="job")


class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))

    status = Column(String, default="pending")  # pending, applied, interviewing, rejected, accepted
    cover_letter = Column(Text)
    applied_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    notes = Column(Text, nullable=True)

    # Relationships
    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")
