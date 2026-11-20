# 02 - Validar

## Qué valida

Que la decisión mTLS sea reproducible: mismo `config` + mismo `cert` produce
siempre el mismo veredicto. Se valida sobre **metadatos declarados**, no sobre
TLS real.

## Herramientas

- `byotc_audit.py`: 8 tests, salida JSON con `config_sha256` y `certs_sha256`.
- `byotc_audit_zig`: misma lógica, salida tabular. Doble implementación.

```powershell
python -m unittest discover -v
python byotc_audit.py fixtures/byotc_config.json fixtures/byotc_certs.json
python byotc_audit.py fixtures/byotc_config.json fixtures/byotc_certs.json > r1.json
python byotc_audit.py fixtures/byotc_config.json fixtures/byotc_certs.json > r2.json
# r1 y r2 deben ser identicos (determinismo)
```

## Veredictos esperados sobre la fixture

| Certificado | Veredicto | Motivo |
|---|---|---|
| `cert-ca-lab-dns` | ACCEPTED | `san_dns_allowlisted` |
| `cert-ca-atacante` | REJECTED | `chain_rejected` |
| `cert-solo-ip` | REJECTED | `san_not_allowlisted` (el allowlist de la fixture no contiene la IP; si la contuviera, el código seguiría rechazándola: `san_ip_not_compared`) |
| `cert-dns-distinto` | REJECTED | `san_not_allowlisted` |

## Criterio de validez

- Los hashes son deterministas (JSON con `sort_keys`).
- Python y Zig coinciden en `aceptados` y en los motivos.
- Ningún test usa red, certificados reales ni claves.

## Estado: COMPLETO

Validado sobre metadatos sintéticos. Pendiente de validación con certificado
real en el estado 03.
