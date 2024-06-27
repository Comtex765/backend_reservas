from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.crud import crud_historial
from ..database import get_db

router = APIRouter()


@router.get("/reporte_uso_laboratorios")
def reporte_uso_laboratorios(db: Session = Depends(get_db)):
    reporte = crud_historial.reporte_uso_laboratorios(db=db)
    return reporte


@router.get("/historial_por_laboratorio")
def historial_por_laboratorio(laboratorio_id: int, db: Session = Depends(get_db)):
    historial = crud_historial.get_historial_por_laboratorio(
        db=db, laboratorio_id=laboratorio_id
    )
    if not historial:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró historial para laboratorio_id={laboratorio_id}",
        )
    return [
        {
            "historial": {
                "id_historial": h.Historial.id_historial,
                "id_reserva": h.Historial.id_reserva,
                "id_usuario": h.Historial.id_usuario,
                "id_laboratorio": h.Historial.id_laboratorio,
            },
            "usuario": {
                "id_usuario": h.Usuario.id_usuario,
                "nombre": h.Usuario.nombre,
                "apellido": h.Usuario.apellido,
                "correo": h.Usuario.correo,
                "usuario": h.Usuario.usuario,
                "celular": h.Usuario.celular,
            },
            "laboratorio": {
                "id_laboratorio": h.Laboratorio.id_laboratorio,
                "nombre": h.Laboratorio.nombre_lab,
                "equipos": h.Laboratorio.equipos,
                "capacidad": h.Laboratorio.capacidad,
            },
        }
        for h in historial
    ]


@router.get("/historial_por_usuario")
def historial_por_usuario(usuario_id: int, db: Session = Depends(get_db)):
    historial = crud_historial.get_historial_por_usuario(db=db, usuario_id=usuario_id)
    if not historial:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró historial para usuario_id={usuario_id}",
        )
    return [
        {
            "historial": {
                "id_historial": h.Historial.id_historial,
                "id_reserva": h.Historial.id_reserva,
                "id_usuario": h.Historial.id_usuario,
                "id_laboratorio": h.Historial.id_laboratorio,
            },
            "usuario": {
                "id_usuario": h.Usuario.id_usuario,
                "nombre": h.Usuario.nombre,
                "apellido": h.Usuario.apellido,
                "correo": h.Usuario.correo,
                "usuario": h.Usuario.usuario,
                "celular": h.Usuario.celular,
            },
            "laboratorio": {
                "id_laboratorio": h.Laboratorio.id_laboratorio,
                "nombre": h.Laboratorio.nombre_lab,
                "equipos": h.Laboratorio.equipos,
                "capacidad": h.Laboratorio.capacidad,
            },
        }
        for h in historial
    ]
