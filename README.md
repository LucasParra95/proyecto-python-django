# WebApp de Reservas

Aplicación web desarrollada en Django para la gestión de servicios y clientes de la empresa.

## Requisitos

- Python 3.x
- Django

## Instalación local

1. Clonar el repositorio:
```bash
   git clone <url-del-repo>
   cd WebApp
```

2. Crear y activar el entorno virtual:
```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
```

3. Instalar dependencias:
```bash
   pip install django
```

4. Aplicar migraciones:
```bash
   python manage.py migrate
```

5. Levantar el servidor:
```bash
   python manage.py runserver
```

## Crear superusuario de prueba

Cada integrante debe crear su propio superusuario local para acceder al panel de administración (no se comparte ni se sube al repositorio):

1. Activar el entorno virtual (ver paso 2 de instalación).
2. Ejecutar:
```bash
   python manage.py createsuperuser
```
3. Completar usuario, email (opcional) y contraseña.
4. Ingresar al panel en: http://127.0.0.1:8000/admin/

## Estructura del proyecto

- `WebApp/` — configuración principal del proyecto Django.
- `servicios/` — app con los modelos, vistas y admin de Servicios y Clientes.