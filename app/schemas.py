from pydantic import BaseModel, Field
from typing import Dict, Any

class ConfigurationCreate(BaseModel):
    country_code: str = Field(..., max_length=2, description="ISO 3166-1 alpha-2 country code")
    requirements: Dict[str, Any]

class ConfigurationUpdate(BaseModel):
    country_code: str = Field(..., max_length=2, description="ISO 3166-1 alpha-2 country code")
    requirements: Dict[str, Any]

class Configuration(BaseModel):
    id: int
    country_code: str
    requirements: Dict[str, Any]

    class Config:
        orm_mode = True
