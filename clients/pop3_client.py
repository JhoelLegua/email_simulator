import poplib
import sys
import os
from email import message_from_bytes, message_from_string

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.email_parser import format_email_for_display, parse_email_content

class POP3Client:
    def __init__(self, host='localhost', port=1100, username='user', password='pass'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = None
    
    def connect(self):
        """Establece conexión con el servidor POP3"""
        try:
            self.connection = poplib.POP3(self.host, self.port)
            self.connection.user(self.username)
            self.connection.pass_(self.password)
            return True
        except Exception as e:
            print(f"Error de conexión: {str(e)}")
            return False
    
    def disconnect(self):
        """Cierra la conexión con el servidor"""
        if self.connection:
            try:
                self.connection.quit()
            except:
                pass
            self.connection = None
    
    def get_message_count(self):
        """Obtiene el número de mensajes en el buzón"""
        try:
            return self.connection.stat()[0]
        except Exception as e:
            print(f"Error obteniendo contador de mensajes: {str(e)}")
            return 0
    
    def retrieve_message(self, msg_num):
        """Recupera un mensaje específico"""
        try:
            # Obtener el mensaje completo
            response, lines, octets = self.connection.retr(msg_num)
            
            # Unir las líneas en un solo mensaje
            msg_content = b'\n'.join(lines)
            
            # Parsear el mensaje
            email_message = message_from_bytes(msg_content)
            parsed_email = parse_email_content(email_message.as_string())
            
            return parsed_email
            
        except Exception as e:
            print(f"Error recuperando mensaje {msg_num}: {str(e)}")
            return None
    
    def delete_message(self, msg_num):
        """Marca un mensaje para eliminación"""
        try:
            self.connection.dele(msg_num)
            return True
        except Exception as e:
            print(f"Error eliminando mensaje {msg_num}: {str(e)}")
            return False
        
    def mark_message_as_read(self, msg_num):
        """Marca un mensaje como leído enviando el comando personalizado 'READ' al servidor."""
        try:
            command = f"READ {msg_num}"
            self.connection._putline(command.encode('utf-8'))
            response = self.connection._getline()
            # Si la respuesta es una tupla, tomar el primer elemento
            if isinstance(response, tuple):
                response = response[0]
            if isinstance(response, bytes):
                response = response.decode('utf-8', errors='replace')
            else:
                response = str(response)
            print(f">> Respuesta del servidor: {response.strip()}")
            return response.startswith('+OK')
        except poplib.error_proto as e:
            print(f">> Error de protocolo POP3: {e}")
            return False
        except Exception as e:
            print(f">> Error inesperado marcando mensaje como leído: {str(e)}")
            return False

def receive_pop3_email(host='localhost', port=1100, username='user', password='pass'):
    """
    Función principal para recibir correos vía POP3
    
    Args:
        host (str): Host del servidor POP3
        port (int): Puerto del servidor POP3
        username (str): Nombre de usuario
        password (str): Contraseña
    """
    client = POP3Client(host, port, username, password)
    
    try:
        # Conectar al servidor
        if not client.connect():
            return
        
        # Obtener número de mensajes
        num_messages = client.get_message_count()
        print(f"\nHay {num_messages} mensaje(s) en el buzón.\n")
        
        if num_messages == 0:
            return
        
        # Mostrar menú para cada mensaje
        for i in range(1, num_messages + 1):
            print(f"\n--- Mensaje {i} de {num_messages} ---")
            message = client.retrieve_message(i)
            
            if message:
                print(format_email_for_display(message))
                while True:
                    action = input("\nAcciones: (m)arcar como leído, (b)orrar, (i)gnorar, (s)alir de la sesión: ").lower()
                    if action == 'm':
                        if client.mark_message_as_read(i):
                            print(">> Mensaje marcado como leído en el servidor.")
                        else:
                            print(">> Error: No se pudo marcar el mensaje como leído.")
                        break # Pasar al siguiente mensaje
                    elif action == 'b':
                        if client.delete_message(i):
                            print(f">> Mensaje {i} marcado para eliminación.")
                        break # Pasar al siguiente mensaje
                    elif action == 'i':
                        print(">> Ignorando mensaje.")
                        break # Pasar al siguiente mensaje
                    elif action == 's':
                        print("\nSaliendo de la sesión...")
                        return # Salir de la función
                    else:
                        print("Opción inválida. Intente de nuevo.")
        
        print("\nNo hay más mensajes. Cerrando sesión...")
    
    finally:
        client.disconnect()

if __name__ == '__main__':
    receive_pop3_email()
