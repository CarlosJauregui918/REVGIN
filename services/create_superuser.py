from sqlalchemy import Boolean, Column, String, Integer, DateTime, ForeignKey
from api.models.user import User
from api.core.database import SessionLocal
from api.core.auth import get_password_hash

def create_superuser():
    db = SessionLocal()
    try:
        # Check if superuser already exists
        existing_user = db.query(User).filter(User.email == 'admin@revgin.com').first()
        if existing_user:
            print("Superuser already exists")
            return

        # Create new superuser
        user = User(
            email='admin@revgin.com',
            hashed_password=get_password_hash('admin123'),
            full_name='Admin User',
            is_active=True,
            is_superuser=True
        )
        db.add(user)
        db.commit()
        print("Superuser created successfully")
    except Exception as e:
        print(f"Error creating superuser: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_superuser() 