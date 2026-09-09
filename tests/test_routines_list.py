import unittest
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import init_db
from app.auth import register_user
from app.routines import save_routine, get_user_routines, get_routine_by_id

class TestRoutinesList(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_path = self.temp_db.name
        self.temp_db.close()
        init_db(self.db_path)
        
        # Registrar 2 usuarios para validar aislamiento
        u1 = register_user("Lionel Messi", "leo@fitarg.com", "InterMiami10", db_path=self.db_path)
        self.user1_id = u1["user"]["id"]
        
        u2 = register_user("Cristiano Ronaldo", "cr7@fitarg.com", "AlNassr777", db_path=self.db_path)
        self.user2_id = u2["user"]["id"]
        
        # Crear rutinas para user1
        save_routine(
            self.user1_id,
            "Pecho y Bíceps",
            "Rutina de fuerza",
            [{"name": "Press Banca", "sets": 4, "reps": 8, "weight": 90}],
            db_path=self.db_path
        )
        save_routine(
            self.user1_id,
            "Piernas y Hombros",
            "Día de tren inferior",
            [{"name": "Sentadilla", "sets": 4, "reps": 10, "weight": 120}],
            db_path=self.db_path
        )

        # Crear rutina para user2
        save_routine(
            self.user2_id,
            "Cardio Extremo",
            "Rutina aeróbica",
            [{"name": "Cinta", "sets": 1, "reps": 1, "weight": 0}],
            db_path=self.db_path
        )

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_get_user_routines_isolation(self):
        """Verifica que cada usuario sólo consulte sus propias rutinas personales."""
        res1 = get_user_routines(self.user1_id, db_path=self.db_path)
        self.assertTrue(res1["success"])
        self.assertEqual(res1["total"], 2)
        names1 = [r["name"] for r in res1["routines"]]
        self.assertIn("Pecho y Bíceps", names1)
        self.assertIn("Piernas y Hombros", names1)
        self.assertNotIn("Cardio Extremo", names1)

        res2 = get_user_routines(self.user2_id, db_path=self.db_path)
        self.assertTrue(res2["success"])
        self.assertEqual(res2["total"], 1)
        self.assertEqual(res2["routines"][0]["name"], "Cardio Extremo")

    def test_get_routine_by_id(self):
        """Verifica la consulta detallada de una rutina individual."""
        res_list = get_user_routines(self.user1_id, db_path=self.db_path)
        r_id = res_list["routines"][0]["id"]

        detail = get_routine_by_id(r_id, self.user1_id, db_path=self.db_path)
        self.assertTrue(detail["success"])
        self.assertEqual(detail["routine"]["id"], r_id)
        self.assertEqual(len(detail["routine"]["exercises"]), 1)

if __name__ == '__main__':
    unittest.main()
