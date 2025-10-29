from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    phone = Column(String)
    district = Column(String)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class District(Base):
    __tablename__ = "districts"
    
    id = Column(Integer, primary_key=True, index=True)
    district_code = Column(String, unique=True, index=True)
    district_name = Column(String)
    state = Column(String, default="Uttar Pradesh")
    
    performances = relationship("DistrictPerformance", back_populates="district")

class DistrictPerformance(Base):
    __tablename__ = "district_performances"
    
    id = Column(Integer, primary_key=True, index=True)
    district_code = Column(String, ForeignKey("districts.district_code"))
    month = Column(String)  # Format: YYYY-MM
    total_households = Column(Integer, default=0)
    total_person_days = Column(Integer, default=0)
    total_expenditure = Column(Float, default=0.0)
    avg_work_completion_rate = Column(Float, default=0.0)
    works_completed = Column(Integer, default=0)
    works_ongoing = Column(Integer, default=0)
    
    district = relationship("District", back_populates="performances")