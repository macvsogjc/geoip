from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

db = SQLAlchemy()

class IPGeolocation(Base):
    __tablename__ = 'geolocations'
    id = db.Column(db.Integer, primary_key=True, index=True)
    ip = db.Column(db.String, unique=True, index=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    country = db.Column(db.String)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def extract_ips(df):
    return df.iloc[:, 0].dropna().tolist()

def save_geolocations(db, geolocations):
    db.bulk_save_objects([IPGeolocation(**geo) for geo in geolocations])
    db.commit()

def analyze_geolocations(geolocations):
    total_ips = len(geolocations)
    countries = list(set([g['country'] for g in geolocations]))
    return {
        'totalIPs': total_ips,
        'countries': countries
    }

Base.metadata.create_all(bind=engine)
