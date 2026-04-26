import math
import datetime
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from geoalchemy2 import Geometry

Base = declarative_base()

# --- APRIL 12: MATCH EVENT SCHEMA (Tracking Data) ---
class MatchEvent(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    player_id = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    location = Column(Geometry('POINT'), index=True) # Added Index for performance
    velocity_mag = Column(Float)   
    velocity_theta = Column(Float) 
    orientation = Column(Float)   # Added for YOLO-OBB body heading (0-360 degrees)

# --- APRIL 23: TRAJECTORY SCHEMA (High-Dimensional Flow) ---
class PlayerTrajectory(Base):
    __tablename__ = 'trajectories'
    id = Column(Integer, primary_key=True)
    player_id = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    path = Column(Geometry('LINESTRING'), index=True) # Added Index for performance

# --- APRIL 23: CAREER STATS SCHEMA (Historical Context) ---
class PlayerCareerStats(Base):
    __tablename__ = 'career_stats'
    id = Column(Integer, primary_key=True)
    player_name = Column(String)
    season = Column(String)
    team = Column(String)
    apps = Column(Integer)
    minutes = Column(Integer)
    goals = Column(Integer)
    assists = Column(Integer)
    xg = Column(Float)
    xa = Column(Float)
    xg90 = Column(Float)

# --- APRIL 11: UNDERSTAT SHOT SCHEMA (Event Data) ---
# This is the "Blueprint" the scraper was looking for!
class UnderstatShot(Base):
    __tablename__ = 'understat_shots'
    id = Column(String, primary_key=True) # Understat provides unique IDs
    minute = Column(Integer)
    player = Column(String)
    team = Column(String)
    result = Column(String)        # e.g., 'Goal', 'Saved', 'Missed'
    xg = Column(Float)             # Expected Goals
    location = Column(Geometry('POINT'), index=True) # Added Index

# --- DATABASE CONNECTION ---
DB_URL = 'postgresql://monish_admin:omnipath_password@db:5432/football_analytics'
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()

# --- VECTOR MATH ENGINE ---
def get_vector(p1, p2, dt):
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    dist = math.sqrt(dx**2 + dy**2)
    velocity = dist / dt
    theta = math.degrees(math.atan2(dy, dx))
    return round(velocity, 2), round(theta, 2)

if __name__ == "__main__":
    # Create all tables (events AND understat_shots)
    print("⏳ Synchronizing schemas with PostGIS...")
    Base.metadata.create_all(engine)
    print("✅ Schema sync complete! Tables 'events' and 'understat_shots' are ready.")

    # Simple sanity check ingestion
    test_shot = session.query(UnderstatShot).first()
    if test_shot:
        print(f"📊 Database Status: Active. Found {session.query(UnderstatShot).count()} shots in storage.")
    else:
        print("Empty database detected. Ready for the Understat Season Scraper.")