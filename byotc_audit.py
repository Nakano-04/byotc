"""B-07 BYOTC-SAN: verificador ANALITICO de decision mTLS.

NO genera certificados, NO toca TLS, NO implementa evasion. Solo reproduce la
logica de decision de `server/cmd/mtls.go` sobre metadatos declarados y emite
ACCEPTED / REJECTED con el motivo y el hash de la configuracion.

Es una herramienta de investigacion: permite medir bajo que configuracion un
certificado controlado por un tercero seria aceptado por el C2.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def digest(obj: dict) -> str:
    raw = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def evaluate(config: dict, cert: dict) -> dict:
    """Reproduce verifyMTLSLeaf() con datos declarados, sin criptografia real."""
    pool = {name.lower() for name in config.get("ca_bundle", [])}
    allow = {name.lower() for name in config.get("allowlist", [])}
    flags = config.get("flags", {})

    issuer = str(cert.get("issuer", "")).lower()
    if issuer not in pool:
        return {"verdict": "REJECTED", "reason": "chain_rejected",
                "detail": f"issuer {issuer!r} no esta en el bundle de CAs"}

    if not allow:
        if flags.get("allow_no_mtls_allowlist") is True:
            return {"verdict": "ACCEPTED", "reason": "lab_escape_empty_allowlist",
                    "detail": "allowlist vacia + C2_ALLOW_NO_MTLS_ALLOWLIST=1"}
        return {"verdict": "REJECTED", "reason": "fail_closed_empty_allowlist",
                "detail": "allowlist vacia sin escape de laboratorio"}

    dns_names = [str(d).lower() for d in cert.get("san_dns", [])]
    matched = [d for d in dns_names if d in allow]
    if matched:
        return {"verdict": "ACCEPTED", "reason": "san_dns_allowlisted",
                "detail": f"SAN DNS permitido: {matched}"}

    san_ips = [str(ip) for ip in cert.get("san_ip", [])]
    ip_match = [ip for ip in san_ips if ip in allow]
    if ip_match:
        return {"verdict": "REJECTED", "reason": "san_ip_not_compared",
                "detail": "el allowlist solo compara DNSNames, no IPAddresses (B-07)"}

    return {"verdict": "REJECTED", "reason": "san_not_allowlisted",
            "detail": f"SAN {dns_names} no coincide con el allowlist"}


def audit(config: dict, certs: list[dict]) -> dict:
    results = []
    for cert in certs:
        result = evaluate(config, cert)
        result["cert"] = cert.get("id", "sin-id")
        results.append(result)
    return {
        "tecnica": "B-07 BYOTC-SAN",
        "config_sha256": digest(config),
        "certs_sha256": digest({"certs": certs}),
        "verdicts": results,
        "aceptados": sum(1 for r in results if r["verdict"] == "ACCEPTED"),
        "nota": "Analisis de configuracion. No genera certificados ni abre conexiones TLS.",
    }


def load(path: str | Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config")
    parser.add_argument("certs")
    args = parser.parse_args()
    print(json.dumps(audit(load(args.config), load(args.certs)), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
