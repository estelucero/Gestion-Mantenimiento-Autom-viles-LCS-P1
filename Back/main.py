import uvicorn
from datosConexion import datosAPI

myIp = datosAPI()

if __name__ == "__main__":
    config = uvicorn.run("app.api:app", host=myIp.ip, port=myIp.puerto, log_level="info")

