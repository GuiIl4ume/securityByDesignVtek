from pydantic import BaseModel, Field
from typing import Literal


class CarSchema(BaseModel):
    manufacturer: str = Field(..., min_length=1, max_length=100)
    model: str = Field(..., min_length=1, max_length=100)
    year: int = Field(..., ge=1886, le=2100)
    power: int = Field(..., gt=0, le=5000)
    torque: int = Field(..., gt=0, le=5000)
    max_speed: int = Field(..., ge=0, le=600)
    fuel_efficiency: float = Field(..., ge=0.0, le=200.0)
    fuel_type: Literal["Gasoline", "Diesel", "Electric", "Hybrid"]
    doors_number: int = Field(..., ge=1, le=10)
    weight: int = Field(..., gt=0, le=10000)
    aerodynamic_level: float = Field(..., ge=0.10, le=1.0)
    turbo_count: int = Field(..., ge=0, le=10)
    millage_in_km: int = Field(..., ge=0)
    zero_to_hundred: float = Field(..., gt=0.0, le=60.0)
    transmission_type: Literal["Manual", "Automatic"]
    is_started: bool = False