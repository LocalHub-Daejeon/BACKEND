from pydantic import BaseModel


class WeatherResponse(BaseModel):
    base_date: str
    base_time: str
    temperature: float
    humidity: int
    wind_speed: float
    precipitation_type: str
