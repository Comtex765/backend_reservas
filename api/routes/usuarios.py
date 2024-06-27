from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import api.models as models
import api.schemas as schemas
from api.crud import crud_usuario
from api.email import email_sender

from api.database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.Usuario)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    tipo_usuario = usuario.id_tipo
    db_tipo_usuario = (
        db.query(models.TipoUsuario)
        .filter(models.TipoUsuario.id_tipo == tipo_usuario)
        .first()
    )
    if not db_tipo_usuario:
        raise HTTPException(status_code=404, detail="Tipo de usuario no encontrado")

    user = crud_usuario.create_usuario(db=db, usuario=usuario)
    if user is not None:
        email_sender.enviar_correo(
            email_receiver=user.correo, nombre_usuario=user.usuario
        )
    return user


@router.get("/{username}", response_model=schemas.Usuario)
def read_usuario(username: str, db: Session = Depends(get_db)):
    usuario = crud_usuario.get_usuario_by_username(db, username)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return usuario


@router.get("/", response_model=list[schemas.Usuario])
def read_usuarios(db: Session = Depends(get_db)):
    usuarios = crud_usuario.get_usuarios(db)
    return usuarios


@router.put("/{username}", response_model=schemas.Usuario)
def update_usuario(
    username: str, usuario_update: schemas.UsuarioUpdate, db: Session = Depends(get_db)
):
    updated_usuario = crud_usuario.update_usuario(db, username, usuario_update)
    if updated_usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User '{username}' not found"
        )
    return updated_usuario


@router.delete("/{usuario_id}", response_model=schemas.Usuario)
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = crud_usuario.get_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return crud_usuario.delete_usuario(db=db, usuario_id=usuario_id)
