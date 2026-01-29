from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, FormData
import uuid

# SQLite database file
DATABASE_URL = "sqlite:///./uuid_forms.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database and create tables"""
    Base.metadata.create_all(bind=engine)
    seed_demo_data()


def seed_demo_data():
    """Seed database with demo UUID-object mappings"""
    db = SessionLocal()
    
    # Check if data already exists
    existing_count = db.query(FormData).count()
    if existing_count > 0:
        db.close()
        return
    
    demo_data = [
        FormData(
            uuid=str(uuid.uuid4()),
            name="John Doe",
            email="john.doe@example.com",
            phone="+1-555-0101",
            address="123 Main St, New York, NY 10001",
            company="Tech Corp",
            position="Software Engineer",
            notes="Senior developer with 5+ years experience"
        ),
        FormData(
            uuid=str(uuid.uuid4()),
            name="Jane Smith",
            email="jane.smith@example.com",
            phone="+1-555-0102",
            address="456 Oak Ave, San Francisco, CA 94102",
            company="Design Studio",
            position="UX Designer",
            notes="Expert in user experience and interface design"
        ),
        FormData(
            uuid=str(uuid.uuid4()),
            name="Bob Johnson",
            email="bob.johnson@example.com",
            phone="+1-555-0103",
            address="789 Pine Rd, Austin, TX 78701",
            company="Data Analytics Inc",
            position="Data Scientist",
            notes="Specializes in machine learning and data visualization"
        ),
        FormData(
            uuid=str(uuid.uuid4()),
            name="Alice Williams",
            email="alice.williams@example.com",
            phone="+1-555-0104",
            address="321 Elm St, Seattle, WA 98101",
            company="Cloud Systems",
            position="DevOps Engineer",
            notes="Cloud infrastructure and CI/CD expert"
        ),
        FormData(
            uuid=str(uuid.uuid4()),
            name="Charlie Brown",
            email="charlie.brown@example.com",
            phone="+1-555-0105",
            address="654 Maple Dr, Boston, MA 02101",
            company="Marketing Solutions",
            position="Product Manager",
            notes="10+ years in product development and strategy"
        )
    ]
    
    db.add_all(demo_data)
    db.commit()
    db.close()
    
    print(f"✓ Seeded database with {len(demo_data)} demo records")
