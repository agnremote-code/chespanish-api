# Chespanish API

Repositorio reservado para la API de Chespanish.

## Estado actual

Todavia no se definio el stack. Este repositorio arranca limpio para que la API se disene como una aplicacion separada de la landing y de la app mobile.

La documentacion tecnica que habia quedado mezclada en la landing fue movida aca como referencia:

- `docs/firebase-data-model.md`
- `docs/api-boundary.md`

## Responsabilidad

La API va a concentrar la logica compartida del producto:

- autenticacion y autorizacion del backend, si decidimos manejarla fuera del cliente
- acceso a base de datos
- endpoints para progreso, usuarios, lecciones y contenido
- integraciones externas

La app mobile y la landing deberian consumir esta API cuando el backend este definido.

## Proximo paso

Evaluar opciones de stack para backend, autenticacion, base de datos y despliegue.
