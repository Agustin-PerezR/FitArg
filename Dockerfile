# ==============================================================================
# FitArg - Dockerfile para Entorno de Pruebas y Despliegue (QA / Producción)
# ==============================================================================

FROM python:3.12-slim

# Evitar escritura de bytecode .pyc y buffer de salida estándar
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FITARG_DB_PATH=/app/data/fitarg.db

WORKDIR /app

# Crear directorio persistente para base de datos SQLite
RUN mkdir -p /app/data

# Copiar código fuente y assets estáticos
COPY app/ /app/app/
COPY static/ /app/static/
COPY scrumDocs/ /app/scrumDocs/

# Exponer el puerto del servidor HTTP
EXPOSE 8000

# Verificación de salud del contenedor
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/').read()" || exit 1

# Comando de inicio del servidor
CMD ["python", "-m", "app.server"]
