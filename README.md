# Blacklist Microservice

Microservicio robusto para la gestión de listas negras de emails, diseñado para ser escalable, seguro y fácil de desplegar.

## 🏗️ Estructura del Proyecto
```text
.
├── app/                    # Lógica principal del microservicio
│   ├── __init__.py         # Configuración de Flask y extensiones (Factory Pattern)
│   ├── config.py           # Gestión de variables de entorno y constantes
│   ├── models.py           # Definición de tablas con SQLAlchemy
│   ├── schemas.py          # Validación y serialización con Marshmallow
│   └── resources.py        # Definición de Endpoints (Flask-RESTful)
├── migrations/             # Historial de versiones de la base de datos (Alembic)
├── .env                    # Variables sensibles (No subir al repo)
├── application.py          # Punto de entrada para el servidor (WSGI)
├── docker-compose.yml      # Orquestación de la base de datos PostgreSQL
├── gen_token.py            # Utility script para generación de JWT estáticos
└── requirements.txt        # Dependencias del proyecto
```

## 🚀 Requisitos Previos
- **Python 3.14+** (Probado en CachyOS/Arch Linux)
- **Docker & Docker Compose**
- **Postman** o **cURL**

## 🛠️ Configuración Local

1. **Clonar y preparar entorno:**
   ```bash
   git clone https://github.com/DevOps-Misw4304-202610/Proyecto1.git
   cd Proyecto1
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Levantar Base de Datos (Docker):**
   Asegúrate de no tener un Postgres nativo ocupando el puerto 5432.
   ```bash
   docker compose up -d
   ```

3. **Configurar Variables de Entorno:**
   Crea un archivo `.env` en la raíz con lo siguiente:
   ```env
   DATABASE_URL=postgresql+psycopg://user_blacklist:password123@localhost:5432/blacklist_db
   JWT_SECRET_KEY=clave-secreta-uniandes-2026
   ```

4. **Sincronizar Base de Datos:**
   Usamos **Flask-Migrate** para asegurar que todos tengamos la misma estructura.
   ```bash
   export FLASK_APP=application.py
   flask db upgrade
   ```

5. **Generar Token de Acceso:**
   Para consumir los endpoints protegidos, genera tu token JWT:
   ```bash
   python gen_token.py
   ```

## 🏃 Ejecución
```bash
python application.py
```
El servicio correrá en `http://localhost:5000`.

## 🧪 Pruebas y Verificación

### 1. Verificar Salud (Público)
```bash
curl -X GET http://localhost:5000/health
```

### 2. Agregar a Blacklist (Protegido)
Sustituye `<TOKEN>` por el string generado en el paso 5.
```bash
curl -X POST http://localhost:5000/blacklists \
     -H "Authorization: Bearer <TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{
           "email": "estudiante@uniandes.edu.co",
           "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
           "blocked_reason": "Prueba de integración"
         }'
```

### 3. Verificar en Base de Datos (Docker Exec)
Para confirmar que el dato persiste en el contenedor:
```bash
docker exec -it proyecto1-db-1 psql -U user_blacklist -d blacklist_db -x -c "SELECT * FROM blacklist ORDER BY \"createdAt\" DESC LIMIT 1;"
```

## 🛠️ Guía de Desarrollo para el Equipo

Si necesitas agregar una nueva funcionalidad o endpoint, sigue este flujo para mantener la consistencia:

1. **Modelos:** Si necesitas una nueva tabla, defínela en `app/models.py`.
2. **Migraciones:** Después de cambiar un modelo, genera la migración:
   ```bash
   flask db migrate -m "Descripción del cambio"
   flask db upgrade
   ```
   *¡No olvides hacer commit de la carpeta `migrations/`!*
3. **Schemas:** Define la validación en `app/schemas.py` usando Marshmallow.
4. **Recursos:** Crea la lógica del endpoint en `app/resources.py`.
5. **Rutas:** Registra el nuevo recurso en `app/__init__.py` usando `api.add_resource()`.

---

### Notas de Seguridad
- El archivo `.env` está en el `.gitignore`. Nunca subas credenciales reales al repositorio.
- Para producción (AWS Beanstalk), las variables de entorno se configuran desde la consola de AWS, no desde el archivo `.env`.
  