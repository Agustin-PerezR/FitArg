import unittest
import os
import sys
import tempfile
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import init_db, get_connection
from app.auth import register_user, login_user
from app.password_reset import request_password_reset, validate_reset_token, reset_password_with_token
from app.email_service import clear_sent_emails

class TestPasswordResetWithToken(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_path = self.temp_db.name
        self.temp_db.close()
        init_db(self.db_path)
        clear_sent_emails()
        
        # Registrar usuario de prueba
        reg = register_user("Emiliano Martínez", "dibu@fitarg.com", "Dibu23Aston", db_path=self.db_path)
        self.user_id = reg["user"]["id"]
        
        # Solicitar token de reseteo
        req = request_password_reset("dibu@fitarg.com", db_path=self.db_path)
        self.token = req["token"]

    def tearDown(self):
        clear_sent_emails()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_validate_valid_token(self):
        """Verifica que un token recién generado sea válido."""
        res = validate_reset_token(self.token, db_path=self.db_path)
        self.assertTrue(res["valid"])
        self.assertEqual(res["user_id"], self.user_id)

    def test_validate_invalid_token(self):
        """Verifica que un token inexistente sea rechazado."""
        res = validate_reset_token("invalid_token_999", db_path=self.db_path)
        self.assertFalse(res["valid"])

    def test_reset_password_success_and_login(self):
        """Verifica el cambio exitoso de contraseña y posterior login con la nueva clave."""
        res = reset_password_with_token(self.token, "NewDibuPass2026", db_path=self.db_path)
        self.assertTrue(res["success"])
        self.assertEqual(res["status_code"], 200)

        # Token no debe poder volver a usarse
        check_reuse = validate_reset_token(self.token, db_path=self.db_path)
        self.assertFalse(check_reuse["valid"])

        # Login con contraseña vieja debe fallar
        old_login = login_user("dibu@fitarg.com", "Dibu23Aston", db_path=self.db_path)
        self.assertFalse(old_login["success"])

        # Login con contraseña nueva debe ser exitoso
        new_login = login_user("dibu@fitarg.com", "NewDibuPass2026", db_path=self.db_path)
        self.assertTrue(new_login["success"])
        self.assertEqual(new_login["status_code"], 200)

    def test_reset_password_invalid_password_rules(self):
        """Verifica que la nueva contraseña cumpla las reglas de seguridad mínimas."""
        res = reset_password_with_token(self.token, "123", db_path=self.db_path)
        self.assertFalse(res["success"])
        self.assertEqual(res["status_code"], 400)

if __name__ == '__main__':
    unittest.main()
