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

class verificacionUsuarioLogeo(BaseModel):
    response : bool