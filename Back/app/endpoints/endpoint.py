from datetime import date, timedelta
import mysql.connector
from app.db.mainDB import mydb, mycursor
from app.endpoints.dtos import notificacionDTO, nuevoVehiculoUsuarioOrganizacionDTO, nuevoVehiculoUsuarioParticularDTO, revisionDTO, usuarioOrganizacionLogeoDTO, usuarioOrganizacionRegistroDTO, usuarioParticularLogeoDTO, usuarioParticularRegistroDTO, usuarioRegistradoDTO, vehiculoConRevisionesDTO, vehiculoDTO, vehiculoModificarDTO, vehiculoRegistradoDTO, vehiculoRevisionDTO, viajeDTO, viajeRealizadoDTO, viajeVehiculoDTO

class dbCallService():
    def __init__(self):
        self.dbConexion = mydb
        self.dbCursor = mycursor
    
    #SI SE ME CERRO LA CONEXION, LA VUELVO A ABRIR ANTES DE REALIZAR INTERACCION CON LA DB.
    def chequearCnxDB(self):
        self.dbConexion.ping(reconnect=True, attempts=1, delay=0)

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

    def verificarUsuarioLogeoExitosoUsuarioParticularDB(self, emailIng, passwordIng):
        try:
            verifUP = "SELECT `nombre`, `apellido`, `dni`, `cuil` FROM `usuariosParticular` WHERE email = %s AND contraseña = %s"
            verifUPData = (emailIng, passwordIng)
            self.dbCursor.execute(verifUP, verifUPData)
            result = self.dbCursor.fetchall()
            #SI LA LISTA ESTA VACIA, NO ENCONTRO NADA EN EL SELECT
            if not result:
                return False
            else :
                return usuarioParticularLogeoDTO(nombre = result[0][0], apellido=result[0][1], dni=result[0][2], cuil= result[0][3], email = emailIng, esParticular=True)
            
        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}
        
    def verificarUsuarioLogeoExitosoUsuarioOrganizacionDB(self, emailIng, passwordIng):
        try:
            verifUP = "SELECT `razonSocial`, `cuit` FROM `usuariosOrganizacion` WHERE email = %s AND contraseña = %s"
            verifUPData = (emailIng, passwordIng)
            self.dbCursor.execute(verifUP, verifUPData)
            result = self.dbCursor.fetchall()
            #SI LA LISTA ESTA VACIA, NO ENCONTRO NADA EN EL SELECT
            if not result:
                return False
            else :
                return usuarioOrganizacionLogeoDTO(razonSocial=result[0][0], email=emailIng, cuit=result[0][1], esParticular=False)
            
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
        
    def generarListaVehiculos(self, lista):
        try:
            vehiculosList = []
            for i in range(len(lista)):
                vehiculosList.append(vehiculoDTO(patente=lista[i][0], modelo=lista[i][1], marca=lista[i][2], fechaFabricacion=lista[i][3], vim=lista[i][4], cantKm=lista[i][5]))
            return vehiculosList
        except mysql.connector.Error as err:
                self.dbConexion.rollback()
                return {"error":"Algo fue mal: {}".format(err)}
        
    def obtenerVehiculosParticularDB(self, cuil):
        try:
            obtVehiculoPartUP = "SELECT patente, modelo, marca, fechaFabricacion , vim, cantKM FROM vehiculosParticular WHERE cuilDueño = %s"
            obtVehiculoPartUPData = (cuil,)
            self.dbCursor.execute(obtVehiculoPartUP, obtVehiculoPartUPData)
            vehiculos=self.generarListaVehiculos(self.dbCursor.fetchall())

            if not vehiculos:
                return False
            else:
                return vehiculos
            
        except mysql.connector.Error as err:
                self.dbConexion.rollback()
                return {"error":"Algo fue mal: {}".format(err)}
        
    def obtenerVehiculosOrganizacionDB(self, cuit):
        try:
            obtVehiculoOrgUP = "SELECT patente, modelo, marca, fechaFabricacion , vim, cantKM FROM vehiculosOrganizacion WHERE cuitDueño = %s"
            obtVehiculoOrgUPData = (cuit,)
            self.dbCursor.execute(obtVehiculoOrgUP, obtVehiculoOrgUPData)
            vehiculos=self.generarListaVehiculos(self.dbCursor.fetchall())

            if not vehiculos:
                return False
            else:
                return vehiculos
            
        except mysql.connector.Error as err:
                self.dbConexion.rollback()
                return {"error":"Algo fue mal: {}".format(err)}
        
    def obtenerVehiculo(self, patente, esParticular):
        try:
            if esParticular:    
                obtVehiculoPartUP = "SELECT patente, modelo, marca, fechaFabricacion , vim, cantKM FROM vehiculosParticular WHERE patente = %s"
                obtVehiculoPartUPData = (patente,)
                self.dbCursor.execute(obtVehiculoPartUP, obtVehiculoPartUPData)
                vehiculo=self.generarListaVehiculos(self.dbCursor.fetchall())
                return vehiculo
            else:
                obtVehiculoOrgUP = "SELECT patente, modelo, marca, fechaFabricacion , vim, cantKM FROM vehiculosOrganizacion WHERE patente = %s"
                obtVehiculoOrgUPData = (patente,)
                self.dbCursor.execute(obtVehiculoOrgUP, obtVehiculoOrgUPData)
                vehiculo=self.generarListaVehiculos(self.dbCursor.fetchall())
                return vehiculo

        except mysql.connector.Error as err:
                self.dbConexion.rollback()
                return {"error":"Algo fue mal: {}".format(err)}

    def calculoRevision(self, vehiculoRevision : vehiculoRevisionDTO):
        

        vehiculoRevision.estado = "en_orden"

        if(vehiculoRevision.nombre.lower() == 'cambio_aceite'):

            aux = vehiculoRevision.fechaUltRevision+timedelta(days=183)

            if(self.fechaValida(aux)):
                vehiculoRevision.fechaProxRevision = aux
            else:
                vehiculoRevision.fechaProxRevision = date.today()+timedelta(days=183)
            return vehiculoRevision
        
        if(vehiculoRevision.nombre.lower() == 'revision_neumaticos' or vehiculoRevision.nombre.lower() == 'revision_fluidos'):
            aux = vehiculoRevision.fechaUltRevision+timedelta(days=30)
            if(self.fechaValida(aux)):
                vehiculoRevision.fechaProxRevision = aux
            else:
                vehiculoRevision.fechaProxRevision = date.today()+timedelta(days=30)
            return vehiculoRevision
        
        if(vehiculoRevision.nombre.lower() == 'servicio_completo' or vehiculoRevision.nombre.lower() == 'revision_escape'):
            aux = vehiculoRevision.fechaUltRevision+timedelta(days=365)
            if(self.fechaValida(aux)):
                vehiculoRevision.fechaProxRevision = aux
            else:
                vehiculoRevision.fechaProxRevision = date.today()+timedelta(days=365)
            return vehiculoRevision
        
        
        if(vehiculoRevision.nombre.lower() == 'revision_bateria' or vehiculoRevision.nombre.lower() == 'revision_refrig'):
            aux = vehiculoRevision.fechaUltRevision+timedelta(days=912)
            
            if(self.fechaValida(aux)):
                vehiculoRevision.fechaProxRevision = aux
            else:
                vehiculoRevision.fechaProxRevision = date.today()+timedelta(days=912)
                
            return vehiculoRevision
        
        if(vehiculoRevision.nombre.lower() == 'revision_vtv'):

            aux = vehiculoRevision.fechaUltRevision+timedelta(days=1095)

            if(self.fechaValida(aux)):
                vehiculoRevision.fechaProxRevision = aux
            else:
                vehiculoRevision.fechaProxRevision = date.today()+timedelta(days=1095)

            return vehiculoRevision


    
    def agregarRevisionVehiculoParticularDB(self, vehiculoRevision : vehiculoRevisionDTO):
        try:
            auxiliar = self.calculoRevision(vehiculoRevision)
            revisionUP="INSERT INTO `revisionesVehiculoParticular` (`nombre`, `fechaUltRevision`, `fechaProxRevision`, `estado`, `patenteVehiculo`) VALUES (%s,%s,%s,%s,%s);"
            revisionUPData=(auxiliar.nombre, auxiliar.fechaUltRevision, auxiliar.fechaProxRevision, auxiliar.estado, auxiliar.patente)
            self.dbCursor.execute(revisionUP, revisionUPData)
            self.dbConexion.commit()
            return True
        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}
        

    def agregarRevisionVehiculoOrganizacionDB(self, vehiculoRevision : vehiculoRevisionDTO):
        try:
            auxiliar = self.calculoRevision(vehiculoRevision)
            revisionUP="INSERT INTO `revisionesVehiculoOrganizacion` (`nombre`, `fechaUltRevision`, `fechaProxRevision`, `estado`, `patenteVehiculo`) VALUES (%s,%s,%s,%s,%s);"
            revisionUPData=(auxiliar.nombre, auxiliar.fechaUltRevision, auxiliar.fechaProxRevision, auxiliar.estado, auxiliar.patente)
            self.dbCursor.execute(revisionUP, revisionUPData)
            self.dbConexion.commit()
            return True
        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}
        
    
    def obtenerRevisionesRegistradas(self, esParticular):
        try:
            if esParticular:
                self.dbCursor.execute("SELECT id, patenteVehiculo, nombre, fechaProxRevision, estado FROM `revisionesVehiculoParticular`")
                patentes = self.dbCursor.fetchall()
                return patentes
            else:
                self.dbCursor.execute("SELECT id, patenteVehiculo, nombre, fechaProxRevision, estado FROM `revisionesVehiculoOrganizacion`")
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

    #TUPLA REVISION DE FORMA (ID, PATENTE, NOMBREREVISION, FECHAPROXREVISION, ESTADO)
    def actualizarRevision(self, revisionTuple, esParticular):
        try:
            #SI YA ESTA ACTUALIZADO, NO PERDER TIEMPO REACTUALIZANDO.
            if(revisionTuple[4] == 'por_vencer'):
               return

            if esParticular:

                    
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
                if(revisionTuple[2] == 'revision_bateria' or revisionTuple[2] == 'revision_refrig'):
                    delta = revisionTuple[3] - date.today()
                    if(delta.days <= 31):
                        self.actualizarNuevoEstadoPorVencer(revisionTuple[0], True)
                        return
                    else:
                        return
                    
                if(revisionTuple[2] == 'revision_vtv'):
                    delta = revisionTuple[3] - date.today()
                    if(delta.days <= 62):
                        self.actualizarNuevoEstadoPorVencer(revisionTuple[0], True)
                        return
                    else:
                        return
                        
            
            #LO MISMO PERO SE CARGA PARA CUANDO SON DE ORGANIZACION
            else:

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
                if(revisionTuple[2] == 'revision_bateria' or revisionTuple[2] == 'revision_refrig'):
                    delta = revisionTuple[3] - date.today()
                    if(delta.days <= 31):
                        self.actualizarNuevoEstadoPorVencer(revisionTuple[0], False)
                        return
                    else:
                        return
                    
                if(revisionTuple[2] == 'revision_vtv'):
                    delta = revisionTuple[3] - date.today()
                    if(delta.days <= 62):
                        self.actualizarNuevoEstadoPorVencer(revisionTuple[0], False)
                        return
                    else:
                        return
                    
                        
        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}

    def actualizarRevisionesRegistradas(self):
        try:
            aux = self.obtenerRevisionesRegistradas(True)
            for i in range(len(aux)):
                self.actualizarRevision(aux[i], True)
            
            aux2 = self.obtenerRevisionesRegistradas(False)
            for i in range(len(aux2)):
                self.actualizarRevision(aux2[i], False)

            return True
            
        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}

    def obtenerRevisionesVencidas(self, esParticular):
        try:
            if esParticular:
                self.dbCursor.execute("SELECT id, nombre, fechaProxRevision, patenteVehiculo FROM `revisionesVehiculoParticular` WHERE estado = 'por_vencer'")
                obtRevisiones = self.dbCursor.fetchall()
                return obtRevisiones
            else:
                self.dbCursor.execute("SELECT id, nombre, fechaProxRevision, patenteVehiculo FROM `revisionesVehiculoOrganizacion` WHERE estado = 'por_vencer'")
                obtRevisiones = self.dbCursor.fetchall()
                return obtRevisiones
        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}
            
    def ingresarNotificacionesDB(self):
        try:
            revisionesParticVencidas = self.obtenerRevisionesVencidas(True)
            for i in range(len(revisionesParticVencidas)):
                revPartVencUP = "INSERT IGNORE INTO `controlPendienteParticular` (`nombre`,`fechaHastaVencer`,`patenteVehiculo`,`idRevision`,`estaLeida`) VALUES (%s,%s,%s,%s,FALSE)"
                revParVencUPData = (revisionesParticVencidas[i][1], revisionesParticVencidas[i][2], revisionesParticVencidas[i][3], revisionesParticVencidas[i][0])
                self.dbCursor.execute(revPartVencUP, revParVencUPData)
                self.dbConexion.commit()

            revisionesOrgVencidas = self.obtenerRevisionesVencidas(False)
            for i in range(len(revisionesOrgVencidas)):
                revOrgVencUP = "INSERT IGNORE INTO `controlPendienteOrganizacion` (`nombre`,`fechaHastaVencer`,`patenteVehiculo`,`idRevision`,`estaLeida`) VALUES (%s,%s,%s,%s,FALSE)"
                revOrgVencUPData = (revisionesOrgVencidas[i][1], revisionesOrgVencidas[i][2], revisionesOrgVencidas[i][3], revisionesOrgVencidas[i][0])
                self.dbCursor.execute(revOrgVencUP, revOrgVencUPData)
                self.dbConexion.commit()
            return True
        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}
        
    
    def marcarNotificacionLeidaParticularDB(self, idNotif):
        try:
            marcarNotifLeidaUP = "UPDATE `controlPendienteParticular` SET estaLeida = TRUE WHERE id = %s"
            marcarNotifLeidaUPData = (idNotif,)
            self.dbCursor.execute(marcarNotifLeidaUP, marcarNotifLeidaUPData)
            self.dbConexion.commit()
            return True
        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}
        
    def marcarNotificacionLeidaOrganizacionDB(self, idNotif):
        try:
            marcarNotifLeidaUP = "UPDATE `controlPendienteOrganizacion` SET estaLeida = TRUE WHERE id = %s"
            marcarNotifLeidaUPData = (idNotif,)
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
            return vehiculoRevisionDTO(nombre=revVehiculoList[0][1], fechaUltRevision=revVehiculoList[0][2], fechaProxRevision=revVehiculoList[0][3], estado=revVehiculoList[0][4], patente=revVehiculoList[0][5])
        else:
            obtRevVehiculoUP = "SELECT * FROM `revisionesVehiculoOrganizacion` WHERE id = %s"
            obtRevVehiculoUPData = (idRevision,)
            self.dbCursor.execute(obtRevVehiculoUP, obtRevVehiculoUPData)
            revVehiculoList = self.dbCursor.fetchall()
            return vehiculoRevisionDTO(nombre=revVehiculoList[0][1], fechaUltRevision=revVehiculoList[0][2], fechaProxRevision=revVehiculoList[0][3], estado=revVehiculoList[0][4], patente=revVehiculoList[0][5])

    def fechaValida(self, fechaPrueba):
        if(fechaPrueba > date.today()):
            return True
        return False

    def calculoRevisionActualizada(self, vehiculoRevision : vehiculoRevisionDTO):
        vehiculoRevision.estado = "en_orden"

        vehiculoRevision.fechaUltRevision = vehiculoRevision.fechaProxRevision

        if(vehiculoRevision.nombre.lower() == 'cambio_aceite'):

            aux = vehiculoRevision.fechaUltRevision+timedelta(days=183)

            if(self.fechaValida(aux)):
                vehiculoRevision.fechaProxRevision = aux
            else:
                vehiculoRevision.fechaProxRevision = date.today()+timedelta(days=183)
            return vehiculoRevision
        
        if(vehiculoRevision.nombre.lower() == 'revision_neumaticos' or vehiculoRevision.nombre.lower() == 'revision_fluidos'):
            aux = vehiculoRevision.fechaUltRevision+timedelta(days=30)
            if(self.fechaValida(aux)):
                vehiculoRevision.fechaProxRevision = aux
            else:
                vehiculoRevision.fechaProxRevision = date.today()+timedelta(days=30)
            return vehiculoRevision
        
        if(vehiculoRevision.nombre.lower() == 'servicio_completo' or vehiculoRevision.nombre.lower() == 'revision_escape'):
            aux = vehiculoRevision.fechaUltRevision+timedelta(days=365)
            if(self.fechaValida(aux)):
                vehiculoRevision.fechaProxRevision = aux
            else:
                vehiculoRevision.fechaProxRevision = date.today()+timedelta(days=365)
            return vehiculoRevision
        
        
        if(vehiculoRevision.nombre.lower() == 'revision_bateria' or vehiculoRevision.nombre.lower() == 'revision_refrig'):
            aux = vehiculoRevision.fechaUltRevision+timedelta(days=912)
            if(self.fechaValida(aux)):
                vehiculoRevision.fechaProxRevision = aux
            else:
                vehiculoRevision.fechaProxRevision = date.today()+timedelta(days=912)
            return vehiculoRevision
            
        if(vehiculoRevision.nombre.lower() == 'revision_vtv'):

            aux = vehiculoRevision.fechaUltRevision+timedelta(days=1095)
            if(self.fechaValida(aux)):
                vehiculoRevision.fechaProxRevision = aux
            else:
                vehiculoRevision.fechaProxRevision = date.today()+timedelta(days=1095)

            return vehiculoRevision

    def actualizarRevisiones(self):
        try:
            revisionesVencidasVerifParticulares = self.obtenerRevisionesVencidas(True)
            revisionesVencidasVerifOrganizaciones = self.obtenerRevisionesVencidas(False)

            idRevisionesVencidasActualizarParticular = []
            idRevisionesVencidasActualizarOrganizacion = []


            #VERIFICO CUALES DE LAS VENCIDAS YA SE CUMPLIO SU FECHA/KILOMETRAJE
            for i in range(len(revisionesVencidasVerifParticulares)):
                if(revisionesVencidasVerifParticulares[i][2] <= date.today()):
                    idRevisionesVencidasActualizarParticular.append(revisionesVencidasVerifParticulares[i][0])

            for i in range(len(revisionesVencidasVerifOrganizaciones)):
                if(revisionesVencidasVerifOrganizaciones[i][2] <= date.today()):
                    idRevisionesVencidasActualizarOrganizacion.append(revisionesVencidasVerifOrganizaciones[i][0])
                
            
            #ACTUALIZO AQUELLAS REVISIONES QUE YA SE HAYAN CUMPLIDO, LAS BORRO DE NOTIFICACIONES Y LAS AGREGO AL HISTORIAL DE REVISIONES HISTÓRICO
            for i in range(len(idRevisionesVencidasActualizarParticular)):
                vehiculo = self.calculoRevisionActualizada(self.obtenerRevisionVehiculo(idRevisionesVencidasActualizarParticular[i], True))      
                revisionUpdateUP = "UPDATE `revisionesVehiculoParticular` SET fechaUltRevision=%s , fechaProxRevision=%s, estado=%s WHERE id=%s"
                revisionUpdateUPData = (vehiculo.fechaUltRevision, vehiculo.fechaProxRevision, vehiculo.estado, idRevisionesVencidasActualizarParticular[i])
                self.dbCursor.execute(revisionUpdateUP, revisionUpdateUPData)

                revisionUpdateDeleteNotificationUP = "DELETE FROM `controlPendienteParticular` WHERE idRevision=%s"
                revisionUpdateDeleteNotificationUPData = (idRevisionesVencidasActualizarParticular[i],)
                self.dbCursor.execute(revisionUpdateDeleteNotificationUP, revisionUpdateDeleteNotificationUPData)

                revisionCompletadaGuardarUP = "INSERT INTO `controlRealizadoParticular` (`nombre`, `fechaRealizacion`, `patenteVehiculo`) VALUES (%s,%s,%s)"
                revisionCompletadaGuardarUPData = (vehiculo.nombre, vehiculo.fechaUltRevision, vehiculo.patente)
                self.dbCursor.execute(revisionCompletadaGuardarUP, revisionCompletadaGuardarUPData)

                self.dbConexion.commit()

            for i in range(len(idRevisionesVencidasActualizarOrganizacion)):
                vehiculo = self.calculoRevisionActualizada(self.obtenerRevisionVehiculo(idRevisionesVencidasActualizarOrganizacion[i], False))
  
                revisionUpdateUP = "UPDATE `revisionesVehiculoOrganizacion` SET fechaUltRevision=%s, fechaProxRevision=%s, estado=%s WHERE id=%s"
                revisionUpdateUPData = (vehiculo.fechaUltRevision, vehiculo.fechaProxRevision, vehiculo.estado ,idRevisionesVencidasActualizarOrganizacion[i])
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


    def generarListaNotificacion(self, lista, esRevisiones):
        notificaciones = []
        if esRevisiones:
            for i in range(len(lista)):
                notificaciones.append(revisionDTO(nombre=lista[i][0], fechaVence=lista[i][1], patente=lista[i][2]))       
            return notificaciones
        else:
            for i in range(len(lista)):
                notificaciones.append(notificacionDTO(id=lista[i][0], nombre=lista[i][1], fechaVence=lista[i][2], patente=lista[i][3]))
            return notificaciones

        

    def obtenerNotificacionesParticularDB(self, patente):
        try:
            aux = self.obtenerVehiculo(patente, True)

            obtNotifUP= "SELECT nombre, fechaProxRevision, patenteVehiculo FROM `revisionesVehiculoParticular` WHERE patenteVehiculo = %s"
            obtNotifUPData = (patente,)
            self.dbCursor.execute(obtNotifUP, obtNotifUPData)
            notifAux = self.generarListaNotificacion(self.dbCursor.fetchall(), True)

            if not notifAux or aux == None:
                return False
            else:
                return vehiculoConRevisionesDTO(vehiculo=aux[0], listaNotif=notifAux)

        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}
        
    def obtenerNotificacionesOrganizacionDB(self, patente):
        try:
            aux = self.obtenerVehiculo(patente, False)

            obtNotifUP= "SELECT nombre, fechaProxRevision, patenteVehiculo FROM `revisionesVehiculoOrganizacion` WHERE patenteVehiculo = %s"
            obtNotifUPData = (patente,)
            self.dbCursor.execute(obtNotifUP, obtNotifUPData)
            notifAux = self.generarListaNotificacion(self.dbCursor.fetchall(), True)

            if not notifAux or aux == None:
                return False
            else:
                return vehiculoConRevisionesDTO(vehiculo=aux[0], listaNotif=notifAux)

        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}

    def obtenerNotificacionesSinLeerParticularDB(self, patente):
        try:
            obtNotifUP= "SELECT id, nombre, fechaHastaVencer, patenteVehiculo FROM `controlPendienteParticular` WHERE patenteVehiculo = %s AND estaLeida = %s"
            obtNotifUPData = (patente, False)
            self.dbCursor.execute(obtNotifUP, obtNotifUPData)
            notifAux = self.generarListaNotificacion(self.dbCursor.fetchall(), False)

            if not notifAux:
                return False
            else:
                return notifAux

        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}
      
    def obtenerNotificacionesSinLeerOrganizacionDB(self, patente):
        try:
            obtNotifUP= "SELECT id ,nombre, fechaHastaVencer, patenteVehiculo FROM `controlPendienteOrganizacion` WHERE patenteVehiculo = %s AND estaLeida = %s"
            obtNotifUPData = (patente, False)
            self.dbCursor.execute(obtNotifUP, obtNotifUPData)
            notifAux = self.generarListaNotificacion(self.dbCursor.fetchall(), False)

            if not notifAux:
                return False
            else:
                return notifAux

        except mysql.connector.Error as err:
            self.dbConexion.rollback()
            return {"error":"Algo fue mal: {}".format(err)}

    def modificarVehiculoParticularDB(self, vehiculoModif : vehiculoModificarDTO):
        try:

            #ASUMO QUE HAY CAMBIOS, BORRO TODAS LAS REVISIONES, NOTIFICACIONES Y REVISIONES COMPLETADAS ASOCIADOS AL VEHICULO. SOLO PREVISIONAL, SI LLEGO ACTUALIZO BIEN Y NO BORRO.

            nuevaFecha = None

            if(vehiculoModif.fecha != ""):
                nuevaFecha = date.fromisoformat(vehiculoModif.fecha)

            if(vehiculoModif.modelo != ""):
                vehiculoModModeloUP = "UPDATE `vehiculosParticular` SET modelo=%s WHERE patente=%s"
                vehiculoModModeloUPData = (vehiculoModif.modelo, vehiculoModif.patente)
                self.dbCursor.execute(vehiculoModModeloUP, vehiculoModModeloUPData)
                self.dbConexion.commit()

            if(vehiculoModif.marca != ""):
                vehiculoModMarcaUP = "UPDATE `vehiculosParticular` SET marca=%s WHERE patente=%s"
                vehiculoModMarcaUPData = (vehiculoModif.marca, vehiculoModif.patente)
                self.dbCursor.execute(vehiculoModMarcaUP, vehiculoModMarcaUPData)
                self.dbConexion.commit()

            if(nuevaFecha != None):
                vehiculoModnuevaFechaUP = "UPDATE `vehiculosParticular` SET fechaFabricacion=%s WHERE patente=%s"
                vehiculoModnuevaFechaUPData = (nuevaFecha, vehiculoModif.patente)
                self.dbCursor.execute(vehiculoModnuevaFechaUP, vehiculoModnuevaFechaUPData)
                self.dbConexion.commit()

            if(vehiculoModif.vim != ""):
                vehiculoModvimUP = "UPDATE `vehiculosParticular` SET vim=%s WHERE patente=%s"
                vehiculoModvimUPData = (vehiculoModif.vim, vehiculoModif.patente)
                self.dbCursor.execute(vehiculoModvimUP, vehiculoModvimUPData)
                self.dbConexion.commit()

            if(vehiculoModif.cantKM != -1):
                vehiculoModcantKMUP = "UPDATE `vehiculosParticular` SET cantKM=%s WHERE patente=%s"
                vehiculoModcantKMUPData = (vehiculoModif.cantKM, vehiculoModif.patente)
                self.dbCursor.execute(vehiculoModcantKMUP, vehiculoModcantKMUPData)
                self.dbConexion.commit()

            return True
        
        except mysql.connector.Error as err:
                self.dbConexion.rollback()
                return {"error":"Algo fue mal: {}".format(err)}
        

        
    def modificarVehiculoOrganizacionDB(self, vehiculoModif : vehiculoModificarDTO):
        try:

            #ASUMO QUE HAY CAMBIOS, BORRO TODAS LAS REVISIONES, NOTIFICACIONES Y REVISIONES COMPLETADAS ASOCIADOS AL VEHICULO. SOLO PREVISIONAL, SI LLEGO ACTUALIZO BIEN Y NO BORRO.

            nuevaFecha = None

            if(vehiculoModif.fecha != ""):
                nuevaFecha = date.fromisoformat(vehiculoModif.fecha)

            if(vehiculoModif.modelo != ""):
                vehiculoModModeloUP = "UPDATE `vehiculosOrganizacion` SET modelo=%s WHERE patente=%s"
                vehiculoModModeloUPData = (vehiculoModif.modelo, vehiculoModif.patente)
                self.dbCursor.execute(vehiculoModModeloUP, vehiculoModModeloUPData)
                self.dbConexion.commit()

            if(vehiculoModif.marca != ""):
                vehiculoModMarcaUP = "UPDATE `vehiculosOrganizacion` SET marca=%s WHERE patente=%s"
                vehiculoModMarcaUPData = (vehiculoModif.marca, vehiculoModif.patente)
                self.dbCursor.execute(vehiculoModMarcaUP, vehiculoModMarcaUPData)
                self.dbConexion.commit()

            if(nuevaFecha != None):
                vehiculoModnuevaFechaUP = "UPDATE `vehiculosOrganizacion` SET fechaFabricacion=%s WHERE patente=%s"
                vehiculoModnuevaFechaUPData = (nuevaFecha, vehiculoModif.patente)
                self.dbCursor.execute(vehiculoModnuevaFechaUP, vehiculoModnuevaFechaUPData)
                self.dbConexion.commit()

            if(vehiculoModif.vim != ""):
                vehiculoModvimUP = "UPDATE `vehiculosOrganizacion` SET vim=%s WHERE patente=%s"
                vehiculoModvimUPData = (vehiculoModif.vim, vehiculoModif.patente)
                self.dbCursor.execute(vehiculoModvimUP, vehiculoModvimUPData)
                self.dbConexion.commit()

            if(vehiculoModif.cantKM != -1):
                vehiculoModcantKMUP = "UPDATE `vehiculosOrganizacion` SET cantKM=%s WHERE patente=%s"
                vehiculoModcantKMUPData = (vehiculoModif.cantKM, vehiculoModif.patente)
                self.dbCursor.execute(vehiculoModcantKMUP, vehiculoModcantKMUPData)
                self.dbConexion.commit()

            return True
        
        except mysql.connector.Error as err:
                self.dbConexion.rollback()
                return {"error":"Algo fue mal: {}".format(err)}
        

    def eliminarRevisionVehiculoParticularDB(self, patente, nombreRevision):
        try:
            revisionPendienteDeleteUP = "DELETE FROM `controlPendienteParticular` WHERE patenteVehiculo = %s AND nombre = %s"
            revisionPendienteDeleteUPData = (patente, nombreRevision)
            self.dbCursor.execute(revisionPendienteDeleteUP, revisionPendienteDeleteUPData)
            self.dbConexion.commit()

            revisionDeleteUP = "DELETE FROM `revisionesVehiculoParticular` WHERE patenteVehiculo = %s AND nombre =%s"
            revisionDeleteUPData = (patente, nombreRevision)
            self.dbCursor.execute(revisionDeleteUP, revisionDeleteUPData)
            self.dbConexion.commit()

            return True
        except mysql.connector.Error as err:
                self.dbConexion.rollback()
                return {"error":"Algo fue mal: {}".format(err)}
        
        
    def eliminarRevisionVehiculoOrganizacionDB(self, patente, nombreRevision):
        try:
            revisionPendienteDeleteUP = "DELETE FROM `controlPendienteOrganizacion` WHERE patenteVehiculo = %s AND nombre = %s"
            revisionPendienteDeleteUPData = (patente, nombreRevision)
            self.dbCursor.execute(revisionPendienteDeleteUP, revisionPendienteDeleteUPData)
            self.dbConexion.commit()

            revisionDeleteUP = "DELETE FROM `revisionesVehiculoOrganizacion` WHERE patenteVehiculo = %s AND nombre =%s"
            revisionDeleteUPData = (patente, nombreRevision)
            self.dbCursor.execute(revisionDeleteUP, revisionDeleteUPData)
            self.dbConexion.commit()

            return True
        except mysql.connector.Error as err:
                self.dbConexion.rollback()
                return {"error":"Algo fue mal: {}".format(err)}
        
    def obtenerViajesVehiculoDB(self, patente):
        try:
            obtViajeVehiculoUP= "SELECT * FROM `viajesPendienteParticular` WHERE patenteVehiculo = %s"
            obtViajeVehiculoUPData = (patente,)
            self.dbCursor.execute(obtViajeVehiculoUP, obtViajeVehiculoUPData)
            viajes = self.dbCursor.fetchall()

            viajesLista = []
            for i in range(len(viajes)):
                viajesLista.append(viajeVehiculoDTO(idViaje=viajes[i][0], fechaInicio=viajes[i][1], cantKM=viajes[i][2], nombreViaje=viajes[i][3], estadoViaje=viajes[i][4], patenteVehiculo=viajes[i][5]))

            return viajesLista
            

        
        except mysql.connector.Error as err:
                self.dbConexion.rollback()
                return {"error":"Algo fue mal: {}".format(err)}
        
    def eliminarViajeVehiculoDB(self, id):
        try:
            dltViajeVehiculoUP = "DELETE FROM `viajesPendienteParticular` WHERE id = %s"
            dltViajeVehiculoUPData = (id,)
            self.dbCursor.execute(dltViajeVehiculoUP, dltViajeVehiculoUPData)
            self.dbConexion.commit()

            return True

        except mysql.connector.Error as err:
                self.dbConexion.rollback()
                return {"error":"Algo fue mal: {}".format(err)}