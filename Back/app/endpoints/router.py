from fastapi import APIRouter, HTTPException
from app.endpoints.dtos import usuarioParticularRegistroDTO
from app.endpoints.endpoint import dbCallService


router = APIRouter(prefix="/users", tags=["User"])

call_service = dbCallService()

#PUT-GET-POST-DELETE-PATCH
@router.get("/")
def index():
    return {"message":"prueba"}

#RECIBE UN USUARIO CON TODOS SUS DATOS, Y DEVUELVE EL MAIL DEL REGISTRADO O UN ERROR CON DETALLES.
@router.post("/registroUsuario")
def registrarUsuario(usuarioParticular : usuarioParticularRegistroDTO) :
    response = call_service.registrarUsuarioParticularDB(usuarioParticular)
    
    if ("error" in response):
        raise HTTPException(status_code = 400, detail = response["error"])
    
    return response