import unittest
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import init_db
from app.auth import register_user, login_user, hash_password, verify_password, validate_registration_data

class TestUserRegistrationAndAuth(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_path = self.temp_db.name
        self.temp_db.close()
        init_db(self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_password_hashing(self):
        """Prueba que el hashing de contraseñas sea seguro y verificable."""
        pwd = "Password123"
        hashed = hash_password(pwd)
        self.assertTrue(verify_password(pwd, hashed))
        self.assertFalse(verify_password("WrongPassword", hashed))

    def test_validation_rules(self):
        """Prueba las validaciones de email, nombre y complejidad de clave."""
        # Nombre corto
        errors = validate_registration_data("A", "test@fitarg.com", "Secret123")
        self.assertTrue(any("nombre" in e.lower() for e in errors))

        # Email inválido
        errors = validate_registration_data("Lionel Messi", "invalid-email", "Secret123")
        self.assertTrue(any("correo" in e.lower() for e in errors))

        # Contraseña sin números o muy corta
        errors = validate_registration_data("Lionel Messi", "messi@fitarg.com", "pass")
        self.assertTrue(any("contraseña" in e.lower() for e in errors))

    def test_successful_registration(self):
        """Prueba el registro exitoso de un nuevo usuario."""
        res = register_user("Julián Álvarez", "julian@fitarg.com", "Arana999", db_path=self.db_path)
        self.assertTrue(res["success"])
        self.assertEqual(res["status_code"], 201)
        self.assertEqual(res["user"]["name"], "Julián Álvarez")
        self.assertEqual(res["user"]["email"], "julian@fitarg.com")

    def test_duplicate_email_registration(self):
        """Prueba que no se permita registrar dos usuarios con el mismo email."""
        register_user("Ángel Di María", "fideo@fitarg.com", "Rosario11", db_path=self.db_path)
        res_dup = register_user("Ángel Duplicate", "fideo@fitarg.com", "AnotherPass1", db_path=self.db_path)
        
        self.assertFalse(res_dup["success"])
        self.assertEqual(res_dup["status_code"], 409)
        self.assertTrue(any("ya se encuentra registrado" in e.lower() for e in res_dup["errors"]))

    def test_login_after_registration(self):
        """Prueba inicio de sesión exitoso y fallido tras registrarse."""
        register_user("Rodrigo De Paul", "motorcito@fitarg.com", "Motor777", db_path=self.db_path)
        
        # Login correcto
        login_ok = login_user("motorcito@fitarg.com", "Motor777", db_path=self.db_path)
        self.assertTrue(login_ok["success"])
        self.assertEqual(login_ok["status_code"], 200)
        self.assertIn("token", login_ok)

        # Login incorrecto
        login_fail = login_user("motorcito@fitarg.com", "WrongPassword1", db_path=self.db_path)
        self.assertFalse(login_fail["success"])
        self.assertEqual(login_fail["status_code"], 401)

if __name__ == '__main__':
    unittest.main()
