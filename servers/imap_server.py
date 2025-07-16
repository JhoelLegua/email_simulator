import socket
import threading
import sys
import os

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.email_db import get_all_emails

class IMAPSession:
    def __init__(self, client_socket):
        self.client = client_socket
    
    def send_response(self, message):
        """Simula una respuesta IMAP básica"""
        self.client.send(f"{message}\r\n".encode())
    
    def handle_client(self):
        """Maneja la conexión del cliente"""
        try:
            # Simular saludo IMAP
            self.send_response("* OK IMAP server ready")
            
            while True:
                try:
                    data = self.client.recv(1024)
                    if not data:
                        break
                    while True:
                        print("\nHay mensajes en el buzón INBOX.")
                        print("\nOpciones:")
                        print("1. Ver todos los mensajes")
                        print("2. Ver mensajes no leídos")
                        print("3. Salir")
                        
                        choice = input("\nElija una opción (1-3): ")
                        
                        if choice == '1':
                            emails = get_all_emails()
                            print("\n=== Todos los mensajes ===")
                            for email in emails:
                                print("\n" + "="*50)
                                print(f"ID: {email[0]}")
                                print(f"De: {email[1]}")
                                print(f"Para: {email[2]}")
                                print(f"Asunto: {email[3]}")
                                print(f"Estado: {email[6]}")
                                print(f"Fecha: {email[7]}")
                                print("-"*50)
                                print(f"Mensaje:\n{email[4]}")
                                print("="*50)
                            input("\nPresione Enter para volver al menú...")
                        
                        elif choice == '2':
                            unread_emails = get_all_emails(status_filter='unread')
                            print("\n=== Mensajes no leídos ===")
                            for email in unread_emails:
                                print("\n" + "="*50)
                                print(f"ID: {email[0]}")
                                print(f"De: {email[1]}")
                                print(f"Para: {email[2]}")
                                print(f"Asunto: {email[3]}")
                                print(f"Estado: {email[6]}")
                                print(f"Fecha: {email[7]}")
                                print("-"*50)
                                print(f"Mensaje:\n{email[4]}")
                                print("="*50)
                            input("\nPresione Enter para volver al menú...")
                        
                        elif choice == '3':
                            print("\nSaliendo...")
                            return
                        else:
                            print("\nOpción inválida")
                except Exception as e:
                    print(f"Error: {str(e)}")
                    break
        finally:
            self.client.close()

class IMAPServer:
    def __init__(self, host='localhost', port=1430):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.running = False
    
    def start(self):
        """Inicia el servidor"""
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        self.running = True
        print(f"Servidor IMAP escuchando en {self.host}:{self.port}")
        try:
            while self.running:
                try:
                    client_socket, address = self.socket.accept()
                    print(f"Nueva conexión IMAP desde {address}")
                    session = IMAPSession(client_socket)
                    session.handle_client()
                except OSError:
                    # El socket fue cerrado, salir del bucle
                    break
        except KeyboardInterrupt:
            print("\nDeteniendo servidor IMAP...")
        finally:
            self.stop()
    
    def stop(self):
        """Detiene el servidor"""
        self.running = False
        self.socket.close()

def start_server(host='localhost', port=1430):
    server = IMAPServer(host, port)
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
