from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
from routers import vehicles, drivers, trips, fuel, maintenance, compliance, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vehicle Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(vehicles.router)
app.include_router(drivers.router)
app.include_router(trips.router)
app.include_router(fuel.router)
app.include_router(maintenance.router)
app.include_router(compliance.router)

@app.get("/")
def root():
    return {"message": "Vehicle Management System API is running"}