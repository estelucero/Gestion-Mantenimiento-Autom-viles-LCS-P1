import mysql.connector
from app.db.mainDB import mydb, mycursor
from app.endpoints.dtos import usuarioParticularRegistroDTO, usuarioRegistradoDTO, verificacionUsuarioLogeo

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
        
    def verificarUsuarioLogeoExitosoDB(self, email, password):
        try:
            verifUP = "SELECT `email` , `contraseña` FROM `usuariosParticular` WHERE email = %s AND contraseña = %s"
            verifUPData = (email, password)
            mycursor.execute(verifUP, verifUPData)
            result = mycursor.fetchall()
            #SI LA LISTA ESTA VACIA, NO ENCONTRO NADA EN EL SELECT
            if not result:
                return verificacionUsuarioLogeo(response = False)
            else :
                return verificacionUsuarioLogeo(response = True)
            
        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}