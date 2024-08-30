from datetime import date, timedelta
import mysql.connector
from app.db.mainDB import mydb, mycursor
from app.endpoints.dtos import nuevoVehiculoUsuarioOrganizacionDTO, nuevoVehiculoUsuarioParticularDTO, usuarioOrganizacionRegistroDTO, usuarioParticularRegistroDTO, usuarioRegistradoDTO, vehiculoRegistradoDTO, vehiculoRevisionDTO, verificacionUsuarioLogeoDTO

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
        
    def registrarUsuarioOrganizacionDB(self, usuarioOrganizacion : usuarioOrganizacionRegistroDTO):
        try:
            registroUP = "INSERT INTO `usuariosOrganizacion` (`razonSocial`, `email`, `contraseña`, `cuit`) VALUES (%s, %s, %s, %s);"
            registroUPData = (usuarioOrganizacion.razonSocial, usuarioOrganizacion.email, usuarioOrganizacion.contraseña, usuarioOrganizacion.cuit)
            self.dbCursor.execute(registroUP, registroUPData)
            self.dbConexion.commit()
            return usuarioRegistradoDTO(email = usuarioOrganizacion.email)
        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}

    def verificarUsuarioLogeoExitosoUsuarioParticularDB(self, email, password):
        try:
            verifUP = "SELECT `email` , `contraseña` FROM `usuariosParticular` WHERE email = %s AND contraseña = %s"
            verifUPData = (email, password)
            self.dbCursor.execute(verifUP, verifUPData)
            result = self.dbCursor.fetchall()
            #SI LA LISTA ESTA VACIA, NO ENCONTRO NADA EN EL SELECT
            if not result:
                return verificacionUsuarioLogeoDTO(response = False)
            else :
                return verificacionUsuarioLogeoDTO(response = True)
            
        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}
        
    def verificarUsuarioLogeoExitosoUsuarioOrganizacionDB(self, email, password):
        try:
            verifUP = "SELECT `email` , `contraseña` FROM `usuariosOrganizacion` WHERE email = %s AND contraseña = %s"
            verifUPData = (email, password)
            self.dbCursor.execute(verifUP, verifUPData)
            result = self.dbCursor.fetchall()
            #SI LA LISTA ESTA VACIA, NO ENCONTRO NADA EN EL SELECT
            if not result:
                return verificacionUsuarioLogeoDTO(response = False)
            else :
                return verificacionUsuarioLogeoDTO(response = True)
            
        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}
        
    def registrarNuevoVehiculoUsuarioParticularDB(self, vehiculoNuevo : nuevoVehiculoUsuarioParticularDTO):
            try:
                vehiculoUP = "INSERT INTO `vehiculosParticular` (`patente`, `modelo`, `marca`, `fechaFabricacion`, `vim`, `cantKM`, `tipoCombustible`, `cuilDueño`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"
                vehiculoUPData = (vehiculoNuevo.patente, vehiculoNuevo.modelo, vehiculoNuevo.marca, vehiculoNuevo.fechaFabricacion, vehiculoNuevo.vim, vehiculoNuevo.cantKm, vehiculoNuevo.tipoCombustible, vehiculoNuevo.cuilDueño)
                self.dbCursor.execute(vehiculoUP, vehiculoUPData)
                self.dbConexion.commit()
                return vehiculoRegistradoDTO(patente = vehiculoNuevo.patente, marca = vehiculoNuevo.marca, modelo = vehiculoNuevo.modelo)
            
            except mysql.connector.Error as err:
                self.dbConexion.rollback()
                return {"error":"Algo fue mal: {}".format(err)}
            
    def registrarNuevoVehiculoUsuarioOrganizacionDB(self, vehiculoNuevo : nuevoVehiculoUsuarioOrganizacionDTO):
            try:
                vehiculoUP = "INSERT INTO `vehiculosOrganizacion` (`patente`, `modelo`, `marca`, `fechaFabricacion`, `vim`, `cantKM`, `tipoCombustible`, `cuitDueño`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"
                vehiculoUPData = (vehiculoNuevo.patente, vehiculoNuevo.modelo, vehiculoNuevo.marca, vehiculoNuevo.fechaFabricacion, vehiculoNuevo.vim, vehiculoNuevo.cantKm, vehiculoNuevo.tipoCombustible, vehiculoNuevo.cuitDueño)
                self.dbCursor.execute(vehiculoUP, vehiculoUPData)
                self.dbConexion.commit()
                return vehiculoRegistradoDTO(patente = vehiculoNuevo.patente, marca = vehiculoNuevo.marca, modelo = vehiculoNuevo.modelo)
            
            except mysql.connector.Error as err:
                self.dbConexion.rollback()
                return {"error":"Algo fue mal: {}".format(err)}
            

    def vehiculoVerificacion(self, patente, esParticular):
        try:
            if(esParticular):
                vehiculoVERIF = "SELECT `vim` FROM `vehiculosParticular` WHERE patente = %s"
            else:
                vehiculoVERIF = "SELECT `vim` FROM `vehiculosOrganizacion` WHERE patente = %s"
            vehiculoVERIFData = (patente,)
            self.dbCursor.execute(vehiculoVERIF, vehiculoVERIFData)
            result = self.dbCursor.fetchall()

            #SI LA LISTA ESTA VACIA, NO EXISTE EL VEHICULO EN LA DB DIRECTAMENTE.
            if not result :
                return False
            else:
                 return True
            
        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}


    
    def eliminarVehiculoUsuarioParticularDB(self, patente):
        try:
            if not self.vehiculoVerificacion(patente, True):
                return False

            vehiculoDELETE = "DELETE FROM `vehiculosParticular` WHERE patente = %s"
            vehiculoDELETEData = (patente,)
            self.dbCursor.execute(vehiculoDELETE, vehiculoDELETEData)
            self.dbConexion.commit()
            return True
        
        except mysql.connector.Error as err:
                self.dbConexion.rollback()
                return {"error":"Algo fue mal: {}".format(err)}
        

    def eliminarVehiculoUsuarioOrganizacionDB(self, patente):
        try:
            if not self.vehiculoVerificacion(patente, False):
                return False

            vehiculoDELETE = "DELETE FROM `vehiculosOrganizacion` WHERE patente = %s"
            vehiculoDELETEData = (patente,)
            self.dbCursor.execute(vehiculoDELETE, vehiculoDELETEData)
            self.dbConexion.commit()
            return True
        
        except mysql.connector.Error as err:
                self.dbConexion.rollback()
                return {"error":"Algo fue mal: {}".format(err)}
        

    def calculoRevision(self, vehiculoRevision : vehiculoRevisionDTO, esParticular):
        
        if vehiculoRevision.revisionPorFecha:

            if(vehiculoRevision.nombre.lower() == 'cambio_aceite'):
                vehiculoRevision.fechaProxRevision = vehiculoRevision.fechaUltRevision+timedelta(days=183)
                return vehiculoRevision
            
            if(vehiculoRevision.nombre.lower() == 'revision_neumaticos'):
                vehiculoRevision.fechaProxRevision = vehiculoRevision.fechaUltRevision+timedelta(days=30)
                return vehiculoRevision

            if(vehiculoRevision.nombre.lower() == 'revision_fluidos'):
                vehiculoRevision.fechaProxRevision = vehiculoRevision.fechaUltRevision+timedelta(days=30)
                return vehiculoRevision
            
            if(vehiculoRevision.nombre.lower() == 'servicio_completo'):
                vehiculoRevision.fechaProxRevision = vehiculoRevision.fechaUltRevision+timedelta(days=365)
                return vehiculoRevision
            
            if(vehiculoRevision.nombre.lower() == 'revision_escape'):
                vehiculoRevision.fechaProxRevision = vehiculoRevision.fechaUltRevision+timedelta(days=365)
                return vehiculoRevision
            
            if(vehiculoRevision.nombre.lower() == 'revision_bateria'):
                vehiculoRevision.fechaProxRevision = vehiculoRevision.fechaUltRevision+timedelta(days=912)
                return vehiculoRevision

        else:

            #ASIGNO LOS KM DEL VEHICULO A LA REVISION X KM
            if esParticular:
                try :
                    vehiculoGETKM = "SELECT `CantKM` FROM vehiculosParticular WHERE patente = %s"
                    vehiculoGETKMData = (vehiculoRevision.patente,)
                    self.dbCursor.execute(vehiculoGETKM, vehiculoGETKMData)
                    result = self.dbCursor.fetchall()
                    vehiculoRevision.kmActual = result[0][0]
                
                except mysql.connector.Error as err:
                    self.dbConexion.rollback()
                    return {"error":"Algo fue mal: {}".format(err)}
            
            else:
                
                try :
                    vehiculoGETKM = "SELECT `CantKM` FROM vehiculosOrganizacion WHERE patente = %s"
                    vehiculoGETKMData = (vehiculoRevision.patente,)
                    self.dbCursor.execute(vehiculoGETKM, vehiculoGETKMData)
                    result = self.dbCursor.fetchall()
                    vehiculoRevision.kmActual = result[0][0]
                
                except mysql.connector.Error as err:
                    self.dbConexion.rollback()
                    return {"error":"Algo fue mal: {}".format(err)}
                
            if(vehiculoRevision.nombre.lower() == 'revision_frenos'):
                vehiculoRevision.kmProxRevision = vehiculoRevision.kmActual + 20000
                return vehiculoRevision
            
            if(vehiculoRevision.nombre.lower() == 'rotacion_neumaticos'):
                vehiculoRevision.kmProxRevision = vehiculoRevision.kmActual + 13500
                return vehiculoRevision
            
            if(vehiculoRevision.nombre.lower() == 'revision_correa'):
                vehiculoRevision.kmProxRevision = vehiculoRevision.kmActual + 80000
                return vehiculoRevision
            
            if(vehiculoRevision.nombre.lower() == 'cambio_bujias'):
                vehiculoRevision.kmProxRevision = vehiculoRevision.kmActual + 100000
                return vehiculoRevision

    
    def agregarRevisionVehiculoParticularDB(self, vehiculoRevision : vehiculoRevisionDTO):
        try:
            auxiliar = self.calculoRevision(vehiculoRevision, True)
            revisionUP="INSERT INTO `revisionesVehiculoParticular` (`nombre`, `fechaUltRevision`, `fechaProxRevision`, `kmUltRevision`, `kmProxRevision`, `estado`, `patenteVehiculo`, `revisaPorFecha`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"
            revisionUPData=(auxiliar.nombre, auxiliar.fechaUltRevision, auxiliar.fechaProxRevision, auxiliar.kmActual, auxiliar.kmProxRevision, auxiliar.estado, auxiliar.patente, auxiliar.revisionPorFecha)
            self.dbCursor.execute(revisionUP, revisionUPData)
            self.dbConexion.commit()
            return True
        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}
        

    def agregarRevisionVehiculoOrganizacionDB(self, vehiculoRevision : vehiculoRevisionDTO):
        try:
            auxiliar = self.calculoRevision(vehiculoRevision, False)
            revisionUP="INSERT INTO `revisionesVehiculoOrganizacion` (`nombre`, `fechaUltRevision`, `fechaProxRevision`, `kmUltRevision`, `kmProxRevision`, `estado`, `patenteVehiculo`, `revisaPorFecha`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"
            revisionUPData=(auxiliar.nombre, auxiliar.fechaUltRevision, auxiliar.fechaProxRevision, auxiliar.kmActual, auxiliar.kmProxRevision, auxiliar.estado, auxiliar.patente, auxiliar.revisionPorFecha)
            self.dbCursor.execute(revisionUP, revisionUPData)
            self.dbConexion.commit()
            return True
        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}