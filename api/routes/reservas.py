from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import api.schemas as schemas
from api.crud import crud_reserva
from api.crud import crud_usuario
from api.database import get_db
from api.email import sender_confirmation

router = APIRouter()


@router.post("/", response_model=schemas.Reserva)
async def create_reserva(reserva: schemas.ReservaCreate, db: Session = Depends(get_db)):
    reserva = crud_reserva.create_reserva(db=db, reserva=reserva)
    user = crud_usuario.get_usuario(db=db, usuario_id=reserva.id_usuario)
    if reserva is not None:
        sender_confirmation.enviar_correo(
            email_receiver=user.correo,
            nombre_usuario=user.usuario,
            fecha=reserva.fecha,
            ini=reserva.hora_inicio,
            fin=reserva.hora_fin,
        )
    return reserva

    return user


@router.get("/{reserva_id}", response_model=schemas.Reserva)
async def read_reserva(reserva_id: int, db: Session = Depends(get_db)):
    db_reserva = crud_reserva.get_reserva(db=db, reserva_id=reserva_id)
    if db_reserva is None:
        raise HTTPException(status_code=404, detail="Reserva not found")
    return db_reserva


@router.get("/", response_model=list[schemas.Reserva])
async def read_reservas(db: Session = Depends(get_db)):
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
