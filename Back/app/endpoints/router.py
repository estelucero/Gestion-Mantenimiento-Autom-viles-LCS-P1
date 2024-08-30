from fastapi import APIRouter, HTTPException, Query
from app.endpoints.dtos import nuevoVehiculoUsuarioOrganizacionDTO, nuevoVehiculoUsuarioParticularDTO, usuarioOrganizacionRegistroDTO, usuarioParticularRegistroDTO, vehiculoRevisionDTO
from app.endpoints.endpoint import dbCallService
from fastapi_restful.tasks import repeat_every

router = APIRouter(prefix="/users", tags=["User"])

call_service = dbCallService()

#PUT-GET-POST-DELETE-PATCH
@router.get("/")
def index():
    return {"message":"prueba"}

#RECIBE UN USUARIO PARTICULAR CON TODOS SUS DATOS, Y DEVUELVE EL MAIL DEL REGISTRADO O UN ERROR CON DETALLES.
@router.post("/registroUsuarioParticular")
def registrarUsuarioParticular(usuarioParticular : usuarioParticularRegistroDTO) :
    response = call_service.registrarUsuarioParticularDB(usuarioParticular)
    
    if ("error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response

#RECIBE UN USUARIO ORGANIZACION CON TODOS SUS DATOS, Y DEVUELVE EL MAIL DEL REGISTRADO O UN ERROR CON DETALLES.
@router.post("/registroUsuarioOrganizacion")
def registrarUsuarioOrganizacion(usuarioOrganizacion : usuarioOrganizacionRegistroDTO) :
    response = call_service.registrarUsuarioOrganizacionDB(usuarioOrganizacion)

    if ("error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response


#RECIBE UN EMAIL Y PASSWORD DEL FRONT, DEVUELVE BOOLEAN TRUE O FALSE SI SE PUEDE LOGEAR O NO
@router.get("/verificarLogeoExitosoUsuarioParticular")
def verifRegistroUsuarioParticular(email = Query(), password = Query()) : 
    response = call_service.verificarUsuarioLogeoExitosoUsuarioParticularDB(email, password)

    if ("error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response

#RECIBE UN EMAIL Y PASSWORD DEL FRONT, DEVUELVE BOOLEAN TRUE O FALSE SI SE PUEDE LOGEAR O NO
@router.get("/verificarLogeoExitosoUsuarioOrganizacion")
def verifRegistroUsuarioOrganizacion(email = Query(), password = Query()) : 
    response = call_service.verificarUsuarioLogeoExitosoUsuarioOrganizacionDB(email, password)

    if ("error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response

#RECIBE UN VEHICULO CON TODOS SUS DATOS Y EL CUIL DEL DUEÑO.  DEVUELVE UN OBJETO VEHICULOREGISTRADODTO SI SE REGISTRA CORRECTAMENTE. SI NO ERROR.
@router.post("/registrarVehiculoUsuarioParticular")
def registrarVehiculoUsuarioParticular(vehiculoNuevo : nuevoVehiculoUsuarioParticularDTO) :
    response = call_service.registrarNuevoVehiculoUsuarioParticularDB(vehiculoNuevo)

    if ("error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response

#RECIBE UN VEHICULO CON TODOS SUS DATOS Y EL CUIT DEL DUEÑO. DEVUELVE UN OBJETO VEHICULOREGISTRADODTO SI SE REGISTRA CORRECTAMENTE. SI NO ERROR.
@router.post("/registrarVehiculoUsuarioOrganizacion")
def registrarVehiculoUsuarioOrganizacion(vehiculoNuevo : nuevoVehiculoUsuarioOrganizacionDTO) :
    response = call_service.registrarNuevoVehiculoUsuarioOrganizacionDB(vehiculoNuevo)

    if ("error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response

#RECIBE UNA PATENTE, DEVUELVE TRUE SI SE ELIMINO O FALSE SI NO NINGUN AUTO CON ESA PATENTE. SI NO, ERROR.
@router.delete("/eliminarVehiculoUsuarioParticular")
def eliminarVehiculoUsuarioParticular(patente = Query()):
    response = call_service.eliminarVehiculoUsuarioParticularDB(patente)

    if (response != True and response != False):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response

#RECIBE UNA PATENTE, DEVUELVE TRUE SI SE ELIMINO O FALSE SI NO NINGUN AUTO CON ESA PATENTE. SI NO, ERROR.
@router.delete("/eliminarVehiculoUsuarioOrganizacion")
def eliminarVehiculoUsuarioOrganizacion(patente = Query()):
    response = call_service.eliminarVehiculoUsuarioOrganizacionDB(patente)

    if (response != True and response != False):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response


#AMBAS AGREGAR REVISION RECIBEN LO MISMO. UNA LISTA DE OBJETOS DE ESE TIPO, LOS ITERA Y LOS VA AGREGANDO. NECESITO QUE HANDLEES LAS FECHAS EN EL FRONT, NO PUEDE HABER NULL EN LOS CAMPOS DE LAS FECHAS CDO LO ENVIES.
#DEVUELVE UN ERROR SI FALLA EL AGREGAR
@router.post("/agregarRevisionesVehiculoParticular")    
def agregarRevisionesVehiculoParticular(revisiones : list[vehiculoRevisionDTO]):
    for vehiculoRevision in revisiones:
        response = call_service.agregarRevisionVehiculoParticularDB(vehiculoRevision)

    if (response != True and "error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response

@router.post("/agregarRevisionesVehiculoOrganizacion")    
def agregarRevisionesVehiculoOrganizacion(revisiones : list[vehiculoRevisionDTO]):
    for vehiculoRevision in revisiones:
        response = call_service.agregarRevisionVehiculoOrganizacionDB(vehiculoRevision)

    if (response != True and "error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response


@router.get("/verificarYActualizarRevisionesAVencer")
#@repeat_every(seconds=40)
def verificarYActualizarRevisionesAVencer():

    response = call_service.actualizarRevisionesRegistradasParticularDB()
    
    if (response != True and "error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    