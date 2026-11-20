"""Tests del banco de SANs frontera."""

import unittest

from san_probe import decide, load, probe

DATA = load("fixtures/san_frontera.json")


class TestDecision(unittest.TestCase):
    def test_baseline_acepta(self):
        self.assertEqual(decide(["edge.lab.local"], "edge.lab.local"), "ACCEPTED")

    def test_mayusculas_acepta(self):
        self.assertEqual(decide(["edge.lab.local"], "EDGE.LAB.LOCAL"), "ACCEPTED")

    def test_trailing_dot_rechaza(self):
        self.assertEqual(decide(["edge.lab.local"], "edge.lab.local."), "REJECTED")

    def test_sufijo_rechaza(self):
        self.assertEqual(decide(["edge.lab.local"], "edge.lab.local.evil.com"), "REJECTED")


class TestProbe(unittest.TestCase):
    def test_ocho_casos(self):
        r = probe(DATA["allowlist"], DATA["casos"])
        self.assertEqual(len(r["casos"]), 8)

    def test_aceptados(self):
        r = probe(DATA["allowlist"], DATA["casos"])
        self.assertEqual(r["aceptados"], 2)  # F1 y F2

    def test_frontera_marcada(self):
        r = probe(DATA["allowlist"], DATA["casos"])
        por_id = {f["id"]: f for f in r["casos"]}
        self.assertFalse(por_id["F1"]["frontera"])
        self.assertFalse(por_id["F2"]["frontera"])
        self.assertTrue(por_id["F3"]["frontera"])


if __name__ == "__main__":
    unittest.main()
