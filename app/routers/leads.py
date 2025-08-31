from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas
from ..database import get_db
from ..services import crud as crud_leads

router = APIRouter()

@router.get("/", response_model=list[schemas.Lead])
def read_leads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_leads.get_leads(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.Lead)
def create_lead(lead: schemas.LeadCreate, db: Session = Depends(get_db)):
    return crud_leads.create_lead(db=db, lead=lead)
