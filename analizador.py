import pandas as pd
from scipy.stats import skew, kurtosis

class AnalizadorDeDatos:
    def __init__(self, df):
        self.df = df

    def calcular_estadisticos(self):
        estadisticos = pd.DataFrame(index=['Asimetría', 'Curtosis', 'Desviación Estándar', 'Promedio'], columns=self.df.columns)

        for ticker in self.df.columns:
            precios = self.df[ticker].dropna()  # Eliminar valores NaN si los hay

            # Calcular estadísticos
            asimetria = skew(precios)
            curt = kurtosis(precios)
            desviacion_estandar = precios.std()
            promedio = precios.mean()

            # Almacenar estadísticos en el DataFrame
            estadisticos[ticker] = [asimetria, curt, desviacion_estandar, promedio]

        return estadisticos

# Uso del código
# Suponiendo que tienes un DataFrame df con los datos de los tickers
# df = obtener_datos(tickers, fecha_inicio, fecha_fin)  # Esta función debería devolver un DataFrame con los datos de los tickers

analizador = AnalizadorDeDatos(df)
estadisticos = analizador.calcular_estadisticos()
print(estadisticos)
