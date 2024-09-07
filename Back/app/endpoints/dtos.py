from datetime import date
from typing import Optional
from pydantic import BaseModel

class ejemploDTO(BaseModel):
    nombre : str
    apellido : str
    edad : int

class usuarioParticularRegistroDTO(BaseModel):
    nombre : str
    apellido : str
    dni : str
    email : str
    contraseña : str
    cuil : str

class usuarioRegistradoDTO(BaseModel):
    email : str

class usuarioOrganizacionRegistroDTO(BaseModel):
    razonSocial : str
    email : str
    contraseña : str
    cuit : str

class nuevoVehiculoUsuarioParticularDTO(BaseModel):
    patente : str
    modelo : str
    marca : str
    fechaFabricacion : date
    vim : str
    cantKm : float
    cuilDueño : str

class nuevoVehiculoUsuarioOrganizacionDTO(BaseModel):
    patente : str
    modelo : str
    marca : str
    fechaFabricacion : date
    vim : str
    cantKm : float
    cuitDueño : str

class vehiculoDTO(BaseModel):
    patente : str
    modelo : str
    marca : str
    fechaFabricacion : date
    vim : str
    cantKm : float

class vehiculoRegistradoDTO(BaseModel): 
    patente : str
    modelo : str
    marca : str

class vehiculoRevisionDTO(BaseModel):
    nombre : str
    fechaUltRevision : date
    fechaProxRevision : date
    estado : str
    patente : str

class notifMarcarLeidaDTO(BaseModel):
    idNotif : int

class viajeDTO(BaseModel):
    fechaInicio : date
    distanciaKM : float
    nombre : str
    patente : str

class viajeRealizadoDTO(BaseModel):
    id : int
    distanciaKM : float
    patente : str

class notificacionDTO(BaseModel):
    nombre : str
    fechaVence : date
    patente : str

class vehiculoModificarDTO(BaseModel):
    patenteAnterior: str
    patenteNueva: Optional[str] = None
    modelo: Optional[str] = None
    marca: Optional[str] = None
    fecha: Optional[str] = None
    vim: Optional[str] = None
    cantKM: Optional[float] = None

class vehiculoConRevisionesDTO(BaseModel):
    vehiculo : vehiculoDTO
    listaNotif : list[notificacionDTO]

class usuarioParticularLogeoDTO(BaseModel):
    nombre : str
    apellido : str
    dni : str
    email : str
    cuil : str
    esParticular : bool

class usuarioOrganizacionLogeoDTO(BaseModel):
    razonSocial : str
    email : str
    cuit : str
    esParticular : bool