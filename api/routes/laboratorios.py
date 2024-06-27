from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import api.schemas as schemas
from api.crud import crud_laboratorio

from api.database import get_db

router = APIRouter()


@router.get("/", response_model=list[schemas.Laboratorio])
def read_laboratorios(db: Session = Depends(get_db)):
    return crud_laboratorio.get_laboratorios(db=db)

@router.get("/{lab}", response_model=schemas.Laboratorio)
def read_usuario(lab: str, db: Session = Depends(get_db)):
    usuario = crud_laboratorio.get_laboratorio_by_name(db, lab)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return usuario


@router.post("/", response_model=schemas.Laboratorio)
def create_laboratorio(
    laboratorio: schemas.LaboratorioCreate, db: Session = Depends(get_db)
):
    return crud_laboratorio.create_laboratorio(db=db, laboratorio=laboratorio)


@router.put("/{laboratorio_id}", response_model=schemas.Laboratorio)
def update_laboratorio(
    laboratorio_id: int,
    laboratorio: schemas.LaboratorioUpdate,
    db: Session = Depends(get_db),
):
    return crud_laboratorio.update_laboratorio(
        db=db, laboratorio_id=laboratorio_id, laboratorio=laboratorio
    )


@router.delete("/{laboratorio_id}", response_model=schemas.Laboratorio)
def delete_laboratorio(laboratorio_id: int, db: Session = Depends(get_db)):
    return crud_laboratorio.delete_laboratorio(db=db, laboratorio_id=laboratorio_id)
