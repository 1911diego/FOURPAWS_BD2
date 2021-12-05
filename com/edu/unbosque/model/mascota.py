import datetime
from com.edu.unbosque.model import model as modelo
from com.edu.unbosque.connection import ConnectionPostgres as c

connection = c.createConnection()

def createPet(id_propietario, nombre, fecha_nacimiento, id_especie, tamano, peligroso, fotografia, microchip, sexo):

    especie = "dog"
    if id_especie == "2":
        especie = "cat"

    cursor = connection.cursor()
    cursor.execute("INSERT INTO mascota (id_propietario, nombre, fecha_nacimiento, id_especie, tamano, peligroso,fotografia, microchip, sexo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (id_propietario, nombre, fecha_nacimiento, id_especie, tamano, peligroso, fotografia, microchip, sexo))
    modelo.crearMascota(id_propietario, nombre, especie)
    connection.commit()
    cursor.close()
    connection.close()

def listaMascotas(id_propietario):
    try:
       cursor = connection.sursor()
       mascotas = cursor.execute("SELECT * from mascota WHERE id_propietario = '" + id_propietario + "'")
       return mascotas
    except Exception as e:
        print(e)
        return "error"

def crearCaso(id_caso, descripcion):
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO caso (id_caso, nombre) values (%s, %s)", (id_caso, descripcion))
        cursor.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(e)
        return "error"