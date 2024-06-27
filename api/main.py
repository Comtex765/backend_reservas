from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from . import models, schemas, jwt_utils
from api.crud import crud_usuario, crud_laboratorio
from .database import get_db

load_dotenv()


app = FastAPI()


@app.get("/")
def route():
    return {"success": "True"}

# OAuth2 esquema de seguridad
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Ruta para obtener el token JWT
@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = crud_usuario.authenticate_usuario(db, form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = jwt_utils.create_access_token(data={"sub": usuario.usuario})
    return {"access_token": access_token}

@app.get("/usuarios/me", response_model=schemas.Usuario)
def read_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = jwt_utils.verify_token(token)
    usuario_id = payload.get("sub")
    usuario = crud_usuario.get_usuario_by_username(db, usuario_id)
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return usuario

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

@app.get("/usuarios/{username}", response_model=schemas.Usuario)
def read_usuario(username: str, db: Session = Depends(get_db)):
    usuario = crud_usuario.get_usuario_by_username(db, username)
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return usuario

@app.get("/usuarios/", response_model=list[schemas.Usuario])
def read_usuarios(db: Session = Depends(get_db)):
    usuarios = crud_usuario.get_usuarios(db)
    return usuarios

@app.put("/usuarios/{username}", response_model=schemas.Usuario)
def update_usuario(username: str, usuario_update: schemas.UsuarioUpdate, db: Session = Depends(get_db)):
    updated_usuario = crud_usuario.update_usuario(db, username, usuario_update)
    if updated_usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User '{username}' not found")
    return updated_usuario

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