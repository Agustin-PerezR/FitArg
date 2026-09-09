import hashlib
import os
import re
import secrets
from app.db import get_connection

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

def hash_password(password: str, salt: str = None) -> str:
    """Genera hash seguro PBKDF2-HMAC-SHA256 con salt."""
    if not salt:
        salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return f"{salt}${key.hex()}"

def verify_password(password: str, stored_hash: str) -> bool:
    """Valida la contraseña contra el hash almacenado."""
    try:
        salt, key = stored_hash.split('$')
        new_hash = hash_password(password, salt)
        return secrets.compare_digest(new_hash, stored_hash)
    except Exception:
        return False

def validate_registration_data(name: str, email: str, password: str):
    """Valida los campos requeridos para el registro de usuario."""
    errors = []
    
    if not name or len(name.strip()) < 2:
        errors.append("El nombre debe tener al menos 2 caracteres.")
        
    if not email or not EMAIL_REGEX.match(email.strip().lower()):
        errors.append("El formato del correo electrónico es inválido.")
        
    if not password or len(password) < 6:
        errors.append("La contraseña debe tener al menos 6 caracteres.")
    elif not any(c.isdigit() for c in password) or not any(c.isalpha() for c in password):
        errors.append("La contraseña debe contener al menos una letra y un número.")
        
    return errors

def register_user(name: str, email: str, password: str, db_path=None):
    """Registra un nuevo usuario en la base de datos."""
    name = (name or '').strip()
    email = (email or '').strip().lower()
    
    errors = validate_registration_data(name, email, password)
    if errors:
        return {"success": False, "status_code": 400, "errors": errors}
        
    conn = get_connection(db_path)
    cursor = conn.cursor()
    
    # Verificar si el email ya existe
    cursor.execute("SELECT id, is_active FROM users WHERE email = ?", (email,))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        return {"success": False, "status_code": 409, "errors": ["El correo electrónico ya se encuentra registrado."]}
        
    pwd_hash = hash_password(password)
    cursor.execute(
        "INSERT INTO users (name, email, password_hash, is_active) VALUES (?, ?, ?, 1)",
        (name, email, pwd_hash)
    )
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "status_code": 201,
        "user": {
            "id": user_id,
            "name": name,
            "email": email
        },
        "message": "Usuario registrado exitosamente."
    }

def login_user(email: str, password: str, db_path=None):
    """Autentica a un usuario activo."""
    email = (email or '').strip().lower()
    if not email or not password:
        return {"success": False, "status_code": 400, "errors": ["Email y contraseña requeridos."]}
        
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, password_hash, is_active FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    
    if not user or not user["is_active"]:
        return {"success": False, "status_code": 401, "errors": ["Credenciales inválidas o cuenta desactivada."]}
        
    if not verify_password(password, user["password_hash"]):
        return {"success": False, "status_code": 401, "errors": ["Credenciales inválidas o cuenta desactivada."]}
        
    token = secrets.token_urlsafe(32)
    return {
        "success": True,
        "status_code": 200,
        "token": token,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }
    }
