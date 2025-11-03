class Varasto:
    def __init__(self, tilavuus, alku_saldo = 0):
        self.tilavuus = self._validoi_tilavuus(tilavuus)
        self.saldo = self._validoi_alku_saldo(alku_saldo, self.tilavuus)

    def _validoi_tilavuus(self, tilavuus):
        """Validoi ja palauta tilavuus, nollaa jos virheellinen."""
        if tilavuus > 0.0:
            return tilavuus
        # virheellinen, nollataan
        return 0.0

    def _validoi_alku_saldo(self, alku_saldo, tilavuus):
        """Validoi ja palauta alku_saldo, korjaa jos virheellinen."""
        if alku_saldo < 0.0:
            # virheellinen, nollataan
            return 0.0
        if alku_saldo <= tilavuus:
            # mahtuu
            return alku_saldo
        # täyteen ja ylimäärä hukkaan!
        return tilavuus

    # huom: ominaisuus voidaan myös laskea. Ei tarvita erillistä kenttää.
    def paljonko_mahtuu(self):
        return self.tilavuus - self.saldo

    def lisaa_varastoon(self, maara):
        if maara < 0:
            return
        if maara <= self.paljonko_mahtuu():
            self.saldo = self.saldo + maara
        else:
            self.saldo = self.tilavuus

    def ota_varastosta(self, maara):
        if maara < 0:
            return 0.0
        if maara > self.saldo:
            kaikki_mita_voidaan = self.saldo
            self.saldo = 0.0

            return kaikki_mita_voidaan

        self.saldo = self.saldo - maara

        return maara

    def __str__(self):
        return f"saldo = {self.saldo}, vielä tilaa {self.paljonko_mahtuu()}"
