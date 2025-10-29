from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    name: str
    phone: str
    district: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class User(BaseModel):
    id: int
    email: str
    name: str
    phone: str
    district: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class DistrictBase(BaseModel):
    district_code: str
    district_name: str
    state: str = "Uttar Pradesh"

class District(DistrictBase):
    id: int
    
    class Config:
        from_attributes = True

class PerformanceBase(BaseModel):
    district_code: str
    month: str
    total_households: int = 0
    total_person_days: int = 0
    total_expenditure: float = 0.0
    avg_work_completion_rate: float = 0.0
    works_completed: int = 0
    works_ongoing: int = 0

class Performance(PerformanceBase):
    id: int
    
    class Config:
        from_attributes = True

class DistrictSummary(BaseModel):
    district_code: str
    district_name: str
    total_households: int
    total_person_days: int
    total_expenditure: float
    avg_work_completion_rate: float

class CompareResponse(BaseModel):
    districts: List[str]
    data: List[Performance]