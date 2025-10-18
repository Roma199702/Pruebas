class Material:
    def puntos(self, kg):
        raise NotImplementedError

    def max_kg_por_bolsa(self):
        raise NotImplementedError

class Plastico(Material):
    def puntos(self, kg):
        return kg * 5  # ejemplo: 5 puntos por kg

    def max_kg_por_bolsa(self):
        return 8

class Vidrio(Material):
    def puntos(self, kg):
        return kg * 2  # 2 puntos por kg

    def max_kg_por_bolsa(self):
        return 5

class PapelCarton(Material):
    def puntos(self, kg):
        return kg * 3  # 3 puntos por kg

    def max_kg_por_bolsa(self):
        return 7