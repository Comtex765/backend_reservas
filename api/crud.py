from .models import Usuario
from sqlalchemy.orm import Session
from .schemas import UsuarioCreate, UsuarioUpdate

def get_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()

def get_usuario_by_username(db: Session, username: str):
    return db.query(Usuario).filter(Usuario.usuario == username).first()

def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Usuario).offset(skip).limit(limit).all()

def create_usuario(db: Session, usuario: UsuarioCreate):
    db_usuario = Usuario(
        id_tipo=usuario.id_tipo,
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        correo=usuario.correo,
        usuario=usuario.usuario,
        contrasena=usuario.contrasena,
        celular=usuario.celular
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def update_usuario(db: Session, usuario_id: int, usuario: UsuarioUpdate):
    db_usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if db_usuario:
        for key, value in usuario.dict(exclude_unset=True).items():
            setattr(db_usuario, key, value)
        db.commit()
        db.refresh(db_usuario)
    return db_usuario

def delete_usuario(db: Session, usuario_id: int):
    db_usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
    return db_usuario