import os
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import jwt
from . import schemas
from . import crud
from .database import get_db, test_db_connection
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


app = FastAPI()
test_db_connection()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.get("/")
def route():
    return {"success": "True"}


@app.post("/usuarios/", response_model=schemas.Usuario)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = crud.get_usuario_by_usuario(db, usuario.usuario)
    if db_usuario:
        raise HTTPException(status_code=400, detail="Usuario ya registrado")
    return crud.create_usuario(db=db, usuario=usuario)


@app.post("/token", response_model=schemas.Token)
def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    usuario = crud.get_usuario_by_usuario(db, form_data.username)
    if not usuario or not crud.verify_password(form_data.password, usuario.contraseña):
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": usuario.usuario}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/usuarios/", response_model=list[schemas.Usuario])
def read_usuarios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    usuarios = crud.get_usuarios(db, skip=skip, limit=limit)
    return usuarios


@app.get("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def read_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = crud.get_usuario_by_id(db, usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario


@app.put("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def update_usuario(
    usuario_id: int, usuario: schemas.UsuarioUpdate, db: Session = Depends(get_db)
):
    db_usuario = crud.get_usuario_by_id(db, usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return crud.update_usuario(db=db, usuario_id=usuario_id, usuario=usuario)


@app.delete("/usuarios/{usuario_id}", response_model=schemas.Usuario)
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = crud.get_usuario_by_id(db, usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return crud.delete_usuario(db=db, usuario_id=usuario_id)
