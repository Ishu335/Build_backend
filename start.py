import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from seed_data import seed_data
import uvicorn

if __name__ == "__main__":
    print("Seeding database...")
    seed_data()
    print("Starting server...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)