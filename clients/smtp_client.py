import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_address, subject, body, from_address='usuario@localhost', smtp_host='localhost', smtp_port=1025):
    """
    Envía un correo electrónico usando el servidor SMTP local
    
    Args:
        to_address (str): Dirección de correo del destinatario
        subject (str): Asunto del correo
        body (str): Cuerpo del mensaje
        from_address (str): Dirección del remitente
        smtp_host (str): Host del servidor SMTP
        smtp_port (int): Puerto del servidor SMTP
    
    Returns:
        bool: True si el envío fue exitoso, False en caso contrario
    """
    try:
        # Crear mensaje
        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['To'] = to_address
        msg['Subject'] = subject
        
        # Agregar el cuerpo del mensaje
        msg.attach(MIMEText(body, 'plain'))
        
        # Conectar al servidor y enviar
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.send_message(msg)
        
        return True
    
    except Exception as e:
        print(f"Error enviando el correo: {str(e)}")
        return False

if __name__ == '__main__':
    # Ejemplo de uso
    to_addr = input("Para: ")
    subject = input("Asunto: ")
    print("Cuerpo del mensaje (termina con una línea vacía):")
    
    body_lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        body_lines.append(line)
    
    body = "\n".join(body_lines)
    
    if send_email(to_addr, subject, body):
        print("Correo enviado exitosamente")
    else:
        print("Error al enviar el correo")
