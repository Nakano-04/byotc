# 00 - Primitiva

## La operación de confianza

La primitiva es la **decisión de aceptar un certificado de cliente** en el
canal mTLS del C2. No es un ataque: es una operación de confianza que el
servidor realiza en cada check-in.

Fuente real: `server/cmd/mtls.go`, `verifyMTLSLeaf()` y `buildServerTLSConfig()`.

## Entradas de la decisión

| Entrada | Qué es |
|---|---|
| `rawCerts[0]` | leaf presentado por el agente |
| `pool` | bundle de CAs raíz de confianza (`caPath`) |
| `Intermediates` | CAs intermedias del propio certificado |
| `allow` | allowlist de SAN (`C2_MTLS_ALLOW`, coma-separada) |
| `flags` | `C2_ALLOW_NO_MTLS_ALLOWLIST`, `C2_ALLOW_NO_MTLS` |

## Operación

```
1. parsear leaf y construir pool de intermedios
2. leaf.Verify(Roots=pool, Intermediates, ExtKeyUsageClientAuth)
3. si allow vacío: fail-closed salvo flag de laboratorio
4. si allow no vacío: aceptar si leaf.DNSNames ∩ allow != ∅
```

## Lo que NO es la primitiva

- No es generación de certificados.
- No es una conexión TLS.
- No es explotación de `crypto/x509`.

## Salida

Un veredicto `ACCEPTED / REJECTED` con motivo. Esta salida es la que consume el
estado 02 (validación).

## Estado: COMPLETO

Analizada sobre código real. Sin datos de ejecución aún.
