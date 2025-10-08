"""
Create a test user for the application
"""
from app.core.database import SessionLocal
from app.models.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_test_user():
    db = SessionLocal()

    try:
        # Check if user exists
        existing = db.query(User).filter(User.email == "test@example.com").first()
        if existing:
            print(f"User already exists with ID: {existing.id}")
            return

        # Create user
        user = User(
            email="test@example.com",
            hashed_password=pwd_context.hash("password123"),
            full_name="Test User"
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        print(f"Test user created successfully!")
        print(f"Email: test@example.com")
        print(f"Password: password123")
        print(f"User ID: {user.id}")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()
