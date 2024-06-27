import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def enviar_correo(email_receiver, nombre_usuario, fecha, ini, fin):
    email_sender = "ferchon123443@gmail.com"
    password = "erqz bezl blbc wrcx"

    # Crear el mensaje
    msg = MIMEMultipart()
    msg["From"] = email_sender
    msg["To"] = email_receiver
    msg["Subject"] = "Reserva Creada"

    # Cuerpo del mensaje
    body = f"""
    ¡Hola {nombre_usuario}!

        Te informamos que se ha creado exitosamente tu reserva.
        Ten en cuenta la siguiente información
        ¡Te esperamos!

        - Fecha -> {fecha}
        - Horario {ini.strftime("v: %H:%M")} - {fin.strftime("v: %H:%M")}
        </p>

    Saludos,
    El equipo Cyber Assasins
    </body>
    </html>

    
    """
    msg.attach(MIMEText(body, "plain"))

    # Conectar al servidor SMTP de Gmail
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_sender, password)

        # Enviar el correo
        server.sendmail(email_sender, email_receiver, msg.as_string())
        print(f"Correo enviado correctamente a {email_receiver}")

    except Exception as e:
        print(f"Error al enviar el correo a {email_receiver}: {str(e)}")

    finally:
        server.quit()
