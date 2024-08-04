from typing import List

from app import schemas
from app.db.core import NotFoundError, get_db
from app.db.glucose_levels import (
    create_glucose_level,
    get_glucose_level,
    get_glucose_levels,
)
from fastapi import APIRouter, HTTPException, Request
from fastapi.params import Depends
from sqlalchemy.orm import Session

from .limiter import limiter

router = APIRouter(
    prefix="/levels",
)


@router.get("/", response_model=List[schemas.GlucoseLevel])
@limiter.limit("5/minute")
def read_glucose_levels(
    request: Request,
    user_id: str,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
):
    glucose_levels = get_glucose_levels(
        db, user_id=user_id, skip=skip, limit=limit
    )
    return glucose_levels


@router.get("/{id}", response_model=schemas.GlucoseLevel)
@limiter.limit("5/minute")
def read_glucose_level(
    request: Request, id: int, db: Session = Depends(get_db)
):
    try:
        glucose_level = get_glucose_level(db, glucose_level_id=id)
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e
    return glucose_level


@router.post("/", response_model=schemas.GlucoseLevel)
@limiter.limit("5/minute")
def create(
    request: Request,
    glucose_level: schemas.GlucoseLevelCreate,
    db: Session = Depends(get_db),
):
    try:
        glucose_level = create_glucose_level(
            db=db, glucose_level=glucose_level
        )
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e
    return glucose_level
