from pydantic import BaseModel

class ejemploDTO(BaseModel):
    nombre : str
    apellido : str
    edad : int

class usuarioParticularRegistroDTO(BaseModel):
    nombre : str
    apellido : str
    dni : int
    email : str
    contraseña : str
    cuil : str

class usuarioRegistradoDTO(BaseModel):
    email : str