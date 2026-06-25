# Chespanish API

Repositorio reservado para la API de Chespanish.

## Stack

- FastAPI
- Python
- Supabase Postgres
- Pydantic
- SQLAlchemy o SQLModel
- Alembic
- Pytest

Este repositorio arranca limpio para que la API se disene como una aplicacion separada de la landing y de la app mobile.

La documentacion tecnica que habia quedado mezclada en la landing fue movida aca como referencia:

- `docs/firebase-data-model.md`
- `docs/api-boundary.md`
- `docs/architecture.md`
- `docs/project-architecture.md`
- `docs/testing-notes.md`
- `docs/auth-data-model.md`

## Responsabilidad

La API va a concentrar la logica compartida del producto:

- autenticacion y autorizacion del backend, si decidimos manejarla fuera del cliente
- acceso a base de datos
- endpoints para progreso, usuarios, lecciones y contenido
- integraciones externas

La app mobile y la landing deberian consumir esta API cuando el backend este definido.

## Proximo paso

El scaffold inicial de FastAPI ya esta creado con:

- estructura base de carpetas
- endpoint `GET /health`
- configuracion de entorno
- CORS local para landing y mobile
- tests con Pytest
- preparacion para conectar Supabase Postgres

## Desarrollo local

Crear y activar un entorno virtual:

```bash
py -m venv .venv
.venv\Scripts\activate
```

Instalar dependencias:

```bash
py -m pip install -e ".[dev]"
```

Copiar variables de entorno:

```bash
copy .env.example .env
```

Ejecutar la API:

```bash
py -m uvicorn app.main:app --reload
```

Probar el health check:

```text
GET http://localhost:8000/health
```

Ejecutar tests:

```bash
py -m pytest
```

Notas de testing y warnings conocidos:

```text
docs/testing-notes.md
```

## Siguiente hito

Crear el proyecto en Supabase y aplicar la migracion inicial:

```text
supabase/migrations/20260625211500_create_profiles.sql
```

Despues implementar el primer flujo de registro/login con Supabase Auth y perfiles.
