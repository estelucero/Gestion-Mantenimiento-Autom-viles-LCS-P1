from datetime import date, timedelta
import mysql.connector
from app.db.mainDB import mydb, mycursor
from app.endpoints.dtos import notifMarcarLeidaDTO, nuevoVehiculoUsuarioOrganizacionDTO, nuevoVehiculoUsuarioParticularDTO, usuarioOrganizacionRegistroDTO, usuarioParticularRegistroDTO, usuarioRegistradoDTO, vehiculoRegistradoDTO, vehiculoRevisionDTO, verificacionUsuarioLogeoDTO, viajeDTO, viajeRealizadoDTO

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
                vehiculoUP = "INSERT INTO `vehiculosParticular` (`patente`, `modelo`, `marca`, `fechaFabricacion`, `vim`, `cantKM`, `cuilDueño`) VALUES (%s,%s,%s,%s,%s,%s,%s);"
                vehiculoUPData = (vehiculoNuevo.patente, vehiculoNuevo.modelo, vehiculoNuevo.marca, vehiculoNuevo.fechaFabricacion, vehiculoNuevo.vim, vehiculoNuevo.cantKm, vehiculoNuevo.cuilDueño)
                self.dbCursor.execute(vehiculoUP, vehiculoUPData)
                self.dbConexion.commit()
                return vehiculoRegistradoDTO(patente = vehiculoNuevo.patente, marca = vehiculoNuevo.marca, modelo = vehiculoNuevo.modelo)
            
            except mysql.connector.Error as err:
                self.dbConexion.rollback()
                return {"error":"Algo fue mal: {}".format(err)}
            
    def registrarNuevoVehiculoUsuarioOrganizacionDB(self, vehiculoNuevo : nuevoVehiculoUsuarioOrganizacionDTO):
            try:
                vehiculoUP = "INSERT INTO `vehiculosOrganizacion` (`patente`, `modelo`, `marca`, `fechaFabricacion`, `vim`, `cantKM`, `cuitDueño`) VALUES (%s,%s,%s,%s,%s,%s,%s);"
                vehiculoUPData = (vehiculoNuevo.patente, vehiculoNuevo.modelo, vehiculoNuevo.marca, vehiculoNuevo.fechaFabricacion, vehiculoNuevo.vim, vehiculoNuevo.cantKm, vehiculoNuevo.cuitDueño)
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
            vehiculoRevision.kmActual = self.obtenerCantKMActualesVehiculo(vehiculoRevision.patente, esParticular)
              
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


    def actualizarNuevoEstadoPorVencer(self, idRevision, esParticular):

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
        
    def obtenerCantKMActualesVehiculo(self, patente, esParticular):
        if esParticular:
            obtenerKMActualesUP = "SELECT CantKM FROM `vehiculosParticular` WHERE patente = %s"
            obtenerKMActualesUPData = (patente,)
            self.dbCursor.execute(obtenerKMActualesUP, obtenerKMActualesUPData)
            kmActuales = self.dbCursor.fetchall()
            return kmActuales[0][0]
        else:
            obtenerKMActualesUP = "SELECT CantKM FROM `vehiculosOrganizacion` WHERE patente = %s"
            obtenerKMActualesUPData = (patente,)
            self.dbCursor.execute(obtenerKMActualesUP, obtenerKMActualesUPData)
            kmActuales = self.dbCursor.fetchall()
            return kmActuales[0][0]

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
                            self.actualizarNuevoEstadoPorVencer(revisionTuple[0], True)
                            return
                        else:
                            return

                    #AVISOS 2 DIA ANTES.    
                    if(revisionTuple[2] == 'servicio_completo' or revisionTuple[2] == 'revision_escape'):
                        delta = revisionTuple[3] - date.today()
                        if(delta.days <= 2):
                            self.actualizarNuevoEstadoPorVencer(revisionTuple[0], True)
                            return
                        else:
                            return
                    
                    #AVISOS 1 MES ANTES.
                    if(revisionTuple[2] == 'revision_bateria'):
                        delta = revisionTuple[3] - date.today()
                        if(delta.days <= 31):
                            self.actualizarNuevoEstadoPorVencer(revisionTuple[0], True)
                            return
                        else:
                            return
                        
                #REVISIONES X KM        
                else:

                    #OBTENER LOS KM ACTUALES DEL VEHICULO A REVISAR
                    kmActuales = self.obtenerCantKMActualesVehiculo(revisionTuple[1], True)
                    
                    #AVISO 2000 km ANTES DE TENERLOS QUE CAMBIAR
                    if(revisionTuple[2] == 'revision_frenos' or revisionTuple[2] == 'rotacion_neumaticos'):
                        #SI LOS KM QUE SE RECORRIERON SON MAYORES A LOS DE LA PROXIMA REVISION - CUANTOS KM ANTES AVISAR
                        if( kmActuales - revisionTuple[7] >= revisionTuple[4]-2000 ):
                            self.actualizarNuevoEstadoPorVencer(revisionTuple[0], True)
                            return
                        else:
                            return
                    
                    #AVISO 25000 km ANTES DE TENERLOS QUE CAMBIAR
                    if(revisionTuple[2] == 'revision_correa' or revisionTuple[2] == 'cambio_bujias'):
                        if( kmActuales - revisionTuple[7] >= revisionTuple[4]-25000 ):
                            self.actualizarNuevoEstadoPorVencer(revisionTuple[0], True)
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
                            self.actualizarNuevoEstadoPorVencer(revisionTuple[0], False)
                            return
                        else:
                            return

                    #AVISOS 2 DIA ANTES.
                    if(revisionTuple[2] == 'servicio_completo' or revisionTuple[2] == 'revision_escape'):
                        delta = revisionTuple[3] - date.today()
                        if(delta.days <= 2):
                            self.actualizarNuevoEstadoPorVencer(revisionTuple[0], False)
                            return
                        else:
                            return
                        
                    #AVISOS 1 MES ANTES.
                    if(revisionTuple[2] == 'revision_bateria'):
                        delta = revisionTuple[3] - date.today()
                        if(delta.days <= 31):
                            self.actualizarNuevoEstadoPorVencer(revisionTuple[0], False)
                            return
                        else:
                            return
                        
                #REVISIONES X KM        
                else:
                    #OBTENER LOS KM ACTUALES DEL VEHICULO A REVISAR
                    kmActuales = self.obtenerCantKMActualesVehiculo(revisionTuple[1], False)
                    
                    #AVISO 2000 km ANTES DE TENERLOS QUE CAMBIAR
                    if(revisionTuple[2] == 'revision_frenos' or revisionTuple[2] == 'rotacion_neumaticos'):
                        #SI LOS KM QUE SE RECORRIERON SON MAYORES A LOS DE LA PROXIMA REVISION - CUANTOS KM ANTES AVISAR
                        if( kmActuales - revisionTuple[7] >= revisionTuple[4]-2000 ):
                            self.actualizarNuevoEstadoPorVencer(revisionTuple[0], False)
                            return
                        else:
                            return
                    
                    #AVISO 25000 km ANTES DE TENERLOS QUE CAMBIAR
                    if(revisionTuple[2] == 'revision_correa' or revisionTuple[2] == 'cambio_bujias'):
                        if( kmActuales - revisionTuple[7] >= revisionTuple[4]-25000 ):
                            self.actualizarNuevoEstadoPorVencer(revisionTuple[0], False)
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


    def obtenerRevisionesVencidas(self, esParticular):
        try:
            if esParticular:
                self.dbCursor.execute("SELECT id, nombre, fechaProxRevision, kmProxRevision, patenteVehiculo, revisaPorFecha FROM `revisionesVehiculoParticular` WHERE estado = 'por_vencer'")
                obtRevisiones = self.dbCursor.fetchall()
                return obtRevisiones
            else:
                self.dbCursor.execute("SELECT id, nombre, fechaProxRevision, kmProxRevision, patenteVehiculo, revisaPorFecha FROM `revisionesVehiculoOrganizacion` WHERE estado = 'por_vencer'")
                obtRevisiones = self.dbCursor.fetchall()
                return obtRevisiones
        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}
            
    def ingresarNotificacionesParticularDB(self):
        try:
            revisionesParticVencidas = self.obtenerRevisionesVencidas(True)
            for i in range(len(revisionesParticVencidas)):
                revPartVencUP = "INSERT INTO `controlPendienteParticular` (`nombre`,`fechaHastaVencer`,`kmHastaVencer`,`patenteVehiculo`,`idRevision`,`estaLeida`) VALUES (%s,%s,%s,%s,%s,FALSE)"
                revParVencUPData = (revisionesParticVencidas[i][1], revisionesParticVencidas[i][2], revisionesParticVencidas[i][3], revisionesParticVencidas[i][4], revisionesParticVencidas[i][0])
                self.dbCursor.execute(revPartVencUP, revParVencUPData)
                self.dbConexion.commit()
            return True
        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}
        
    
    def marcarNotificacionLeidaDB(self, notif : notifMarcarLeidaDTO):
        try:
            marcarNotifLeidaUP = "UPDATE `controlPendienteParticular` SET estaLeida = TRUE WHERE id = %s"
            marcarNotifLeidaUPData = (notif.idNotif,)
            self.dbCursor.execute(marcarNotifLeidaUP, marcarNotifLeidaUPData)
            self.dbConexion.commit()
            return True
        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}
        

    def obtenerRevisionVehiculo(self, idRevision, esParticular):
        if esParticular:
            obtRevVehiculoUP = "SELECT * FROM `revisionesVehiculoParticular` WHERE id = %s"
            obtRevVehiculoUPData = (idRevision,)
            self.dbCursor.execute(obtRevVehiculoUP, obtRevVehiculoUPData)
            revVehiculoList = self.dbCursor.fetchall()
            return vehiculoRevisionDTO(nombre=revVehiculoList[0][1], fechaUltRevision=revVehiculoList[0][2], fechaProxRevision=revVehiculoList[0][3], kmActual=revVehiculoList[0][4], kmProxRevision=revVehiculoList[0][5], estado=revVehiculoList[0][6], patente=revVehiculoList[0][7], revisionPorFecha=revVehiculoList[0][8])
        else:
            obtRevVehiculoUP = "SELECT * FROM `revisionesVehiculoOrganizacion` WHERE id = %s"
            obtRevVehiculoUPData = (idRevision,)
            self.dbCursor.execute(obtRevVehiculoUP, obtRevVehiculoUPData)
            revVehiculoList = self.dbCursor.fetchall()
            return vehiculoRevisionDTO(nombre=revVehiculoList[0][1], fechaUltRevision=revVehiculoList[0][2], fechaProxRevision=revVehiculoList[0][3], kmActual=revVehiculoList[0][4], kmProxRevision=revVehiculoList[0][5], estado=revVehiculoList[0][6], patente=revVehiculoList[0][7], revisionPorFecha=revVehiculoList[0][8])

    def calculoRevisionActualizada(self, vehiculoRevision : vehiculoRevisionDTO, esParticular):
        vehiculoRevision.estado = "en_orden"

        if vehiculoRevision.revisionPorFecha:

            vehiculoRevision.fechaUltRevision = vehiculoRevision.fechaProxRevision

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
            vehiculoRevision.kmActual = self.obtenerCantKMActualesVehiculo(vehiculoRevision.patente, esParticular)       
                
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
            
    def actualizarRevisiones(self):
        try:
            revisionesVencidasVerifParticulares = self.obtenerRevisionesVencidas(True)
            revisionesVencidasVerifOrganizaciones = self.obtenerRevisionesVencidas(False)

            idRevisionesVencidasActualizarParticular = []
            idRevisionesVencidasActualizarOrganizacion = []


            #VERIFICO CUALES DE LAS VENCIDAS YA SE CUMPLIO SU FECHA/KILOMETRAJE
            for i in range(len(revisionesVencidasVerifParticulares)):
                if(revisionesVencidasVerifParticulares[i][5] == True):
                    if(revisionesVencidasVerifParticulares[i][2] <= date.today()):
                        idRevisionesVencidasActualizarParticular.append(revisionesVencidasVerifParticulares[i][0])
                else:
                    if(revisionesVencidasVerifParticulares[i][3] <= self.obtenerCantKMActualesVehiculo(revisionesVencidasVerifParticulares[i][4], True)):
                        idRevisionesVencidasActualizarParticular.append(revisionesVencidasVerifParticulares[i][0])

            for i in range(len(revisionesVencidasVerifOrganizaciones)):
                if(revisionesVencidasVerifOrganizaciones[i][5] == True):
                    if(revisionesVencidasVerifOrganizaciones[i][2] <= date.today()):
                        idRevisionesVencidasActualizarOrganizacion.append(revisionesVencidasVerifOrganizaciones[i][0])
                else:
                    if(revisionesVencidasVerifOrganizaciones[i][3] <= self.obtenerCantKMActualesVehiculo(revisionesVencidasVerifOrganizaciones[i][4], False)):
                        idRevisionesVencidasActualizarOrganizacion.append(revisionesVencidasVerifOrganizaciones[i][0])
            
            #ACTUALIZO AQUELLAS REVISIONES QUE YA SE HAYAN CUMPLIDO, LAS BORRO DE NOTIFICACIONES Y LAS AGREGO AL HISTORIAL DE REVISIONES HISTÓRICO
            for i in range(len(idRevisionesVencidasActualizarParticular)):
                vehiculo = self.calculoRevisionActualizada(self.obtenerRevisionVehiculo(idRevisionesVencidasActualizarParticular[i], True), True)      
                revisionUpdateUP = "UPDATE `revisionesVehiculoParticular` SET fechaUltRevision=%s , fechaProxRevision=%s , kmUltRevision=%s , kmProxRevision=%s, estado=%s WHERE id=%s"
                revisionUpdateUPData = (vehiculo.fechaUltRevision, vehiculo.fechaProxRevision, vehiculo.kmActual, vehiculo.kmProxRevision, vehiculo.estado, idRevisionesVencidasActualizarParticular[i])
                self.dbCursor.execute(revisionUpdateUP, revisionUpdateUPData)

                revisionUpdateDeleteNotificationUP = "DELETE FROM `controlPendienteParticular` WHERE idRevision=%s"
                revisionUpdateDeleteNotificationUPData = (idRevisionesVencidasActualizarParticular[i],)
                self.dbCursor.execute(revisionUpdateDeleteNotificationUP, revisionUpdateDeleteNotificationUPData)

                revisionCompletadaGuardarUP = "INSERT INTO `controlRealizadoParticular` (`nombre`, `fechaRealizacion`, `patenteVehiculo`) VALUES (%s,%s,%s)"
                revisionCompletadaGuardarUPData = (vehiculo.nombre, vehiculo.fechaUltRevision, vehiculo.patente)
                self.dbCursor.execute(revisionCompletadaGuardarUP, revisionCompletadaGuardarUPData)

                self.dbConexion.commit()

            for i in range(len(idRevisionesVencidasActualizarOrganizacion)):
                vehiculo = self.calculoRevisionActualizada(self.obtenerRevisionVehiculo(idRevisionesVencidasActualizarOrganizacion[i], False), False)
  
                revisionUpdateUP = "UPDATE `revisionesVehiculoOrganizacion` SET fechaUltRevision=%s , fechaProxRevision=%s , kmUltRevision=%s , kmProxRevision=%s, estado=%s WHERE id=%s"
                revisionUpdateUPData = (vehiculo.fechaUltRevision, vehiculo.fechaProxRevision, vehiculo.kmActual, vehiculo.kmProxRevision, vehiculo.estado ,idRevisionesVencidasActualizarParticular[i])
                self.dbCursor.execute(revisionUpdateUP, revisionUpdateUPData)

                revisionUpdateDeleteNotificationUP = "DELETE FROM `controlPendienteOrganizacion` WHERE idRevision=%s"
                revisionUpdateDeleteNotificationUPData = (idRevisionesVencidasActualizarOrganizacion[i],)
                self.dbCursor.execute(revisionUpdateDeleteNotificationUP, revisionUpdateDeleteNotificationUPData)

                revisionCompletadaGuardarUP = "INSERT INTO `controlRealizadoOrganizacion` (`nombre`, `fechaRealizacion`, `patenteVehiculo`) VALUES (%s,%s,%s)"
                revisionCompletadaGuardarUPData = (vehiculo.nombre, vehiculo.fechaUltRevision, vehiculo.patente)
                self.dbCursor.execute(revisionCompletadaGuardarUP, revisionCompletadaGuardarUPData)

                self.dbConexion.commit()

            return True
        
        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}
        
    def ingresarViajeDB(self, viaje : viajeDTO):
        try:
            ingresarViajeUP = "INSERT INTO `viajesPendienteParticular` (`fechaInicio`, `distanciaKM`, `nombre`, `estado`, `patenteVehiculo`) VALUES (%s,%s,%s,%s,%s)"
            ingresarViajeUPData = (viaje.fechaInicio, viaje.distanciaKM, viaje.nombre, False, viaje.patente)
            self.dbCursor.execute(ingresarViajeUP, ingresarViajeUPData)
            self.dbConexion.commit()
            return True
        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}
        
    def obtenerViajesRealizados(self):
        try:
            self.dbCursor.execute("SELECT id, fechaInicio, estado, patenteVehiculo, distanciaKM FROM `viajesPendienteParticular`")
            aux = self.dbCursor.fetchall()
            viajesRealizados = []

            for i in range(len(aux)):
                if(aux[i][1] <= date.today()) and aux[i][2] == False:
                    viajesRealizados.append(viajeRealizadoDTO(id=aux[i][0], distanciaKM=aux[i][4], patente=aux[i][3]))

            return viajesRealizados
            
        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}

    def agregarKMVehiculoParticular(self, cantKM, patente):
        try:
            agregarKMUP = "UPDATE `vehiculosParticular` SET cantKM=%s WHERE patente = %s"
            agregarKMUPData = (self.obtenerCantKMActualesVehiculo(patente,True)+cantKM, patente)
            self.dbCursor.execute(agregarKMUP, agregarKMUPData)
            self.dbConexion.commit()
            return
        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}

    def realizarViaje(self, idViaje):
        try:
            realizarViajeUP = "UPDATE `viajesPendienteParticular` SET estado=%s WHERE id=%s"
            realizarViajeUPData = (True, idViaje)
            self.dbCursor.execute(realizarViajeUP, realizarViajeUPData)
            self.dbConexion.commit()
            return
        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}

    def actualizarViajesDB(self):
        aux = self.obtenerViajesRealizados()
        for i in range(len(aux)):
            self.agregarKMVehiculoParticular(aux[i].distanciaKM, aux[i].patente)
            self.realizarViaje(aux[i].id)

        return True


        



            
    