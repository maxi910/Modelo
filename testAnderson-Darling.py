from analizador import AnalizadorDeDatos  # Importa la clase desde el otro archivo
from scipy.stats import anderson
import pandas as pd
import numpy as np

class TestAndersonDarling:
    def __init__(self, analizador):
        self.analizador = analizador

    def realizar_test(self, dist='norm'):
        resultados = {}

        for ticker in self.analizador.df.columns:
            precios = self.analizador.df[ticker].dropna()
            resultado = anderson(precios, dist=dist)
            resultados[ticker] = resultado

        return resultados

    def imprimir_resultados(self, resultados):
        for ticker, resultado in resultados.items():
            print(f"Resultados para {ticker}:")
            print("Estadístico de Anderson-Darling:", resultado.statistic)

            for i in range(len(resultado.critical_values)):
                sl, cv = resultado.significance_level[i], resultado.critical_values[i]
                if resultado.statistic < cv:
                    print(f"A un nivel de significancia del {sl}%, los datos parecen ser normales (Estadístico: {resultado.statistic} < Valor crítico: {cv}).")
                else:
                    print(f"A un nivel de significancia del {sl}%, los datos no parecen ser normales (Estadístico: {resultado.statistic} > Valor crítico: {cv}).")
            print()

# Uso del código
df = pd.DataFrame({'AAPL': np.random.normal(size=100)})  # Reemplaza esto con tus datos reales

analizador = AnalizadorDeDatos(df)
test = TestAndersonDarling(analizador)
resultados = test.realizar_test(dist='norm')  # Puedes cambiar 'norm' a otra distribución soportada como 'expon', 'logistic', etc.
test.imprimir_resultados(resultados)
