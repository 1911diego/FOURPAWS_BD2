import smtplib

def enviarCorreoRegistro(to):
    messagge = 'Se creo su usuario en la plataforma de fourPaws'
    subject = 'Registro usuario'
    messagge = 'Subject: {}\n\n{}'.format(subject, messagge)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('fourpawsatom@gmail.com', 'Nidise1234')
    server.sendmail('fourpawsatom@gmail.com', to, messagge)
    server.quit()
    print('Se ha enviado el correo exitosamente')
