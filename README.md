# Grupo 5

Plataforma de reservas de servicios para eventos desarrollada con Python y Django. Permite registrar y administrar servicios, empleados, coordinadores y clientes, gestionar reservas y consultar la información mediante listados con búsqueda.

El proyecto fue desarrollado de manera grupal en el marco de **Alkemy**.

## Características principales

- Gestión de clientes.
- Gestión de servicios.
- Gestión de empleados.
- Gestión de coordinadores.
- Gestión de reservas.
- Búsqueda en los listados de las entidades.
- Baja lógica y restauración de clientes, servicios, empleados y coordinadores.
- Eliminación física de reservas.
- Selección de múltiples servicios dentro de una reserva.
- Control de disponibilidad de servicios por fecha.
- Cálculo del precio total de una reserva.
- Panel de administración de Django.
- API REST de solo consulta para servicios.
- Base de datos SQLite.
- Interfaz basada en Django Templates y Bootstrap.

## Tecnologías utilizadas

- **Python**
- **Django 6.1**
- **Django REST Framework 3.18.0**
- **django-bootstrap5 26.2**
- **django-bootstrap-datepicker-plus 6.0.0**
- **SQLite**
- **HTML/CSS/JavaScript** mediante templates y archivos estáticos de Django.

## Requisitos

Para ejecutar el proyecto localmente se necesita:

- Python 3.x
- Git
- Un entorno virtual de Python

Las dependencias exactas del proyecto se encuentran en `requirements.txt`.

## Instalación y ejecución

### 1. Clonar el proyecto

Clonar el repositorio y acceder a la carpeta del proyecto.

```bash
git clone <url-del-repo>
cd Grupo-5
```

> La URL del repositorio no se incluye en esta documentación. Reemplazar `<url-del-repo>` por la URL correspondiente al repositorio.

### 2. Crear el entorno virtual

Desde la carpeta raíz del proyecto:

```bash
python -m venv env
```

### 3. Activar el entorno virtual

En Windows:

```bash
env\Scripts\activate
```

En Linux/macOS:

```bash
source env/bin/activate
```

### 4. Instalar las dependencias

Con el entorno virtual activado:

```bash
pip install -r requirements.txt
```

### 5. Aplicar las migraciones

```bash
python manage.py migrate
```

### 6. Poblar la base de datos

El proyecto no incluye un script o fixture específico para cargar datos iniciales.

Los datos pueden cargarse manualmente de dos maneras:

- Desde la aplicación en funcionamiento, utilizando los formularios correspondientes.
- Desde la shell de Django mediante los modelos.

Para utilizar la shell:

```bash
python manage.py shell
```

Por ejemplo:

```python
from servicios.models import Cliente

Cliente.objects.create(
    nombre="Juan",
    apellido="Pérez",
    activo=True
)
```

La cantidad y el tipo de datos de prueba quedan a criterio del usuario.

### 7. Iniciar el servidor

```bash
python manage.py runserver
```

La aplicación quedará disponible normalmente en:

```text
http://127.0.0.1:8000/
```

## Panel de administración

Django proporciona un panel de administración accesible en:

```text
http://127.0.0.1:8000/admin/
```

Para crear un superusuario local:

```bash
python manage.py createsuperuser
```

Luego completar las credenciales solicitadas.

El usuario administrador es local para cada instalación y no debe compartirse ni incluirse en el repositorio.

## Estructura del proyecto

La estructura principal es:

```text
Grupo 5/
├── api/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── env/
│
├── servicios/
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── templatetags/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── WebApp/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── .gitignore
├── db.sqlite3
├── manage.py
├── README.md
└── requirements.txt
```

### Aplicaciones

#### `servicios`

Es la aplicación principal de gestión. Contiene los modelos, formularios, vistas, templates y archivos estáticos relacionados con clientes, servicios, empleados, coordinadores y reservas.

#### `api`

Contiene la API REST desarrollada con Django REST Framework. Actualmente proporciona endpoints de consulta para los servicios.

