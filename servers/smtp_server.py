import asyncio
from aiosmtpd.controller import Controller
from email import message_from_bytes
import sys
import os

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.email_db import add_email
from utils.email_parser import parse_email_content

class CustomSMTPHandler:
    async def handle_DATA(self, server, session, envelope):
        """
        Maneja el evento de recepción de datos de un mensaje de correo
        
        Args:
            server: El servidor SMTP
            session: La sesión SMTP
            envelope: El sobre que contiene los datos del mensaje
            
        Returns:
            str: Código de estado SMTP
        """
        try:
            # Convertir los datos del mensaje a string
            msg = message_from_bytes(envelope.content)
            
            # Parsear el mensaje
            parsed_email = parse_email_content(msg.as_string())
            
            # Guardar en la base de datos
            email_id = add_email(
                sender=envelope.mail_from,
                recipients=envelope.rcpt_tos,
                subject=parsed_email['subject'],
                body_text=parsed_email['body'],
                raw_message=msg.as_string()
            )
            
            print(f"\nCorreo recibido y guardado con ID: {email_id}")
            print(f"De: {envelope.mail_from}")
            print(f"Para: {', '.join(envelope.rcpt_tos)}")
            print(f"Asunto: {parsed_email['subject']}\n")
            
            return '250 Mensaje recibido correctamente'  # Código de éxito SMTP
            
        except Exception as e:
            print(f"Error procesando el mensaje: {str(e)}")
            return f"550 Error procesando el mensaje: {str(e)}"  # Código de error SMTP

def start_server(host='localhost', port=1025):
    """
    Inicia el servidor SMTP
    
    Args:
        host (str): Host donde escuchará el servidor
        port (int): Puerto donde escuchará el servidor
    
    Returns:
        Controller: Instancia del controlador del servidor
    """
    handler = CustomSMTPHandler()
    controller = Controller(handler, hostname=host, port=port)
    controller.start()
    print(f"Servidor SMTP (aiosmtpd) iniciado en {host}:{port}")
    return controller

if __name__ == '__main__':
    # Iniciar el servidor si se ejecuta directamente
    controller = start_server()
    try:
        # Mantener el programa corriendo
        input("Presione Enter para detener el servidor...\n")
    except KeyboardInterrupt:
        pass
    finally:
        controller.stop()
