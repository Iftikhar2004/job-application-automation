"""
Reset database and recreate tables with updated schema
"""
import os
from app.core.database import engine
from app.models.models import Base

def reset_database():
    """Drop all tables and recreate them"""
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)

    print("Creating all tables with new schema...")
    Base.metadata.create_all(bind=engine)

    print("Database reset complete!")

if __name__ == "__main__":
    db_path = "job_automation.db"
    if os.path.exists(db_path):
        print(f"Removing existing database: {db_path}")
        os.remove(db_path)

    reset_database()
