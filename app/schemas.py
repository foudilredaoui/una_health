from pydantic import BaseModel
from datetime import datetime

class GlucoseLevelBase(BaseModel):
    user_id: str
    device: str
    serial_number: str
    timestamp: datetime
    glucose_value: float

class GlucoseLevelCreate(GlucoseLevelBase):
    pass

class GlucoseLevel(GlucoseLevelBase):
    id: int

    class Config:
        orm_mode = True
