# BYOTC - Bring Your Own Trusted Certificate

Repositorio de **investigación** sobre la decisión de confianza mTLS del C2-DECT
y su medición auditable. BYOTC-SAN es el primer hallazgo: el allowlist de SAN
compara solo `DNSNames`, no `IPAddresses` ni `URIs`.

> Todo el contenido es análisis, protocolos y resultados verificables. No se
> incluye código que genere certificados maliciosos, abra conexiones TLS ni
> explote activos. Uso exclusivo en laboratorio aislado con RoE firmada.

## El ciclo de investigación

Cada hallazgo recorre siete estados. Cada estado tiene su carpeta en `states/`:

| # | Estado | Qué produce |
|---|---|---|
| 00 | `primitiva` | La operación de confianza que se estudia (decisión mTLS) |
| 01 | `explotar` | Banco de SANs frontera en busca de primitiva nueva (modelo: 0 hallazgos) |
| 02 | `validar` | Veredicto `ACCEPTED / REJECTED` con hash de config y cert |
| 03 | `efecto-emulado-real` | Cerrado: no explotable, falso negativo |
| 04 | `medicion` | TTD, bypass observado e IC95% |
| 05 | `auditoria` | Gates, hashes y gobernanza G1/G3/G8 |
| 06 | `publicacion` | Release de investigación con resultados reproduccibles |

## Estado actual del hallazgo BYOTC-SAN

| Estado | Estado de avance |
|---|---|
| 00 primitiva | Completo (análisis de `server/cmd/mtls.go`) |
| 01 explotar | Protocolo documentado, sin ejecutar |
| 02 validar | Completo sobre metadatos (8 tests Python + Zig) |
| 03 efecto emulado real | Cerrado: no explotable (análisis de código + fixtures) |
| 04 medicion | Metodología lista, sin datos reales |
| 05 auditoria | Completa (`artifacts.sha256`, gates) |
| 06 publicacion | `RELEASE.md` (research 1.0.0) |

## Herramientas

- `byotc_audit.py` y `byotc_audit_zig`: verifican la decisión mTLS sobre
  metadatos declarados. No generan certificados ni tocan TLS.
- `footprint_zig`: huella conductual determinista (idéntica a Python).
- `verify_manifest_zig`: integridad de todo el contenido.

```powershell
python -m unittest discover -v
zig build test
python byotc_audit.py fixtures/byotc_config.json fixtures/byotc_certs.json
```

## Relación con otros repos

Este repo es el compendio de BYOTC. El marco general vive en
`c2dect-investigacion` (`OFENSIVA/`), el plan de laboratorio en
`OFENSIVA/09-plan-ejecucion-lab.md`, y los prototipos de medición en
`c2dect-soc-validation`, `c2dect-hardening`, `c2dect-unicorn-fuzzing` y
`c2dect-telemetry-dataset`.
