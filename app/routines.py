import json
from app.db import get_connection

def get_user_routines(user_id: int, db_path=None):
    if not user_id:
        return {"success": False, "status_code": 400, "error": "ID de usuario requerido."}
        
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_id, name, description, exercises_json, created_at, updated_at FROM routines WHERE user_id = ? ORDER BY updated_at DESC", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    
    routines = []
    for r in rows:
        try:
            exercises = json.loads(r["exercises_json"])
        except Exception:
            exercises = []
            
        routines.append({
            "id": r["id"],
            "user_id": r["user_id"],
            "name": r["name"],
            "description": r["description"] or "",
            "exercises_count": len(exercises),
            "exercises": exercises,
            "created_at": r["created_at"],
            "updated_at": r["updated_at"]
        })
        
    return {"success": True, "status_code": 200, "routines": routines, "total": len(routines)}

def get_routine_by_id(routine_id: int, user_id: int, db_path=None):
    if not routine_id or not user_id:
        return {"success": False, "status_code": 400, "error": "ID de rutina y usuario requeridos."}
        
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_id, name, description, exercises_json, created_at, updated_at FROM routines WHERE id = ? AND user_id = ?", (routine_id, user_id))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return {"success": False, "status_code": 404, "error": "Rutina no encontrada o no pertenece al usuario."}
        
    try:
        exercises = json.loads(row["exercises_json"])
    except Exception:
        exercises = []
        
    return {
        "success": True,
        "status_code": 200,
        "routine": {
            "id": row["id"],
            "user_id": row["user_id"],
            "name": row["name"],
            "description": row["description"] or "",
            "exercises": exercises,
            "created_at": row["created_at"],
            "updated_at": row["updated_at"]
        }
    }

def save_routine(user_id: int, name: str, description: str, exercises: list, routine_id: int = None, db_path=None):
    if not user_id:
        return {"success": False, "status_code": 400, "error": "ID de usuario requerido."}
        
    name = (name or '').strip()
    if not name or len(name) < 2:
        return {"success": False, "status_code": 400, "error": "El nombre de la rutina debe tener al menos 2 caracteres."}
        
    exercises_list = exercises if isinstance(exercises, list) else []
    exercises_json = json.dumps(exercises_list, ensure_ascii=False)
    description = (description or '').strip()
    
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    if routine_id:
        cursor.execute("SELECT id FROM routines WHERE id = ? AND user_id = ?", (routine_id, user_id))
        if not cursor.fetchone():
            conn.close()
            return {"success": False, "status_code": 404, "error": "Rutina no encontrada para editar."}
            
        cursor.execute("UPDATE routines SET name = ?, description = ?, exercises_json = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ? AND user_id = ?", (name, description, exercises_json, routine_id, user_id))
        conn.commit()
        conn.close()
        return {"success": True, "status_code": 200, "message": "Rutina actualizada con éxito.", "routine_id": routine_id}
    else:
        cursor.execute("INSERT INTO routines (user_id, name, description, exercises_json) VALUES (?, ?, ?, ?)", (user_id, name, description, exercises_json))
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return {"success": True, "status_code": 201, "message": "Rutina creada con éxito.", "routine_id": new_id}

def delete_routine(routine_id: int, user_id: int, db_path=None):
    if not routine_id or not user_id:
        return {"success": False, "status_code": 400, "error": "ID de rutina y usuario requeridos."}
        
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM routines WHERE id = ? AND user_id = ?", (routine_id, user_id))
    if not cursor.fetchone():
        conn.close()
        return {"success": False, "status_code": 404, "error": "Rutina no encontrada o no pertenece al usuario."}
        
    cursor.execute("DELETE FROM routines WHERE id = ? AND user_id = ?", (routine_id, user_id))
    conn.commit()
    conn.close()
    
    return {"success": True, "status_code": 200, "message": "Rutina eliminada correctamente."}
