import unittest
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import init_db
from app.auth import register_user
from app.routines import save_routine, get_routine_by_id, delete_routine, get_user_routines

class TestRoutineDeletion(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_path = self.temp_db.name
        self.temp_db.close()
        init_db(self.db_path)
        
        # Crear 2 usuarios
        u1 = register_user("Paulo Dybala", "joya@fitarg.com", "RomaJoya21", db_path=self.db_path)
        self.user1_id = u1["user"]["id"]
        
        u2 = register_user("Leandro Paredes", "leo_p@fitarg.com", "BocaParedes5", db_path=self.db_path)
        self.user2_id = u2["user"]["id"]
        
        # Crear rutina para user1
        res1 = save_routine(
            self.user1_id,
            "Rutina de Piernas",
            "Sentadilla y Prensa",
            [{"name": "Sentadillas", "sets": 4, "reps": 8, "weight": 100}],
            db_path=self.db_path
        )
        self.routine1_id = res1["routine_id"]

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_successful_routine_deletion(self):
        """Verifica la eliminación correcta de una rutina perteneciente al usuario."""
        del_res = delete_routine(self.routine1_id, self.user1_id, db_path=self.db_path)
        self.assertTrue(del_res["success"])
        self.assertEqual(del_res["status_code"], 200)

        # Consultar la rutina debe devolver 404
        check = get_routine_by_id(self.routine1_id, self.user1_id, db_path=self.db_path)
        self.assertFalse(check["success"])
        self.assertEqual(check["status_code"], 404)

        # El listado de rutinas debe estar vacío
        routines_list = get_user_routines(self.user1_id, db_path=self.db_path)
        self.assertEqual(routines_list["total"], 0)

    def test_delete_routine_unauthorized_user(self):
        """Verifica que un usuario no pueda borrar la rutina de otro usuario."""
        del_res = delete_routine(self.routine1_id, self.user2_id, db_path=self.db_path)
        self.assertFalse(del_res["success"])
        self.assertEqual(del_res["status_code"], 404)

        # La rutina original debe seguir existiendo intacta
        check = get_routine_by_id(self.routine1_id, self.user1_id, db_path=self.db_path)
        self.assertTrue(check["success"])

if __name__ == '__main__':
    unittest.main()
