import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configuración SMTP por variables de entorno
SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
SMTP_USER = os.environ.get('SMTP_USER', 'notificaciones@fitarg.com.ar')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
SMTP_FROM = os.environ.get('SMTP_FROM', 'FitArg <notificaciones@fitarg.com.ar>')
SMTP_USE_TLS = os.environ.get('SMTP_USE_TLS', 'true').lower() in ('true', '1', 'yes')

# Cola en memoria para testing y verificación de envíos
SENT_EMAILS = []

def get_smtp_config():
    """Devuelve la configuración actual de SMTP."""
    return {
        "host": SMTP_HOST,
        "port": SMTP_PORT,
        "user": SMTP_USER,
        "from": SMTP_FROM,
        "tls": SMTP_USE_TLS,
        "configured": bool(SMTP_USER and SMTP_PASSWORD)
    }

def send_email(to_email: str, subject: str, html_body: str, text_body: str = None):
    """Envía un correo electrónico vía SMTP o almacena en la cola si está en modo desarrollo/pruebas."""
    to_email = (to_email or '').strip()
    if not to_email:
        return {"success": False, "error": "Destinatario no especificado."}

    text_body = text_body or html_body

    email_record = {
        "to": to_email,
        "subject": subject,
        "html_body": html_body,
        "text_body": text_body,
        "from": SMTP_FROM
    }
    SENT_EMAILS.append(email_record)

    # Si hay credenciales reales configuradas, realizar el envío por socket SMTP
    if SMTP_PASSWORD and SMTP_HOST:
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = SMTP_FROM
            msg['To'] = to_email

            part1 = MIMEText(text_body, 'plain', 'utf-8')
            part2 = MIMEText(html_body, 'html', 'utf-8')
            msg.attach(part1)
            msg.attach(part2)

            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
                if SMTP_USE_TLS:
                    server.starttls()
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.sendmail(SMTP_FROM, [to_email], msg.as_string())
                
            return {"success": True, "mode": "smtp_live", "message": "Email enviado por SMTP."}
        except Exception as e:
            return {"success": False, "mode": "smtp_error", "error": f"Fallo al conectar con servidor SMTP: {str(e)}"}
    
    return {
        "success": True,
        "mode": "dev_queue",
        "message": "Email encolado exitosamente (modo desarrollo/pruebas)."
    }

def send_password_reset_email(to_email: str, user_name: str, reset_token: str, base_url: str = 'http://localhost:8000'):
    """Genera y envía el correo con el enlace y token de recuperación de contraseña."""
    reset_url = f"{base_url}/reset-password.html?token={reset_token}"
    subject = "Recuperación de Contraseña - FitArg 🇦🇷"
    
    html_body = f"""
    <div style="font-family: Arial, sans-serif; background-color: #f4f7fb; padding: 24px;">
      <div style="max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 12px; padding: 32px; border: 1px solid #74acdf;">
        <h2 style="color: #1e293b; margin-bottom: 12px;">🏋️ FitArg - Restablecer Contraseña</h2>
        <p style="color: #475569;">Hola <strong>{user_name}</strong>,</p>
        <p style="color: #475569;">Recibimos una solicitud para restablecer la contraseña de tu cuenta en FitArg.</p>
        <div style="text-align: center; margin: 28px 0;">
          <a href="{reset_url}" style="background-color: #74acdf; color: #0b1329; padding: 12px 24px; text-decoration: none; border-radius: 8px; font-weight: bold; display: inline-block;">
            Restablecer mi Contraseña
          </a>
        </div>
        <p style="color: #64748b; font-size: 13px;">O copiá y pegá este enlace en tu navegador:</p>
        <p style="color: #0284c7; font-size: 12px; word-break: break-all;">{reset_url}</p>
        <p style="color: #94a3b8; font-size: 12px; margin-top: 24px; border-top: 1px solid #e2e8f0; padding-top: 16px;">
          Este enlace expirará en 1 hora. Si no solicitaste este cambio, podés ignorar este correo.
        </p>
      </div>
    </div>
    """
    
    text_body = f"Hola {user_name},\n\nPara restablecer tu contraseña en FitArg ingresá a: {reset_url}\n\nToken: {reset_token}"
    return send_email(to_email, subject, html_body, text_body)

def get_sent_emails():
    return SENT_EMAILS

def clear_sent_emails():
    SENT_EMAILS.clear()
