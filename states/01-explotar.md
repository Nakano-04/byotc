# 01 - Explotar (banco de SANs frontera)

Este estado describe el experimento para buscar una **primitiva nueva**: que la
normalización de un SAN permita una coincidencia que el operador no pretendió.

## Qué se busca

`verifyMTLSLeaf` hace `strings.ToLower(dns)` y compara exacto contra el
allowlist. La hipótesis H-BYOTC-1: algún nombre SAN "frontera" (trailing dot,
punycode, wildcard, NUL embebido) que el operador consideraría equivalente a
`edge.lab.local` es **aceptado** por el código aunque no debería.

Resultado del modelo (`san_probe.py` / `san_probe_zig`, 8 casos):

| ID | SAN | Veredicto | Frontera |
|---|---|---|---|
| F1 | `edge.lab.local` | ACCEPTED | no (baseline) |
| F2 | `EDGE.LAB.LOCAL` | ACCEPTED | no |
| F3 | `edge.lab.local.` | REJECTED | sí |
| F4 | `xn--edge.lab.local` | REJECTED | sí |
| F5 | `*.lab.local` | REJECTED | sí |
| F6 | `edge.lab.local.evil.com` | REJECTED | sí |
| F7 | `edge.lab.local\0.evil.com` | REJECTED | sí |
| F8 | `""` | REJECTED | sí |

**Conclusión del modelo:** la normalización es segura. Solo coinciden el
baseline y el case-folding, que es intencionado. No hay colisión por trailing
dot, punycode, wildcard ni NUL. Es un hallazgo negativo (0 primitivas nuevas).

## Ejecución real (pendiente)

El modelo usa `strings.ToLower` de Python/Zig. Go puede normalizar distinto en
casos IDN. Para validar H-BYOTC-1 hace falta ejecutar contra el C2 real:

1. VM aislada, snapshot limpio, RoE firmada (`tools/gate/make_lab_roe.py`).
2. Generar 8 certificados de prueba con esos SANs (clave efímera, solo lab).
3. Presentarlos al C2 y registrar el veredicto real de `verifyMTLSLeaf`.
4. Comparar con el modelo; cualquier divergencia es un hallazgo nuevo.

## Gobernanza (aplicada al ejecutar)

- RoE firmada vigente, `scope=engagement`.
- `allow_impact_modules=true` por tenant.
- Killswitch, kill-date, techo de tiempo, escala.
- `DetectionRecord` con `RuleID` y `Source` (G1).
- Sin cierre automático; cierre = retest (G3).
- Hashes sanitizados, sin claves publicadas (G8).

## Estado: MODELO COMPLETO, EJECUCIÓN REAL PENDIENTE

No publicar certificados ni claves. Solo veredictos y hashes.
