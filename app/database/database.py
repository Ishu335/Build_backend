from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "sqlite:///./mgnrega.db"
# DATABASE_URL = "postgresql://postgres:admin@localhost:5432/<database>"
# DATABASE_URL = "postgresql://postgres:admin@localhost:5432/BuildBharat" 
DATABASE_URL = "postgresql://neondb_owner:npg_7SpmlbAvgyx3@ep-wispy-dew-ae1zy8je-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()