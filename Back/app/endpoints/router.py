from fastapi import APIRouter, HTTPException, Query
from app.endpoints.dtos import nuevoVehiculoUsuarioOrganizacionDTO, nuevoVehiculoUsuarioParticularDTO, usuarioOrganizacionRegistroDTO, usuarioParticularRegistroDTO, vehiculoModificarDTO, vehiculoRevisionDTO, viajeDTO
from app.endpoints.endpoint import dbCallService

router = APIRouter(prefix="/users", tags=["User"])

call_service = dbCallService()

#PUT-GET-POST-DELETE-PATCH
@router.get("/")
def index():
    return {"message":"prueba"}

#RECIBE UN USUARIO PARTICULAR CON TODOS SUS DATOS, Y DEVUELVE EL MAIL DEL REGISTRADO O UN ERROR CON DETALLES.
@router.post("/registroUsuarioParticular")
def registrarUsuarioParticular(usuarioParticular : usuarioParticularRegistroDTO) :
    call_service.chequearCnxDB()

    response = call_service.registrarUsuarioParticularDB(usuarioParticular)
    
    if ("error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response

#RECIBE UN USUARIO ORGANIZACION CON TODOS SUS DATOS, Y DEVUELVE EL MAIL DEL REGISTRADO O UN ERROR CON DETALLES.
@router.post("/registroUsuarioOrganizacion")
def registrarUsuarioOrganizacion(usuarioOrganizacion : usuarioOrganizacionRegistroDTO) :
    call_service.chequearCnxDB()

    response = call_service.registrarUsuarioOrganizacionDB(usuarioOrganizacion)

    if ("error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response


#RECIBE UN EMAIL Y PASSWORD DEL FRONT, DEVUELVE BOOLEAN TRUE O FALSE SI SE PUEDE LOGEAR O NO
@router.get("/verificarLogeoExitosoUsuarioParticular")
def verifRegistroUsuarioParticular(email = Query(), password = Query()) : 
    call_service.chequearCnxDB()

    response = call_service.verificarUsuarioLogeoExitosoUsuarioParticularDB(email, password)

    if (response != False and "error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response

#RECIBE UN EMAIL Y PASSWORD DEL FRONT, DEVUELVE BOOLEAN TRUE O FALSE SI SE PUEDE LOGEAR O NO
@router.get("/verificarLogeoExitosoUsuarioOrganizacion")
def verifRegistroUsuarioOrganizacion(email = Query(), password = Query()) : 
    call_service.chequearCnxDB()

    response = call_service.verificarUsuarioLogeoExitosoUsuarioOrganizacionDB(email, password)

    if (response != False and "error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response

#RECIBE UN VEHICULO CON TODOS SUS DATOS Y EL CUIL DEL DUEÑO.  DEVUELVE UN OBJETO VEHICULOREGISTRADODTO SI SE REGISTRA CORRECTAMENTE. SI NO ERROR.
@router.post("/registrarVehiculoUsuarioParticular")
def registrarVehiculoUsuarioParticular(vehiculoNuevo : nuevoVehiculoUsuarioParticularDTO) :
    call_service.chequearCnxDB()

    response = call_service.registrarNuevoVehiculoUsuarioParticularDB(vehiculoNuevo)

    if ("error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response

#RECIBE UN VEHICULO CON TODOS SUS DATOS Y EL CUIT DEL DUEÑO. DEVUELVE UN OBJETO VEHICULOREGISTRADODTO SI SE REGISTRA CORRECTAMENTE. SI NO ERROR.
@router.post("/registrarVehiculoUsuarioOrganizacion")
def registrarVehiculoUsuarioOrganizacion(vehiculoNuevo : nuevoVehiculoUsuarioOrganizacionDTO) :
    call_service.chequearCnxDB()

    response = call_service.registrarNuevoVehiculoUsuarioOrganizacionDB(vehiculoNuevo)

    if ("error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response

#RECIBE UNA PATENTE, DEVUELVE TRUE SI SE ELIMINO O FALSE SI NO NINGUN AUTO CON ESA PATENTE. SI NO, ERROR.
@router.delete("/eliminarVehiculoUsuarioParticular")
def eliminarVehiculoUsuarioParticular(patente = Query()):
    call_service.chequearCnxDB()

    response = call_service.eliminarVehiculoUsuarioParticularDB(patente)

    if (response != True and response != False):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response

#RECIBE UNA PATENTE, DEVUELVE TRUE SI SE ELIMINO O FALSE SI NO NINGUN AUTO CON ESA PATENTE. SI NO, ERROR.
@router.delete("/eliminarVehiculoUsuarioOrganizacion")
def eliminarVehiculoUsuarioOrganizacion(patente = Query()):
    call_service.chequearCnxDB()

    response = call_service.eliminarVehiculoUsuarioOrganizacionDB(patente)

    if (response != True and response != False):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response

#RECIBEN LOS DATOS (si no los modifica enviar "", si es un numero -1), DEVUELVE TRUE SI LO MODIFICO, O ERROR SI FALLA.
#SI NO HACE CAMBIOS, CHEQUEAR EN FRONT. ACA ASUMO QUE HAY UN CAMBIO AL MENOS.
#BORRO TODAS LAS TABLAS RELACIONADAS AL VEHICULO (REVISIONES, VIAJES, NOTIFICACIONES Y CONTROLES COMPLETADOS) SI LLEGO LO HAGO BIEN Y ACTUALIZO LOS DATOS.
#¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡ LA FECHA ME LA ENVIAN COMO UN STRING EJ(1992-05-22)!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

@router.patch("/modificarVehiculoParticular")
def modificarVehiculoParticular(vehiculoModif : vehiculoModificarDTO):
    call_service.chequearCnxDB()

    response = call_service.modificarVehiculoParticularDB(vehiculoModif)

    if (response != True and "error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])

    return response

@router.patch("/modificarVehiculoOrganizacion")
def modificarVehiculoOrganizacion(vehiculoModif : vehiculoModificarDTO):
    call_service.chequearCnxDB()

    response = call_service.modificarVehiculoOrganizacionDB(vehiculoModif)

    if (response != True and "error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])

    return response

#RECIBE EL CUIL DEL DUEÑO, DEVUELVE LA LISTA DE SUS VEHICULOS MODELADOS COMO EL OBJETO vehiculoDTO. SI NO ENCUENTRA NADA, DEVUELVE FALSE. SI HAY ERROR, ERROR.
@router.get("/obtenerVehiculosParticular")
def obtenerVehiculosParticular(cuilDueño = Query()):
    call_service.chequearCnxDB()

    response = call_service.obtenerVehiculosParticularDB(cuilDueño)

    if (response != False and response != True and "error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response

#IGUAL PERO CON CUIT
@router.get("/obtenerVehiculosOrganizacion")
def obtenerVehiculosOrganizacion(cuitDueño = Query()):
    call_service.chequearCnxDB()

    response = call_service.obtenerVehiculosOrganizacionDB(cuitDueño)

    if (response != False and response != True and "error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response

#AMBAS AGREGAR REVISION RECIBEN LO MISMO. UNA LISTA DE OBJETOS DE ESE TIPO, LOS ITERA Y LOS VA AGREGANDO. NECESITO QUE HANDLEES LAS FECHAS EN EL FRONT, NO PUEDE HABER NULL EN LOS CAMPOS DE LAS FECHAS CDO LO ENVIES.
#DEVUELVE UN ERROR SI FALLA EL AGREGAR
@router.post("/agregarRevisionesVehiculoParticular")    
def agregarRevisionesVehiculoParticular(revisiones : list[vehiculoRevisionDTO]):

    for vehiculoRevision in revisiones:
        call_service.chequearCnxDB()
        response = call_service.agregarRevisionVehiculoParticularDB(vehiculoRevision)

    if (response != True and "error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response

@router.post("/agregarRevisionesVehiculoOrganizacion")    
def agregarRevisionesVehiculoOrganizacion(revisiones : list[vehiculoRevisionDTO]):
    for vehiculoRevision in revisiones:
        call_service.chequearCnxDB()
        response = call_service.agregarRevisionVehiculoOrganizacionDB(vehiculoRevision)

    if (response != True and "error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response

#ACTUALIZA LAS FLAGS (EN ORDEN -> PROXIMA A VENCER)DE LAS REVISIONES CUANDO ESTAN CERCA DE VENCER.
@router.put("/verificarYActualizarRevisionesAVencer")
#@repeat_every(seconds=40)
def verificarYActualizarRevisionesAVencer():
    call_service.chequearCnxDB()

    response = call_service.actualizarRevisionesRegistradas()
    
    if (response != True and "error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])

#GENERA LAS NOTIFICACIONES NECESARIAS CUANDO UNA REVISION ESTA PROXIMA A VENCER    
@router.post("/generarRevisionesVencidas")
def generarRevisionesVencidas():
    call_service.chequearCnxDB()

    response = call_service.ingresarNotificacionesDB()

    if (response != True and "error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response

#RECIBE LA ID DE LA NOTIF, DEVUELVE TRUE SI LA MARCA, DEVUELVE UN ERROR SI NO.
@router.put("/marcarNotificacionLeidaPart")
def marcarNotificacionLeidaParticular(idNotif):
    call_service.chequearCnxDB()
    
    response = call_service.marcarNotificacionLeidaParticularDB(idNotif)

    if (response != True and "error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response

@router.put("/marcarNotificacionLeidaOrg")
def marcarNotificacionLeidaOrganizacion(idNotif):
    call_service.chequearCnxDB()
    
    response = call_service.marcarNotificacionLeidaOrganizacionDB(idNotif)

    if (response != True and "error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response

#LAS REVISIONES QUE YA SE HAYAN PASADO DE FECHA O KM LAS DA POR SOLUCIONADAS Y ACTUALIZA LOS VALORES DE LAS REVISIONES.
#ELIMINA LAS NOTIFICACIONES RELACIONADAS A ESA REVISION.
#LA REVISION ELIMINADA SE GUARDA EN LA TABLA DE REVISION COMPLETADA PARA TENER EL HISTORIAL
@router.put("/actualizarRevisiones")
def actualizarRevisiones():
    call_service.chequearCnxDB()

    response = call_service.actualizarRevisiones()

    if (response != True and "error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response

#RECIBE UN OBJETO VIAJE, DEVUELVE TRUE SI NO HAY ERRORES
@router.post("/ingresarViaje")
def ingresarViaje(viaje : viajeDTO):
    call_service.chequearCnxDB()

    response = call_service.ingresarViajeDB(viaje)

    if (response != True and "error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response

#ACTUALIZA LOS VIAJES, CIERRA LOS COMPLETADOS Y ACTUALIZA LOS KMS
@router.put("/actualizarViajes")
def actualizarViaje():
    call_service.chequearCnxDB()

    response = call_service.actualizarViajesDB()

    if (response != True and "error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response

#RECIBEN LA PATENTE DEL VEHICULO, DEVUELVE UNA LISTA DE OBJETOS notificacionDTO SI ENCUENTRA ALGO, SI NO ENCUENTRA DEVUELVE FALSE. SI HAY ERROR DEVUELVE ERROR.
@router.get("/obtenerNotificacionesParticular")
def obtenerNotificacionesParticular(patente = Query()):
    call_service.chequearCnxDB()

    response = call_service.obtenerNotificacionesParticularDB(patente)
    
    if (response != None and response != False and "error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response

@router.get("/obtenerNotificacionesOrganizacion")
def obtenerNotificacionesOrganizacion(patente = Query()):
    call_service.chequearCnxDB()

    response = call_service.obtenerNotificacionesOrganizacionDB(patente)

    if (response != None and response != False and "error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response

#LO MISMO QUE LAS OTRAS PERO SOLO DEVUELVEN LAS QUE NO FUERON LEIDAS
@router.get("/obtenerNotificacionesSinLeerParticular")
def obtenerNotificacionesSinLeerParticular(patente = Query()):
    call_service.chequearCnxDB()

    response = call_service.obtenerNotificacionesSinLeerParticularDB(patente)

    if (response != None and response != False and "error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response

@router.get("/obtenerNotificacionesSinLeerOrganizacion")
def obtenerNotificacionesSinLeerOrganizacion(patente = Query()):
    call_service.chequearCnxDB()

    response = call_service.obtenerNotificacionesSinLeerOrganizacionDB(patente)

    if (response != None and response != False and "error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response

@router.delete("/eliminarRevisionVehiculoParticular")
def eliminarRevisionVehiculoParticular(patente = Query(), nombreRevision = Query()):
    call_service.chequearCnxDB()

    response = call_service.eliminarRevisionVehiculoParticularDB(patente, nombreRevision)
  
    if (response != True and "error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response

@router.delete("/eliminarRevisionVehiculoOrganizacion")
def eliminarRevisionVehiculoOrganizacion(patente = Query(), nombreRevision = Query()):

    call_service.chequearCnxDB()

    response = call_service.eliminarRevisionVehiculoOrganizacionDB(patente, nombreRevision)
  
    if (response != True and "error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response

@router.get("/obtenerViajesVehiculo")
def obtenerViajesVehiculo(patente = Query()):
    call_service.chequearCnxDB()

    response = call_service.obtenerViajesVehiculoDB(patente)

    if ("error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response

@router.delete("/eliminarViaje")
def eliminarViajeVehiculo(id = Query()):
    call_service.chequearCnxDB()

    response = call_service.eliminarViajeVehiculoDB(id)

    if (response != True and "error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])

    return response