import unittest
from varasto import Varasto

class TestVarasto(unittest.TestCase):
    def setUp(self):
        self.varasto = Varasto(10)

    def test_konstruktori_luo_tyhjan_varaston(self):
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_uudella_varastolla_oikea_tilavuus(self):
        self.assertAlmostEqual(self.varasto.tilavuus, 10)

    def test_negatiivinen_tilavuus_nollataan(self):
        varasto = Varasto(-1)
        self.assertAlmostEqual(varasto.tilavuus, 0)

    def test_negatiivinen_alkusaldo_nollataan(self):
        varasto = Varasto(10, -1)
        self.assertAlmostEqual(varasto.saldo, 0)

    def test_alkusaldo_mahtuu_varastoon(self):
        varasto = Varasto(10, 5)
        self.assertAlmostEqual(varasto.saldo, 5)

    def test_ylimenevä_alkusaldo_täyttää_varaston(self):
        varasto = Varasto(10, 15)
        self.assertAlmostEqual(varasto.saldo, 10)

    def test_paljonko_mahtuu_palauttaa_oikean_määrän(self):
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 10)

    def test_lisaa_varastoon_negatiivinen_maara_ei_muuta_saldoa(self):
        self.varasto.lisaa_varastoon(-1)
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_lisaa_varastoon_mahtuva_maara(self):
        self.varasto.lisaa_varastoon(5)
        self.assertAlmostEqual(self.varasto.saldo, 5)

    def test_lisaa_varastoon_ylimenevä_maara_täyttää_varaston(self):
        self.varasto.lisaa_varastoon(15)
        self.assertAlmostEqual(self.varasto.saldo, 10)

    def test_ota_varastosta_negatiivinen_maara_palauttaa_nollan(self):
        saatu_maara = self.varasto.ota_varastosta(-1)
        self.assertAlmostEqual(saatu_maara, 0)
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_ota_varastosta_liikaa_palauttaa_kaiken_mita_voi(self):
        self.varasto.lisaa_varastoon(5)
        saatu_maara = self.varasto.ota_varastosta(10)
        self.assertAlmostEqual(saatu_maara, 5)
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_ota_varastosta_toimii_normaalisti(self):
        self.varasto.lisaa_varastoon(8)
        saatu_maara = self.varasto.ota_varastosta(3)
        self.assertAlmostEqual(saatu_maara, 3)
        self.assertAlmostEqual(self.varasto.saldo, 5)

    def test_str_palauttaa_oikean_merkkijonon(self):
        self.varasto.lisaa_varastoon(5)
        self.assertEqual(str(self.varasto), "saldo = 5, vielä tilaa 5")