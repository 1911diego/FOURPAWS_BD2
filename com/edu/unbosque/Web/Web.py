from flask import Flask, render_template, request, flash, url_for,redirect

from com.edu.unbosque.model import Usuario as usuario

app = Flask(__name__)
app.secret_key = "1234"

@app.route('/inicio',methods=['GET','POST'])
def inicio():
    if request.method == 'GET':
        return  render_template('Inicio.html')
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
                    return redirect(url_for('ingresar'))

@app.route('/Registrar',methods=['POST'])
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

    validacion = usuario.createUser(numeroDoc,nombre,telefono,tipoDoc,tipoUsuario,direccion,localidad,barrio,email,clave)

    if validacion == 0:
        flash(f"Hubo un error al tratar de iniciar sesión", "error")
        return render_template('Inicio.html')
    else:
        flash(f"Registro exitoso!", "success")
        return redirect(url_for('ingresar'))






@app.route('/Ingreso',methods=['GET'])
def ingresar():

    return render_template('Ingreso.html')



if __name__ == '__main__':
    app.run(debug=True)