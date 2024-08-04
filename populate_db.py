from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from load_data import import_glucose_data
from app.config import settings

DATABASE_URL = settings.database_url
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

SEED_DATA_DIR = "seed/"

# Import data
import_glucose_data(db, SEED_DATA_DIR)

db.close()
