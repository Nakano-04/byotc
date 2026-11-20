# Base de conocimiento BYOTC

Todo lo que se sabe hoy, en un solo lugar. Cada afirmación lleva su fuente.

## 1. La primitiva (código real)

`server/cmd/mtls.go`, función `verifyMTLSLeaf()`:

- valida la cadena del leaf contra un `x509.CertPool` de CAs raíz;
- `ExtKeyUsageClientAuth` en `x509.VerifyOptions`;
- allowlist vacía = fail-closed, salvo `C2_ALLOW_NO_MTLS_ALLOWLIST=1`;
- compara **solo `leaf.DNSNames`** en minúsculas.

`buildServerTLSConfig()` rechaza arrancar si hay CA pero no hay allowlist.

## 2. Los tres caminos

| Camino | Naturaleza | ¿Novedoso? |
|---|---|---|
| CA propia en el bundle | Configuración / supply chain | No |
| `C2_ALLOW_NO_MTLS_ALLOWLIST=1` | Escape hatch de laboratorio | No, ya auditado |
| Allowlist con IP vs SAN DNS/IP | Bug de implementación | **Sí** |

## 3. El hallazgo (cerrado)

El allowlist no compara `IPAddresses` ni `URIs`. Un operador que configure
`C2_MTLS_ALLOW=10.0.0.5` nunca verá aceptado un certificado con esa IP en el
SAN. Es un **falso negativo**: el código es más restrictivo de lo que el flag
sugiere. No es un bypass; es una discrepancia de implementación.

**No explotable.** La cadena se verifica contra un pool explícito y el allowlist
vacío es fail-closed. Ignorar IP/URI hace el sistema más estricto, no más débil.
No hay primitiva de ataque: el uplift para un atacante es cero. Ver
`states/03-efecto-emulado-real.md`.

## 4. Nombre

"Trusted" describe mejor que "vulnerable": el certificado se acepta porque la
pila lo considera válido. El sufijo `-SAN`evita que parezca un rename de BYOVD.

## 5. Lecciones transversales

- Zig no vuelve "desconocida" la huella: `footprint.py` y `footprint_zig`
  producen el mismo SHA256. El lenguaje no cambia la conducta.
- Lo que Zig aporta es reproducibilidad: versión + semilla + `build_id`.
- Toda medición lleva semilla, `n` e IC95%. Un bypass con `n=1` es anécdota.
- G1: todo TTP ejecutado tiene `DetectionRecord` con `RuleID` y `Source`.
- G3: ningún hallazgo se cierra automáticamente; cierre = retest.
- G8: rutas y hashes sanitizados, sin secretos.

## 6. Veredicto ofensivo

No vale la pena weaponizar. No hay primitiva explotable, el uplift es cero y el
valor está en el hardening: documentar el formato del allowlist y añadir un
test que haga visible el falso negativo.

## 7. Fuentes

- `AUDITORIA_OFENSIVA_c2-dect_2026.md` (vectores y escape hatches)
- `c2dect-investigacion/OFENSIVA/07-bypass-auditable.md`
- `c2dect-investigacion/OFENSIVA/08-zig-instrumento-auditable.md`
- `c2dect-investigacion/OFENSIVA/09-plan-ejecucion-lab.md`
- `c2dect-investigacion/OFENSIVA/10-byotc-san.md`
