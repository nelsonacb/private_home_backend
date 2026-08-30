# 🏠 Casa Particular Backend

API REST para la gestión de alojamientos turísticos tipo "casa particular" en Cuba. Este backend está construido con Django y Django REST Framework, e incluye autenticación JWT, roles, permisos, filtros avanzados y documentación interactiva.

## ✨ Características

- 🔐 Autenticación con JWT (SimpleJWT) + refresh tokens y blacklist.
- 👥 Roles de usuario: Admin, Propietario (Owner), Personal (Staff) y Huésped (Guest).
- 🏘️ Gestión de propiedades y habitaciones.
- 📅 Reservas con estados y validaciones de fechas.
- 💵 Pagos en efectivo o transferencia.
- 🧹 Tareas para el personal (limpieza, mantenimiento, etc.).
- ⭐ Opiniones y calificaciones de huéspedes.
- 🔍 Filtros por múltiples campos con `django-filter`.
- 📚 Documentación automática con Swagger/OpenAPI (drf-spectacular).
- 🛡️ Manejo centralizado de errores.
- 📦 Estructura modular y escalable.

## 🛠️ Tecnologías

- Python 3.10+
- Django 5.0+
- Django REST Framework
- PostgreSQL
- SimpleJWT
- django-filter
- drf-spectacular
- django-cors-headers

## 📋 Requisitos previos

- Python 3.10 o superior
- PostgreSQL instalado y corriendo
- pip y virtualenv (opcional pero recomendado)

## 🚀 Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/nelsonacb/casa-particular-backend.git
   cd casa-particular-backend 

2. Crea y activa un entorno virtual:

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate

3. Instala las dependencias:

    ```bash
    pip install -r requirements.txt

4. Crea un archivo .env en la raíz (puedes copiar .env.example) y configura las variables:

    ```bash
    SECRET_KEY=tu-secret-key
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1
    DB_NAME=casa_particular_db
    DB_USER=postgres
    DB_PASSWORD=tu-password
    DB_HOST=localhost
    DB_PORT=5432

5. Crea la base de datos en PostgreSQL:

    ```bash
    CREATE DATABASE casa_particular_db;

6. Crea las migraciones:
    ```bash
    python manage.py makemigrations

7. Aplica las migraciones:
    ```bash
    python manage.py migrate

8. (Opcional) Crea un superusuario:
    ```bash
    python manage.py createsuperuser

9. (Opcional) Puebla la base de datos con datos de ejemplo:
    ```bash
    python manage.py seed_data

10. Ejecuta el servidor:
    ```bash
    python manage.py runserver

## 📚 Documentación de la API

Una vez que el servidor esté corriendo, puedes acceder a:

Swagger UI: http://127.0.0.1:8000/api/docs/

ReDoc: http://127.0.0.1:8000/api/redoc/

Esquema OpenAPI: http://127.0.0.1:8000/api/schema/

## 📂 Estructura del proyecto

private_home_backend/
├── apps/
│   ├── users/          # Usuarios, autenticación, perfiles
│   ├── properties/     # Propiedades y habitaciones
│   ├── bookings/       # Reservas
│   ├── payments/       # Pagos
│   ├── tasks/          # Tareas
│   ├── reviews/        # Opiniones
│   └── common/         # Utilidades y seeders
├── config/             # Configuración principal de Django
├── manage.py
├── requirements.txt
└── .env.example

## Hecho con ❤️ para la comunidad cubana de desarrollo.