import socket
import threading
import sys
import os

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.email_db import get_all_emails, get_email_by_id, update_email_status, delete_email_permanently

class POP3Session:
    def __init__(self, client_socket):
        self.client = client_socket
        self.authenticated = False
        self.marked_for_deletion = set()
        self.emails = []
    
    def send_response(self, message):
        """Envía una respuesta al cliente (acepta str, bytes, memoryview; siempre termina con CRLF)"""
        if isinstance(message, str):
            message = message.encode('utf-8')
        elif not isinstance(message, bytes):
            message = bytes(message)
        if not message.endswith(b"\r\n"):
            message = message + b"\r\n"
        self.client.send(message)
    
    def handle_command(self, command):
        """Maneja los comandos POP3 recibidos"""
        command = command.strip().decode()
        parts = command.split()
        cmd = parts[0].upper()
        
        if not self.authenticated and cmd not in ['USER', 'PASS', 'QUIT']:
            self.send_response("-ERR Autenticación requerida")
            return True
        
        if cmd == 'USER':
            self.send_response("+OK Usuario aceptado")
        
        elif cmd == 'PASS':
            self.authenticated = True
            self.emails = get_all_emails(status_filter='unread')
            self.send_response("+OK Inicio de sesión exitoso")
        
        elif cmd == 'STAT':
            total_size = sum(len(str(email[4])) for email in self.emails)
            self.send_response(f"+OK {len(self.emails)} {total_size}")
        
        elif cmd == 'LIST':
            self.send_response(f"+OK {len(self.emails)} mensajes")
            for i, email in enumerate(self.emails, 1):
                size = len(str(email[4]))  # Tamaño del cuerpo del mensaje
                self.send_response(f"{i} {size}")
            self.send_response(".")
        
        elif cmd == 'RETR':
            try:
                msg_num = int(parts[1])
                if 1 <= msg_num <= len(self.emails):
                    email = self.emails[msg_num - 1]
                    self.send_response(f"+OK mensaje {msg_num}")
                    self.send_response(email[5])  # Enviar el mensaje completo (raw_message)
                    self.send_response(".")
                else:
                    self.send_response("-ERR No existe ese mensaje")
            except (IndexError, ValueError):
                self.send_response("-ERR Comando inválido")
        
        elif cmd == 'DELE':
            try:
                msg_num = int(parts[1])
                if 1 <= msg_num <= len(self.emails):
                    self.marked_for_deletion.add(self.emails[msg_num - 1][0])  # Guardar el ID del email
                    self.send_response(f"+OK mensaje {msg_num} marcado para eliminar")
                else:
                    self.send_response("-ERR No existe ese mensaje")
            except (IndexError, ValueError):
                self.send_response("-ERR Comando inválido")
        
        elif cmd == 'READ':
            try:
                msg_num = int(parts[1])
                if 1 <= msg_num <= len(self.emails):
                    email_id = self.emails[msg_num - 1][0]  # Obtener el ID del email
                    update_email_status(email_id, 'read')
                    self.send_response(f"+OK mensaje {msg_num} marcado como leído")
                else:
                    self.send_response("-ERR No existe ese mensaje")
            except (IndexError, ValueError):
                self.send_response("-ERR Comando inválido")
        
        elif cmd == 'QUIT':
            # Procesar eliminaciones
            for email_id in self.marked_for_deletion:
                delete_email_permanently(email_id)
            self.send_response("+OK Servidor POP3 cerrando conexión")
            return False
        
        else:
            self.send_response(f"-ERR Comando desconocido: {cmd}")
        
        return True

class POP3Server:
    def __init__(self, host='localhost', port=1100):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.running = False
    
    def handle_client(self, client_socket, address):
        """Maneja una conexión de cliente"""
        print(f"Nueva conexión POP3 desde {address}")
        session = POP3Session(client_socket)
        
        try:
            # Enviar saludo
            session.send_response("+OK Servidor POP3 listo")
            
            # Procesar comandos
            while True:
                try:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    
                    if not session.handle_command(data):
                        break
                except Exception as e:
                    print(f"Error procesando comando: {str(e)}")
                    break
        
        finally:
            client_socket.close()
            print(f"Conexión cerrada con {address}")
    
    def start(self):
        """Inicia el servidor POP3"""
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        self.running = True
        print(f"Servidor POP3 escuchando en {self.host}:{self.port}")
        try:
            while self.running:
                try:
                    client_socket, address = self.socket.accept()
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, address)
                    )
                    client_thread.start()
                except OSError:
                    # El socket fue cerrado, salir del bucle
                    break
        except KeyboardInterrupt:
            print("\nDeteniendo servidor POP3...")
        finally:
            self.stop()
    
    def stop(self):
        """Detiene el servidor POP3"""
        self.running = False
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        self.socket.close()

def start_server(host='localhost', port=1100):
    """
    Inicia el servidor POP3 en un hilo separado
    
    Returns:
        tuple: (servidor, hilo)
    """
    server = POP3Server(host, port)
    server_thread = threading.Thread(target=server.start)
    server_thread.daemon = True
    server_thread.start()
    return server, server_thread

if __name__ == '__main__':
    server, thread = start_server()
    try:
        while True:
            input("Presione Enter para detener el servidor...\n")
            break
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
