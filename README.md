Marketplace Digital de Servicios Generales

Proyecto de título desarrollado en Python (Django) como parte del programa de Analista Programador.
El sistema permite la publicación, búsqueda y contratación de servicios locales (gasfitería, limpieza, electricidad, etc.) a través de una plataforma colaborativa.

Características principales

Registro e inicio de sesión de usuarios.

Publicación de servicios con categoría, descripción y contacto.

Filtrado por categorías y búsqueda por texto.

Sistema de solicitudes (contactar proveedor).

Panel administrativo para gestión de usuarios, categorías y servicios.

Estructura escalable, adaptable a entornos productivos.

Tecnologías utilizadas

Python 3.12

Django 5.2.7

Bootstrap 5

SQLite3 (base de datos local)

HTML / CSS / JS

python-dotenv (manejo de variables de entorno)

Instalación y configuración

1 Clonar el repositorio
git clone https://github.com/tu-usuario/marketplace_digi.git
cd marketplace_digi


(Reemplaza la URL por la de tu repositorio real.)

2 Crear y activar el entorno virtual
En Windows
python -m venv .venv
.venv\Scripts\activate

En Linux / Mac
python3 -m venv .venv
source .venv/bin/activate

3 Instalar dependencias
pip install -r requirements.txt


Si no tienes un requirements.txt aún, puedes generarlo con:

pip freeze > requirements.txt

4 Crear el archivo .env

En la raíz del proyecto (/marketplace_digi), crea un archivo llamado .env con este contenido:

DJANGO_SECRET_KEY=tu_clave_aqui
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

5 Aplicar migraciones y crear superusuario
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

6 Ejecutar el servidor local
python manage.py runserver


Luego abre en tu navegador:

http://127.0.0.1:8000/

Estructura del proyecto
marketplace_digi/
│
├── marketplace/         # Configuración principal del proyecto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── services/            # App principal (modelos, vistas, formularios)
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── templates/
│   │   └── services/
│   └── admin.py
│
├── templates/           # Templates globales (base, login, registro)
├── static/              # Archivos estáticos
├── db.sqlite3           # Base de datos local (no incluida en repo)
├── .env                 # Variables de entorno (ignorado por git)
├── .gitignore
├── manage.py
└── README.md

Comandos útiles

Crear datos de prueba (opcional):

python manage.py seed_marketplace --users 5 --services 20


Reiniciar base de datos:

rm db.sqlite3
python manage.py migrate

Créditos y autoría

Autor: Michel Valenzuela
Carrera: Analista Programador
Institución: CFT Cenco
Año: 2025

Licencia

Este proyecto se distribuye con fines académicos y educativos.
Puedes usarlo y modificarlo libremente citando la fuente original.