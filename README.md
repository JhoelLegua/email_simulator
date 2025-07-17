# 📧 Simulador de Servidor de Correo

¡Bienvenido! Este proyecto es un **simulador educativo** que te permite experimentar y entender cómo funcionan los protocolos de correo electrónico más usados: **SMTP**, **POP3** e **IMAP**. Ideal para estudiantes, docentes y entusiastas de las redes.

---

## ✨ Características

- 🚀 Servidor SMTP para el envío de correos
- 📥 Servidor POP3 para la descarga de correos
- 📂 Servidor IMAP para la gestión de correos en el servidor
- 🗄️ Base de datos **PostgreSQL** para almacenamiento persistente
- 💻 Interfaz de línea de comandos intuitiva y amigable
- 📚 Documentación web interactiva para cada protocolo:
  - 🔍 Explicaciones detalladas y ejemplos
  - 🎯 Demostraciones interactivas en vivo
  - 📊 Diagramas de flujo y comparativas
  - 💡 Tips y mejores prácticas

---

## 🛠️ Requisitos

- Python 3.x
- PostgreSQL instalado y corriendo
- Navegador web moderno para la documentación interactiva
- Instalar dependencias:
  ```bash
  pip install -r requirements.txt
  ```
- Crear la base de datos y usuario en PostgreSQL (por defecto: `email_simulator`, usuario: `postgres`, contraseña: `postgres`). Puedes modificar estos valores en `data/email_db.py`.

---

## 📁 Estructura del Proyecto

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
│   ├── email_parser.py
│   └── http_handler.py  # Manejador de respuestas HTTP
├── view/            # Documentación web interactiva
│   ├── smtp.html    # Documentación SMTP
│   ├── pop3.html    # Documentación POP3
│   ├── imap.html    # Documentación IMAP
│   └── global.css   # Estilos compartidos
├── main_app.py      # Script principal
├── ver_correos_bd.py # Visualización directa de la BD
└── README.md
```

---

## ⚙️ Configuración Rápida

Los servidores utilizan los siguientes puertos por defecto:
- 📤 SMTP: localhost:1025
- 📬 POP3: localhost:1100
- 📑 IMAP: localhost:1430
- 📚 Documentación Web: localhost:5000

La documentación web está disponible en:
- 📖 SMTP: http://localhost:5000/smtp
- 📖 POP3: http://localhost:5000/pop3
- 📖 IMAP: http://localhost:5000/imap

---

## ▶️ ¿Cómo usarlo?

1. Ejecuta el script principal:
   ```bash
   python main_app.py
   ```

2. En el menú principal, elige:
   - 1️⃣ Iniciar todos los servidores
   - 2️⃣ Enviar un correo (SMTP)
   - 3️⃣ Recibir correos (POP3)
   - 4️⃣ Gestionar correos (IMAP)
   - 5️⃣ Salir

---

## 📝 Ejemplo de aplicación

```
=== Simulador de Servidor de Correo ===
1. Iniciar Servidores
2. Enviar Correo (SMTP)
3. Recibir Correo (POP3)
4. Gestionar Correo (IMAP)
5. Salir
=====================================
Elija una opción (1-5): 2
Para: juan@gmail.com
Asunto: juan
Cuerpo del mensaje (termina con una línea vacía):
juan

Correo recibido y guardado con ID: 8
De: usuario@localhost
Para: juan@gmail.com
Asunto: juan

Correo enviado exitosamente!

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
ID: 8
Para: ["juan@gmail.com"]
Asunto: juan
Estado: unread
Fecha: 2025-07-16 01:30:43.474295
--------------------------------------------------
Mensaje:
juan
==================================================
```

---

## 📡 Protocolos Implementados

### ✉️ SMTP (Simple Mail Transfer Protocol)
- Puerto 1025
- Simula el envío de correos
- No requiere autenticación en esta versión
- Documentación web interactiva con:
  - Diagrama de flujo del protocolo
  - Ejemplos de comandos y respuestas
  - Demo interactiva de envío
  - Guía de códigos de respuesta

### 📥 POP3 (Post Office Protocol v3)
- Puerto 1100
- Permite descargar correos
- Autenticación simulada (acepta cualquier credencial)
- Soporta eliminación de correos
- Documentación web interactiva con:
  - Ciclo de vida de una sesión POP3
  - Comandos esenciales explicados
  - Simulador de sesión POP3
  - Tips de uso y limitaciones

### 📂 IMAP (Internet Message Access Protocol)
- Puerto 1430
- Gestión de correos en el servidor
- Autenticación simulada
- Soporte para marcar correos como leídos
- Documentación web interactiva con:
  - Estructura de carpetas IMAP
  - Comandos avanzados con ejemplos
  - Comparativa detallada con POP3
  - Demo interactiva de gestión de correos

---

## 👀 Visualización de la base de datos PostgreSQL

¿Quieres ver los correos almacenados directamente en la base de datos? ¡Muy fácil!

```bash
python ver_correos_bd.py
```

Esto mostrará todos los correos y sus campos en consola de forma clara y ordenada.

---

## ⚠️ Limitaciones

Este es un simulador educativo con las siguientes limitaciones:
- ❌ No implementa seguridad (SSL/TLS)
- 🔑 Autenticación simulada
- 📄 Solo maneja texto plano (no adjuntos)
- 📁 Un solo buzón (INBOX)
- 🧩 No implementa todas las características de los protocolos

---

## 🧑‍💻 Desarrollo y Extensión

El proyecto está estructurado de manera modular para facilitar la extensión y modificación:
- Cada protocolo tiene su propio módulo servidor y cliente
- La base de datos está centralizada
- Las utilidades son compartidas entre módulos

---

## 🤝 Contribución

¡Toda contribución es bienvenida! 🚀
1. Haz un fork del repositorio
2. Crea una rama para tu mejora o corrección
3. Realiza tus cambios y haz commit
4. Haz push a tu rama
5. Abre un Pull Request

---

## 📝 Licencia

Este proyecto es software libre y puede ser redistribuido bajo los términos que usted considere apropiados.
