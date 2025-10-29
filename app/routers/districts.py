from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.database import get_db
from app.models import models, schemas
from typing import List, Optional

router = APIRouter(prefix="/api", tags=["districts"])

@router.get("/districts", response_model=List[schemas.District])
def get_districts(db: Session = Depends(get_db)):
    return db.query(models.District).all()

@router.get("/districts/{district_code}", response_model=schemas.District)
def get_district(district_code: str, db: Session = Depends(get_db)):
    district = db.query(models.District).filter(models.District.district_code == district_code).first()
    if not district:
        raise HTTPException(status_code=404, detail="District not found")
    return district

@router.get("/districts/{district_code}/performance", response_model=List[schemas.Performance])
def get_district_performance(district_code: str, months: int = 12, db: Session = Depends(get_db)):
    performances = db.query(models.DistrictPerformance)\
        .filter(models.DistrictPerformance.district_code == district_code)\
        .order_by(models.DistrictPerformance.month.desc())\
        .limit(months).all()
    return performances

@router.get("/districts/{district_code}/latest", response_model=schemas.Performance)
def get_latest_performance(district_code: str, db: Session = Depends(get_db)):
    performance = db.query(models.DistrictPerformance)\
        .filter(models.DistrictPerformance.district_code == district_code)\
        .order_by(models.DistrictPerformance.month.desc())\
        .first()
    if not performance:
        raise HTTPException(status_code=404, detail="No performance data found")
    return performance

@router.get("/performance/summary", response_model=List[schemas.DistrictSummary])
def get_performance_summary(db: Session = Depends(get_db)):
    results = db.query(
        models.District.district_code,
        models.District.district_name,
        func.sum(models.DistrictPerformance.total_households).label('total_households'),
        func.sum(models.DistrictPerformance.total_person_days).label('total_person_days'),
        func.sum(models.DistrictPerformance.total_expenditure).label('total_expenditure'),
        func.avg(models.DistrictPerformance.avg_work_completion_rate).label('avg_work_completion_rate')
    ).join(models.DistrictPerformance)\
     .group_by(models.District.district_code, models.District.district_name)\
     .all()
    
    return [schemas.DistrictSummary(
        district_code=r.district_code,
        district_name=r.district_name,
        total_households=r.total_households or 0,
        total_person_days=r.total_person_days or 0,
        total_expenditure=r.total_expenditure or 0.0,
        avg_work_completion_rate=r.avg_work_completion_rate or 0.0
    ) for r in results]

@router.get("/compare")
def compare_districts(district_codes: str, months: int = 6, db: Session = Depends(get_db)):
    codes = district_codes.split(',')
    performances = db.query(models.DistrictPerformance)\
        .filter(models.DistrictPerformance.district_code.in_(codes))\
        .order_by(models.DistrictPerformance.month.desc())\
        .limit(months * len(codes)).all()
    
    return {"districts": codes, "data": performances}

@router.post("/sync/{district_code}")
def trigger_sync(district_code: str, months: int = 12, db: Session = Depends(get_db)):
    # Mock sync operation - in real app, this would fetch from external API
    return {"message": f"Sync triggered for {district_code}", "status": "success"}