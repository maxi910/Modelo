import pandas as pd
from scipy.stats import skew, kurtosis
from datos import APITiingo, APIStub

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
# tiingo = APITiingo(tu_clave_api_tiingo)
# df = tiingo.obtener_datos(tickers, fecha_inicio, fecha_fin)

# Ejemplo usando APIStub
stub = APIStub()
df = stub.obtener_datos(tickers, fecha_inicio, fecha_fin) 

analizador = AnalizadorDeDatos(df)
estadisticos = analizador.calcular_estadisticos()
print(estadisticos)
