# MGNREGA Performance Backend API

FastAPI backend for the MGNREGA District Performance tracking system.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Seed the database with sample data:
```bash
python seed_data.py
```

3. Run the server:
```bash
python run.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login

### Districts & Performance
- `GET /api/districts` - Get all districts
- `GET /api/districts/{code}` - Get specific district
- `GET /api/districts/{code}/performance` - Get district performance data
- `GET /api/districts/{code}/latest` - Get latest performance
- `GET /api/performance/summary` - Get performance summary for all districts
- `GET /api/compare` - Compare multiple districts
- `POST /api/sync/{code}` - Trigger data sync

## Docker

Build and run with Docker:
```bash
docker build -t mgnrega-backend .
docker run -p 8000:8000 mgnrega-backend
```

Or use docker-compose from the root directory:
```bash
docker-compose up
```