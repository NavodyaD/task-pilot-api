from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

# Get DATABASE_URL from .env
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./classroom_management.db")

# Create database engine
engine = create_engine(DATABASE_URL)

# Create session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()
