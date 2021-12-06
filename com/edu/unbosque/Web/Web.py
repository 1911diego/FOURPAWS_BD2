from flask import Flask, render_template, request, flash, url_for, redirect, session, jsonify

from com.edu.unbosque.model import Usuario as usuario
from com.edu.unbosque.model import mascota as mascota
from com.edu.unbosque.Mail import mail as mail

app = Flask(__name__)
app.secret_key = "1234"




@app.route('/inicio', methods=['GET', 'POST'])
def inicio():
    if request.method == 'GET':
        session['user'] = None
        return render_template('Inicio.html', session=session)
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
                    listaMascotasUsuario = mascota.listaMascotas(validacion)

                    print(listaMascotasUsuario)
                    return render_template('Ingreso.html', session=session,listaMascotas = listaMascotasUsuario)


@app.route('/crearCaso',methods=['GET','POST'])
def crearCaso():
    if request.method == 'GET':
        idMascota = request.args.get('idMascota')
        return render_template('Caso.html',idMascota = idMascota)
    else:
        idMascota = request.form.get("idMascota")
        tipoCaso = request.form.get("idTipoCaso")
        descripcion = request.form.get("descripcion")

        validacion = usuario.registrarCaso(idMascota,tipoCaso,descripcion)

        if validacion == 1:
            flash(f"Has creado un nuevo caso con éxito", "success")
            return render_template('Caso.html')
        else:
            flash(f"Hubo un error al tratar de iniciar sesión", "error")
            flash(f"Has creado un nuevo caso con éxito", "success")
            return render_template('Caso.html')


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

@app.route('/Mascotas',methods=['GET','POST'])
def mascotas():
    if request.method == 'POST':
        nombreMascota = request.form.get("nombreMascota")
        fechaNacimiento = request.form.get("fechaNacimiento")
        especie = request.form.get("especie")
        tamanio = request.form.get("tamanio")
        peligroso = request.form.get("peligroso")
        microchip = request.form.get("microchip")
        sexo = request.form.get("sexo")
        urlFoto = request.form.get("urlFoto")

        print("Fecha Nacimiento" + fechaNacimiento)
        print(especie)
        esPeligroso = "No"
        tieneMicrochip = False

        if peligroso is not None:
            esPeligroso = "Si"

        if microchip is not None:
            tieneMicrochip = True

        ingresa = mascota.createPet(session['user'],nombreMascota,fechaNacimiento,especie,tamanio,esPeligroso,urlFoto,tieneMicrochip,sexo)
        if ingresa == 0:
            flash(f"Hubo un error al tratar de crear la mascota", "error")
            return render_template('Mascota.html')
        else:
            flash(f"Ha creado su mascota con éxito", "success")
            return render_template('Mascota.html')
    else:
        return render_template('Mascota.html')
@app.route('/Ingreso', methods=['GET'])
def ingresar():
    listaMascotasUsuario = mascota.listaMascotas(session["user"])
    return render_template('Ingreso.html',listaMascotas = listaMascotasUsuario)


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


@app.route('/registrarVisita',methods=['GET','POST'])
def registrarVisita():
    if request.method == 'GET':
        listaMascotas = mascota.listaTotalMascotas()
        return render_template('RegistroVisita.html',listaMascotas = listaMascotas)
    else:
        return 0

@app.route('/registrarNuevaVisita',methods=['GET','POST'])
def registrarNuevaVisita():
    if request.method == 'GET':
        idMascota = request.args.get('idMascota')
        return render_template('RegistrarNuevaVisita.html',idMascota = idMascota)
    else:
         idMascota = request.form.get('idMascota')
         idVisita = request.form.get("idTipoVisita")
         idCaso = request.form.get("idTipoCaso")
         validacion = usuario.registrarVisita(session['user'],idMascota,idVisita,idCaso)
         if validacion == 1:
            flash(f"Ha registrado una nueva visita con éxito", "success")
            return render_template('RegistrarNuevaVisita.html')
         else:
            flash(f"Ha ocurrido un error al tratar de crear una nueva visita", "error")
            return render_template('RegistrarNuevaVisita.html')

if __name__ == '__main__':
    app.add_url_rule("/", endpoint="inicio")
    app.run(debug=True, host="localhost", port="8080")
