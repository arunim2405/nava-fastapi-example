from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# Master DB URL (Replace with your DB connection string)
MASTER_DB_URL = "sqlite:///./master.db"

# Initialize Master DB
master_engine = create_engine(MASTER_DB_URL)
MasterSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=master_engine)
Base.metadata.create_all(bind=master_engine)

def get_master_db():
    db = MasterSessionLocal()
    try:
        yield db
    finally:
        db.close()