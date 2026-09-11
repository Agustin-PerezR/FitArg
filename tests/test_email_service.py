import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.email_service import (
    get_smtp_config,
    send_email,
    send_password_reset_email,
    get_sent_emails,
    clear_sent_emails
)

class TestEmailService(unittest.TestCase):
    def setUp(self):
        clear_sent_emails()

    def tearDown(self):
        clear_sent_emails()

    def test_smtp_configuration(self):
        """Verifica la lectura de parámetros de configuración SMTP."""
        config = get_smtp_config()
        self.assertIn("host", config)
        self.assertIn("port", config)
        self.assertIn("user", config)
        self.assertIn("from", config)
        self.assertIn("tls", config)

    def test_send_email_queued(self):
        """Verifica el encolado y armado de contenido de correos."""
        res = send_email("usuario@fitarg.com", "Bienvenido a FitArg", "<h1>Hola!</h1>")
        self.assertTrue(res["success"])
        
        emails = get_sent_emails()
        self.assertEqual(len(emails), 1)
        self.assertEqual(emails[0]["to"], "usuario@fitarg.com")
        self.assertEqual(emails[0]["subject"], "Bienvenido a FitArg")
        self.assertIn("<h1>Hola!</h1>", emails[0]["html_body"])

    def test_send_password_reset_email(self):
        """Verifica el formato del email de restablecimiento con token y link."""
        res = send_password_reset_email("leomessi@fitarg.com", "Lionel Messi", "token_abc_123", "https://fitarg.com.ar")
        self.assertTrue(res["success"])

        emails = get_sent_emails()
        self.assertEqual(len(emails), 1)
        self.assertEqual(emails[0]["to"], "leomessi@fitarg.com")
        self.assertIn("token_abc_123", emails[0]["html_body"])
        self.assertIn("https://fitarg.com.ar/reset-password.html?token=token_abc_123", emails[0]["html_body"])
        self.assertIn("Lionel Messi", emails[0]["html_body"])

if __name__ == '__main__':
    unittest.main()
