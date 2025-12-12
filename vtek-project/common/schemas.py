from pydantic import BaseModel

class CarSchema(BaseModel):
    manufacturer: str
    model: str
    year: int
    power: int
    torque: int
    max_speed: int
    fuel_efficiency: float
    fuel_type: str
    doors_number: int
    weight: int
    aerodynamic_level: float
    turbo_count: int
    millage_in_km: int
    zero_to_hundred: float
    transmission_type: str
    is_started: bool = False