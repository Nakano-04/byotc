# 03 - Efecto emulado real

## Qué se registra aquí

El efecto observado en laboratorio cuando se ejecuta el escenario E3: el
servidor rechaza un certificado con SAN IP aunque la allowlist contenga esa IP.
El efecto es **emulado** porque ocurre en un C2 de laboratorio, y **real**
porque la decisión la toma el código auténtico de Go.

## Formato del registro

```json
{
  "escenario": "E3",
  "t0": 12.34,
  "config_sha256": "...",
  "cert_sha256": "...",
  "verdict": "REJECTED",
  "reason": "san_ip_not_compared",
  "sensor": "c2-mtls-log",
  "roe_sha256": "..."
}
```

## Requisitos

- VM aislada con snapshot limpio.
- RoE firmada vigente.
- Sin claves ni certificados publicados.
- Hash de la config y del certificado, nunca su contenido.

## Criterio de cierre (G1/G3)

- G1: el registro lleva `RuleID` y `Source`.
- G3: el hallazgo no se cierra automáticamente; cierre = retest con evidencia.
- G8: hashes sanitizados.

## Estado: PENDIENTE

No se ha ejecutado. El protocolo está en `01-explotar.md` y el plan de
laboratorio en `c2dect-investigacion/OFENSIVA/09-plan-ejecucion-lab.md`.

> No rellenar este estado con datos sintéticos. Si no se ejecuta, se marca
> `no-ejecutada`.
