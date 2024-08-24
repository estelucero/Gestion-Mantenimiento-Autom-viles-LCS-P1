from fastapi import FastAPI
from app.endpoints.dtos import ejemploDTO

app = FastAPI()

#PUT-GET-POST-DELETE-PATCH

@app.get("/")
def index():
    return {"message":"prueba"}

@app.put("/ejemploDTO")
def registrarUsuario(usuario : ejemploDTO):

    return print("Ingreso nombre:"+usuario.nombre+
                " Ingreso apellido:"+usuario.apellido+
                " Ingreso edad:"+str(usuario.edad))