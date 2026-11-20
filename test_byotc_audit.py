"""Tests del verificador BYOTC-SAN (datos sinteticos)."""

import unittest

from byotc_audit import audit, digest, evaluate

CONFIG = {
    "ca_bundle": ["ca-lab"],
    "allowlist": ["edge.lab.local"],
    "flags": {},
}


class TestByotcAudit(unittest.TestCase):
    def test_cadena_rechazada(self):
        r = evaluate(CONFIG, {"issuer": "ca-atacante", "san_dns": ["edge.lab.local"]})
        self.assertEqual(r["verdict"], "REJECTED")
        self.assertEqual(r["reason"], "chain_rejected")

    def test_allowlist_vacio_fail_closed(self):
        cfg = dict(CONFIG, allowlist=[])
        r = evaluate(cfg, {"issuer": "ca-lab", "san_dns": []})
        self.assertEqual(r["reason"], "fail_closed_empty_allowlist")

    def test_escape_de_laboratorio(self):
        cfg = dict(CONFIG, allowlist=[], flags={"allow_no_mtls_allowlist": True})
        r = evaluate(cfg, {"issuer": "ca-lab"})
        self.assertEqual(r["verdict"], "ACCEPTED")
        self.assertEqual(r["reason"], "lab_escape_empty_allowlist")

    def test_dns_allowlisted_insensible_a_mayusculas(self):
        r = evaluate(CONFIG, {"issuer": "ca-lab", "san_dns": ["EDGE.LAB.LOCAL"]})
        self.assertEqual(r["verdict"], "ACCEPTED")

    def test_ip_en_allowlist_no_comparado(self):
        cfg = dict(CONFIG, allowlist=["10.0.0.5"])
        r = evaluate(cfg, {"issuer": "ca-lab", "san_ip": ["10.0.0.5"]})
        self.assertEqual(r["verdict"], "REJECTED")
        self.assertEqual(r["reason"], "san_ip_not_compared")

    def test_san_no_allowlisted(self):
        r = evaluate(CONFIG, {"issuer": "ca-lab", "san_dns": ["otro.lab.local"]})
        self.assertEqual(r["reason"], "san_not_allowlisted")

    def test_audit_y_hash_determinista(self):
        certs = [
            {"id": "c1", "issuer": "ca-lab", "san_dns": ["edge.lab.local"]},
            {"id": "c2", "issuer": "ca-atacante", "san_dns": []},
        ]
        r = audit(CONFIG, certs)
        self.assertEqual(r["aceptados"], 1)
        self.assertEqual(len(r["verdicts"]), 2)
        self.assertEqual(r["config_sha256"], digest(CONFIG))


if __name__ == "__main__":
    unittest.main()
