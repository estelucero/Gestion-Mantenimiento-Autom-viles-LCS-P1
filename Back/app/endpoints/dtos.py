from pydantic import BaseModel

class ejemploDTO(BaseModel):
    nombre : str
    apellido : str
    edad : int