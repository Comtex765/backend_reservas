from sqlalchemy.orm import Session
from api.models import Reserva
from api import schemas


def create_reserva(db: Session, reserva: schemas.ReservaCreate):
    db_reserva = Reserva(
        id_usuario=reserva.id_usuario,
        id_laboratorio=reserva.id_laboratorio,
        id_estado=reserva.id_estado,
        fecha=reserva.fecha,
        hora_inicio=reserva.hora_inicio,
        hora_fin=reserva.hora_fin,
    )
    db.add(db_reserva)
    db.commit()
    db.refresh(db_reserva)
    return db_reserva


def get_reserva(db: Session, reserva_id: int):
    return db.query(Reserva).filter(Reserva.id_reserva == reserva_id).first()


def get_reservas(db: Session):
    return db.query(Reserva).all()


def update_reserva(db: Session, reserva_id: int, reserva_update: schemas.ReservaUpdate):
    db_reserva = db.query(Reserva).filter(Reserva.id_reserva == reserva_id).first()
    if db_reserva:
        for key, value in reserva_update.dict().items():
            setattr(db_reserva, key, value)  # Update each attribute with new value
        db.commit()
        db.refresh(db_reserva)
    return db_reserva


def delete_reserva(db: Session, reserva_id: int):
    db_reserva = db.query(Reserva).filter(Reserva.id_reserva == reserva_id).first()
    if db_reserva:
        db.delete(db_reserva)
        db.commit()
    return db_reserva