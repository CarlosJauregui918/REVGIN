from .database import engine, Base
from ..models.user import User, UserToken
from ..models.company import Company

def init_db():
    # Create all tables
    Base.metadata.create_all(bind=engine) 