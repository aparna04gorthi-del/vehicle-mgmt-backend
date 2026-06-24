from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Compliance
from pydantic import BaseModel
from typing import Optional
from datetime import date
import uuid

router = APIRouter(prefix="/compliance", tags=["Compliance"])

class ComplianceCreate(BaseModel):
    vehicle_id: Optional[uuid.UUID] = None
    insurance_expiry: Optional[date] = None
    fitness_expiry: Optional[date] = None
    pollution_expiry: Optional[date] = None
    permit_expiry: Optional[date] = None
    remarks: Optional[str] = None

@router.get("/")
def get_compliance(db: Session = Depends(get_db)):
    return db.query(Compliance).all()

@router.post("/")
def create_compliance(compliance: ComplianceCreate, db: Session = Depends(get_db)):
    db_compliance = Compliance(**compliance.model_dump())
    db.add(db_compliance)
    db.commit()
    db.refresh(db_compliance)
    return db_compliance

@router.put("/{compliance_id}")
def update_compliance(compliance_id: uuid.UUID, compliance: ComplianceCreate, db: Session = Depends(get_db)):
    db_compliance = db.query(Compliance).filter(Compliance.compliance_id == compliance_id).first()
    if not db_compliance:
        raise HTTPException(status_code=404, detail="Compliance record not found")
    for key, value in compliance.model_dump().items():
        setattr(db_compliance, key, value)
    db.commit()
    db.refresh(db_compliance)
    return db_compliance

@router.delete("/{compliance_id}")
def delete_compliance(compliance_id: uuid.UUID, db: Session = Depends(get_db)):
    db_compliance = db.query(Compliance).filter(Compliance.compliance_id == compliance_id).first()
    if not db_compliance:
        raise HTTPException(status_code=404, detail="Compliance record not found")
    db.delete(db_compliance)
    db.commit()
    return {"message": "Compliance record deleted"}