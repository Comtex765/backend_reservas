from api.models import Usuario
from sqlalchemy.orm import Session
from api.schemas import UsuarioCreate, UsuarioUpdate
from api.jwt_utils import verify_password, get_password_hash

def get_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()

def get_usuario_by_username(db: Session, username: str):
    return db.query(Usuario).filter(Usuario.usuario == username).first()

def get_usuarios(db: Session):
    return db.query(Usuario).all()

def create_usuario(db: Session, usuario: UsuarioCreate):
    hashed_password = get_password_hash(usuario.contraseña)
    db_usuario = Usuario(
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        correo=usuario.correo,
        usuario=usuario.usuario,
        contraseña=hashed_password,
        celular=usuario.celular,
        id_tipo=usuario.id_tipo
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

def authenticate_usuario(db: Session, username: str, password: str):
    usuario = db.query(Usuario).filter(Usuario.usuario == username).first()
    if not usuario:
        return None
    if not verify_password(password, usuario.contrasena):
        return None
    return usuario