"""Simple test to demonstrate the API works"""
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.models import Job
from datetime import datetime

client = TestClient(app)

# First, let's verify we have data
db = SessionLocal()
jobs = db.query(Job).all()
print(f"\n📊 Database has {len(jobs)} jobs")
db.close()

# Test the API endpoints
print("\n🚀 Testing API Endpoints:\n")

# Test 1: Health check
resp = client.get("/health")
print(f"✅ Health Check: {resp.json()}")

# Test 2: Root endpoint
resp = client.get("/")
print(f"✅ Root: {resp.json()}")

# Test 3: Get jobs
resp = client.get("/api/jobs/")
jobs_data = resp.json()
print(f"✅ Jobs API: Found {len(jobs_data)} jobs")

if jobs_data:
    for i, job in enumerate(jobs_data[:3], 1):
        print(f"   {i}. {job['title']} at {job['company']}")
else:
    print("   (No jobs returned - this is the issue we're debugging)")

# Test 4: Create a job via API
print("\n🔨 Creating a new job via API...")
new_job = {
    "title": "DevOps Engineer",
    "company": "CloudTech",
    "location": "Remote",
    "description": "Looking for DevOps engineer with Kubernetes experience",
    "job_url": "http://example.com/devops",
    "source": "Test"
}

resp = client.post("/api/jobs/", json=new_job)
if resp.status_code == 200:
    created = resp.json()
    print(f"✅ Created job: {created['title']}")
else:
    print(f"❌ Failed: {resp.status_code} - {resp.text}")

# Test 5: Get jobs again
resp = client.get("/api/jobs/")
jobs_data = resp.json()
print(f"\n✅ After creation: {len(jobs_data)} jobs found")

print("\n" + "="*60)
print("✨ API Testing Complete!")
print("="*60)
