from datetime import datetime
from app.db import get_connection
from app.auth import hash_password, verify_password, validate_registration_data

def get_user_profile(user_id: int, db_path=None):
    if not user_id:
        return {"success": False, "status_code": 400, "error": "ID de usuario requerido."}
        
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, is_active, created_at, updated_at FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if not user or not user["is_active"]:
        return {"success": False, "status_code": 404, "error": "Usuario no encontrado o dado de baja."}
        
    return {
        "success": True,
        "status_code": 200,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "created_at": user["created_at"],
            "updated_at": user["updated_at"]
        }
    }

def update_user_profile(user_id: int, name: str, current_password: str = None, new_password: str = None, db_path=None):
    if not user_id:
        return {"success": False, "status_code": 400, "error": "ID de usuario requerido."}
        
    name = (name or '').strip()
    if not name or len(name) < 2:
        return {"success": False, "status_code": 400, "error": "El nombre debe tener al menos 2 caracteres."}
        
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, password_hash, is_active FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    
    if not user or not user["is_active"]:
        conn.close()
        return {"success": False, "status_code": 404, "error": "Usuario no encontrado."}
        
    pwd_to_save = user["password_hash"]
    if current_password or new_password:
        if not current_password or not new_password:
            conn.close()
            return {"success": False, "status_code": 400, "error": "Para cambiar la contraseña debe ingresar la actual y la nueva."}
            
        if not verify_password(current_password, user["password_hash"]):
            conn.close()
            return {"success": False, "status_code": 401, "error": "La contraseña actual es incorrecta."}
            
        if len(new_password) < 6 or not any(c.isdigit() for c in new_password) or not any(c.isalpha() for c in new_password):
            conn.close()
            return {"success": False, "status_code": 400, "error": "La nueva contraseña debe tener al menos 6 caracteres, letras y números."}
            
        pwd_to_save = hash_password(new_password)
        
    cursor.execute(
        "UPDATE users SET name = ?, password_hash = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (name, pwd_to_save, user_id)
    )
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "status_code": 200,
        "message": "Perfil actualizado correctamente.",
        "user": {
            "id": user["id"],
            "name": name,
            "email": user["email"]
        }
    }

def deactivate_user_account(user_id: int, password: str, db_path=None):
    if not user_id or not password:
        return {"success": False, "status_code": 400, "error": "ID de usuario y contraseña de confirmación requeridos."}
        
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, password_hash, is_active FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    
    if not user or not user["is_active"]:
        conn.close()
        return {"success": False, "status_code": 404, "error": "La cuenta no existe o ya ha sido dada de baja."}
        
    if not verify_password(password, user["password_hash"]):
        conn.close()
        return {"success": False, "status_code": 401, "error": "Contraseña de confirmación incorrecta."}
        
    cursor.execute("UPDATE users SET is_active = 0, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    
    return {"success": True, "status_code": 200, "message": "Tu cuenta ha sido dada de baja correctamente."}
