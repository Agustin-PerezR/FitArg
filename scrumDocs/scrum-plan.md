# Plan de Requerimientos — FitArg

_Generado automáticamente el 2026-09-09T14:38:31.078Z — no editar a mano, se sobreescribe en cada publicación._

Orden sugerido de desarrollo (respeta dependencias entre Requerimientos). Cada fila indica de qué Requerimientos depende, si tiene.

| Orden | Código | Requerimiento | Historia de Usuario | Módulo | Entrega | Estado | Desarrollador | Depende de | Rechazos |
|---|---|---|---|---|---|---|---|---|---|
| 1 | RF-01 | Dockerizar la app para el entorno de pruebas | RO-01 | — | — | Hacer | dev-fitarg-3 | — | — |
| 2 | RF-01 | Configurar servicio de correo SMTP | RO-02 | — | — | Hecho | dev-fitarg-3 | — | — |
| 3 | RF-01 | Configurar estilos base, modo oscuro y paleta institucional | RO-03 | — | — | Hecho | dev-fitarg-3 | — | — |
| 4 | RF-01 | Registro de nuevos usuarios | HU-01 | — | — | Hecho | dev-fitarg-3 | RF-01 | — |
| 5 | RF-02 | Visualización y edición de perfil | HU-01 | — | — | Hecho | dev-fitarg-3 | RF-01 | — |
| 6 | RF-01 | Solicitud de recuperación y envío de token por email | HU-02 | — | — | Hacer | dev-fitarg-3 | RF-01, RF-01 | — |
| 7 | RF-01 | Listado de rutinas personales | HU-03 | — | — | Hacer | dev-fitarg-3 | RF-01 | — |
| 8 | RF-03 | Baja lógica de cuenta de usuario | HU-01 | — | — | Hecho | dev-fitarg-3 | RF-02 | — |
| 9 | RF-02 | Restablecimiento de contraseña con token | HU-02 | — | — | Hacer | dev-fitarg-3 | RF-01 | — |
| 10 | RF-02 | Creación y edición de rutinas de entrenamiento | HU-03 | — | — | Hacer | dev-fitarg-3 | RF-01 | — |
| 11 | RF-03 | Eliminación de rutina con confirmación | HU-03 | — | — | Hacer | dev-fitarg-3 | RF-01 | — |

## Detalle

### RF-01 — Dockerizar la app para el entorno de pruebas
- Estimado: 4h

### RF-01 — Configurar servicio de correo SMTP
Configuraci�n del servicio SMTP y m�dulo de env�o de emails con plantilla HTML personalizada y tests unitarios.
- Estimado: 2h

### RF-01 — Configurar estilos base, modo oscuro y paleta institucional
Configuraci�n completada: tokens CSS con paleta celeste y blanca argentina, soporte modo oscuro, componentes UI base y 5 tests unitarios aprobados.
- Estimado: 3h

### RF-01 — Registro de nuevos usuarios
Implementaci�n de formulario de registro y endpoint POST /api/auth/register con validaciones completas y suite de tests unitarios.
- Estimado: 4h

### RF-02 — Visualización y edición de perfil
Implementaci�n de pantalla de perfil, endpoint GET /api/profile y actualizaci�n con cambio seguro de contrase�a, cubierto con tests unitarios.
- Estimado: 3h

### RF-01 — Solicitud de recuperación y envío de token por email
- Estimado: 3h

### RF-01 — Listado de rutinas personales
- Estimado: 3h

### RF-03 — Baja lógica de cuenta de usuario
Implementaci�n de pantalla y endpoint POST /api/profile/deactivate para baja l�gica de cuenta tras confirmar contrase�a, validado con tests unitarios.
- Estimado: 2h

### RF-02 — Restablecimiento de contraseña con token
- Estimado: 3h

### RF-02 — Creación y edición de rutinas de entrenamiento
- Estimado: 5h

### RF-03 — Eliminación de rutina con confirmación
- Estimado: 2h
