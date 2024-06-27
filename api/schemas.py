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
    contrasena: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str


class LaboratorioBase(BaseModel):
    nombre_lab: str
    capacidad: int
    equipos: int


class LaboratorioCreate(LaboratorioBase):
    pass


class LaboratorioUpdate(LaboratorioBase):
    pass


class Laboratorio(LaboratorioBase):
    id_laboratorio: int

    class Config:
        orm_mode = True


class LoginRequest(BaseModel):
    usuario: str
    contrasena: str
