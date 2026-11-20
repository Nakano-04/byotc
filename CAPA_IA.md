# Capa de IA aplicada a la telemetría mTLS

La capa de IA vive en el repositorio privado de C2-DECT
(`modules/mtls-trust-abuse/detection_record.py`), no aquí. Este documento
resume el contrato para que el resultado sea auditable desde la investigación.

## Modelo

`mtls-telemetry-score-v1`: scoring determinista y transparente, no un LLM
opaco. Cada feature tiene un peso declarado:

| Feature | Peso |
|---|---:|
| `foreign_ca` (CA del leaf fuera del bundle) | 0.35 |
| `san_ip_only` (SAN solo IP, allowlist no lo compara) | 0.20 |
| `allowlist_empty_lab_escape` (escape hatch activo) | 0.25 |
| `unusual_time` (hora fuera de 08-18) | 0.10 |
| `new_host` (host no visto en la línea base) | 0.10 |

Suma máxima = 1.0. Umbral `>= 0.5` => `priorizar`; si no, `observar`.

## DetectionRecord

Cada registro lleva `schema`, `rule_id`, `source`, `technique`, `verdict`,
`t0`, `config_sha256`, `cert_sha256`, eventos y `sha256` propio (G1). El
`sha256` se calcula sobre el registro canónico (JSON ordenado), por lo que es
byte-reproducible.

## Gobernanza de la IA

- Solo se aplica sobre evidencia real (`Outcome.executed`); nunca sobre el
  modelo `simulated`.
- **No cierra hallazgos** (G3): `priorizar` es una sugerencia al analista.
- Versión de modelo y pesos viajan en la salida: cualquier cambio es visible.
- Sin secretos ni certificados en la salida (G8).

## Verificación

17 tests en el repo privado: hash estable, canonización, features, umbral,
versión del modelo, y que el sobre incluya `DetectionRecord` + `IA` solo con
evidencia real.
