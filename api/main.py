from fastapi import FastAPI, Depends, HTTPException
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from . import models
from . import schemas
from api.crud import crud_usuario, crud_laboratorio
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
    return crud_usuario.create_usuario(db=db, usuario=usuario)

@app.get("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def read_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = crud_usuario.get_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return db_usuario

@app.get("/usuarios/", response_model=list[schemas.Usuario])
def read_usuarios(db: Session = Depends(get_db)):
    usuarios = crud_usuario.get_usuarios(db)
    return usuarios

@app.put("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def update_usuario(usuario_id: int, usuario: schemas.UsuarioUpdate, db: Session = Depends(get_db)):
    db_usuario = crud_usuario.get_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return crud_usuario.update_usuario(db=db, usuario_id=usuario_id, usuario=usuario)

@app.delete("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = crud_usuario.get_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return crud_usuario.delete_usuario(db=db, usuario_id=usuario_id)


@app.get("/laboratorios/", response_model=list[schemas.Laboratorio])
def read_laboratorios(db: Session = Depends(get_db)):
    return crud_laboratorio.get_laboratorios(db=db)

@app.post("/laboratorios/", response_model=schemas.Laboratorio)
def create_laboratorio(laboratorio: schemas.LaboratorioCreate, db: Session = Depends(get_db)):
    return crud_laboratorio.create_laboratorio(db=db, laboratorio=laboratorio)

@app.put("/laboratorios/{laboratorio_id}", response_model=schemas.Laboratorio)
def update_laboratorio(laboratorio_id: int, laboratorio: schemas.LaboratorioUpdate, db: Session = Depends(get_db)):
    return crud_laboratorio.update_laboratorio(db=db, laboratorio_id=laboratorio_id, laboratorio=laboratorio)

@app.delete("/laboratorios/{laboratorio_id}", response_model=schemas.Laboratorio)
def delete_laboratorio(laboratorio_id: int, db: Session = Depends(get_db)):
    return crud_laboratorio.delete_laboratorio(db=db, laboratorio_id=laboratorio_id)