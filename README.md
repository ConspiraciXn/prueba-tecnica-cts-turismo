# Prueba Técnica - CTS Turismo
Prueba técnica de desarrollo, CTS Turismo.

## Instrucciones - Backend
1. Cambiar directorio a `backend` con el comando `cd backend`.
2. Crear entorno virtual con el comando `python -m venv .venv`.
3. Activar entorno virtual con el comando `source .venv/bin/activate`.
4. Instalar dependencias con el comando `pip install -r requirements.txt`.
5. Ejecutar migraciones iniciales de base de datos con el comando `python manage.py migrate`.
6. Levantar Redis:
   - Opción A (sin Docker): instala Redis local (`brew install redis` en macOS, `sudo apt install redis-server` en Ubuntu) y ejecútalo con `redis-server`.
   - Opción B (con Docker): `docker compose up redis -d` desde la raíz del proyecto.
7. Ajustar el `.env` con `REDIS_URL` (por defecto `redis://localhost:6379/0`). Para pruebas sin Redis puedes definir `CELERY_TASK_ALWAYS_EAGER=True`.
8. Iniciar el worker de Celery con `celery -A proyecto_sorteo worker -l info`.
9. Levantar servidor de desarrollo con el comando `python manage.py runserver`.

# Test automatizados
- Ejecutar `python manage.py test` para correr la suite de pruebas de los flujos principales.

## Instrucciones - Frontend
1. Cambiar directorio a `frontend` con el comando `cd frontend`.
2. Instalar dependencias con el comando `npm install`.
3. Levantar servidor de desarrollo con el comando `npm run dev`.

## Decisiones técnicas tomadas
- Estructura de API: utilicé los serializers ya que son la forma predeterminada de trabajar con DRF, pero en lo personal prefiero trabajar sin ellos usando api_view y definiendo el cuerpo completo de la operación, permitiendo un control total de cada endpoint (aunque sea más trabajo). También definí respuestas de éxito y de error para mantener una estructura consistente de respuestas a lo largo de la API.
- Base de datos: Mantuve la BD original SQLite para agilizar el desarrollo, pero también se podría cambiar rapidamente por una PostgreSQL u otro motor.
- Envío de emails: Las notificaciones (verificación y ganador) se orquestan vía Celery + Redis usando la API de Mailgun. Para pruebas sin Redis puedes definir `CELERY_TASK_ALWAYS_EAGER=True` en tu `.env` y se ejecutarán de forma síncrona.
- API de VUE: En el frontend prefiero el uso de Options API, por eso la mayoría de vistas y componentes la utilizan, pero incluí un ejemplo con Composition API (Register.vue) para mostrar cómo se puede implementar de esa manera también.


## Variables de entorno relevantes

| Variable | Descripción | Valor por defecto |
| --- | --- | --- |
| `DEBUG` | Activa modo debug de Django | `True` |
| `FRONTEND_BASE_URL` | URL usada en enlaces enviados al usuario | `http://localhost:5173` |
| `MAILGUN_API_BASE_URL` | Endpoint de la API de Mailgun | `https://api.mailgun.net/v3` |
| `MAILGUN_DOMAIN` | Dominio configurado en Mailgun | — |
| `MAILGUN_API_KEY` | API key de Mailgun | — |
| `MAILGUN_SENDER` | Remitente utilizado en los correos | — |
| `REDIS_URL` | Broker/result backend para Celery | `redis://localhost:6379/0` |
| `CELERY_TASK_ALWAYS_EAGER` | Ejecutar tareas en modo síncrono (útil sin Redis) | `False` |


## Endpoints principales

### Público
- `POST /api/participants/register/`
  - Registra un participante.
  - Ejemplo de body:
    ```json
    {
      "first_name": "Ana",
      "last_name": "Pérez",
      "email": "ana@example.com",
      "rut": "12.345.678-9",
      "phone": "+56 9 1234 5678",
      "address": "Av. Siempre Viva 742"
    }
    ```
- `POST /api/participants/verify-email/validate/`
  - Valida el `uid` y `token` recibidos en el correo antes de permitir el ingreso de la contraseña.
- `POST /api/participants/verify-email/`
  - Crea la contraseña y activa la cuenta.
  - Body ejemplo:
    ```json
    {
      "uid": "Mg",
      "token": "6k7-c2c6d4a0e6fbd98d5f8a",
      "password": "MiClaveSegura1",
      "confirm_password": "MiClaveSegura1"
    }
    ```

### Administración (requiere header `Authorization: Token <token>`)
- `POST /api/admin/login/`
  - Devuelve `token`, `id`, `email`, `first_name`, `last_name` del administrador.
  - Body ejemplo:
    ```json
    {
      "email": "admin@example.com",
      "password": "********"
    }
    ```
- `GET /api/admin/participants/?search=&verified=`
  - Lista participantes, admitiendo filtros opcionales `search` (nombre, apellido, correo, RUT) y `verified=true|false`.
  - Respuesta parcial:
    ```json
    {
      "status": "success",
      "data": {
        "results": [{
          "id": 8,
          "first_name": "Ana",
          "last_name": "Pérez",
          "email": "ana@example.com",
          "rut": "12.345.678-9",
          "verified": true,
          "registered_at": "2025-02-05T13:10:23.812345"
        }],
        "count": 1
      }
    }
    ```
- `POST /api/admin/draw-winner/`
  - Selecciona aleatoriamente un ganador verificado y dispara el correo de notificación.
  - Respuesta ejemplo:
    ```json
    {
      "status": "success",
      "message": "Ganador seleccionado correctamente.",
      "data": {
        "id": 8,
        "first_name": "Ana",
        "last_name": "Pérez",
        "email": "ana@example.com",
        "rut": "12.345.678-9",
        "email_sent": true
      }
    }
    ```
