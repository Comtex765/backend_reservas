from sqlalchemy.orm import Session
from api.models import Historial
from api import schemas
from datetime import datetime, date
from sqlalchemy import func


def create_historial(db: Session, historial: schemas.HistorialCreate):
    db_historial = Historial(
        id_reserva=historial.id_reserva,
        id_usuario=historial.id_usuario,
        id_laboratorio=historial.id_laboratorio,
    )
    db.add(db_historial)
    db.commit()
    db.refresh(db_historial)
    return db_historial


def get_historial(db: Session, historial_id: int):
    return db.query(Historial).filter(Historial.id_historial == historial_id).first()


def get_historiales(db: Session):
    return db.query(Historial).all()


def update_historial(
    db: Session, historial_id: int, historial_update: schemas.HistorialUpdate
):
    db_historial = (
        db.query(Historial).filter(Historial.id_historial == historial_id).first()
    )
    if db_historial:
        for key, value in historial_update.dict(exclude_unset=True).items():
            setattr(db_historial, key, value)  # Update each attribute with new value
        db.commit()
        db.refresh(db_historial)
    return db_historial


def delete_historial(db: Session, historial_id: int):
    db_historial = (
        db.query(Historial).filter(Historial.id_historial == historial_id).first()
    )
    if db_historial:
        db.delete(db_historial)
        db.commit()
    return db_historial


def get_historial_por_usuario_laboratorio(
    db: Session, usuario_id: int, laboratorio_id: int
):
    return (
        db.query(Historial)
        .filter(
            Historial.id_usuario == usuario_id,
            Historial.id_laboratorio == laboratorio_id,
        )
        .all()
    )


def reporte_uso_laboratorios(db: Session):
    today = date.today()
    start_of_year = datetime(today.year, 1, 1)
    end_of_year = datetime(today.year, 12, 31)

    return (
        db.query(
            Historial.id_laboratorio,
            func.count(Historial.id_historial).label("total_reservas"),
            func.sum(
                func.date_trunc("second", Historial.hora_fin - Historial.hora_inicio)
            ).label("total_tiempo_reserva"),
        )
        .filter(Historial.fecha >= start_of_year, Historial.fecha <= end_of_year)
        .group_by(Historial.id_laboratorio)
        .all()
    )
