from sqlalchemy.orm import Session
from api.models import Laboratorio
from api import models, schemas


def get_laboratorios(db: Session):
    return db.query(Laboratorio).all()

def get_laboratorio_by_name(db: Session, lab: str):
    return db.query(Laboratorio).filter(Laboratorio.nombre_lab == lab).first()


def create_laboratorio(db: Session, laboratorio: schemas.LaboratorioCreate):
    db_laboratorio = models.Laboratorio(
        nombre_lab=laboratorio.nombre_lab,
        capacidad=laboratorio.capacidad,
        equipos=laboratorio.equipos,
    )
    db.add(db_laboratorio)
    db.commit()
    db.refresh(db_laboratorio)
    return db_laboratorio


def update_laboratorio(
    db: Session, laboratorio_id: int, laboratorio: schemas.LaboratorioUpdate
):
    db_laboratorio = (
        db.query(Laboratorio)
        .filter(Laboratorio.id_laboratorio == laboratorio_id)
        .first()
    )
    if db_laboratorio:
        for key, value in laboratorio.dict(exclude_unset=True).items():
            setattr(db_laboratorio, key, value)
        db.commit()
        db.refresh(db_laboratorio)
    return db_laboratorio


def delete_laboratorio(db: Session, laboratorio_id: int):
    db_laboratorio = (
        db.query(Laboratorio)
        .filter(Laboratorio.id_laboratorio == laboratorio_id)
        .first()
    )
    if db_laboratorio:
        db.delete(db_laboratorio)
        db.commit()
    return db_laboratorio
