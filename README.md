# Simulador de Servidor de Correo

Este proyecto implementa un simulador básico de servidor de correo que demuestra el funcionamiento de los protocolos SMTP, POP3 e IMAP. Es una herramienta educativa que permite entender cómo funcionan los protocolos de correo electrónico más comunes.

## Características

- Servidor SMTP para el envío de correos
- Servidor POP3 para la descarga de correos
- Servidor IMAP para la gestión de correos en el servidor
- Base de datos **PostgreSQL** para almacenamiento persistente
- Interfaz de línea de comandos intuitiva

## Requisitos

- Python 3.x
- PostgreSQL instalado y corriendo
- Instalar dependencias:
  ```bash
  pip install -r requirements.txt
  ```
- Crear la base de datos y usuario en PostgreSQL (por defecto: `email_simulator`, usuario: `postgres`, contraseña: `postgres`). Puedes modificar estos valores en `data/email_db.py`.

## Estructura del Proyecto

```
├── servers/          # Implementaciones de servidores
│   ├── smtp_server.py
│   ├── pop3_server.py
│   └── imap_server.py
├── clients/          # Implementaciones de clientes
│   ├── smtp_client.py
│   ├── pop3_client.py
│   └── imap_client.py
├── data/            # Gestión de datos
│   └── email_db.py  # Base de datos PostgreSQL
├── utils/           # Utilidades
│   └── email_parser.py
├── main_app.py      # Script principal
├── ver_correos_bd.py # Visualización directa de la BD
└── README.md
```

## Configuración

Los servidores utilizan los siguientes puertos por defecto:
- SMTP: localhost:1025
- POP3: localhost:1100
- IMAP: localhost:1430

## Uso

1. Ejecuta el script principal:
   ```bash
   python main_app.py
   ```

2. En el menú principal, elige:
   - Opción 1 para iniciar todos los servidores
   - Opción 2 para enviar un correo (SMTP)
   - Opción 3 para recibir correos (POP3)
   - Opción 4 para gestionar correos (IMAP)
   - Opción 5 para salir

## Ejemplo de aplicación

```
=== Simulador de Servidor de Correo ===
1. Iniciar Servidores
2. Enviar Correo (SMTP)
3. Recibir Correo (POP3)
4. Gestionar Correo (IMAP)
5. Salir
=====================================
Elija una opción (1-5): 1

[...]

Elija una opción (1-5): 2
Ingrese remitente: usuario@localhost
Ingrese destinatario: test@gmail.com
Ingrese asunto: Prueba
Ingrese cuerpo: Hola mundo
Correo enviado exitosamente.

Elija una opción (1-5): 4
=== Gestionar Correo (IMAP) ===
Hay mensajes en el buzón INBOX.
Opciones:
1. Ver todos los mensajes
2. Ver mensajes no leídos
3. Salir
Elija una opción (1-3): 1

=== Todos los mensajes ===
==================================================
ID: 1
De: usuario@localhost
Para: ["test@gmail.com"]
Asunto: Prueba
Estado: unread
Fecha: 2025-07-16 01:30:43.474295
--------------------------------------------------
Mensaje:
Hola mundo
==================================================
```

## Protocolos Implementados

### SMTP (Simple Mail Transfer Protocol)
- Puerto 1025
- Simula el envío de correos
- No requiere autenticación en esta versión

### POP3 (Post Office Protocol v3)
- Puerto 1100
- Permite descargar correos
- Autenticación simulada (acepta cualquier credencial)
- Soporta eliminación de correos

### IMAP (Internet Message Access Protocol)
- Puerto 1430
- Gestión de correos en el servidor
- Autenticación simulada
- Soporte para marcar correos como leídos

## Visualización de la base de datos PostgreSQL

Para ver los correos almacenados directamente en la base de datos, puedes ejecutar:

```bash
python ver_correos_bd.py
```

Esto mostrará todos los correos y sus campos en consola.

## Limitaciones

Este es un simulador educativo con las siguientes limitaciones:
- No implementa seguridad (SSL/TLS)
- Autenticación simulada
- Solo maneja texto plano (no adjuntos)
- Un solo buzón (INBOX)
- No implementa todas las características de los protocolos

## Desarrollo

El proyecto está estructurado de manera modular para facilitar la extensión y modificación:
- Cada protocolo tiene su propio módulo servidor y cliente
- La base de datos está centralizada
- Las utilidades son compartidas entre módulos

## Contribución

Siéntase libre de contribuir al proyecto:
1. Fork del repositorio
2. Crear una rama para su característica
3. Commit de sus cambios
4. Push a la rama
5. Crear un Pull Request

## Licencia

Este proyecto es software libre y puede ser redistribuido bajo los términos que usted considere apropiados.
