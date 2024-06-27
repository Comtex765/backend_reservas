
/*==============================================================*/
/* Table: ESTADO_RESERVA                                        */
/*==============================================================*/
create table ESTADO_RESERVA (
   ID_ESTADO            SERIAL               not null,
   ESTADO               VARCHAR(100)         null,
   constraint PK_ESTADO_RESERVA primary key (ID_ESTADO)
);

/*==============================================================*/
/* Table: HISTORIAL                                             */
/*==============================================================*/
create table HISTORIAL (
   ID_HISTORIAL         SERIAL               not null,
   ID_RESERVA           INT4                 null,
   ID_USUARIO           INT4                 null,
   ID_LABORATORIO       INT4                 null,
   constraint PK_HISTORIAL primary key (ID_HISTORIAL)
);

/*==============================================================*/
/* Table: LABORATORIOS                                          */
/*==============================================================*/
create table LABORATORIOS (
   ID_LABORATORIO       SERIAL               not null,
   NOMBRE_LAB           VARCHAR(100)         null,
   CAPACIDAD            INT4                 null,
   EQUIPOS              INT4                 null,
   constraint PK_LABORATORIOS primary key (ID_LABORATORIO)
);

/*==============================================================*/
/* Table: RESERVA                                               */
/*==============================================================*/
create table RESERVA (
   ID_RESERVA           SERIAL               not null,
   ID_USUARIO           INT4                 not null,
   ID_LABORATORIO       INT4                 not null,
   ID_ESTADO            INT4                 null,
   FECHA                DATE                 null,
   HORA_INICIO          TIME                 null,
   HORA_FIN             TIME                 null,
   constraint PK_RESERVA primary key (ID_RESERVA, ID_USUARIO, ID_LABORATORIO)
);

/*==============================================================*/
/* Table: TIPO_USUARIO                                          */
/*==============================================================*/
create table TIPO_USUARIO (
   ID_TIPO              SERIAL               not null,
   TIPO                 VARCHAR(100)         null,
   constraint PK_TIPO_USUARIO primary key (ID_TIPO)
);

/*==============================================================*/
/* Table: USUARIOS                                              */
/*==============================================================*/
create table USUARIOS (
   ID_USUARIO           SERIAL               not null,
   ID_TIPO              INT4                 null,
   NOMBRE               VARCHAR(50)          null,
   APELLIDO             VARCHAR(50)          null,
   CORREO               VARCHAR(100)         null,
   USUARIO              VARCHAR(100)         null,
   CONTRASENA           VARCHAR(200)         null,
   CELULAR              CHAR(10)             null,
   constraint PK_USUARIOS primary key (ID_USUARIO)
);

alter table HISTORIAL
   add constraint FK_HISTORIA_REFERENCE_RESERVA foreign key (ID_RESERVA, ID_USUARIO, ID_LABORATORIO)
      references RESERVA (ID_RESERVA, ID_USUARIO, ID_LABORATORIO)
      on delete restrict on update restrict;

alter table RESERVA
   add constraint FK_RESERVA_REFERENCE_USUARIOS foreign key (ID_USUARIO)
      references USUARIOS (ID_USUARIO)
      on delete restrict on update restrict;

alter table RESERVA
   add constraint FK_RESERVA_REFERENCE_LABORATO foreign key (ID_LABORATORIO)
      references LABORATORIOS (ID_LABORATORIO)
      on delete restrict on update restrict;

alter table RESERVA
   add constraint FK_RESERVA_REFERENCE_ESTADO_R foreign key (ID_ESTADO)
      references ESTADO_RESERVA (ID_ESTADO)
      on delete restrict on update restrict;

alter table USUARIOS
   add constraint FK_USUARIOS_REFERENCE_TIPO_USU foreign key (ID_TIPO)
      references TIPO_USUARIO (ID_TIPO)
      on delete restrict on update restrict;

