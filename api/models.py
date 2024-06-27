from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
    Time,
    Sequence,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    id_tipo = Column(Integer, ForeignKey("tipo_usuario.id_tipo"), nullable=False)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    correo = Column(String, nullable=False, unique=True)
    usuario = Column(String, nullable=False, unique=True)
    contrasena = Column(String, nullable=False)
    celular = Column(String(10), nullable=True)

    tipo_usuario = relationship("TipoUsuario", back_populates="usuarios")


class TipoUsuario(Base):
    __tablename__ = "tipo_usuario"

    id_tipo = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False, unique=True)

    usuarios = relationship("Usuario", back_populates="tipo_usuario")


class EstadoReserva(Base):
    __tablename__ = "estado_reserva"
    id_estado = Column(
        Integer, Sequence("estado_reserva_id_estado_seq"), primary_key=True
    )
    estado = Column(String(100))


class Historial(Base):
    __tablename__ = "historial"
    id_historial = Column(
        Integer, Sequence("historial_id_historial_seq"), primary_key=True
    )
    id_reserva = Column(Integer, ForeignKey("reserva.id_reserva"))
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    id_laboratorio = Column(Integer, ForeignKey("laboratorios.id_laboratorio"))

    reserva = relationship("Reserva")
    usuario = relationship("Usuario")
    laboratorio = relationship("Laboratorio")


class Laboratorio(Base):
    __tablename__ = "laboratorios"
    id_laboratorio = Column(
        Integer, Sequence("laboratorios_id_laboratorio_seq"), primary_key=True
    )
    nombre_lab = Column(String(100))
    capacidad = Column(Integer)
    equipos = Column(Integer)


class Reserva(Base):
    __tablename__ = "reserva"
    id_reserva = Column(Integer, Sequence("reserva_id_reserva_seq"), primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    id_laboratorio = Column(Integer, ForeignKey("laboratorios.id_laboratorio"))
    id_estado = Column(Integer, ForeignKey("estado_reserva.id_estado"))
    fecha = Column(Date)
    hora_inicio = Column(Time)
    hora_fin = Column(Time)

    usuario = relationship("Usuario")
    laboratorio = relationship("Laboratorio")
    estado_reserva = relationship("EstadoReserva")