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
        

        vehiculoRevision.estado = "en_orden"
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
        
    
    def obtenerRevisionesRegistradas(self, esParticular):
        try:
            if esParticular:
                self.dbCursor.execute("SELECT id, patenteVehiculo, nombre, fechaProxRevision, kmProxRevision, revisaPorFecha, estado, kmUltRevision FROM `revisionesVehiculoParticular`")
                patentes = self.dbCursor.fetchall()
                return patentes
            else:
                self.dbCursor.execute("SELECT id, patenteVehiculo, nombre, fechaProxRevision, kmProxRevision, revisaPorFecha, estado, kmUltRevision FROM `revisionesVehiculoOrganizacion`")
                patentes = self.dbCursor.fetchall()
                return patentes
        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}


    def actualizarNuevoEstado(self, idRevision, esParticular):

        try:
            if esParticular:
                actualizarRevUP = "UPDATE `revisionesVehiculoParticular` SET estado = 'por_vencer' WHERE id = %s"
                actualizarRevUPDATA = (idRevision,)
                self.dbCursor.execute(actualizarRevUP, actualizarRevUPDATA)
                self.dbConexion.commit()
                return
            else:
                actualizarRevUP = "UPDATE `revisionesVehiculoOrganizacion` SET estado = 'por_vencer' WHERE id = %s"
                actualizarRevUPDATA = (idRevision,)
                self.dbCursor.execute(actualizarRevUP, actualizarRevUPDATA)
                self.dbConexion.commit()
                return
        
        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}
        


    #TUPLA REVISION DE FORMA (ID, PATENTE, NOMBREREVISION, FECHAPROXREVISION, KMPROXREVISION, REVISAPORFECHA, ESTADO, KMANTERIOREVISION)
    def actualizarRevision(self, revisionTuple, esParticular):
        try:
            #SI YA ESTA ACTUALIZADO, NO PERDER TIEMPO REACTUALIZANDO.
            if(revisionTuple[6] == 'por_vencer'):
                return

            if esParticular:

                #REVISIONES X FECHA
                if(revisionTuple[5] == True):
                    
                    #AVISOS 1 DIA ANTES.
                    if(revisionTuple[2] == 'cambio_aceite' or revisionTuple[2] == 'revision_neumaticos' or revisionTuple[2] == 'revision_fluidos'):
                        delta = revisionTuple[3] - date.today()
                        if(delta.days <= 1):
                            self.actualizarNuevoEstado(revisionTuple[0], True)
                            return
                        else:
                            return

                    #AVISOS 2 DIA ANTES.    
                    if(revisionTuple[2] == 'servicio_completo' or revisionTuple[2] == 'revision_escape'):
                        delta = revisionTuple[3] - date.today()
                        if(delta.days <= 2):
                            self.actualizarNuevoEstado(revisionTuple[0], True)
                            return
                        else:
                            return
                    
                    #AVISOS 1 MES ANTES.
                    if(revisionTuple[2] == 'revision_bateria'):
                        delta = revisionTuple[3] - date.today()
                        if(delta.days <= 31):
                            self.actualizarNuevoEstado(revisionTuple[0], True)
                            return
                        else:
                            return
                        
                #REVISIONES X KM        
                else:

                    #OBTENER LOS KM ACTUALES DEL VEHICULO A REVISAR
                    obtenerKMActualesUP = "SELECT CantKM FROM `vehiculosParticular` WHERE patente = %s"
                    obtenerKMActualesUPData = (revisionTuple[1],)
                    self.dbCursor.execute(obtenerKMActualesUP, obtenerKMActualesUPData)
                    kmActuales = self.dbCursor.fetchall()
                    
                    #AVISO 2000 km ANTES DE TENERLOS QUE CAMBIAR
                    if(revisionTuple[2] == 'revision_frenos' or revisionTuple[2] == 'rotacion_neumaticos'):
                        #SI LOS KM QUE SE RECORRIERON SON MAYORES A LOS DE LA PROXIMA REVISION - CUANTOS KM ANTES AVISAR
                        if( kmActuales[0][0] - revisionTuple[7] >= revisionTuple[5]-2000 ):
                            self.actualizarNuevoEstado(revisionTuple[0], True)
                            return
                        else:
                            return
                    
                    #AVISO 25000 km ANTES DE TENERLOS QUE CAMBIAR
                    if(revisionTuple[2] == 'revision_correa' or revisionTuple[2] == 'cambio_bujias'):
                        if( kmActuales[0][0] - revisionTuple[7] >= revisionTuple[5]-25000 ):
                            self.actualizarNuevoEstado(revisionTuple[0], True)
                            return
                        else:
                            return
            
            #LO MISMO PERO SE CARGA PARA CUANDO SON DE ORGANIZACION
            else:
                #REVISIONES POR FECHA
                if(revisionTuple[5] == True):

                    #AVISOS 1 DIA ANTES.
                    if(revisionTuple[2] == 'cambio_aceite' or revisionTuple[2] == 'revision_neumaticos' or revisionTuple[2] == 'revision_fluidos'):
                        delta = revisionTuple[3] - date.today()
                        if(delta.days <= 1):
                            self.actualizarNuevoEstado(revisionTuple[0], False)
                            return
                        else:
                            return

                    #AVISOS 2 DIA ANTES.
                    if(revisionTuple[2] == 'servicio_completo' or revisionTuple[2] == 'revision_escape'):
                        delta = revisionTuple[3] - date.today()
                        if(delta.days <= 2):
                            self.actualizarNuevoEstado(revisionTuple[0], False)
                            return
                        else:
                            return
                        
                    #AVISOS 1 MES ANTES.
                    if(revisionTuple[2] == 'revision_bateria'):
                        delta = revisionTuple[3] - date.today()
                        if(delta.days <= 31):
                            self.actualizarNuevoEstado(revisionTuple[0], False)
                            return
                        else:
                            return
                        
                #REVISIONES X KM        
                else:
                    #OBTENER LOS KM ACTUALES DEL VEHICULO A REVISAR
                    obtenerKMActualesUP = "SELECT CantKM FROM `vehiculosOrganizacion` WHERE patente = %s"
                    obtenerKMActualesUPData = (revisionTuple[1],)
                    self.dbCursor.execute(obtenerKMActualesUP, obtenerKMActualesUPData)
                    kmActuales = self.dbCursor.fetchall()
                    
                    #AVISO 2000 km ANTES DE TENERLOS QUE CAMBIAR
                    if(revisionTuple[2] == 'revision_frenos' or revisionTuple[2] == 'rotacion_neumaticos'):
                        #SI LOS KM QUE SE RECORRIERON SON MAYORES A LOS DE LA PROXIMA REVISION - CUANTOS KM ANTES AVISAR
                        if( kmActuales[0][0] - revisionTuple[7] >= revisionTuple[5]-2000 ):
                            self.actualizarNuevoEstado(revisionTuple[0], False)
                            return
                        else:
                            return
                    
                    #AVISO 25000 km ANTES DE TENERLOS QUE CAMBIAR
                    if(revisionTuple[2] == 'revision_correa' or revisionTuple[2] == 'cambio_bujias'):
                        if( kmActuales[0][0] - revisionTuple[7] >= revisionTuple[5]-25000 ):
                            self.actualizarNuevoEstado(revisionTuple[0], False)
                            return
                        else:
                            return
                        
        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}

    def actualizarRevisionesRegistradasParticularDB(self):
        try:
            aux = self.obtenerRevisionesRegistradas(True)
            for i in range(len(aux)):
                self.actualizarRevision(aux[i], True)
            return True
        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}
