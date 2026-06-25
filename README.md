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

## Responsabilidad

La API va a concentrar la logica compartida del producto:

- autenticacion y autorizacion del backend, si decidimos manejarla fuera del cliente
- acceso a base de datos
- endpoints para progreso, usuarios, lecciones y contenido
- integraciones externas

La app mobile y la landing deberian consumir esta API cuando el backend este definido.

## Proximo paso

Scaffold inicial de FastAPI:

- estructura base de carpetas
- endpoint `GET /health`
- configuracion de entorno
- CORS local para landing y mobile
- tests con Pytest
- preparacion para conectar Supabase Postgres
