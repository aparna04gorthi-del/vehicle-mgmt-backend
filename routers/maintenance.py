from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Maintenance
from pydantic import BaseModel
from typing import Optional
from datetime import date
import uuid

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])

class MaintenanceCreate(BaseModel):
    vehicle_id: Optional[uuid.UUID] = None
    service_type: Optional[str] = None
    service_date: Optional[date] = None
    cost: Optional[float] = None
    vendor: Optional[str] = None
    remarks: Optional[str] = None

@router.get("/")
def get_maintenance(db: Session = Depends(get_db)):
    return db.query(Maintenance).all()

@router.post("/")
def create_maintenance(maintenance: MaintenanceCreate, db: Session = Depends(get_db)):
    db_maintenance = Maintenance(**maintenance.model_dump())
    db.add(db_maintenance)
    db.commit()
    db.refresh(db_maintenance)
    return db_maintenance

@router.put("/{maintenance_id}")
def update_maintenance(maintenance_id: uuid.UUID, maintenance: MaintenanceCreate, db: Session = Depends(get_db)):
    db_maintenance = db.query(Maintenance).filter(Maintenance.maintenance_id == maintenance_id).first()
    if not db_maintenance:
        raise HTTPException(status_code=404, detail="Maintenance record not found")
    for key, value in maintenance.model_dump().items():
        setattr(db_maintenance, key, value)
    db.commit()
    db.refresh(db_maintenance)
    return db_maintenance

@router.delete("/{maintenance_id}")
def delete_maintenance(maintenance_id: uuid.UUID, db: Session = Depends(get_db)):
    db_maintenance = db.query(Maintenance).filter(Maintenance.maintenance_id == maintenance_id).first()
    if not db_maintenance:
        raise HTTPException(status_code=404, detail="Maintenance record not found")
    db.delete(db_maintenance)
    db.commit()
    return {"message": "Maintenance record deleted"}