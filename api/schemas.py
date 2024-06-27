from pydantic import BaseModel


class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    correo: str
    usuario: str
    telefono: str


class UsuarioCreate(UsuarioBase):
    contraseña: str


class UsuarioUpdate(UsuarioBase):
    contraseña: str


class Usuario(UsuarioBase):
    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
