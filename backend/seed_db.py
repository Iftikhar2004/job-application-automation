"""Seed database with test data"""
from app.core.database import SessionLocal
from app.models.models import Job, User, UserProfile, JobApplication
from datetime import datetime

db = SessionLocal()

# Clear existing data
db.query(JobApplication).delete()
db.query(Job).delete()
db.query(UserProfile).delete()
db.query(User).delete()
db.commit()

# Create test user
user = User(
    email="test@example.com",
    hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyWui/SjLGSu",
    full_name="John Doe"
)
db.add(user)
db.commit()
db.refresh(user)
print(f"Created user ID: {user.id}")

# Create user profile
profile = UserProfile(
    user_id=user.id,
    skills=str(['python', 'fastapi', 'django', 'react', 'docker', 'aws']),
    experience_years=5
)
db.add(profile)
db.commit()

# Create jobs
jobs = [
    Job(title="Senior Python Developer", company="TechCorp", location="Remote",
        description="Python dev needed", job_url="http://ex.com/1", source="Indeed",
        required_skills=str(['python', 'fastapi']), experience_required=5, match_score=85,
        posted_date=datetime.now(), scraped_at=datetime.now(), is_active=True,
        salary_min=120000, salary_max=150000),

    Job(title="Full Stack Developer", company="StartupXYZ", location="NY",
        description="Full stack role", job_url="http://ex.com/2", source="Indeed",
        required_skills=str(['python', 'react']), experience_required=3, match_score=90,
        posted_date=datetime.now(), scraped_at=datetime.now(), is_active=True,
        salary_min=100000, salary_max=130000),

    Job(title="ML Engineer", company="AI Solutions", location="SF",
        description="ML role", job_url="http://ex.com/3", source="Indeed",
        required_skills=str(['python', 'ml']), experience_required=4, match_score=75,
        posted_date=datetime.now(), scraped_at=datetime.now(), is_active=True,
        salary_min=140000, salary_max=180000),
]

for job in jobs:
    db.add(job)
db.commit()
print(f"Created {len(jobs)} jobs")

# Create applications
jobs_list = db.query(Job).all()
for i, job in enumerate(jobs_list[:2]):
    app = JobApplication(
        user_id=user.id,
        job_id=job.id,
        status=['pending', 'applied'][i],
        created_at=datetime.now()
    )
    if i == 1:
        app.applied_at = datetime.now()
    db.add(app)

db.commit()
print("✅ Database seeded successfully!")
db.close()
