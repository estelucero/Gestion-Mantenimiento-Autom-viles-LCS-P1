import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="shurimashuffle"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS tp_inicial_database")

mycursor.execute("USE tp_inicial_database")

mycursor.execute("CREATE TABLE IF NOT EXISTS usuariosParticular (nombre VARCHAR(20), apellido VARCHAR(25), dni INTEGER(10), email VARCHAR(60), contraseña VARCHAR(30), cuil VARCHAR(13) PRIMARY KEY)")

mycursor.execute("CREATE TABLE IF NOT EXISTS usuariosOrganizacion (razonSocial VARCHAR(20), email VARCHAR(60), contraseña VARCHAR(30), cuit VARCHAR(13) PRIMARY KEY)")

mycursor.execute("CREATE TABLE IF NOT EXISTS vehiculosParticular (patente VARCHAR(7) PRIMARY KEY, modelo VARCHAR(60), marca VARCHAR(60), fechaFabricacion DATE, vim VARCHAR(17), cantKM DOUBLE(10,2), tipoCombustible VARCHAR(10), cuilDueño VARCHAR(13), FOREIGN KEY(cuilDueño) REFERENCES usuariosParticular(cuil))")

mycursor.execute("CREATE TABLE IF NOT EXISTS vehiculosOrganizacion (patente VARCHAR(7) PRIMARY KEY, modelo VARCHAR(60), marca VARCHAR(60), fechaFabricacion DATE, vim VARCHAR(17), cantKM DOUBLE(10,2), tipoCombustible VARCHAR(10), cuitDueño VARCHAR(13), FOREIGN KEY(cuitDueño) REFERENCES usuariosOrganizacion(cuit))")

mycursor.execute("CREATE TABLE IF NOT EXISTS viajesPendientesParticular (fechaInicio DATE, distanciaKM DOUBLE(7, 2), nombre VARCHAR(30), id VARCHAR(10) PRIMARY KEY, estado BOOLEAN, patenteVehiculo VARCHAR(7), cuilUsuario VARCHAR(13), FOREIGN KEY(patenteVehiculo) REFERENCES vehiculosParticular(patente), FOREIGN KEY(cuilUsuario) REFERENCES usuariosParticular(cuil))")

mycursor.execute("CREATE TABLE IF NOT EXISTS revisionesVehiculoParticular (nombre VARCHAR(20) PRIMARY KEY, fechaUltRevision DATE, periodicidadRevision DATE, patenteVehiculo VARCHAR(7), FOREIGN KEY(patenteVehiculo) REFERENCES vehiculosParticular(patente))")

mycursor.execute("CREATE TABLE IF NOT EXISTS revisionesVehiculoOrganizacion (nombre VARCHAR(20) PRIMARY KEY, fechaUltRevision DATE, periodicidadRevision DATE, estado VARCHAR(15), patenteVehiculo VARCHAR(7), FOREIGN KEY(patenteVehiculo) REFERENCES vehiculosOrganizacion(patente))")

mycursor.execute("CREATE TABLE IF NOT EXISTS controlPendienteParticular (fechaHastaVencer DATE, id VARCHAR(10) PRIMARY KEY, cuilDueño VARCHAR(13), patenteVehiculo VARCHAR(7), FOREIGN KEY(cuilDueño) REFERENCES usuariosParticular(cuil), FOREIGN KEY(patenteVehiculo) REFERENCES vehiculosParticular(patente))")

mycursor.execute("CREATE TABLE IF NOT EXISTS controlPendienteOrganizacion (fechaHastaVencer DATE, id VARCHAR(10) PRIMARY KEY, cuitDueño VARCHAR(13), patenteVehiculo VARCHAR(7), FOREIGN KEY(cuitDueño) REFERENCES usuariosOrganizacion(cuit), FOREIGN KEY(patenteVehiculo) REFERENCES vehiculosOrganizacion(patente))")

mycursor.execute("CREATE TABLE IF NOT EXISTS controlRealizadoParticular (fechaRealizacion DATE, id VARCHAR(10) PRIMARY KEY, cuilDueño VARCHAR(13), patenteVehiculo VARCHAR(7), FOREIGN KEY(cuilDueño) REFERENCES usuariosParticular(cuil), FOREIGN KEY(patenteVehiculo) REFERENCES vehiculosParticular(patente))")

mycursor.execute("CREATE TABLE IF NOT EXISTS controlRealizadoOrganizacion (fechaRealizacion DATE, id VARCHAR(10) PRIMARY KEY, cuitDueño VARCHAR(13), patenteVehiculo VARCHAR(7), FOREIGN KEY(cuitDueño) REFERENCES usuariosOrganizacion(cuit), FOREIGN KEY(patenteVehiculo) REFERENCES vehiculosOrganizacion(patente))")