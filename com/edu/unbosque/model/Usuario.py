import random
from datetime import date

from com.edu.unbosque.connection import ConnectionPostgres as c
from werkzeug.security import generate_password_hash, check_password_hash
from com.edu.unbosque.model import model as modelo

connection = c.createConnection()

#Metodo que crea un usuario
def createUser(documento, nombre, telefono, tipo_documento, tipo_usuario, direccion, localidad, barrio, correo, password):
    try:
        password = generate_password_hash(password, 'pbkdf2:sha256', 30)
        print(password)
        estado = '1'
        if tipo_usuario == "1":
            estado = '0'
        cursor = connection.cursor()
        cursor.execute("INSERT INTO ubicacion (direccion, localidad, barrio) VALUES (%s, %s, %s)",
                   (direccion, localidad, barrio))
        connection.commit()
        cursor.execute("SELECT id_ubicacion FROM ubicacion WHERE direccion = '" + direccion + "'")
        id_ubicacion = cursor.fetchone()[0]
        print(id_ubicacion)
        cursor.execute(
            "INSERT INTO usuariodetalle (documento, nombre, telefono, tipo_documento, tipo_usuario, id_ubicacion, estado) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (documento, nombre, telefono, tipo_documento, tipo_usuario, id_ubicacion, estado))
        connection.commit()
        cursor.execute("INSERT INTO usuario (documento_usr, correo, password) VALUES (%s, %s, %s)",
                   (documento, correo, password))
        modelo.crearPersona(nombre, documento)
        connection.commit()
        cursor.close()
        connection.close()

        return 1
    except Exception as e:
        print(e)
        return 0

#Metodo que inicia sesión, hace las validaciones correspondientes
def iniciarSesion(correo, password):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT password FROM usuario WHERE correo = '" + correo + "'")
        passwordEncryp = cursor.fetchone()
        if passwordEncryp==None:
            return "correo inválido"
        else:
            if check_password_hash(passwordEncryp[0], password):
                cursor.execute(
                    "SELECT documento_usr FROM usuario WHERE correo = '" + correo + "'")
                id_user = cursor.fetchone()[0]
                print(id_user)
                cursor.close()
                connection.close()

                return id_user
            else:
                return "contraseña inválida"

        return "error"
    except Exception as e:
        print(e)
        return "error"

def listaVeterinarias():
    try:
        cursor = connection.cursor()
        cursor.execute("select ud.nombre, ud.estado from usuario u INNER join usuariodetalle ud on u.documento_usr = ud.documento where ud.tipo_usuario = '1' and ud.estado = '0'")
        vet = cursor.fetchall()
        cursor.close()
        connection.close()
        return vet
    except Exception as e:
        print(e)
        return "error"

def aprobarRechazar(id_veterinaria, id_funcionario, estado):
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE usuariodetalle set estado = '" + estado + "' WHERE documento = '" + id_veterinaria + "'")
        cursor.execute("INSERT INTO aprobacion_func (id_veterinaria, id_funcionario) values (%s, %s)", (id_veterinaria, id_funcionario))
        cursor.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(e)
        return False

def totalPropietariosPorLocalidad():
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT u.localidad, count(ud) as cantidad FROM usuariodetalle as ud INNER JOIN ubicacion as u ON ud.id_ubicacion = u.id_ubicacion WHERE ud.tipo_usuario = '2' GROUP BY u.localidad")
        pro = cursor.fetchall()
        for i in pro:
            print(i)
        return pro
    except Exception as e:
        print(e)
        return 'error'


def registrarVisita(id_veterinaria, id_mascota, id_tipovisita, id_casomascota):
    try:
        id_registro = random.randrange(1, 10000, 1)
        id_doc = random.randrange(1, 10000, 1)
        cursor = connection.cursor()
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        print("d1 =", d1)
        cursor.execute("SELECT * FROM registro WHERE id_mascota = '" + id_mascota + "' AND id_tipo_visita = '2'")
        obj = cursor.fetchone()
        if obj is None:
            cursor.execute(
                "INSERT INTO registro (id_registro, fecha_registro, id_tipo_visita, id_caso, id_mascota, id_veterinaria) VALUES (%s, %s, %s, %s, %s, %s)",
                (id_registro, d1, id_tipovisita, id_casomascota, id_mascota, id_veterinaria))
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        return "error"

def listaRegistro(id_vet):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT r.fecha_registro, m.nombre, c.nombre, v.nombre FROM registro AS r INNER JOIN mascota AS m ON r.id_mascota = m.id_mascota INNER JOIN caso AS c ON c.id_caso = r.id_caso INNER JOIN tipovisita AS v ON r.id_tipo_visita = v.id_tipo_visita WHERE r.id_veterinaria = '" + id_vet + "' ORDER BY r.fecha_registro DESC")
        reg = cursor.fetchall()
        return reg
    except Exception as e:
        return 'error'

def actualizarUsr(documento, nombre, telefono, direccion, localidad, barrio, correo, password):
    try:
        password = generate_password_hash(password, 'pbkdf2:sha256', 30)
        cursor = connection.cursor()
        cursor.execute("SELECT id_ubicacion FROM ubicacion WHERE direccion = '" + direccion + "'")
        id_ubicacion = cursor.fetchone()[0]
        cursor.execute("UPDATE ubicacion SET direccion = '" + direccion + "', localidad = '" + localidad + "', barrio = '" + barrio + "' WHERE id_ubicacion = '" + id_ubicacion + "'")
        cursor.execute("UPDATE usuariodetalle SET nombre = '" + nombre + "', telefono = '" + telefono + "' WHERE documento = '" + documento + "'")
        cursor.execute("UPDATE usuario SET correo = '" + correo + "', password = '" + password + "' WHERE documento_usr = '" + documento + "'")
        return True
    except Exception as e:
        return False