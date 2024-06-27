import os
from fastapi import FastAPI, Depends, HTTPException
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from . import models
from . import schemas
from . import crud
from .database import get_db

load_dotenv()


app = FastAPI()


@app.get("/")
def route():
    return {"success": "True"}

@app.post("/usuarios/", response_model=schemas.Usuario)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    # Obtener el tipo de usuario desde el cuerpo de la solicitud
    tipo_usuario = usuario.id_tipo

    # Verificar si el tipo de usuario existe en la base de datos
    db_tipo_usuario = db.query(models.TipoUsuario).filter(models.TipoUsuario.id_tipo == tipo_usuario).first()
    if not db_tipo_usuario:
        raise HTTPException(status_code=404, detail="Tipo de usuario no encontrado")

    # Crear el usuario en la base de datos
    return crud.create_usuario(db=db, usuario=usuario)

@app.get("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def read_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = crud.get_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return db_usuario

@app.get("/usuarios/", response_model=list[schemas.Usuario])
def read_usuarios(db: Session = Depends(get_db)):
    usuarios = crud.get_usuarios(db)
    return usuarios

@app.put("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def update_usuario(usuario_id: int, usuario: schemas.UsuarioUpdate, db: Session = Depends(get_db)):
    db_usuario = crud.get_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return crud.update_usuario(db=db, usuario_id=usuario_id, usuario=usuario)

@app.delete("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = crud.get_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return crud.delete_usuario(db=db, usuario_id=usuario_id)