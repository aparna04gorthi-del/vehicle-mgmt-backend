from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Trip
from pydantic import BaseModel
from typing import Optional
from datetime import date
import uuid

router = APIRouter(prefix="/trips", tags=["Trips"])

class TripCreate(BaseModel):
    vehicle_id: Optional[uuid.UUID] = None
    driver_id: Optional[uuid.UUID] = None
    start_location: Optional[str] = None
    end_location: Optional[str] = None
    start_km: Optional[float] = None
    end_km: Optional[float] = None
    trip_date: Optional[date] = None
    status: Optional[str] = None

@router.get("/")
def get_trips(db: Session = Depends(get_db)):
    return db.query(Trip).all()

@router.post("/")
def create_trip(trip: TripCreate, db: Session = Depends(get_db)):
    db_trip = Trip(**trip.model_dump())
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip

@router.put("/{trip_id}")
def update_trip(trip_id: uuid.UUID, trip: TripCreate, db: Session = Depends(get_db)):
    db_trip = db.query(Trip).filter(Trip.trip_id == trip_id).first()
    if not db_trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    for key, value in trip.model_dump().items():
        setattr(db_trip, key, value)
    db.commit()
    db.refresh(db_trip)
    return db_trip

@router.delete("/{trip_id}")
def delete_trip(trip_id: uuid.UUID, db: Session = Depends(get_db)):
    db_trip = db.query(Trip).filter(Trip.trip_id == trip_id).first()
    if not db_trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    db.delete(db_trip)
    db.commit()
    return {"message": "Trip deleted"}