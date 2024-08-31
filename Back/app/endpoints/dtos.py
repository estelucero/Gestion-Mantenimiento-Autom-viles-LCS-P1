from datetime import date
from tokenize import Double
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

class verificacionUsuarioLogeoDTO(BaseModel):
    response : bool

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

class vehiculoRegistradoDTO(BaseModel): 
    patente : str
    modelo : str
    marca : str

class vehiculoRevisionDTO(BaseModel):
    nombre : str
    fechaUltRevision : date
    fechaProxRevision : date
    kmActual : float
    kmProxRevision : float
    estado : str
    patente : str
    revisionPorFecha : bool

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