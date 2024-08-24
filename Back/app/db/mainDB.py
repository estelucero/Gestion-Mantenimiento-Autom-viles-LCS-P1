import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="-"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS tp_inicial_database")

mycursor.execute("USE tp_inicial_database")

mycursor.execute("CREATE TABLE usuariosParticular (nombre VARCHAR(20), apellido VARCHAR(25), dni INTEGER(10), email VARCHAR(60), contraseña VARCHAR(30), cuil VARCHAR(13))")

""" PARA VER LAS DB QUE TENGA CREADAS
mycursor.execute("SHOW DATABASES")
for db in mycursor:
    print(db)
"""