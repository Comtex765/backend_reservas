from api.models import Usuario
from sqlalchemy.orm import Session
from api.schemas import UsuarioCreate, UsuarioUpdate
import hashlib


def calculate_sha256(data):
    # Convert data to bytes if it’s not already
    if isinstance(data, str):
        data = data.encode()

        # Calculate SHA-256 hash
        sha256_hash = hashlib.sha256(data).hexdigest()

    return sha256_hash


def verify_password(plain_password: str, hashed_password: str):
    return calculate_sha256(plain_password) == hashed_password


def get_password_hash(password: str):
    return calculate_sha256(password)


def get_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()


def get_usuario_by_username(db: Session, username: str):
    return db.query(Usuario).filter(Usuario.usuario == username).first()


def get_usuarios(db: Session):
    return db.query(Usuario).all()


def create_usuario(db: Session, usuario: UsuarioCreate):
    hashed_password = get_password_hash(usuario.contrasena)

    db_usuario = Usuario(
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        correo=usuario.correo,
        usuario=usuario.usuario,
        contrasena=str(hashed_password),
        celular=usuario.celular,
        id_tipo=usuario.id_tipo,
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def update_usuario(db: Session, username: str, usuario_update: UsuarioUpdate):
    db_usuario = db.query(Usuario).filter(Usuario.usuario == username).first()
    if db_usuario:
        for key, value in usuario_update.dict(exclude_unset=True).items():
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
    user = get_usuario_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.contrasena):
        return False
    return user
