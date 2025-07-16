import os
import sys
import time
import subprocess
from threading import Thread

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from servers.smtp_server import start_server as start_smtp_server
from servers.pop3_server import start_server as start_pop3_server
from servers.imap_server import start_server as start_imap_server
from clients.smtp_client import send_email
from clients.pop3_client import receive_pop3_email
from clients.imap_client import manage_imap_email

def clear_screen():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu():
    """Muestra el menú principal"""
    print("\n=== Simulador de Servidor de Correo ===")
    print("1. Iniciar Servidores")
    print("2. Enviar Correo (SMTP)")
    print("3. Recibir Correo (POP3)")
    print("4. Gestionar Correo (IMAP)")
    print("5. Salir")
    print("=====================================")

def main():
    servers = []
    server_threads = []
    servers_running = False
    
    while True:
        clear_screen()
        print_menu()
        choice = input("\nElija una opción (1-5): ")
        
        if choice == '1' and not servers_running:
            try:
                print("\nIniciando servidores...")
                
                # Iniciar servidor SMTP
                smtp_server = start_smtp_server()
                servers.append(smtp_server)
                
                # Iniciar servidor POP3
                pop3_server, pop3_thread = start_pop3_server()
                servers.append(pop3_server)
                server_threads.append(pop3_thread)
                
                # Iniciar servidor IMAP
                imap_server, imap_thread = start_imap_server()
                servers.append(imap_server)
                server_threads.append(imap_thread)
                
                servers_running = True
                print("\nTodos los servidores están en ejecución:")
                print("- SMTP: localhost:1025")
                print("- POP3: localhost:1100")
                print("- IMAP: localhost:1430")
                input("\nPresione Enter para continuar...")
                
            except Exception as e:
                print(f"\nError iniciando servidores: {str(e)}")
                input("\nPresione Enter para continuar...")
        
        elif choice == '2':
            if not servers_running:
                print("\nDebe iniciar los servidores primero.")
                input("\nPresione Enter para continuar...")
                continue
            
            print("\n=== Enviar Correo ===")
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
                print("\nCorreo enviado exitosamente!")
            else:
                print("\nError enviando el correo.")
            
            input("\nPresione Enter para continuar...")
        
        elif choice == '3':
            if not servers_running:
                print("\nDebe iniciar los servidores primero.")
                input("\nPresione Enter para continuar...")
                continue
            
            print("\n=== Recibir Correo (POP3) ===")
            receive_pop3_email()
            input("\nPresione Enter para continuar...")
        
        elif choice == '4':
            if not servers_running:
                print("\nDebe iniciar los servidores primero.")
                input("\nPresione Enter para continuar...")
                continue
            
            print("\n=== Gestionar Correo (IMAP) ===")
            manage_imap_email()
            input("\nPresione Enter para continuar...")
        
        elif choice == '5':
            if servers_running:
                print("\nDeteniendo servidores...")
                for server in servers:
                    try:
                        server.stop()
                    except:
                        pass
                for thread in server_threads:
                    try:
                        thread.join(timeout=2)
                    except:
                        pass
            print("\n¡Gracias por usar el simulador!")
            break
        
        else:
            print("\nOpción inválida.")
            input("\nPresione Enter para continuar...")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario.")
    except Exception as e:
        print(f"\nError inesperado: {str(e)}")
