import http.server
import json
import os
import urllib.parse
from app.db import init_db
from app.auth import register_user, login_user

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

class FitArgHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
        self.end_headers()

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else '{}'
        
        try:
            body = json.loads(post_data) if post_data else {}
        except json.JSONDecodeError:
            return self._send_json({"success": False, "error": "JSON inválido"}, 400)

        # Rutas de Autenticación
        if parsed_path.path == '/api/auth/register':
            res = register_user(body.get('name'), body.get('email'), body.get('password'))
            return self._send_json(res, res.get('status_code', 200))

        if parsed_path.path == '/api/auth/login':
            res = login_user(body.get('email'), body.get('password'))
            return self._send_json(res, res.get('status_code', 200))

        return self._send_json({"success": False, "error": "Ruta no encontrada"}, 404)

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        # Redirigir la raíz a index.html
        if parsed_path.path in ('/', ''):
            self.path = '/index.html'
            return super().do_GET()
            
        # Permitir servir archivos estáticos con prefijo /static/
        if self.path.startswith('/static/'):
            self.path = self.path[7:] # remover /static
            return super().do_GET()

        return super().do_GET()

def run_server(port=8000):
    init_db()
    server_address = ('', port)
    httpd = http.server.HTTPServer(server_address, FitArgHTTPRequestHandler)
    print(f"FitArg Server iniciado en http://localhost:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
        httpd.server_close()

if __name__ == '__main__':
    run_server()
