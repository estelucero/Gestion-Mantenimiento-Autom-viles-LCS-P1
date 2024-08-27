import sys, mysql.connector
sys.path.append("Gestion-Mantenimiento-Autom-viles-LCS-P1/Back/app")
from db.mainDB import mydb, mycursor
from app.endpoints.dtos import usuarioParticularRegistroDTO, usuarioRegistradoDTO

class dbCallService():
    def __init__(self):
        self.dbConexion = mydb
        self.dbCursor = mycursor
    
    #PRIMERO SE CARGA EL STORED PROCEDURE CON LOS DATOS A COMPLETAR %S Y LUEGO SE COMPLETA CON OTRO OBJETO, EN ESTE CASO UPDATA.
    def registrarUsuarioParticularDB(self, usuarioParticular : usuarioParticularRegistroDTO):
        try :
            registroUP = "INSERT INTO `usuariosParticular` (`nombre`, `apellido`, `dni`, `email`, `contraseña`, `cuil`) VALUES (%s, %s, %s, %s, %s, %s);"
            registroUPData = (usuarioParticular.nombre, usuarioParticular.apellido, usuarioParticular.dni, usuarioParticular.email, usuarioParticular.contraseña, usuarioParticular.cuil)
            self.dbCursor.execute(registroUP, registroUPData)
            self.dbConexion.commit()
            return usuarioRegistradoDTO(email = usuarioParticular.email)
        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}