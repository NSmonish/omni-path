from pydantic import BaseModel, Field, field_validator
from typing import Optional

class TrackingCoordinate(BaseModel):
    """
    Production-grade schema for a single player tracking frame.
    Enforces pitch boundaries (120x80m) to ensure data integrity.
    """
    player_id: str
    x: float = Field(..., ge=0, le=120)
    y: float = Field(..., ge=0, le=80)
    timestamp: float
    velocity: Optional[float] = None
    heading: Optional[float] = Field(None, ge=0, le=360) # Player body orientation in degrees

    @field_validator('x', 'y')
    @classmethod
    def check_coordinates(cls, v: float) -> float:
        # Custom logic can go here (e.g. outlier detection)
        return round(v, 3)
