import unittest
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import init_db, get_connection
from app.auth import register_user, login_user
from app.profile import deactivate_user_account, get_user_profile

class TestUserDeactivation(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_path = self.temp_db.name
        self.temp_db.close()
        init_db(self.db_path)
        
        # Registrar usuario de prueba
        reg = register_user("Nicolás Otamendi", "general@fitarg.com", "OtaGeneral19", db_path=self.db_path)
        self.user_id = reg["user"]["id"]

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_deactivate_wrong_password(self):
        """Verifica que no se dé de baja la cuenta si la contraseña es errónea."""
        res = deactivate_user_account(self.user_id, "WrongPassword", db_path=self.db_path)
        self.assertFalse(res["success"])
        self.assertEqual(res["status_code"], 401)

        # El usuario debe seguir activo
        profile = get_user_profile(self.user_id, db_path=self.db_path)
        self.assertTrue(profile["success"])

    def test_successful_deactivation(self):
        """Verifica la baja lógica exitosa con contraseña correcta."""
        res = deactivate_user_account(self.user_id, "OtaGeneral19", db_path=self.db_path)
        self.assertTrue(res["success"])
        self.assertEqual(res["status_code"], 200)

        # Confirmar que en la DB is_active sea 0
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT is_active FROM users WHERE id = ?", (self.user_id,))
        user = cursor.fetchone()
        conn.close()
        self.assertEqual(user["is_active"], 0)

        # Intentar consultar perfil debe retornar 404
        profile = get_user_profile(self.user_id, db_path=self.db_path)
        self.assertFalse(profile["success"])
        self.assertEqual(profile["status_code"], 404)

        # Intentar login debe fallar con 401
        login_res = login_user("general@fitarg.com", "OtaGeneral19", db_path=self.db_path)
        self.assertFalse(login_res["success"])
        self.assertEqual(login_res["status_code"], 401)

if __name__ == '__main__':
    unittest.main()
