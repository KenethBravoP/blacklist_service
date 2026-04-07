# Entrega 1 - Microservicio de blacklist global

Microservicio REST en Flask para la gestion de lista negra global de emails.

## Endpoints

### POST /blacklists
Agrega un email a la blacklist.

Body JSON:
```json
{
  "email": "persona@example.com",
  "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
  "blocked_reason": "fraude"
}
```

### GET /blacklists/<email>
Consulta si un email esta en la blacklist.

### GET /health
Endpoint adicional para health checks en AWS Elastic Beanstalk.

## Autenticacion
Todos los endpoints funcionales usan bearer token estatico:

```text
Authorization: Bearer devops-static-token
```

En produccion configure el token en la variable de entorno `AUTH_TOKEN`.

## Variables de entorno

- `DATABASE_URL`: conexion a PostgreSQL o RDS.
- `AUTH_TOKEN`: token bearer estatico.
- `JWT_SECRET_KEY`: secreto de Flask JWT Extended.

## Ejecucion local

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows use .venv\Scripts\activate
pip install -r requirements.txt
export AUTH_TOKEN=devops-static-token
python application.py
```

## Pruebas

```bash
pytest -q
```

## Despliegue manual en Elastic Beanstalk

1. Cree la base de datos PostgreSQL en RDS y permita el acceso desde el security group del ambiente Beanstalk.
2. En Elastic Beanstalk cree una aplicacion Python Web Server Environment.
3. Configure las variables de entorno:
   - `DATABASE_URL`
   - `AUTH_TOKEN`
   - `JWT_SECRET_KEY`
4. Suba un ZIP con el contenido raiz del proyecto, incluyendo `application.py`, `requirements.txt`, `Procfile`, `.ebextensions` y la carpeta `app`.
5. Configure el health check path como `/health`.
6. Valide los endpoints con Postman usando la URL publica del ambiente.

## Respuestas sugeridas

### POST exitoso
```json
{
  "message": "Email added to blacklist",
  "data": {
    "email": "persona@example.com",
    "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
    "blocked_reason": "fraude",
    "request_ip": "127.0.0.1",
    "created_at": "2026-04-07T00:00:00Z"
  }
}
```

### GET si existe
```json
{
  "email": "persona@example.com",
  "is_blacklisted": true,
  "blocked_reason": "fraude"
}
```

### GET si no existe
```json
{
  "email": "persona@example.com",
  "is_blacklisted": false,
  "blocked_reason": null
}
```
