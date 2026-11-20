# 04 - Medición

## Métricas

| Métrica | Definición | Estado |
|---|---|---|
| `bypass_observado` | 1 - recall del sensor para la técnica | Metodología lista |
| `ttd` | `t_alerta - t0` | Sin datos |
| `ttc` | `t_contencion - t0` | Sin datos |
| `aceptados / total` | Tasa de aceptación de la decisión | 1/4 sobre fixture sintética |

## Protocolo

1. Ejecutar N veces (objetivo `n=10`), registrando `t0` real.
2. Correr `byotc_audit` sobre cada repetición.
3. Bootstrap con semilla fija para IC95%.
4. Publicar `n`, semilla e IC95% junto al resultado.

## Regla de honestidad

Un bypass con `n=1` es una anécdota, no evidencia. Todo resultado lleva su
intervalo de confianza y su muestra.

## Herramientas relacionadas

- `footprint_zig`: huella conductual determinista (idéntica a Python).
- `byotc_audit_zig`: veredicto y motivo por certificado.

## Estado: METODOLOGÍA LISTA, SIN DATOS REALES

La única medición publicada hoy es la de la fixture sintética (1/4).
