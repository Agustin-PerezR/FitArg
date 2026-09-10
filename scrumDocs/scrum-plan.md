# Plan de Requerimientos — FitArg

_Generado automáticamente el 2026-09-10T14:06:35.308Z — no editar a mano, se sobreescribe en cada publicación._

Orden sugerido de desarrollo (respeta dependencias entre Requerimientos). Cada fila indica de qué Requerimientos depende, si tiene.

| Orden | Código | Requerimiento | Historia de Usuario | Módulo | Entrega | Estado | Desarrollador | Depende de | Rechazos |
|---|---|---|---|---|---|---|---|---|---|
| 1 | RF-01 | Dockerizar la app para el entorno de pruebas | RO-01 | — | — | testing | dev-fitarg-3 | — | — |
| 2 | RF-01 | Configurar servicio de correo SMTP | RO-02 | — | — | testing | dev-fitarg-3 | — | — |
| 3 | RF-01 | Configurar estilos base, modo oscuro y paleta institucional | RO-03 | — | — | testing | dev-fitarg-3 | — | — |
| 4 | RF-01 | Registro de nuevos usuarios | HU-01 | — | — | Hecho | dev-fitarg-3 | RF-01 | — |
| 5 | RF-02 | Visualización y edición de perfil | HU-01 | — | — | testing | dev-fitarg-3 | RF-01 | — |
| 6 | RF-01 | Solicitud de recuperación y envío de token por email | HU-02 | — | — | Haciendo | dev-fitarg-3 | RF-01, RF-01 | — |
| 7 | RF-01 | Listado de rutinas personales | HU-03 | — | — | testing | dev-fitarg-3 | RF-01 | — |
| 8 | RF-03 | Baja lógica de cuenta de usuario | HU-01 | — | — | testing | dev-fitarg-3 | RF-02 | — |
| 9 | RF-02 | Restablecimiento de contraseña con token | HU-02 | — | — | testing | dev-fitarg-3 | RF-01 | — |
| 10 | RF-02 | Creación y edición de rutinas de entrenamiento | HU-03 | — | — | testing | dev-fitarg-3 | RF-01 | — |
| 11 | RF-03 | Eliminación de rutina con confirmación | HU-03 | — | — | testing | dev-fitarg-3 | RF-01 | — |

## Detalle

### RF-01 — Dockerizar la app para el entorno de pruebas
Ajuste de mapeo a 8088:8000 con contenedor corriendo internamente en puerto 8000. PR #13 abierto en GitHub hacia dev.
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
Implementaci�n de pantalla forgot-password.html y endpoint POST /api/auth/forgot-password con generaci�n de token y despacho de email, validado con tests unitarios.
- Estimado: 30h

### RF-01 — Listado de rutinas personales
Implementaci�n de pantalla routines.html y endpoint GET /api/routines con filtrado interactivo y aislamiento de datos por usuario, verificado con tests unitarios.
- Estimado: 3h

### RF-03 — Baja lógica de cuenta de usuario
Implementaci�n de pantalla y endpoint POST /api/profile/deactivate para baja l�gica de cuenta tras confirmar contrase�a, validado con tests unitarios.
- Estimado: 2h

### RF-02 — Restablecimiento de contraseña con token
Implementaci�n de pantalla reset-password.html y endpoint POST /api/auth/reset-password con validaci�n de tokens �nicos no reutilizables y suite de tests unitarios.
- Estimado: 3h

### RF-02 — Creación y edición de rutinas de entrenamiento
Implementaci�n de editor interactivo routine-editor.html y endpoint POST /api/routines/save para alta y edici�n de rutinas completas, verificado con tests unitarios.
- Estimado: 5h

### RF-03 — Eliminación de rutina con confirmación
Implementaci�n de di�logo de confirmaci�n de borrado en UI y endpoint POST /api/routines/delete con validaci�n de propiedad de la rutina, verificado con tests unitarios.
- Estimado: 2h
