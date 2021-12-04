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



createPet("000898a", "Candy", "2020-12-15", "1", 145.6, "NO", "urlfoto", "TRUE", "HEMBRA")