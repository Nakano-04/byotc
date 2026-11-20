# 05 - Auditoría

## Gates

| Gate | Qué comprueba | Estado |
|---|---|---|
| A1 | Todo veredicto lleva `config_sha256` | PASS |
| A2 | Todo veredicto lleva `certs_sha256` | PASS |
| A3 | Python y Zig coinciden | PASS |
| A4 | Sin claves ni certificados en el repo | PASS |
| A5 | `artifacts.sha256` cubre todo el contenido | PASS |
| A6 | Cero em-dashes | PASS |

## Gobernanza

- **G1**: `DetectionRecord` con `RuleID` y `Source` para todo TTP ejecutado.
- **G3**: sin cierre automático; cierre = retest con evidencia.
- **G8**: rutas y hashes sanitizados, sin secretos.

## Verificación de integridad

```powershell
python verify_manifest.py generate
python verify_manifest.py
.\zig-out\bin\verify_manifest_zig.exe artifacts.sha256
```

## Estado: COMPLETO

Los gates A1-A6 pasan sobre el contenido del repo. La auditoría del estado 03
(ejecución real) queda condicionada a que ese estado deje de estar pendiente.
