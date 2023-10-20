import numpy as np
import pandas as pd
from scipy.stats import gmean, hmean
from datos import APITiingo, APIStub  # Comentado porque no tengo el módulo datos
import matplotlib.pyplot as plt

class CalculadoraDePromedios:
    def __init__(self, datos):
        self.datos = datos

    def media_aritmetica(self, columna):
        return self.datos[columna].mean()

    def media_geometrica(self, columna):
        return gmean(self.datos[columna].dropna())

    def media_armonica(self, columna):
        return hmean(self.datos[columna].dropna())

    def media_movil(self, columna, ventana):
        return self.datos[columna].rolling(window=ventana).mean()

    def media_movil_exponencial(self, columna, span):
        return self.datos[columna].ewm(span=span).mean()

tickers_usuario = input("Ticker: ") 
tickers_usuario = [ticker.strip() for ticker in tickers_usuario] 

df = pd.DataFrame({ticker: np.random.normal(size=100) for ticker in tickers_usuario}) 

calculadora = CalculadoraDePromedios(df)  

# Solicitar al usuario que ingrese el nombre de la columna
columna = input("Ingrese el nombre de la columna para calcular la media móvil exponencial: ").strip()

if columna in df.columns:
    media_movil_exponencial = calculadora.media_movil_exponencial(columna, span=20)
    print(f"Media Móvil Exponencial (span de 20) para {columna}:", media_movil_exponencial)

    plt.figure(figsize=(10,6))
    plt.plot(media_movil_exponencial, label=f'Media Móvil Exponencial (span de 20) para {columna}')
    plt.title(f'Media Móvil Exponencial para {columna}')
    plt.xlabel('Índice')
    plt.ylabel('Valor')
    plt.legend()
    plt.grid(True)
    plt.show()
else:
    print(f"La columna '{columna}' no se encuentra en el DataFrame.")
