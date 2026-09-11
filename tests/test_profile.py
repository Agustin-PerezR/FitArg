import unittest
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import init_db
from app.auth import register_user, verify_password
from app.profile import get_user_profile, update_user_profile

class TestUserProfile(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_path = self.temp_db.name
        self.temp_db.close()
        init_db(self.db_path)
        
        # Registrar usuario de prueba
        reg = register_user("Enzo Fernández", "enzo@fitarg.com", "Chelsea2026", db_path=self.db_path)
        self.user_id = reg["user"]["id"]

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_get_user_profile(self):
        """Verifica la consulta correcta de los datos del perfil."""
        res = get_user_profile(self.user_id, db_path=self.db_path)
        self.assertTrue(res["success"])
        self.assertEqual(res["user"]["name"], "Enzo Fernández")
        self.assertEqual(res["user"]["email"], "enzo@fitarg.com")

    def test_get_nonexistent_profile(self):
        """Verifica error al consultar un ID inexistente."""
        res = get_user_profile(99999, db_path=self.db_path)
        self.assertFalse(res["success"])
        self.assertEqual(res["status_code"], 404)

    def test_update_name(self):
        """Verifica actualización de nombre de perfil."""
        res = update_user_profile(self.user_id, "Enzo Jeremías Fernández", db_path=self.db_path)
        self.assertTrue(res["success"])
        self.assertEqual(res["user"]["name"], "Enzo Jeremías Fernández")

        # Confirmar en base de datos
        check = get_user_profile(self.user_id, db_path=self.db_path)
        self.assertEqual(check["user"]["name"], "Enzo Jeremías Fernández")

    def test_update_password(self):
        """Verifica cambio de contraseña con validación de clave previa."""
        # Cambio con clave actual correcta
        res_ok = update_user_profile(
            self.user_id,
            "Enzo Fernández",
            current_password="Chelsea2026",
            new_password="NewPassword888",
            db_path=self.db_path
        )
        self.assertTrue(res_ok["success"])

        # Intentar cambio con clave actual incorrecta
        res_fail = update_user_profile(
            self.user_id,
            "Enzo Fernández",
            current_password="WrongOldPassword",
            new_password="AnotherPassword999",
            db_path=self.db_path
        )
        self.assertFalse(res_fail["success"])
        self.assertEqual(res_fail["status_code"], 401)

if __name__ == '__main__':
    unittest.main()
