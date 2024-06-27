from pydantic import BaseModel, EmailStr


class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    correo: EmailStr
    usuario: str
    celular: str

class UsuarioCreate(UsuarioBase):
    id_tipo: int
    contrasena: str



class UsuarioUpdate(UsuarioBase):
    contrasena: str

class Usuario(UsuarioBase):
    id_usuario: int
    id_tipo: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
