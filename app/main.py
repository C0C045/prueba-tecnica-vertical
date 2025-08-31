from fastapi import FastAPI
from .routers import leads, external
from .database import Base, engine

app = FastAPI()

app.include_router(leads.router, prefix="/leads", tags=["Leads"])
app.include_router(external.router, prefix="/external-data", tags=["External API"])

@app.get("/")
def root():
    return {"message": "API corriendo 🚀"}

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