#### `WebApp`

Contiene la configuración principal del proyecto Django, incluyendo `settings.py`, `urls.py`, ASGI y WSGI.

## Modelos

El proyecto cuenta con cinco entidades principales.

### Cliente

Representa a los clientes que realizan reservas.

Campos:

- `nombre`
- `apellido`
- `activo`

Los clientes utilizan **baja lógica**. Cuando un cliente es dado de baja, permanece en la base de datos pero deja de considerarse activo. Puede ser restaurado posteriormente.

### Servicio

Representa los servicios que pueden contratarse para un evento.

Campos:

- `nombre`
- `descripcion`
- `precio`
- `activo`

Los servicios también utilizan **baja lógica** y pueden restaurarse posteriormente.

### Empleado

Representa a los empleados encargados de tomar reservas.

Campos:

- `nombre`
- `apellido`
- `numero_legajo`
- `activo`

El número de legajo es único.

Los empleados utilizan **baja lógica** y pueden restaurarse posteriormente.

### Coordinador

Representa al coordinador responsable de una reserva.

Campos:

- `nombre`
- `apellido`
- `numero_documento`
- `fecha_alta`
- `activo`

El número de documento es único.

Los coordinadores utilizan **baja lógica** y pueden restaurarse posteriormente.

### ReservaServicio

Representa una reserva realizada por un cliente.

Una reserva contiene:

- Un cliente.
- Uno o varios servicios.
- Un empleado encargado de tomar la reserva.
- Un coordinador responsable.
- Fecha y hora en que se realizó la reserva.
- Fecha en la que se realizará el servicio.

La relación entre reservas y servicios es **muchos a muchos**, por lo que una misma reserva puede incluir múltiples servicios.

Además, la reserva dispone de propiedades para:

- Obtener los nombres de los servicios contratados.
- Calcular el precio total acumulado de los servicios incluidos.

## Gestión de reservas

Las reservas solamente pueden realizarse utilizando registros activos:

- Cliente activo.
- Servicios activos.
- Empleado activo.
- Coordinador activo.

### Disponibilidad por fecha

La disponibilidad se controla individualmente por servicio.

Una fecha se considera **ocupada para un servicio determinado cuando ya existe una reserva que contiene ese servicio en esa fecha**.

La disponibilidad no depende de:

- Cliente.
- Empleado.
- Coordinador.
- Otros servicios incluidos en la reserva.

Por lo tanto, si un servicio ya está reservado para una fecha, ese mismo servicio no puede seleccionarse nuevamente para otra reserva en esa fecha.

### Eliminación de reservas

A diferencia de clientes, servicios, empleados y coordinadores, las reservas **no utilizan baja lógica**.

Cuando una reserva se elimina, se elimina físicamente de la base de datos.

## Búsqueda

Los listados de las entidades principales disponen de funcionalidad de búsqueda.

La búsqueda permite localizar registros según los campos configurados para cada listado.

## URLs de la aplicación

Las rutas de gestión web se encuentran dentro de la aplicación `servicios`, que se incluye en el proyecto principal mediante:

```python
path('servicios/', include("servicios.urls")),
```

Por lo tanto, las rutas disponibles son las siguientes.

### Inicio

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/servicios/` | Página principal de la aplicación |

### Clientes

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/servicios/clientes` | Listar clientes activos |
| GET/POST | `/servicios/clientes/nuevo` | Crear cliente |
| GET/POST | `/servicios/clientes/editar/<id>` | Editar cliente |
| GET/POST | `/servicios/clientes/baja/<id>` | Dar de baja un cliente |
| GET | `/servicios/clientes/inactivos` | Listar clientes inactivos |
| GET/POST | `/servicios/clientes/inactivos/restaurar/<id>` | Restaurar cliente |

