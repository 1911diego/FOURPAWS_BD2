import datetime

import model.connection as c

connection = c.createConnection()


def createPet(id_propietario, nombre, fecha_nacimiento, id_especie, tamano, peligroso, fotografia, microchip, sexo):
    cursor = connection.cursor()

    cursor.execute("INSERT INTO mascota (id_propietario, nombre, fecha_nacimiento, id_especie, tamano, peligroso,fotografia, microchip, sexo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (id_propietario, nombre, fecha_nacimiento, id_especie, tamano, peligroso, fotografia, microchip, sexo))
    connection.commit()
    cursor.close()
    connection.close()


createPet("00008000", "Mara", "2020-12-15", "1", 145.6, "NO", "urlfoto", "TRUE", "HEMBRA")