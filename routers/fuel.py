from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import FuelEntry
from pydantic import BaseModel
from typing import Optional
from datetime import date
import uuid

router = APIRouter(prefix="/fuel", tags=["Fuel"])

class FuelCreate(BaseModel):
    vehicle_id: Optional[uuid.UUID] = None
    fuel_date: Optional[date] = None
    litres: Optional[float] = None
    cost: Optional[float] = None
    fuel_station: Optional[str] = None
    payment_mode: Optional[str] = None

@router.get("/")
def get_fuel_entries(db: Session = Depends(get_db)):
    return db.query(FuelEntry).all()

@router.post("/")
def create_fuel_entry(fuel: FuelCreate, db: Session = Depends(get_db)):
    db_fuel = FuelEntry(**fuel.model_dump())
    db.add(db_fuel)
    db.commit()
    db.refresh(db_fuel)
    return db_fuel

@router.put("/{fuel_id}")
def update_fuel_entry(fuel_id: uuid.UUID, fuel: FuelCreate, db: Session = Depends(get_db)):
    db_fuel = db.query(FuelEntry).filter(FuelEntry.fuel_id == fuel_id).first()
    if not db_fuel:
        raise HTTPException(status_code=404, detail="Fuel entry not found")
    for key, value in fuel.model_dump().items():
        setattr(db_fuel, key, value)
    db.commit()
    db.refresh(db_fuel)
    return db_fuel

@router.delete("/{fuel_id}")
def delete_fuel_entry(fuel_id: uuid.UUID, db: Session = Depends(get_db)):
    db_fuel = db.query(FuelEntry).filter(FuelEntry.fuel_id == fuel_id).first()
    if not db_fuel:
        raise HTTPException(status_code=404, detail="Fuel entry not found")
    db.delete(db_fuel)
    db.commit()
    return {"message": "Fuel entry deleted"}