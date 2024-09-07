import mysql.connector

from datosConexion import datosSQL

data = datosSQL()

mydb = mysql.connector.connect(
  host= data.host,
  user= data.user,
  passwd= data.password,
  database= data.database
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS usuariosParticular (nombre VARCHAR(20), apellido VARCHAR(25), dni VARCHAR(10), email VARCHAR(60), contraseña VARCHAR(30), cuil VARCHAR(13) PRIMARY KEY, UNIQUE(email), UNIQUE(dni));")

mycursor.execute("CREATE TABLE IF NOT EXISTS usuariosOrganizacion (razonSocial VARCHAR(50), email VARCHAR(60), contraseña VARCHAR(30), cuit VARCHAR(13) PRIMARY KEY, UNIQUE(email));")

mycursor.execute("CREATE TABLE IF NOT EXISTS vehiculosParticular (patente VARCHAR(7) PRIMARY KEY, modelo VARCHAR(60), marca VARCHAR(60), fechaFabricacion DATE, vim VARCHAR(17), cantKM DOUBLE(10,2), cuilDueño VARCHAR(13), UNIQUE(vim),FOREIGN KEY(cuilDueño) REFERENCES usuariosParticular(cuil));")

mycursor.execute("CREATE TABLE IF NOT EXISTS vehiculosOrganizacion (patente VARCHAR(7) PRIMARY KEY, modelo VARCHAR(60), marca VARCHAR(60), fechaFabricacion DATE, vim VARCHAR(17), cantKM DOUBLE(10,2), cuitDueño VARCHAR(13), UNIQUE(vim), FOREIGN KEY(cuitDueño) REFERENCES usuariosOrganizacion(cuit));")

mycursor.execute("CREATE TABLE IF NOT EXISTS viajesPendienteParticular (id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, fechaInicio DATE, distanciaKM DOUBLE(7, 2), nombre VARCHAR(30), estado BOOLEAN, patenteVehiculo VARCHAR(7), FOREIGN KEY(patenteVehiculo) REFERENCES vehiculosParticular(patente));")

mycursor.execute("CREATE TABLE IF NOT EXISTS revisionesVehiculoParticular (id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(20), fechaUltRevision DATE, fechaProxRevision DATE, estado VARCHAR(15), patenteVehiculo VARCHAR(7), UNIQUE(patenteVehiculo, nombre), FOREIGN KEY(patenteVehiculo) REFERENCES vehiculosParticular(patente));")

mycursor.execute("CREATE TABLE IF NOT EXISTS revisionesVehiculoOrganizacion (id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(20), fechaUltRevision DATE, fechaProxRevision DATE, estado VARCHAR(15), patenteVehiculo VARCHAR(7), UNIQUE(patenteVehiculo, nombre), FOREIGN KEY(patenteVehiculo) REFERENCES vehiculosOrganizacion(patente));")
                                                                                                                                                                                                                                                                    #SI HAY ERROR SON ESTOS UNIQUES, ES POR LA FECHA NO FIXEADA PARA TESTING.                                                              
mycursor.execute("CREATE TABLE IF NOT EXISTS controlPendienteParticular (id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(20), fechaHastaVencer DATE, patenteVehiculo VARCHAR(7), idRevision INT UNSIGNED, estaLeida BOOLEAN, UNIQUE(patenteVehiculo, nombre), FOREIGN KEY(patenteVehiculo) REFERENCES vehiculosParticular(patente), FOREIGN KEY(idRevision) REFERENCES revisionesVehiculoParticular(id));")

mycursor.execute("CREATE TABLE IF NOT EXISTS controlPendienteOrganizacion (id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(20), fechaHastaVencer DATE, patenteVehiculo VARCHAR(7), idRevision INT UNSIGNED, estaLeida BOOLEAN, UNIQUE(patenteVehiculo, nombre), FOREIGN KEY(patenteVehiculo) REFERENCES vehiculosOrganizacion(patente), FOREIGN KEY(idRevision) REFERENCES revisionesVehiculoOrganizacion(id));")

mycursor.execute("CREATE TABLE IF NOT EXISTS controlRealizadoParticular (id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(20), fechaRealizacion DATE, patenteVehiculo VARCHAR(7), FOREIGN KEY(patenteVehiculo) REFERENCES vehiculosParticular(patente));")

mycursor.execute("CREATE TABLE IF NOT EXISTS controlRealizadoOrganizacion (id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(20), fechaRealizacion DATE, patenteVehiculo VARCHAR(7), FOREIGN KEY(patenteVehiculo) REFERENCES vehiculosOrganizacion(patente));")

""" EJEMPLO DE COMO INTERACTUAR CON LA DB
sql = "INSERT INTO `usuariosParticular` (`nombre`, `apellido`, `dni`, `email`, `contraseña`, `cuil`) VALUES ('asd', 'asd', '22222', 'asd', 'asd', '12315523');"
mycursor.execute(sql)
mydb.commit()
"""