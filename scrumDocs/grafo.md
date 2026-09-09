# Grafo de Dependencias -- FitArg

_Generado automaticamente el 2026-09-09T15:14:43.620Z -- no editar a mano, se sobreescribe en cada publicacion._

```mermaid
graph TD
  subgraph US_1788961186890["HU-01: Gestión de Usuarios (ABM de Perfil)"]
    REQ_1788962591125["RF-01: Registro de nuevos usuarios"]
    REQ_1788962599160["RF-02: Visualización y edición de perfil"]
    REQ_1788962657708["RF-03: Baja lógica de cuenta de usuario"]
  end
  subgraph US_1788961195716["HU-02: Recuperación de Contraseña por Email"]
    REQ_1788962657905["RF-01: Solicitud de recuperación y envío de token por email"]
    REQ_1788962658008["RF-02: Restablecimiento de contraseña con token"]
  end
  subgraph US_1788961200799["HU-03: Gestión de Rutinas Personales (CRUD)"]
    REQ_1788962658133["RF-01: Listado de rutinas personales"]
    REQ_1788962658244["RF-02: Creación y edición de rutinas de entrenamiento"]
    REQ_1788962658342["RF-03: Eliminación de rutina con confirmación"]
  end
  subgraph US_1788962846177["RO-01: Dockerizar la app para el entorno de pruebas"]
    REQ_1788962846188["RF-01: Dockerizar la app para el entorno de pruebas"]
  end
  subgraph US_1788962858890["RO-02: Configurar servicio de correo SMTP"]
    REQ_1788962858900["RF-01: Configurar servicio de correo SMTP"]
  end
  subgraph US_1788962859056["RO-03: Configurar estilos base, modo oscuro y paleta institucional"]
    REQ_1788962859059["RF-01: Configurar estilos base, modo oscuro y paleta institucional"]
  end
  REQ_1788962859059 --> REQ_1788962591125
  REQ_1788962591125 --> REQ_1788962599160
  REQ_1788962599160 --> REQ_1788962657708
  REQ_1788962591125 --> REQ_1788962657905
  REQ_1788962858900 --> REQ_1788962657905
  REQ_1788962657905 --> REQ_1788962658008
  REQ_1788962591125 --> REQ_1788962658133
  REQ_1788962658133 --> REQ_1788962658244
  REQ_1788962658133 --> REQ_1788962658342
```