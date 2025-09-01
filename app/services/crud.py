from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, TimeoutError, IntegrityError
from fastapi import HTTPException, status
from .. import models, schemas

def get_leads(db: Session, skip: int = 0, limit: int = 100):
    try:
        query = (
            db.query(models.Lead)
            .offset(skip)
            .limit(limit)
            .execution_options(timeout=10)
        )
        leads = query.all()
        return leads
    except TimeoutError:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="La consulta a la base de datos excedió el tiempo límite.",
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al consultar leads: {str(e)}",
        )


def create_lead(db: Session, lead: schemas.LeadCreate):
    try:
        db_lead = models.Lead(**lead.dict())
        db.add(db_lead)
        db.commit()
        db.refresh(db_lead)
        return db_lead
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El lead ya existe o los datos son inválidos.",
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el lead: {str(e)}",
        )

def delete_lead(db: Session, lead_id: int):
    try:
        db_lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
        if not db_lead:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Lead con id {lead_id} no encontrado."
            )

        db.delete(db_lead)
        db.commit()
        return {"message": f"Lead con id {lead_id} eliminado correctamente."}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el lead: {str(e)}"
        )
