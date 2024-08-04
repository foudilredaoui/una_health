from datetime import datetime

from sqlalchemy.orm import Session

from .models import GlucoseLevel


def get_glucose_levels(
    db: Session,
    user_id: str,
    start_timestamp: datetime,
    stop_timestamp: datetime,
    sort_by: str = "timestamp",
    sort_order: str = "asc",
    limit: int = 100,
    offset: int = 0,
):
    query = db.query(GlucoseLevel).filter(GlucoseLevel.user_id == user_id)

    if start_timestamp:
        query = query.filter(GlucoseLevel.timestamp >= start_timestamp)
    if stop_timestamp:
        query = query.filter(GlucoseLevel.timestamp <= stop_timestamp)

    if sort_order == "desc":
        query = query.order_by(getattr(GlucoseLevel, sort_by).desc())
    else:
        query = query.order_by(getattr(GlucoseLevel, sort_by))

    levels = query.offset(offset).limit(limit).all()

    return levels


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
