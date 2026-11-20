# 03 - Efecto emulado real - CIERRE DEL CICLO

## Veredicto final

**BYOTC-SAN NO es explotable como capacidad de ataque.** El ciclo se cierra
con un hallazgo negativo: la técnica descrita produce un falso negativo
(rechazo), no una aceptación indebida.

Esto se ha verificado leyendo el código real (`server/cmd/mtls.go:29-69`) y
ejecutando el verificador sobre las cuatro fixtures.

## Análisis de explotabilidad (línea por línea)

| Línea | Control | Efecto sobre un atacante |
|---|---|---|
| 33 | `len(rawCerts)==0` | Rechaza sin certificado |
| 35-37 | `x509.ParseCertificate` | Rechaza cert malformado |
| 45-49 | `VerifyOptions` con `Roots=pool` | Exige que la CA esté en el bundle |
| 50-52 | `leaf.Verify(opts)` | Rechaza cadena no confiable |
| 53-57 | allowlist vacío | Fail-closed salvo escape de laboratorio |
| 63-67 | solo `leaf.DNSNames` | Compara DNS, ignora IP y URI |

### Por qué NO hay primitiva explotable

1. **La cadena se verifica contra un pool explícito** (`Roots: pool`). Un
   certificado emitido por una CA controlada por el atacante es rechazado en
   la línea 51. El "Bring Your Own Trusted Certificate" requiere que el atacante
   ya controle el trust store, lo cual es compromiso de configuración, no
   explotación de este código.

2. **El allowlist vacío es fail-closed** (líneas 53-57). El escape
   `C2_ALLOW_NO_MTLS_ALLOWLIST=1` está documentado como modo laboratorio en la
   auditoría de 2026. Activarlo es configuración, no vulnerabilidad.

3. **Ignorar IPAddresses/URIs hace el sistema MÁS estricto, no más débil.** Un
   allowlist con `10.0.0.5` rechaza un certificado con esa IP en el SAN. Eso es
   un falso negativo operativo (un operador legítimo queda fuera), no una
   puerta de entrada para un atacante.

4. **No se usa `crypto/x509` propio ni parser propio.** Es la librería estándar
   de Go. No hay bug de parsing explotable.

## Qué SÍ es el hallazgo

Un **defecto de usabilidad / documentación del flag**: `C2_MTLS_ALLOW` acepta
nombres DNS en la práctica, pero un operador razonable podría poner una IP y
obtener un rechazo silencioso sin explicación clara. El valor es para el equipo
azul y para el desarrollador: validar el formato del allowlist y documentar que
solo DNS.

## Por qué NO vale la pena desde un punto de vista ofensivo

| Criterio | Evaluación |
|---|---|
| Novedad | Ninguna: es configuración + librería estándar |
| Uplift para un atacante | Cero: no abre acceso que no existiera |
| Reproducibilidad | Alta como medición, nula como ataque |
| Riesgo legal de publicarlo como weapon | Alto, sin contrapartida técnica |
| Valor para el proyecto | Alto como hallazgo de hardening, nulo como arma |

Weaponizar esto equivaldría a publicar un generador de certificados genérico
que no puede vencer ninguno de los cuatro controles anteriores. No aportaría
nada que el paper no diga mejor y convertiría un artefacto verificable en una
herramienta dirigida a terceros.

## Estado final del ciclo

| Estado | Situación |
|---|---|
| 00 primitiva | Completo |
| 01 explotar | Documentado, cerrado como **no explotable** |
| 02 validar | Completo (14 tests) |
| 03 efecto emulado real | Cerrado: veredicto REJECTED, falso negativo |
| 04 medición | Metodología lista; 1/4 aceptados sobre fixture sintética |
| 05 auditoría | Completo (gates A1-A6) |
| 06 publicación | Release 1.0.0 |

## Corolario para el proyecto C2-DECT

El hallazgo refuerza la tesis del framework: la auditoría ofensiva encontró un
control que funciona (fail-closed, pool explícito). El trabajo pendiente no es
atacarlo, sino **documentar el formato del allowlist** y añadir un test que
verifique que IP/URI no coinciden - para que el falso negativo deje de ser
silencioso.
