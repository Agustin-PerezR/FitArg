import unittest
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import init_db, get_connection
from app.auth import register_user
from app.password_reset import request_password_reset
from app.email_service import get_sent_emails, clear_sent_emails

class TestForgotPasswordRequest(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_path = self.temp_db.name
        self.temp_db.close()
        init_db(self.db_path)
        clear_sent_emails()
        
        # Registrar usuario de prueba
        reg = register_user("Alexis Mac Allister", "alexis@fitarg.com", "Liverpool10", db_path=self.db_path)
        self.user_id = reg["user"]["id"]

    def tearDown(self):
        clear_sent_emails()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_request_reset_success(self):
        """Verifica generación de token en DB y envío de correo al usuario registrado."""
        res = request_password_reset("alexis@fitarg.com", "http://localhost:8000", db_path=self.db_path)
        self.assertTrue(res["success"])
        self.assertEqual(res["status_code"], 200)
        self.assertTrue(res["token"])

        # Confirmar en DB
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT token, user_id, used FROM password_reset_tokens WHERE user_id = ?", (self.user_id,))
        token_row = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(token_row)
        self.assertEqual(token_row["used"], 0)
        self.assertEqual(token_row["token"], res["token"])

        # Confirmar en cola de emails
        emails = get_sent_emails()
        self.assertEqual(len(emails), 1)
        self.assertEqual(emails[0]["to"], "alexis@fitarg.com")
        self.assertIn(res["token"], emails[0]["html_body"])

    def test_request_reset_nonexistent_email(self):
        """Verifica error cuando el email no pertenece a ningún usuario."""
        res = request_password_reset("inexistente@fitarg.com", db_path=self.db_path)
        self.assertFalse(res["success"])
        self.assertEqual(res["status_code"], 404)

if __name__ == '__main__':
    unittest.main()
