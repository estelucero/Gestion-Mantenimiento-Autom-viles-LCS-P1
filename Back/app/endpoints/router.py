from fastapi import APIRouter
from app.endpoints.dtos import ejemploDTO


router = APIRouter(prefix="/users", tags=["User"])

#PUT-GET-POST-DELETE-PATCH
@router.get("/")
def index():
    return {"message":"prueba"}

@router.put("/ejemploDTO")
def registrarUsuario(usuario : ejemploDTO):

    return print("Ingreso nombre:"+usuario.nombre+
                " Ingreso apellido:"+usuario.apellido+
                " Ingreso edad:"+str(usuario.edad))