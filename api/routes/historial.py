from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import api.schemas as schemas
from api.crud import crud_historial

from api.database import get_db


router = APIRouter()


@router.post("", response_model=schemas.Historial)
def create_historial(historial: schemas.HistorialCreate, db: Session = Depends(get_db)):
    return crud_historial.create_historial(db=db, historial=historial)


@router.get("/{historial_id}", response_model=schemas.Historial)
def read_historial(historial_id: int, db: Session = Depends(get_db)):
    db_historial = crud_historial.get_historial(db=db, historial_id=historial_id)
    if db_historial is None:
        raise HTTPException(status_code=404, detail="Historial not found")
    return db_historial


@router.get("/", response_model=list[schemas.Historial])
def read_historiales(db: Session = Depends(get_db)):
    return crud_historial.get_historiales(db=db)


@router.put("/{historial_id}", response_model=schemas.Historial)
def update_historial(
    historial_id: int,
    historial_update: schemas.HistorialUpdate,
    db: Session = Depends(get_db),
):
    db_historial = crud_historial.update_historial(
        db=db, historial_id=historial_id, historial_update=historial_update
    )
    if db_historial is None:
        raise HTTPException(
            status_code=404, detail=f"Historial '{historial_id}' not found"
        )
    return db_historial


@router.delete("/{historial_id}", response_model=schemas.Historial)
def delete_historial(historial_id: int, db: Session = Depends(get_db)):
    db_historial = crud_historial.delete_historial(db=db, historial_id=historial_id)
    if db_historial is None:
        raise HTTPException(
            status_code=404, detail=f"Historial '{historial_id}' not found"
        )
    return db_historial
