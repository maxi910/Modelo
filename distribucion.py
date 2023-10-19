from fitter import Fitter
import pandas as pd
from testAndersonDarling import TestAndersonDarling
from analizador import AnalizadorDeDatos

class PropositorDeDistribucion:
    def __init__(self, datos):
        self.datos = datos  # Asumiendo que 'datos' es un DataFrame de pandas

    def proponer_distribucion(self, columna):
        f = Fitter(self.datos[columna].dropna())  # Eliminando NaN antes de ajustar la distribución
        f.fit()
        resumen = f.summary()
        mejor_distribucion = f.get_best(method = 'sumsquare_error')  # Puedes cambiar el método según tus necesidades
        return mejor_distribucion

# Ejemplo de uso
# Asegúrate de reemplazar 'df' con el DataFrame que obtienes de la clase en datos.py
propositor = PropositorDeDistribucion(df)  

# Proponiendo una distribución para una columna específica 
# (reemplaza 'columna' con el nombre real de tu columna)
mejor_distribucion = propositor.proponer_distribucion('columna')

print("Mejor Distribución Propuesta:", mejor_distribucion)

# Ahora, puedes usar esta distribución propuesta en tu test de Anderson-Darling
analizador = AnalizadorDeDatos(df)
test_ad = TestAndersonDarling(analizador, ['columna'])  # Asegúrate de adaptar los parámetros según tus necesidades
distribuciones = [mejor_distribucion['name']]  # Usando la distribución propuesta
resultados = test_ad.realizar_test(distribuciones)
test_ad.imprimir_resultados(resultados)
