# 06 - Publicación

## Release de investigación 1.0.0

Ver `RELEASE.md` en la raíz del repo.

## Qué se publica

- El hallazgo (`KNOWLEDGE.md`, `states/00`, `states/02`).
- Las herramientas de verificación (Python + Zig).
- Las fixtures sintéticas y sus hashes.
- El protocolo de laboratorio (`states/01`, `states/03`).

## Qué NO se publica

- Certificados con claves privadas.
- Configuraciones reales de un C2 de producción.
- Código que genere certificados o abra conexiones TLS.
- Datos de laboratorio antes de ejecutarlos bajo RoE (estado 03 pendiente).

## Formato de cita

> BYOTC-SAN: Bring Your Own Trusted Certificate via SAN allowlist mismatch.
> Research release 1.0.0, Nakano-04/byotc, 2026-11-20.

## Estado: PUBLICADO

Contenido disponible en `https://github.com/Nakano-04/byotc`.
