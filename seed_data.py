from sqlalchemy.orm import Session
from app.database.database import SessionLocal, engine
from app.models import models
import random
from datetime import datetime, timedelta

# Create tables
models.Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    
    # Sample districts in UP
    districts_data = [
        ("LKO", "Lucknow"), ("AGR", "Agra"), ("KNP", "Kanpur"), ("GZB", "Ghaziabad"),
        ("VNS", "Varanasi"), ("MRT", "Meerut"), ("ALL", "Allahabad"), ("BRE", "Bareilly"),
        ("MRD", "Moradabad"), ("SHJ", "Shahjahanpur"), ("RMP", "Rampur"), ("FZB", "Firozabad"),
        ("ETW", "Etawah"), ("MNZ", "Mainpuri"), ("FRK", "Farrukhabad"), ("ETH", "Etah")
    ]
    
    # Add districts
    for code, name in districts_data:
        district = db.query(models.District).filter(models.District.district_code == code).first()
        if not district:
            district = models.District(district_code=code, district_name=name)
            db.add(district)
    
    db.commit()
    
    # Add sample performance data for last 12 months
    base_date = datetime.now() - timedelta(days=365)
    for i in range(12):
        month_date = base_date + timedelta(days=30 * i)
        month_str = month_date.strftime("%Y-%m")
        
        for code, name in districts_data:
            existing = db.query(models.DistrictPerformance)\
                .filter(models.DistrictPerformance.district_code == code)\
                .filter(models.DistrictPerformance.month == month_str).first()
            
            if not existing:
                performance = models.DistrictPerformance(
                    district_code=code,
                    month=month_str,
                    total_households=random.randint(5000, 25000),
                    total_person_days=random.randint(50000, 200000),
                    total_expenditure=random.uniform(1000000, 5000000),
                    avg_work_completion_rate=random.uniform(60, 95),
                    works_completed=random.randint(100, 500),
                    works_ongoing=random.randint(20, 100)
                )
                db.add(performance)
    
    db.commit()
    db.close()
    print("Sample data seeded successfully!")

if __name__ == "__main__":
    seed_data()