import os

def get_content_type(path):
    """Determina el Content-Type basado en la extensión del archivo"""
    extension = path.split('.')[-1].lower()
    content_types = {
        'html': 'text/html',
        'css': 'text/css',
        'js': 'application/javascript',
        'png': 'image/png',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'gif': 'image/gif'
    }
    return content_types.get(extension, 'text/plain')

def serve_file(file_path):
    """Lee y prepara una respuesta HTTP para un archivo"""
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
            content_type = get_content_type(file_path)
            
            response = [
                b'HTTP/1.1 200 OK',
                f'Content-Type: {content_type}'.encode(),
                f'Content-Length: {len(content)}'.encode(),
                b'',
                content
            ]
            return b'\r\n'.join(response)
    except FileNotFoundError:
        return b'HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\n404 File not found'

def handle_http_request(request, base_path):
    """Maneja una solicitud HTTP básica"""
    try:
        # Parsear la primera línea de la solicitud
        request_line = request.split(b'\r\n')[0].decode()
        method, path, _ = request_line.split(' ')
        
        if method != 'GET':
            return b'HTTP/1.1 405 Method Not Allowed\r\n\r\nOnly GET requests are supported'
        
        # Si es la ruta raíz, servir el archivo HTML correspondiente
        if path == '/' or path == '/index.html':
            path = '/index.html'
        
        # Manejar rutas a archivos estáticos
        if path.startswith('/static/'):
            file_path = os.path.join(os.path.dirname(base_path), path[1:])
        else:
            file_path = os.path.join(base_path, path[1:])
        
        return serve_file(file_path)
    except Exception as e:
        return f'HTTP/1.1 500 Internal Server Error\r\n\r\n{str(e)}'.encode()
