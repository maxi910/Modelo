from analizador import AnalizadorDeDatos
from scipy.stats import anderson
import pandas as pd
import numpy as np

class TestAndersonDarling:
    def __init__(self, analizador, tickers):
        self.analizador = analizador
        self.tickers = tickers

    def realizar_test(self, distribuciones):
        resultados = {}

        for ticker in self.tickers:  # Iterar sobre los tickers proporcionados por el usuario
            if ticker not in self.analizador.df.columns:
                print(f"El ticker {ticker} no se encuentra en los datos disponibles.")
                continue
            
            precios = self.analizador.df[ticker].dropna()
            resultados[ticker] = {}
            
            for dist in distribuciones:
                resultado = anderson(precios, dist=dist)
                resultados[ticker][dist] = resultado

        return resultados

    def imprimir_resultados(self, resultados):
        for ticker, dists in resultados.items():
            print(f"Resultados para {ticker}:")
            
            for dist, resultado in dists.items():
                print(f"Distribución: {dist}")
                print("Estadístico de Anderson-Darling:", resultado.statistic)

                for i in range(len(resultado.critical_values)):
                    sl, cv = resultado.significance_level[i], resultado.critical_values[i]
                    if resultado.statistic < cv:
                        print(f"A un nivel de significancia del {sl}%, los datos parecen seguir la distribución {dist} (Estadístico: {resultado.statistic} < Valor crítico: {cv}).")
                    else:
                        print(f"A un nivel de significancia del {sl}%, los datos no parecen seguir la distribución {dist} (Estadístico: {resultado.statistic} > Valor crítico: {cv}).")
                print()

    def determinar_distribucion(self, resultados):
        distribuciones_por_ticker = {}

        for ticker, dists in resultados.items():
            mejor_dist = None
            menor_estadistico = float('inf')

            for dist, resultado in dists.items():
                if resultado.statistic < menor_estadistico and resultado.statistic < resultado.critical_values[-1]:
                    mejor_dist = dist
                    menor_estadistico = resultado.statistic

            distribuciones_por_ticker[ticker] = mejor_dist if mejor_dist else 'No se encontró una buena distribución'

        return distribuciones_por_ticker

# Uso del código
tickers_usuario = input("Ingrese los tickers separados por comas: ").split(",")  # Obtener los tickers del usuario
tickers_usuario = [ticker.strip() for ticker in tickers_usuario]  # Limpiar espacios en blanco

# Asegúrate de que los tickers ingresados por el usuario estén en el DataFrame
df = pd.DataFrame({ticker: np.random.normal(size=100) for ticker in tickers_usuario})  # Reemplaza esto con tus datos reales

analizador = AnalizadorDeDatos(df)
test = TestAndersonDarling(analizador, tickers_usuario)  # Pasar los tickers del usuario al constructor
distribuciones = ['norm', 'expon', 'logistic']  
resultados = test.realizar_test(distribuciones)
test.imprimir_resultados(resultados)

# Determinar la distribución que mejor se ajusta a los datos de cada ticker
distribuciones = test.determinar_distribucion(resultados)
print("La distribución que mejor se ajusta a los datos de cada ticker es:")
for ticker, dist in distribuciones.items():
    print(f"{ticker}: {dist}")
