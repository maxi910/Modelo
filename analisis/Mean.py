import numpy as np
import pandas as pd
from scipy.stats import gmean, hmean
from datos import APITiingo, APIStub 
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

