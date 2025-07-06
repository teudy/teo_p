
import smtplib
from email.mime.text import MIMEText

def enviar_correo(retiro):
    mensaje = f"""Nuevo retiro solicitado:

Wallet: {retiro['wallet']}
Monto: {retiro['monto']} BTC
Comisión (5%): {retiro['comision']} BTC
Neto a pagar: {retiro['neto']} BTC
Método: {retiro['metodo']}
Cuenta destino: {retiro['cuenta']}
Fecha (timestamp): {retiro['fecha']}
"""

    msg = MIMEText(mensaje)
    msg["Subject"] = "Nuevo Retiro BTCMovil"
    msg["From"] = "notificador@gmail.com"
    msg["To"] = "teudy58@gmail.com"

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login("notificador@gmail.com", "CONTRASEÑA_APP")
        server.sendmail("notificador@gmail.com", "teudy58@gmail.com", msg.as_string())
        server.quit()
    except Exception as e:
        print("Error al enviar correo:", e)
