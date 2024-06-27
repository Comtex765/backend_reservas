from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud_historial
from ..database import get_db
from ..schemas import Historial

router = APIRouter()


@router.get("/historial_por_usuario_laboratorio")
def historial_por_usuario_laboratorio(
    usuario_id: int, laboratorio_id: int, db: Session = Depends(get_db)
):
    historial = crud_historial.get_historial_por_usuario_laboratorio(
        db=db, usuario_id=usuario_id, laboratorio_id=laboratorio_id
    )
    if not historial:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró historial para usuario_id={usuario_id} y laboratorio_id={laboratorio_id}",
        )
    return historial


@router.get("/reporte_uso_laboratorios")
def reporte_uso_laboratorios(db: Session = Depends(get_db)):
    reporte = crud_historial.reporte_uso_laboratorios(db=db)
    return reporte
