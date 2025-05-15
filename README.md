# 🗓️ Administrador de Eventos

Este es un proyecto de aplicación web desarrollado en Flask para la administración de eventos. Permite a los usuarios autenticarse, crear, editar, visualizar y eliminar eventos, según su rol en el sistema (Administrador, Organizador o Participante).

## 🚀 Tecnologías utilizadas

- Python 3.x
- Flask
- Flask-Login
- Flask-WTF
- Flask-SQLAlchemy
- PyMySQL (para MySQL/MariaDB)
- Bootstrap 5 (en las plantillas)
- REST Client (para pruebas con archivos `.rest`)

## 📁 Estructura del Proyecto

📦 final_project/
├── run.py
├── config.py
├── requirements.txt
├── create_demo_users.py
├── README.md
├── proyecto.pdf
│
├── pruebas/
│ ├── create.rest
│ ├── read.rest
│ ├── read-a-row.rest
│ ├── update.rest
│ └── delete.rest
│
├── app/
│ ├── init.py
│ ├── models.py
│ ├── forms.py
│ ├── routes.py
│ ├── test_routes.py
│ ├── auth_routes.py
│ │
│ ├── templates/
│ │ ├── layout.html
│ │ ├── index.html
│ │ ├── login.html
│ │ ├── register.html
│ │ ├── dashboard.html
│ │ ├── evento_form.html
│ │ ├── eventos.html
│ │ ├── usuarios.html
│ │ └── cambiar_password.html
│ │
│ └── static/
│ └── css/
│ └── styles.css (opcional)


## 👥 Roles de usuario

- **Administrador**: puede ver, editar y eliminar cualquier evento; gestionar usuarios.
- **Organizador**: puede crear y gestionar sus propios eventos.
- **Participante**: puede visualizar eventos, sin permisos de edición ni creación.

## 📌 Funcionalidades principales

- Registro e inicio de sesión con selección de rol
- Panel de control personalizado según rol
- CRUD completo de eventos
- Validaciones de formularios con Flask-WTF
- Pruebas REST con archivos `.rest`
- Protección CSRF en formularios
- Gestión de usuarios (solo para Admin)

## 🔧 Instalación y uso

1. Clonar el repositorio:

```bash
git clone https://github.com/DJWolfboi/Final-Project.git
cd Final-Project
```

2. Crear y activar un entorno virtual (opcional pero recomendado):

   ```bash
   python -m venv venv
   venv\Scripts\activate  # En Windows
   ```

3. Instalar las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4.Configura tu base de datos en config.py.

5.Crea la base de datos en MYSQL:
```
mysql -u root -p < database_schema/04_eventos.sql
```

6. Crear usuarios de prueba
   ```
   python create_demo_users.py
   ```

7. Ejecutar la aplicación
   ```
   python run.py
   ```
   Luego abre en tu navegador:
   ```
   http://127.0.0.1:5000
   ```

🔒 Seguridad
Todas las rutas sensibles requieren autenticación.

Se valida el rol para restringir acceso a funciones según el tipo de usuario.

Protección CSRF en todos los formularios (excepto durante pruebas REST).

📚 Licencia
Este proyecto es de uso académico bajo supervisión del profesor Javier A. Dastas (Ciencias de Computadoras - UPR Arecibo).
