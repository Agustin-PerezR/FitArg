import secrets
from datetime import datetime, timedelta, timezone
from app.db import get_connection
from app.email_service import send_password_reset_email
from app.auth import hash_password, verify_password

def request_password_reset(email: str, base_url: str = 'http://localhost:8000', db_path=None):
    """Genera token de recuperación de contraseña y envía email al usuario."""
    email = (email or '').strip().lower()
    if not email:
        return {"success": False, "status_code": 400, "error": "El correo electrónico es requerido."}
        
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, is_active FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    
    if not user or not user["is_active"]:
        conn.close()
        return {"success": False, "status_code": 404, "error": "No existe una cuenta activa con ese correo electrónico."}
        
    # Generar token único y fecha de expiración (1 hora)
    token = secrets.token_hex(20)
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
    
    cursor.execute(
        "INSERT INTO password_reset_tokens (user_id, token, expires_at, used) VALUES (?, ?, ?, 0)",
        (user["id"], token, expires_at.isoformat())
    )
    conn.commit()
    conn.close()
    
    # Enviar email
    send_password_reset_email(user["email"], user["name"], token, base_url)
    
    return {
        "success": True,
        "status_code": 200,
        "message": "Enlace de recuperación enviado al correo electrónico.",
        "token": token
    }

def validate_reset_token(token: str, db_path=None):
    """Verifica si un token de recuperación es válido y no ha expirado ni sido usado."""
    if not token:
        return {"valid": False, "error": "Token no proporcionado."}
        
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, user_id, expires_at, used FROM password_reset_tokens WHERE token = ?",
        (token,)
    )
    record = cursor.fetchone()
    conn.close()
    
    if not record:
        return {"valid": False, "error": "Token inexistente o inválido."}
        
    if record["used"]:
        return {"valid": False, "error": "Este enlace de recuperación ya ha sido utilizado."}
        
    expires_at = datetime.fromisoformat(record["expires_at"])
    # Normalizar timezone para comparación
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if datetime.now(timezone.utc) > expires_at:
        return {"valid": False, "error": "El enlace de recuperación ha expirado."}
        
    return {"valid": True, "user_id": record["user_id"], "token_id": record["id"]}

def reset_password_with_token(token: str, new_password: str, db_path=None):
    """Restablece la contraseña utilizando un token válido."""
    token_check = validate_reset_token(token, db_path)
    if not token_check["valid"]:
        return {"success": False, "status_code": 400, "error": token_check["error"]}
        
    if not new_password or len(new_password) < 6:
        return {"success": False, "status_code": 400, "error": "La contraseña debe tener al menos 6 caracteres."}
    if not any(c.isdigit() for c in new_password) or not any(c.isalpha() for c in new_password):
        return {"success": False, "status_code": 400, "error": "La contraseña debe contener al menos una letra y un número."}
        
    new_hash = hash_password(new_password)
    user_id = token_check["user_id"]
    token_id = token_check["token_id"]
    
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    # Actualizar clave de usuario
    cursor.execute(
        "UPDATE users SET password_hash = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (new_hash, user_id)
    )
    # Marcar token como utilizado
    cursor.execute(
        "UPDATE password_reset_tokens SET used = 1 WHERE id = ?",
        (token_id,)
    )
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "status_code": 200,
        "message": "Contraseña actualizada exitosamente. Ya podés iniciar sesión con tu nueva clave."
    }
