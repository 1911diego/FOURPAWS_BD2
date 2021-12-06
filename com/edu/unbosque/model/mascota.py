import datetime
import random

from com.edu.unbosque.model import model as modelo
from com.edu.unbosque.connection import ConnectionPostgres as c
from com.edu.unbosque.connection import MongoDB as mongo
import numpy

connection = c.createConnection()


def createPet(id_propietario, nombre, fecha_nacimiento, id_especie, tamano, peligroso, fotografia, microchip, sexo):
    try:
        especie = "dog"
        if id_especie == "2":
            especie = "cat"

        cursor = connection.cursor()
        cursor.execute(
        "INSERT INTO mascota (id_propietario, nombre, fecha_nacimiento, id_especie, tamano, peligroso,fotografia, microchip, sexo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (id_propietario, nombre, fecha_nacimiento, id_especie, tamano, peligroso, fotografia, microchip, sexo))
        connection.commit()
        cursor.execute(
        "SELECT id_mascota FROM mascota WHERE id_propietario = '" + id_propietario + "' AND fecha_nacimiento = '" + fecha_nacimiento + "' AND nombre = '" + nombre + "'")
        id_mascota = cursor.fetchone()[0]
        modelo.crearMascota(id_propietario, id_mascota, especie)
        modelo.taggearFoto1(id_mascota, fotografia)
        cursor.close()
        connection.close()
        return 1
    except Exception as e:
        print (e)
        return 0


def listaMascotas(id_propietario):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * from mascota WHERE id_propietario = '" + id_propietario + "'")
        mascotas = cursor.fetchall()
        return mascotas
    except Exception as e:
        print(e)
        return "error"

def actualizarMascota(id_propietario, nombre, fecha_nacimiento, id_especie, tamano, peligroso, fotografia, microchip, sexo):
    try:
        cursor = connection.cursor()
    except Exception as e:
        return "error"

def totalMacotasEspecie():
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT e.nombre as especie, COUNT(m) as cantidad FROM mascota as m INNER JOIN especie as e ON m.id_especie = e.id_especie GROUP BY e.nombre")
        mas = cursor.fetchall()
        return mas
    except Exception as e:
        print(e)
        return 'error'


def totalMascotasMicro():
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(m) as cantidad FROM mascota AS m WHERE m.microchip = true")
        micro = cursor.fetchone()
        return micro
    except Exception as e:
        return 'error'


def totalMascotasEst():
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(m) as cantidad FROM mascota AS m INNER JOIN registro AS r ON m.id_mascota = r.id_mascota INNER JOIN tipovisita AS t ON r.id_tipo_visita = t.id_tipo_visita WHERE t.id_tipo_visita = '2'")
        est = cursor.fetchone()
        return est
    except Exception as e:
        return 'error'

def totalCaso():
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT c.nombre, COUNT(cm) as cantidad FROM casomascota AS cm INNER JOIN caso AS c ON cm.id_tipocaso = c.id_caso GROUP BY c.nombre")
        casos = cursor.fetchall()
        return casos
    except Exception as e:
        return 'error'

def totalVisitas():
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT u.nombre as veterinaria, v.nombre as tipovisita, count(r) as cantidad FROM usuariodetalle AS u INNER JOIN registro AS r ON u.documento = r.id_veterinaria INNER JOIN tipovisita AS v ON v.id_tipo_visita = r.id_tipo_visita GROUP BY u.nombre, v.nombre")
        visitas = cursor.fetchall()
        return visitas
    except Exception as e:
        return 'error'

def metas():
    try:
        cursor = connection.cursor()
        cursor.callproc('michochip_goals')
        num = cursor.fetchone()
        print(num)
    except Exception as e:
        print(e)
        return 'error'

def infoAdicionalMascotas(id_mascota, especie, nombre):
    lat = numpy.random.uniform(0, 10)
    lon = numpy.random.uniform(-70, -80)
    temperatura = 0
    frecuancia_cardiaca = 0
    frecuancia_resp = 0
    if especie == '1':
        temperatura = random.uniform(38.3, 39.2)
        frecuancia_cardiaca = random.randint(60, 120)
        frecuancia_resp = random.randint(10, 30)
    elif especie == '2':
        temperatura = random.uniform(38, 39.2)
        frecuancia_cardiaca = random.randint(110, 200)
        frecuancia_resp = random.randint(20, 30)
    db = mongo.mongoConnection()
    col = db['mascotas']
    col.insert_one({
        'id_mascota': id_mascota,
        'nombre': nombre,
        'especie': especie,
        'geolocation': {
            'latitud': lat,
            'longitud': lon
        },
        'signos_vitales': {
            'temperature': temperatura,
            'heart-rate': frecuancia_cardiaca,
            'breathing-frecuency': frecuancia_resp
        }
    })