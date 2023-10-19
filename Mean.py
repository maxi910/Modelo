import numpy as np
import pandas as pd
from scipy.stats import gmean, hmean

class CalculadoraDePromedios:
    def __init__(self, datos):
        self.datos = datos  # Asumiendo que 'datos' es un DataFrame de pandas

    def media_aritmetica(self, columna):
        return self.datos[columna].mean()

    def media_geometrica(self, columna):
        return gmean(self.datos[columna].dropna())  # Eliminando NaN antes de calcular la media geométrica

    def media_armonica(self, columna):
        return hmean(self.datos[columna].dropna())  # Eliminando NaN antes de calcular la media armónica

    def media_movil(self, columna, ventana):
        return self.datos[columna].rolling(window=ventana).mean()

    def media_movil_exponencial(self, columna, span):
        return self.datos[columna].ewm(span=span).mean()

# Ejemplo de uso
# Asegúrate de reemplazar 'df' con el DataFrame que obtienes de la clase en datos.py
calculadora = CalculadoraDePromedios(df)  

# Calculando la media móvil exponencial para una columna específica 
# (reemplaza 'columna' con el nombre real de tu columna y 'span' con el valor que desees)
media_movil_exponencial = calculadora.media_movil_exponencial('columna', span=20)

print("Media Móvil Exponencial (span de 20):", media_movil_exponencial)
