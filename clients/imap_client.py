import imaplib
import email
import sys
import os

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.email_parser import format_email_for_display, parse_email_content

class IMAPClient:
    def __init__(self, host='localhost', port=1430, username='user', password='pass'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = None
    
    def connect(self):
        """Establece conexión con el servidor IMAP"""
        try:
            self.connection = imaplib.IMAP4(self.host, self.port)
            self.connection.login(self.username, self.password)
            return True
        except Exception as e:
            print(f"Error de conexión: {str(e)}")
            return False
    
    def disconnect(self):
        """Cierra la conexión con el servidor"""
        if self.connection:
            try:
                self.connection.logout()
            except:
                pass
            self.connection = None
    
    def select_inbox(self):
        """Selecciona el buzón INBOX"""
        try:
            status, data = self.connection.select('INBOX')
            if status == 'OK':
                return int(data[0])
            return 0
        except Exception as e:
            print(f"Error seleccionando INBOX: {str(e)}")
            return 0
    
    def search_messages(self, criteria='ALL'):
        """Busca mensajes según criterios"""
        try:
            status, data = self.connection.search(None, criteria)
            if status == 'OK':
                return data[0].split()
            return []
        except Exception as e:
            print(f"Error buscando mensajes: {str(e)}")
            return []
    
    def fetch_message(self, msg_id):
        """Recupera un mensaje específico"""
        try:
            status, data = self.connection.fetch(msg_id, '(RFC822)')
            if status == 'OK':
                email_body = data[0][1]
                email_message = email.message_from_bytes(email_body)
                parsed_email = parse_email_content(email_message.as_string())
                return parsed_email
            return None
        except Exception as e:
            print(f"Error recuperando mensaje {msg_id}: {str(e)}")
            return None
    
    def mark_as_read(self, msg_id):
        """Marca un mensaje como leído"""
        try:
            self.connection.store(msg_id, '+FLAGS', '\\Seen')
            return True
        except Exception as e:
            print(f"Error marcando mensaje como leído: {str(e)}")
            return False

def manage_imap_email(host='localhost', port=1430, username='user', password='pass'):
    """
    Función principal para gestionar correos vía IMAP
    
    Args:
        host (str): Host del servidor IMAP
        port (int): Puerto del servidor IMAP
        username (str): Nombre de usuario
        password (str): Contraseña
    """
    client = IMAPClient(host, port, username, password)
    
    try:
        # Conectar al servidor
        if not client.connect():
            return
        
        # Seleccionar INBOX
        num_messages = client.select_inbox()
        print(f"\nHay {num_messages} mensaje(s) en el buzón INBOX.\n")
        
        while True:
            print("\nOpciones:")
            print("1. Ver todos los mensajes")
            print("2. Ver mensajes no leídos")
            print("3. Salir")
            
            choice = input("\nElija una opción (1-3): ")
            
            if choice == '1':
                messages = client.search_messages('ALL')
            elif choice == '2':
                messages = client.search_messages('UNSEEN')
            elif choice == '3':
                break
            else:
                print("Opción inválida")
                continue
            
            if not messages:
                print("No hay mensajes para mostrar")
                continue
            
            for msg_id in messages:
                msg_id_str = msg_id.decode() if isinstance(msg_id, bytes) else str(msg_id)
                try:
                    message = client.fetch_message(msg_id_str)
                    if message:
                        print(format_email_for_display(message))
                        if input("\n¿Marcar como leído? (s/n): ").lower() == 's':
                            client.mark_as_read(msg_id_str)
                        if input("\n¿Continuar con el siguiente mensaje? (s/n): ").lower() != 's':
                            break
                except (imaplib.IMAP4.abort, imaplib.IMAP4.error, OSError):
                    # Silenciar cualquier error de desconexión
                    return
        
        print("\nCerrando sesión...")
    except (imaplib.IMAP4.abort, imaplib.IMAP4.error, OSError):
        # Silenciar cualquier error de desconexión
        pass
    finally:
        client.disconnect()

if __name__ == '__main__':
    manage_imap_email()
