class AnalizadorDeDatos:
    def __init__(self, df):
        self.df = df

    def _calcular_asimetria(self, precios):
        return skew(precios)

    def _calcular_curtosis(self, precios):
        return kurtosis(precios)

    def _calcular_desviacion_estandar(self, precios):
        return precios.std()

    def _calcular_promedio(self, precios):
        return precios.mean()

    def calcular_estadisticos(self):
        estadisticos = pd.DataFrame(index=['Asimetría', 'Curtosis', 'Desviación Estándar', 'Promedio'], columns=self.df.columns)

        for ticker in self.df.columns:
            precios = self.df[ticker].dropna()

            estadisticos[ticker] = [
                self._calcular_asimetria(precios),
                self._calcular_curtosis(precios),
                self._calcular_desviacion_estandar(precios),
                self._calcular_promedio(precios)
            ]

        return estadisticos
