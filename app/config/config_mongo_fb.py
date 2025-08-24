from asyncio.log import logger
from app.config.database import SessionLocal
from pymongo import MongoClient

class MongoDB:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name: str):
        return self.db[collection_name]

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
