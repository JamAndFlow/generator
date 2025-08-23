import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient

from app.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# TODO: Enhance databse with pooling and connection management
engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# MongoDB connection setup
MONGO_URI = "mongodb://mongodb:27017"
MONGO_DB_NAME = "questions_db"

mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client[MONGO_DB_NAME]
questions_collection = mongo_db["questions"]


def get_db():
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error("Database error: %s", e)
        db.rollback()
        raise
    finally:
        db.close()
