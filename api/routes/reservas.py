from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import api.schemas as schemas
from api.crud import crud_reserva
from api.database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.Reserva)
def create_reserva(reserva: schemas.ReservaCreate, db: Session = Depends(get_db)):
    return crud_reserva.create_reserva(db=db, reserva=reserva)


@router.get("/{reserva_id}", response_model=schemas.Reserva)
def read_reserva(reserva_id: int, db: Session = Depends(get_db)):
    db_reserva = crud_reserva.get_reserva(db=db, reserva_id=reserva_id)
    if db_reserva is None:
        raise HTTPException(status_code=404, detail="Reserva not found")
    return db_reserva


@router.get("/", response_model=list[schemas.Reserva])
def read_reservas(db: Session = Depends(get_db)):
    return crud_reserva.get_reservas(db=db)


@router.put("/{reserva_id}", response_model=schemas.Reserva)
def update_reserva(
    reserva_id: int,
    reserva_update: schemas.ReservaUpdate,
    db: Session = Depends(get_db),
):
    db_reserva = crud_reserva.update_reserva(
        db=db, reserva_id=reserva_id, reserva_update=reserva_update
    )
    if db_reserva is None:
        raise HTTPException(status_code=404, detail=f"Reserva '{reserva_id}' not found")
    return db_reserva


@router.delete("/{reserva_id}", response_model=schemas.Reserva)
def delete_reserva(reserva_id: int, db: Session = Depends(get_db)):
    db_reserva = crud_reserva.delete_reserva(db=db, reserva_id=reserva_id)
    if db_reserva is None:
        raise HTTPException(status_code=404, detail=f"Reserva '{reserva_id}' not found")
    return db_reserva
