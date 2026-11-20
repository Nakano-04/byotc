# 01 - Explotar (protocolo experimental, no capacidad)

Este estado describe **cómo se dispara la condición** en laboratorio. No
entrega código de explotación. Todo lo aquí descrito requiere VM aislada,
RoE firmada y activos propios.

## Condición a disparar

Que el servidor tome una decisión de aceptación sobre un certificado cuyo
controlador es el laboratorio, y registrar el resultado.

## Tres escenarios experimentales

| Escenario | Configuración | Qué se observa |
|---|---|---|
| E1 | CA propia añadida al bundle | El leaf se acepta: la confianza viene de la config |
| E2 | allowlist vacío + `C2_ALLOW_NO_MTLS_ALLOWLIST=1` | Escape hatch de laboratorio |
| E3 | allowlist con IP, cert con SAN IP | Discrepancia DNS vs IP (el hallazgo) |

E1 y E2 son **configuración**, ya documentada: no son novedad. E3 es el
hallazgo de implementación.

## Reglas del experimento

1. La RoE se genera con `tools/gate/make_lab_roe.py` (semilla pública de test).
2. Se registra `t0` real y la config exacta (hash).
3. No se publica el certificado de prueba ni la clave privada.
4. Se publica solo el `verdict` y los hashes sanitizados (G8).

## Qué NO se hace aquí

- No se genera un certificado con clave ajena.
- No se suplanta a un tercero.
- No se conecta a un C2 real.

## Estado: PROTOCOLO DOCUMENTADO, SIN EJECUTAR

Requiere el laboratorio del plan 09 (`c2dect-investigacion`).
