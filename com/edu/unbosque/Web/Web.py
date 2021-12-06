from flask import Flask, render_template, request, flash, url_for, redirect, session, jsonify

from com.edu.unbosque.model import Usuario as usuario
from com.edu.unbosque.Mail import mail as mail

app = Flask(__name__)
app.secret_key = "1234"


@app.route('/inicio', methods=['GET', 'POST'])
def inicio():
    if request.method == 'GET':
        return render_template('Inicio.html')
    else:
        username = request.form['usuario']
        password = request.form['password']

        validacion = usuario.iniciarSesion(username, password)
        if validacion == "correo inválido":
            flash(f"Usuario o contraseña inválidos", "error")
            return render_template('Inicio.html')
        else:
            if validacion == "contraseña inválida":
                flash(f"Usuario o contraseña inválidos", "error")
                return render_template('Inicio.html')
            else:
                if validacion == "error":
                    flash(f"Hubo un error al tratar de iniciar sesión", "error")
                    return render_template('Inicio.html')
                else:
                    flash(f"Inicio de sesión exitoso", "success")
                    session['user'] = validacion
                    return redirect(url_for('ingresar'))


@app.route('/Registrar', methods=['POST'])
def registrarUsuario():
    tipoUsuario = request.form.get("tipoUsuario")
    tipoDoc = request.form.get("tipoDoc")
    numeroDoc = request.form.get("numeroDoc")
    nombre = request.form.get("nombre")
    telefono = request.form.get("telefono")
    direccion = request.form.get("direccion")
    localidad = request.form.get("localidad")
    barrio = request.form.get("barrio")
    email = request.form.get("email")
    clave = request.form.get("claveNueva")

    validacion = usuario.createUser(numeroDoc, nombre, telefono, tipoDoc, tipoUsuario, direccion, localidad, barrio,
                                    email, clave)

    if validacion == 0:
        flash(f"Hubo un error al tratar de iniciar sesión", "error")
        return render_template('Inicio.html')
    else:
        mail.enviarCorreoRegistro(email)
        flash(f"Registro exitoso!", "success")
        return redirect(url_for('ingresar'))


@app.route('/Ingreso', methods=['GET'])
def ingresar():
    return render_template('Ingreso.html')


@app.route('/api/crearFuncionario', methods=['POST'])
def create_user():
    json = request.get_json(force=True)

    documento = json.get('documento')
    nombre = json.get('nombre')
    telefono = json.get('telefono')
    tipo_documento = json.get('tipo_documento')
    tipo_usuario = json.get('tipo_usuario')
    direccion = json.get('direccion')
    localidad = json.get('localidad')
    barrio = json.get('barrio')
    correo = json.get('correo')
    contrasena = json.get('contrasena')

    if documento is None or nombre is None or telefono is None \
            or tipo_documento is None or direccion is None or localidad is None \
            or barrio is None or correo is None or contrasena is None:
        return jsonify({'message': 'Bad request'}), 400

    validacion = usuario.createUser(documento, nombre, telefono, tipo_documento, tipo_usuario, direccion, localidad, barrio, correo, contrasena)

    if validacion == 0:
        return jsonify({'message': 'Hubo un error al momento de crear el usuario'}), 400

    mail.enviarCorreoRegistro(correo)
    return jsonify({'message': 'Se creo el usuario correctamente'}), 200


if __name__ == '__main__':
    app.add_url_rule("/", endpoint="inicio")
    app.run(debug=True, host="localhost", port="8080")
