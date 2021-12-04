from com.edu.unbosque.connection import ConnectionPostgres as c
from werkzeug.security import generate_password_hash, check_password_hash
from com.edu.unbosque.model import model as modelo

connection = c.createConnection()

#Metodo que crea un usuario
def createUser(documento, nombre, telefono, tipo_documento, tipo_usuario, direccion, localidad, barrio, correo,
               password):
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
        print (e)
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


createUser("000898a", "Ruben Castañeda", "320771545", "1", "2", "cl 67a", "barrios unidos", "j vargas","tello@gmail.com", "12345")
