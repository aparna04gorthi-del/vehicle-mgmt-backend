from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Vehicle
from auth_utils import get_current_user, require_roles
from pydantic import BaseModel
from typing import Optional
from datetime import date
import uuid

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

class VehicleCreate(BaseModel):
    registration_no: str
    vehicle_type: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    chassis_no: Optional[str] = None
    engine_no: Optional[str] = None
    ownership_type: Optional[str] = None
    status: Optional[str] = None
    assigned_site: Optional[str] = None
    rc_no: Optional[str] = None
    rc_expiry: Optional[date] = None

# READ - fleet_manager, admin, site_manager can view
@router.get("/")
def get_vehicles(db: Session = Depends(get_db), current_user=Depends(require_roles('admin', 'fleet_manager', 'site_manager'))):
    if current_user.role == 'site_manager':
        return db.query(Vehicle).filter(Vehicle.assigned_site == current_user.assigned_site).all()
    return db.query(Vehicle).all()

# CREATE - only admin and fleet_manager
@router.post("/")
def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db), current_user=Depends(require_roles('admin', 'fleet_manager'))):
    db_vehicle = Vehicle(**vehicle.model_dump())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

# UPDATE - only admin and fleet_manager
@router.put("/{vehicle_id}")
def update_vehicle(vehicle_id: uuid.UUID, vehicle: VehicleCreate, db: Session = Depends(get_db), current_user=Depends(require_roles('admin', 'fleet_manager'))):
    db_vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()
    if not db_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    for key, value in vehicle.model_dump().items():
        setattr(db_vehicle, key, value)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

# DELETE - only admin
@router.delete("/{vehicle_id}")
def delete_vehicle(vehicle_id: uuid.UUID, db: Session = Depends(get_db), current_user=Depends(require_roles('admin'))):
    db_vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()
    if not db_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    db.delete(db_vehicle)
    db.commit()
    return {"message": "Vehicle deleted"}