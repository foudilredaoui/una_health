from datetime import datetime

from sqlalchemy.orm import Session

from .models import GlucoseLevel


def get_glucose_levels(
    db: Session, user_id: str, skip: int = 0, limit: int = 100
):
    return (
        db.query(GlucoseLevel)
        .filter(GlucoseLevel.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_glucose_level(db: Session, glucose_level_id: int):
    return (
        db.query(GlucoseLevel)
        .filter(GlucoseLevel.id == glucose_level_id)
        .first()
    )


def create_glucose_level(
    db: Session,
    user_id: str,
    timestamp: datetime,
    glucose_level: float,
    device: str,
    serial_number: str,
):
    db_glucose_level = GlucoseLevel(
        user_id=user_id,
        timestamp=timestamp,
        glucose_level=glucose_level,
        device=device,
        serial_number=serial_number,
    )
    db.add(db_glucose_level)
    db.commit()
    db.refresh(db_glucose_level)
    return db_glucose_level
