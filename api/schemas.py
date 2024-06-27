from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, time


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
        from_attributes = True


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
        from_attributes = True


class LoginRequest(BaseModel):
    usuario: str
    contrasena: str


class ReservaBase(BaseModel):
    id_usuario: int
    id_laboratorio: int
    id_estado: int
    fecha: date
    hora_inicio: time
    hora_fin: time


class ReservaCreate(ReservaBase):
    pass


class ReservaUpdate(BaseModel):
    id_usuario: Optional[int]
    id_laboratorio: Optional[int]
    id_estado: Optional[int]
    fecha: Optional[date]
    hora_inicio: Optional[time]
    hora_fin: Optional[time]


class Reserva(ReservaBase):
    id_reserva: int


class Config:
    from_attributes = True


class HistorialBase(BaseModel):
    id_reserva: int
    id_usuario: int
    id_laboratorio: int


class HistorialCreate(HistorialBase):
    pass


class HistorialUpdate(BaseModel):
    id_reserva: Optional[int]
    id_usuario: Optional[int]
    id_laboratorio: Optional[int]


class Historial(HistorialBase):
    id_historial: int

    class Config:
        from_attributes = True
