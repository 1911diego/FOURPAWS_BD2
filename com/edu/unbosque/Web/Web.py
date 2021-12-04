from flask import Flask, render_template, request, flash, url_for

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

        if (username == ""):
            flash(f"Debe ingresar un usuario", "error")
            return render_template('Inicio.html')
        else:
            if (password == ""):
                flash(f"Debe ingresar una contraseña", "error")
                return render_template('Inicio.html')
            else:
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
                            return url_for('/Ingreso')


@app.route('/Ingreso',methods=['POST'])
def ingresar():

    return render_template('Ingreso.html')



if __name__ == '__main__':
    app.run(debug=True)