### Servicios

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/servicios/servicios` | Listar servicios activos |
| GET/POST | `/servicios/servicios/nuevo` | Crear servicio |
| GET/POST | `/servicios/servicios/editar/<id>` | Editar servicio |
| GET/POST | `/servicios/servicios/baja/<id>` | Dar de baja un servicio |
| GET | `/servicios/servicios/inactivos` | Listar servicios inactivos |
| GET/POST | `/servicios/servicios/inactivos/restaurar/<id>` | Restaurar servicio |

### Empleados

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/servicios/empleados` | Listar empleados activos |
| GET/POST | `/servicios/empleados/nuevo` | Crear empleado |
| GET/POST | `/servicios/empleados/editar/<id>` | Editar empleado |
| GET/POST | `/servicios/empleados/baja/<id>` | Dar de baja un empleado |
| GET | `/servicios/empleados/inactivos` | Listar empleados inactivos |
| GET/POST | `/servicios/empleados/inactivos/restaurar/<id>` | Restaurar empleado |

### Coordinadores

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/servicios/coordinadores/` | Listar coordinadores activos |
| GET/POST | `/servicios/coordinadores/nuevo` | Crear coordinador |
| GET/POST | `/servicios/coordinadores/editar/<id>` | Editar coordinador |
| GET/POST | `/servicios/coordinadores/baja/<id>` | Dar de baja un coordinador |
| GET | `/servicios/coordinadores/inactivos` | Listar coordinadores inactivos |
| GET/POST | `/servicios/coordinadores/inactivos/restaurar/<id>` | Restaurar coordinador |

### Reservas

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/servicios/reservas` | Listar reservas |
| GET/POST | `/servicios/reservas/nueva` | Crear reserva |
| GET/POST | `/servicios/reservas/editar/<id>` | Editar reserva |
| GET/POST | `/servicios/reservas/eliminar/<id>` | Eliminar reserva |

> `<id>` representa el identificador entero (`pk`) del registro.

## API REST

La API se encuentra desarrollada utilizando **Django REST Framework** y está incluida en el proyecto mediante:

```python
path('api/', include("api.urls")),
```

Actualmente la API es **de solo consulta** y cuenta con dos endpoints.

### Listar servicios

```http
GET /api/servicios
```

Devuelve todos los servicios almacenados en la base de datos, incluyendo tanto los servicios activos como los inactivos.

La respuesta incluye **todos los campos del modelo `Servicio`**.

Ejemplo:

```json
[
    {
        "id": 1,
        "nombre": "Catering",
        "descripcion": "Servicio de catering para eventos",
        "precio": 50000,
        "activo": true
    }
]
```

### Obtener un servicio por ID

```http
GET /api/servicios/<id>
```

Devuelve la información de un único servicio utilizando su identificador.

Ejemplo:

```http
GET /api/servicios/1
```

Respuesta:

```json
{
    "id": 1,
    "nombre": "Catering",
    "descripcion": "Servicio de catering para eventos",
    "precio": 50000,
    "activo": true
}
```

Si no existe un servicio con el ID solicitado, Django REST Framework devuelve una respuesta **404 Not Found**.

### Características de la API

- Método `GET`.
- Solo lectura.
- No requiere autenticación.
- Incluye servicios activos e inactivos.
- Devuelve todos los campos de `Servicio`.
- Permite consultar un servicio individual mediante su ID.

## Rutas principales del proyecto

El archivo `WebApp/urls.py` incluye las siguientes rutas:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('servicios/', include("servicios.urls")),
    path('api/', include("api.urls")),
]
```

Esto separa la aplicación web tradicional de la API REST:

```text
/servicios/    → Interfaz web de gestión
/api/          → API REST
/admin/        → Panel de administración de Django
```

## Notas

- La base de datos utilizada durante el desarrollo es SQLite.
- No se requiere un sistema de autenticación para utilizar la aplicación.
- El entorno virtual `env/` debe mantenerse fuera del control de versiones.
- La base de datos puede contener datos locales de desarrollo y prueba.
- Para una instalación nueva es necesario ejecutar las migraciones y cargar manualmente los datos que se necesiten.
