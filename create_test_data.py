"""Create test data for the job automation platform"""
import sys
sys.path.insert(0, 'backend')

from app.core.database import SessionLocal
from app.models.models import Job, User, UserProfile, JobApplication, Base
from app.core.database import engine
from datetime import datetime

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Create test user
user = User(
    email="test@example.com",
    hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyWui/SjLGSu",  # password: "test123"
    full_name="John Doe"
)
db.add(user)
db.commit()
db.refresh(user)

# Create user profile
profile = UserProfile(
    user_id=user.id,
    skills=str(['python', 'fastapi', 'django', 'react', 'docker', 'aws', 'postgresql', 'machine learning']),
    experience_years=5,
    resume_text="Experienced full-stack developer with expertise in Python and React",
    linkedin_url="https://linkedin.com/in/johndoe",
    github_url="https://github.com/johndoe"
)
db.add(profile)

# Create test jobs
jobs_data = [
    {
        "title": "Senior Python Developer",
        "company": "TechCorp Inc",
        "location": "Remote",
        "description": "We are seeking an experienced Python Developer with 5+ years of experience. Must have expertise in FastAPI, Django, PostgreSQL, Docker, and AWS. Experience with machine learning and NLP is a plus. You will work on building scalable APIs and data processing pipelines.",
        "requirements": "5+ years Python experience, FastAPI, Django, Docker, AWS, PostgreSQL",
        "salary_min": 120000.0,
        "salary_max": 150000.0,
        "job_url": "https://example.com/job/1",
        "source": "Indeed",
        "required_skills": str(['python', 'fastapi', 'django', 'docker', 'aws', 'postgresql', 'machine learning']),
        "experience_required": 5,
        "match_score": 85.0
    },
    {
        "title": "Full Stack Developer (Python + React)",
        "company": "StartupXYZ",
        "location": "New York, NY",
        "description": "Join our fast-paced startup as a Full Stack Developer. We need someone proficient in Python (FastAPI/Django) and React. You'll build features end-to-end, from database to UI. Must have 3+ years experience.",
        "requirements": "3+ years experience, Python, React, PostgreSQL, REST APIs",
        "salary_min": 100000.0,
        "salary_max": 130000.0,
        "job_url": "https://example.com/job/2",
        "source": "Indeed",
        "required_skills": str(['python', 'react', 'fastapi', 'django', 'postgresql', 'rest']),
        "experience_required": 3,
        "match_score": 90.0
    },
    {
        "title": "Machine Learning Engineer",
        "company": "AI Solutions Ltd",
        "location": "San Francisco, CA",
        "description": "We're looking for an ML Engineer to build and deploy machine learning models. Experience with Python, TensorFlow, PyTorch, and NLP required. You'll work on cutting-edge AI projects involving natural language processing and computer vision.",
        "requirements": "Python, TensorFlow, PyTorch, NLP, Computer Vision, 4+ years experience",
        "salary_min": 140000.0,
        "salary_max": 180000.0,
        "job_url": "https://example.com/job/3",
        "source": "Indeed",
        "required_skills": str(['python', 'machine learning', 'tensorflow', 'pytorch', 'nlp', 'computer vision']),
        "experience_required": 4,
        "match_score": 75.0
    },
    {
        "title": "Backend Developer - Python",
        "company": "FinTech Corp",
        "location": "Remote",
        "description": "Backend developer needed for fintech platform. Must have strong Python skills, experience with FastAPI or Flask, PostgreSQL, Redis, and microservices architecture. Financial domain knowledge is a plus.",
        "requirements": "Python, FastAPI, PostgreSQL, Redis, Microservices, 3+ years",
        "salary_min": 110000.0,
        "salary_max": 140000.0,
        "job_url": "https://example.com/job/4",
        "source": "Indeed",
        "required_skills": str(['python', 'fastapi', 'flask', 'postgresql', 'redis', 'microservices']),
        "experience_required": 3,
        "match_score": 80.0
    },
    {
        "title": "Data Engineer",
        "company": "Data Analytics Inc",
        "location": "Austin, TX",
        "description": "Data Engineer to build ETL pipelines and data infrastructure. Need Python, SQL, Airflow, Spark, and AWS experience. You'll work with big data and build scalable data processing systems.",
        "requirements": "Python, SQL, Airflow, Spark, AWS, 4+ years experience",
        "salary_min": 125000.0,
        "salary_max": 155000.0,
        "job_url": "https://example.com/job/5",
        "source": "Indeed",
        "required_skills": str(['python', 'sql', 'airflow', 'spark', 'aws', 'etl']),
        "experience_required": 4,
        "match_score": 70.0
    }
]

for job_data in jobs_data:
    job = Job(**job_data, posted_date=datetime.utcnow(), scraped_at=datetime.utcnow(), is_active=True)
    db.add(job)

db.commit()

# Create some test applications
jobs = db.query(Job).limit(3).all()
for i, job in enumerate(jobs):
    app = JobApplication(
        user_id=user.id,
        job_id=job.id,
        status=['pending', 'applied', 'interviewing'][i],
        created_at=datetime.utcnow()
    )
    if i == 1:  # Mark second one as applied
        app.applied_at = datetime.utcnow()
    db.add(app)

db.commit()
db.close()

print("✅ Test data created successfully!")
print(f"   - Created user: {user.email} (password: test123)")
print(f"   - Created {len(jobs_data)} jobs")
print(f"   - Created 3 applications")
print("\nYou can now:")
print("   1. Open http://localhost:8000/docs to see the API")
print("   2. Run the frontend: cd frontend && npm install && npm run dev")
