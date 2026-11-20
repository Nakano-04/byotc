# Resultado de verificación - SAN frontera contra Go real

## Qué se ejecutó

`TestSANFronteraBYOTC` en `server/cmd/mtls_test.go` del repositorio C2-DECT.
Usa `newTestPKI` para emitir 8 certificados **en memoria** (sin disco, sin red,
sin publicar claves) y los pasa por `verifyMTLSLeaf` real, que usa
`crypto/x509` de Go `1.25.x`.

Comando:
```
cd server && go test ./cmd -run TestSANFronteraBYOTC -v -count=1
```

Resultado: **PASS**, los 8 veredictos coinciden con el modelo.

## Tabla de veredicto (tres implementaciones)

| ID | SAN | Python (modelo) | Zig (modelo) | Go (real) |
|---|---|---|---|---|
| F1 | `edge.lab.local` | ACCEPTED | ACCEPTED | ACCEPTED |
| F2 | `EDGE.LAB.LOCAL` | ACCEPTED | ACCEPTED | ACCEPTED |
| F3 | `edge.lab.local.` | REJECTED | REJECTED | REJECTED |
| F4 | `xn--edge.lab.local` | REJECTED | REJECTED | REJECTED |
| F5 | `*.lab.local` | REJECTED | REJECTED | REJECTED |
| F6 | `edge.lab.local.evil.com` | REJECTED | REJECTED | REJECTED |
| F7 | `edge.lab.local\0.evil.com` | REJECTED | REJECTED | REJECTED |
| F8 | `""` | REJECTED | REJECTED | REJECTED |

## Conclusión

**No hay primitiva nueva.** La normalización de Go coincide con el modelo:
solo `F1` y `F2` (case-folding intencionado por `strings.ToLower`) son
aceptados. Trailing dot, punycode, wildcard, sufijo y NUL se rechazan.

Esto cierra H-BYOTC-1 como **refutada con evidencia real**. El hallazgo BYOTC
sigue siendo: el allowlist compara solo DNS, no IP/URI (falso negativo de
documentación), y el control es fail-closed. No es explotable.

## Por qué es verificable

- Cualquiera puede correr el test en el repo privado y obtener la misma tabla.
- El test usa la librería real del servidor (`crypto/x509`), no un mock.
- Los certificados son efímeros, en memoria, y no se publican.
- El resultado está byte-a-byte de acuerdo con dos implementaciones
  independientes (Python y Zig).

## Estado del ciclo BYOTC

| Estado | Situación |
|---|---|
| 00 primitiva | Completo |
| 01 explotar | Refutado con Go real: 0 primitivas |
| 02 validar | Completo (21 tests) |
| 03 efecto emulado real | Cerrado con evidencia Go |
| 04 medición | 2/8 aceptados, tres implementaciones coincidentes |
| 05 auditoría | Gates A1-A6 + test Go |
| 06 publicación | Este resultado |
