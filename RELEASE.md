# BYOTC - Research Release 1.0.0

Fecha: 2026-11-20

Release de **investigación**: documentación, protocolos y resultados
verificables sobre la decisión mTLS de C2-DECT. No es una release del framework
ni una herramienta de ataque.

## Contenido

- `KNOWLEDGE.md`: toda la base de conocimiento BYOTC en un solo lugar.
- `states/00` a `states/06`: el ciclo primitiva -> explotar -> validar ->
  efecto emulado real -> medición -> auditoría -> publicación.
- `byotc_audit.py` / `byotc_audit_zig`: verificador de decisión mTLS.
- `footprint_zig`: huella conductual determinista.
- `verify_manifest_zig`: integridad del contenido.

## Estado del ciclo

| Estado | Situación |
|---|---|
| 00 primitiva | Completo |
| 01 explotar | Protocolo documentado, sin ejecutar |
| 02 validar | Completo (8 tests Python + Zig) |
| 03 efecto emulado real | Pendiente (requiere VM + RoE) |
| 04 medición | Metodología lista, sin datos reales |
| 05 auditoría | Completo (gates A1-A6) |
| 06 publicación | Este documento |

## Hallazgo (cerrado)

BYOTC-SAN: `verifyMTLSLeaf()` compara solo `leaf.DNSNames`, no `IPAddresses` ni
`URIs`. Un allowlist con IP nunca acepta un certificado con esa IP en el SAN.
Falso negativo de implementación, verificado sobre código real.

**No explotable.** La cadena se valida contra un pool explícito y el allowlist
vacío es fail-closed. Ignorar IP/URI hace el sistema más estricto. Uplift para
un atacante: cero. El valor del hallazgo es de hardening, no de ataque.

## Banco de SANs frontera (nuevo)

`san_probe.py` / `san_probe_zig` prueban 8 nombres SAN frontera contra la regla
de decisión del allowlist. Resultado del modelo: solo coinciden el baseline y
el case-folding; trailing dot, punycode, wildcard, sufijo y NUL se rechazan.
**0 primitivas nuevas** en el modelo. Ejecución real contra el C2 pendiente
(requiere VM + RoE). Ver `states/01-explotar.md`.

## Verificación

- 3 ejecutables Zig compilados en ReleaseFast.
- Tests Python: 8 BYOTC + 4 footprint + 3 integridad = 15.
- `artifacts.sha256` validado por `verify_manifest_zig`.
- Sin secretos, sin claves, sin em-dashes.

## Uso autorizado

Solo laboratorio aislado con alcance declarado y RoE firmada. El uso contra
activos de terceros sin autorización es ilegal.
