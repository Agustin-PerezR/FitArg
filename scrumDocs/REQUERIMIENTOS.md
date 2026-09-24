# Requerimientos -- FitArg

_Generado automaticamente el 2026-09-24T19:24:38.194Z -- no editar a mano, se sobreescribe en cada publicacion._

## HU-01: Gestión de Usuarios (ABM de Perfil)

### RF-01: Registro de nuevos usuarios (Funcional)

Formulario y endpoint para el registro de nuevos usuarios con validación de datos (email único, contraseña segura y nombre).

**Condiciones de aprobación**

_Sin condiciones de aprobación cargadas: pedíselas al Project Manager o al Scrum Master antes de darlo por terminado._

### RF-02: Visualización y edición de perfil (Funcional)

Pantalla y lógica para que el usuario autenticado pueda consultar y actualizar su información personal.

**Condiciones de aprobación**

_Sin condiciones de aprobación cargadas: pedíselas al Project Manager o al Scrum Master antes de darlo por terminado._

### RF-03: Baja lógica de cuenta de usuario (Funcional)

Flujo para dar de baja la cuenta con diálogo de confirmación de seguridad y desactivación del acceso.

**Condiciones de aprobación**

_Sin condiciones de aprobación cargadas: pedíselas al Project Manager o al Scrum Master antes de darlo por terminado._

## HU-02: Recuperación de Contraseña por Email

### RF-01: Solicitud de recuperación y envío de token por email (Funcional)

Opción 'Olvidé mi contraseña' en pantalla de login y servicio de generación/envío de token temporal al correo registrado.

**Condiciones de aprobación**

_Sin condiciones de aprobación cargadas: pedíselas al Project Manager o al Scrum Master antes de darlo por terminado._

### RF-02: Restablecimiento de contraseña con token (Funcional)

Formulario seguro para validar el token recibido y permitir ingresar y confirmar la nueva contraseña.

**Condiciones de aprobación**

_Sin condiciones de aprobación cargadas: pedíselas al Project Manager o al Scrum Master antes de darlo por terminado._

## HU-03: Gestión de Rutinas Personales (CRUD)

### RF-01: Listado de rutinas personales (Funcional)

Vista principal con el listado interactivo de las rutinas de entrenamiento creadas por el usuario.

**Condiciones de aprobación**

_Sin condiciones de aprobación cargadas: pedíselas al Project Manager o al Scrum Master antes de darlo por terminado._

### RF-02: Creación y edición de rutinas de entrenamiento (Funcional)

Formulario para dar de alta y editar rutinas especificando nombre, selección de ejercicios, series, repeticiones y cargas.

**Condiciones de aprobación**

_Sin condiciones de aprobación cargadas: pedíselas al Project Manager o al Scrum Master antes de darlo por terminado._

### RF-03: Eliminación de rutina con confirmación (Funcional)

Acción de borrado de una rutina personal con modal previo de confirmación para evitar pérdidas accidentales.

**Condiciones de aprobación**

_Sin condiciones de aprobación cargadas: pedíselas al Project Manager o al Scrum Master antes de darlo por terminado._

## RO-01: Dockerizar la app para el entorno de pruebas

### RF-01: Dockerizar la app para el entorno de pruebas (Funcional)

Crear el Dockerfile y configuración de docker-compose para empaquetar la aplicación y desplegarla en la VM existente de pruebas para QA.

**Condiciones de aprobación**

_Sin condiciones de aprobación cargadas: pedíselas al Project Manager o al Scrum Master antes de darlo por terminado._

## RO-02: Configurar servicio de correo SMTP

### RF-01: Configurar servicio de correo SMTP (Funcional)

Aprovisionamiento de credenciales SMTP y variables de entorno para habilitar el servicio de correo necesario para el token de recuperación de contraseña.

**Condiciones de aprobación**

_Sin condiciones de aprobación cargadas: pedíselas al Project Manager o al Scrum Master antes de darlo por terminado._

## RO-03: Configurar estilos base, modo oscuro y paleta institucional

### RF-01: Configurar estilos base, modo oscuro y paleta institucional (Funcional)

Configuración base de estilos CSS/tokens para soporte de modo oscuro y esquema cromático celeste y blanco institucional según style.md.

**Condiciones de aprobación**

_Sin condiciones de aprobación cargadas: pedíselas al Project Manager o al Scrum Master antes de darlo por terminado._
