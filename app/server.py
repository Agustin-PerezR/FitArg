import http.server
import json
import os
import urllib.parse
from app.db import init_db
from app.auth import register_user, login_user
from app.profile import get_user_profile, update_user_profile, deactivate_user_account

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

        # Rutas de Perfil
        if parsed_path.path in ('/api/profile/update', '/api/profile'):
            res = update_user_profile(
                body.get('user_id'),
                body.get('name'),
                body.get('current_password'),
                body.get('new_password')
            )
            return self._send_json(res, res.get('status_code', 200))

        if parsed_path.path == '/api/profile/deactivate':
            res = deactivate_user_account(body.get('user_id'), body.get('password'))
            return self._send_json(res, res.get('status_code', 200))

        return self._send_json({"success": False, "error": "Ruta no encontrada"}, 404)

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        # API Perfil
        if parsed_path.path == '/api/profile':
            params = urllib.parse.parse_qs(parsed_path.query)
            user_id = params.get('user_id', [None])[0]
            try:
                user_id_int = int(user_id) if user_id else None
            except ValueError:
                return self._send_json({"success": False, "error": "ID de usuario inválido"}, 400)
                
            res = get_user_profile(user_id_int)
            return self._send_json(res, res.get('status_code', 200))

        # Redirigir la raíz a index.html
        if parsed_path.path in ('/', ''):
            self.path = '/index.html'
            return super().do_GET()
            
        # Permitir servir archivos estáticos con prefijo /static/
        if self.path.startswith('/static/'):
            self.path = self.path[7:]
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
