from sqlalchemy import Column, String, Integer, Numeric, Date, Text, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    full_name = Column(String)
    assigned_site = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Vehicle(Base):
    __tablename__ = "vehicles"
    __table_args__ = {'extend_existing': True}
    vehicle_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    registration_no = Column(String, unique=True, nullable=False)
    vehicle_type = Column(String)
    make = Column(String)
    model = Column(String)
    year = Column(Integer)
    chassis_no = Column(String)
    engine_no = Column(String)
    ownership_type = Column(String)
    status = Column(String)
    assigned_site = Column(String)
    rc_no = Column(String)
    rc_expiry = Column(Date)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Driver(Base):
    __tablename__ = "drivers"
    __table_args__ = {'extend_existing': True}
    driver_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    phone = Column(String)
    license_no = Column(String)
    license_expiry = Column(Date)
    address = Column(Text)
    status = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Trip(Base):
    __tablename__ = "trips"
    __table_args__ = {'extend_existing': True}
    trip_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.vehicle_id"))
    driver_id = Column(UUID(as_uuid=True), ForeignKey("drivers.driver_id"))
    start_location = Column(String)
    end_location = Column(String)
    start_km = Column(Numeric)
    end_km = Column(Numeric)
    trip_date = Column(Date)
    status = Column(String)

class FuelEntry(Base):
    __tablename__ = "fuel_entries"
    __table_args__ = {'extend_existing': True}
    fuel_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.vehicle_id"))
    date = Column(Date)
    litres = Column(Numeric)
    cost = Column(Numeric)
    fuel_station = Column(String)
    payment_mode = Column(String)

class Maintenance(Base):
    __tablename__ = "maintenance"
    __table_args__ = {'extend_existing': True}
    maintenance_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.vehicle_id"))
    service_type = Column(String)
    service_date = Column(Date)
    cost = Column(Numeric)
    vendor = Column(String)
    remarks = Column(Text)

class Compliance(Base):
    __tablename__ = "compliance"
    __table_args__ = {'extend_existing': True}
    compliance_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.vehicle_id"))
    insurance_expiry = Column(Date)
    fitness_expiry = Column(Date)
    pollution_expiry = Column(Date)
    permit_expiry = Column(Date)
    remarks = Column(Text)