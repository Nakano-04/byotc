#!/usr/bin/env python3
"""Banco de pruebas de SANs frontera para el allowlist mTLS.

NO genera certificados ni toca TLS. Reproduce la regla de decision de
`verifyMTLSLeaf` (strings.ToLower + comparacion exacta contra DNSNames) sobre
una lista de nombres SAN candidatos, para detectar normalizaciones que el
operador podria considerar equivalentes pero que el codigo trata distinto.

Salida: por caso, ACCEPTED/REJECTED y si es "frontera" (distinto del baseline).
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def decide(allow: list[str], dns: str) -> str:
    """Traduccion fiel de verifyMTLSLeaf: lower() + coincidencia exacta."""
    allowed = {name.lower() for name in allow}
    return "ACCEPTED" if dns.lower() in allowed else "REJECTED"


def probe(allow: list[str], casos: list[dict]) -> dict:
    baseline = None
    filas = []
    for caso in casos:
        dns = caso["dns"]
        verdict = decide(allow, dns)
        if caso["id"] == "F1":
            baseline = verdict
        filas.append({
            "id": caso["id"],
            "dns": dns,
            "verdict": verdict,
            "frontera": (verdict != baseline) if baseline else None,
            "nota": caso.get("nota", ""),
        })
    return {
        "regla": "strings.ToLower(dns) in allowlist (exacto)",
        "allowlist": allow,
        "allowlist_sha256": hashlib.sha256(
            json.dumps(allow, sort_keys=True).encode()
        ).hexdigest(),
        "casos": filas,
        "aceptados": sum(1 for f in filas if f["verdict"] == "ACCEPTED"),
        "nota": "Modelo de decision. Requiere validacion con certificados reales en laboratorio.",
    }


def load(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture")
    args = parser.parse_args()
    data = load(args.fixture)
    print(json.dumps(probe(data["allowlist"], data["casos"]), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
