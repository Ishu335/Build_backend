from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import json
import random
from datetime import datetime, timedelta

app = FastAPI(title="MGNREGA Performance API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock data
districts = [
    {"id": 1, "district_code": "LKO", "district_name": "Lucknow", "state_name": "Uttar Pradesh"},
    {"id": 2, "district_code": "AGR", "district_name": "Agra", "state_name": "Uttar Pradesh"},
    {"id": 3, "district_code": "KNP", "district_name": "Kanpur", "state_name": "Uttar Pradesh"},
    {"id": 4, "district_code": "VNS", "district_name": "Varanasi", "state_name": "Uttar Pradesh"},
    {"id": 5, "district_code": "MRT", "district_name": "Meerut", "state_name": "Uttar Pradesh"},
    {"id": 6, "district_code": "ALL", "district_name": "Allahabad", "state_name": "Uttar Pradesh"},
    {"id": 7, "district_code": "BRE", "district_name": "Bareilly", "state_name": "Uttar Pradesh"},
    {"id": 8, "district_code": "GZB", "district_name": "Ghaziabad", "state_name": "Uttar Pradesh"},
    {"id": 9, "district_code": "MUM", "district_name": "Mumbai", "state_name": "Maharashtra"},
    {"id": 10, "district_code": "PUN", "district_name": "Pune", "state_name": "Maharashtra"},
    {"id": 11, "district_code": "NAG", "district_name": "Nagpur", "state_name": "Maharashtra"},
    {"id": 12, "district_code": "BLR", "district_name": "Bangalore", "state_name": "Karnataka"},
    {"id": 13, "district_code": "MYS", "district_name": "Mysore", "state_name": "Karnataka"},
]

states = [
    {"state_code": "UP", "state_name": "Uttar Pradesh"},
    {"state_code": "MH", "state_name": "Maharashtra"},
    {"state_code": "KA", "state_name": "Karnataka"},
]

def generate_performance_data(district_code: str, months: int = 12):
    data = []
    base_date = datetime.now() - timedelta(days=30 * months)
    for i in range(months):
        month_date = base_date + timedelta(days=30 * i)
        person_days = random.randint(50000, 200000)
        households = random.randint(5000, 25000)
        works_completed = random.randint(100, 500)
        works_takenup = works_completed + random.randint(20, 100)
        women_days = int(person_days * random.uniform(0.4, 0.6))
        sc_days = int(person_days * random.uniform(0.15, 0.25))
        st_days = int(person_days * random.uniform(0.05, 0.15))
        
        data.append({
            "id": i + 1,
            "district_code": district_code,
            "month": month_date.strftime("%Y-%m"),
            "total_households_issued_jobcards": households,
            "person_days_generated": person_days,
            "total_expenditure": random.uniform(1000000, 5000000),
            "avg_work_completion_rate": random.uniform(60, 95),
            "total_works_completed": works_completed,
            "total_works_takenup": works_takenup,
            "work_completion_rate": (works_completed / works_takenup) * 100,
            "avg_days_per_household": person_days / households,
            "women_persondays": women_days,
            "sc_persondays": sc_days,
            "st_persondays": st_days,
            "state_name": next(d["state_name"] for d in districts if d["district_code"] == district_code)
        })
    return data

def generate_state_data(state_name: str, months: int = 12):
    state_districts = [d for d in districts if d["state_name"] == state_name]
    aggregated_data = []
    
    for i in range(months):
        month_date = (datetime.now() - timedelta(days=30 * months)) + timedelta(days=30 * i)
        total_households = sum(random.randint(5000, 25000) for _ in state_districts)
        total_person_days = sum(random.randint(50000, 200000) for _ in state_districts)
        total_expenditure = sum(random.uniform(1000000, 5000000) for _ in state_districts)
        total_works_completed = sum(random.randint(100, 500) for _ in state_districts)
        total_works_takenup = sum(random.randint(120, 600) for _ in state_districts)
        
        aggregated_data.append({
            "month": month_date.strftime("%Y-%m"),
            "state_name": state_name,
            "total_households": total_households,
            "total_person_days": total_person_days,
            "total_expenditure": total_expenditure,
            "total_works_completed": total_works_completed,
            "total_works_takenup": total_works_takenup,
            "work_completion_rate": (total_works_completed / total_works_takenup) * 100,
            "districts_count": len(state_districts)
        })
    return aggregated_data

@app.post("/auth/register")
def register(user_data: dict):
    return {"success": True, "user": user_data, "access_token": "mock-token"}

@app.post("/auth/login")
def login(credentials: dict):
    return {"success": True, "user": {"email": credentials.get("email")}, "access_token": "mock-token"}

@app.get("/api/states")
def get_states():
    return states

@app.get("/api/districts")
def get_districts():
    return districts

@app.get("/api/districts/{district_code}")
def get_district(district_code: str):
    district = next((d for d in districts if d["district_code"] == district_code), None)
    if not district:
        raise HTTPException(status_code=404, detail="District not found")
    return district

@app.get("/api/districts/{district_code}/performance")
def get_district_performance(district_code: str, months: int = 12):
    valid_codes = [d["district_code"] for d in districts]
    if district_code not in valid_codes:
        raise HTTPException(status_code=404, detail="District not found")
    return generate_performance_data(district_code, months)

@app.get("/api/districts/{district_code}/latest")
def get_latest_performance(district_code: str):
    valid_codes = [d["district_code"] for d in districts]
    if district_code not in valid_codes:
        raise HTTPException(status_code=404, detail="District not found")
    data = generate_performance_data(district_code, 1)
    return data[0] if data else {}

@app.get("/api/performance/summary")
def get_performance_summary():
    summary = []
    for district in districts:
        code = district["district_code"]
        summary.append({
            "district_code": code,
            "district_name": district["district_name"],
            "total_households": random.randint(50000, 250000),
            "total_person_days": random.randint(500000, 2000000),
            "total_expenditure": random.uniform(10000000, 50000000),
            "avg_work_completion_rate": random.uniform(60, 95)
        })
    return summary

@app.get("/api/compare")
def compare_districts(district_codes: str = Query(..., description="Comma-separated district codes"), months: int = Query(6, ge=1, le=24)):
    codes = [code.strip().upper() for code in district_codes.split(',')]
    
    if len(codes) < 2:
        raise HTTPException(status_code=400, detail="At least 2 district codes required for comparison")
    
    valid_codes = [d["district_code"] for d in districts]
    invalid_codes = [code for code in codes if code not in valid_codes]
    
    if invalid_codes:
        raise HTTPException(status_code=404, detail=f"Invalid district codes: {', '.join(invalid_codes)}")
    
    # Return data in format expected by React app
    comparison_data = {}
    for code in codes:
        comparison_data[code] = generate_performance_data(code, months)
    
    return comparison_data

@app.get("/api/states/compare")
def compare_states(state_names: str = Query(..., description="Comma-separated state names"), months: int = Query(6, ge=1, le=24)):
    names = [name.strip() for name in state_names.split(',')]
    
    if len(names) < 2:
        raise HTTPException(status_code=400, detail="At least 2 state names required for comparison")
    
    valid_states = [s["state_name"] for s in states]
    invalid_states = [name for name in names if name not in valid_states]
    
    if invalid_states:
        raise HTTPException(status_code=404, detail=f"Invalid state names: {', '.join(invalid_states)}")
    
    comparison_data = {}
    for state_name in names:
        state_info = next(s for s in states if s["state_name"] == state_name)
        comparison_data[state_name] = {
            "state_info": state_info,
            "performance_data": generate_state_data(state_name, months)
        }
    
    return {
        "states": names,
        "comparison_period_months": months,
        "data": comparison_data
    }

@app.post("/api/sync/{district_code}")
def trigger_sync(district_code: str, months: int = 12):
    valid_codes = [d["district_code"] for d in districts]
    if district_code not in valid_codes:
        raise HTTPException(status_code=404, detail="District not found")
    return {"message": f"Sync triggered for {district_code}", "status": "success"}

