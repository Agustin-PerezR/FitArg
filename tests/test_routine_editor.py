import unittest
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import init_db
from app.auth import register_user
from app.routines import save_routine, get_routine_by_id

class TestRoutineCreationAndEditing(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_path = self.temp_db.name
        self.temp_db.close()
        init_db(self.db_path)
        
        reg = register_user("Lautaro Martínez", "toro@fitarg.com", "InterMilano20", db_path=self.db_path)
        self.user_id = reg["user"]["id"]

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_create_routine_with_exercises(self):
        """Verifica la creación exitosa de una rutina con lista de ejercicios detallados."""
        exercises = [
            {"name": "Press Militar", "group": "Hombros", "sets": 4, "reps": 8, "weight": 60},
            {"name": "Elevaciones Laterales", "group": "Hombros", "sets": 3, "reps": 12, "weight": 14}
        ]
        res = save_routine(
            self.user_id,
            "Hombros Destructivos",
            "Entrenamiento focalizado en deltoides",
            exercises,
            db_path=self.db_path
        )
        self.assertTrue(res["success"])
        self.assertEqual(res["status_code"], 201)
        r_id = res["routine_id"]

        # Confirmar detalle
        detail = get_routine_by_id(r_id, self.user_id, db_path=self.db_path)
        self.assertTrue(detail["success"])
        self.assertEqual(detail["routine"]["name"], "Hombros Destructivos")
        self.assertEqual(len(detail["routine"]["exercises"]), 2)
        self.assertEqual(detail["routine"]["exercises"][0]["name"], "Press Militar")

    def test_edit_existing_routine(self):
        """Verifica la edición de una rutina existente (cambio de nombre, descripción y ejercicios)."""
        create_res = save_routine(
            self.user_id,
            "Espalda Inicial",
            "Versión 1",
            [{"name": "Dominadas", "sets": 3, "reps": 10, "weight": 0}],
            db_path=self.db_path
        )
        r_id = create_res["routine_id"]

        # Modificar rutina
        new_exercises = [
            {"name": "Dominadas Lastradas", "sets": 4, "reps": 6, "weight": 20},
            {"name": "Remo con Barra", "sets": 4, "reps": 8, "weight": 80}
        ]
        edit_res = save_routine(
            self.user_id,
            "Espalda Pesada Pro",
            "Versión 2 mejorada",
            new_exercises,
            routine_id=r_id,
            db_path=self.db_path
        )
        self.assertTrue(edit_res["success"])
        self.assertEqual(edit_res["status_code"], 200)

        # Confirmar en DB
        check = get_routine_by_id(r_id, self.user_id, db_path=self.db_path)
        self.assertEqual(check["routine"]["name"], "Espalda Pesada Pro")
        self.assertEqual(len(check["routine"]["exercises"]), 2)
        self.assertEqual(check["routine"]["exercises"][0]["weight"], 20)

    def test_create_routine_invalid_name(self):
        """Verifica error al intentar crear una rutina sin nombre o demasiado corto."""
        res = save_routine(self.user_id, "A", "Desc", [], db_path=self.db_path)
        self.assertFalse(res["success"])
        self.assertEqual(res["status_code"], 400)

if __name__ == '__main__':
    unittest.main()
