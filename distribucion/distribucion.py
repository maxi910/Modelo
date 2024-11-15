from fitter import Fitter
import pandas as pd
from testAnderson-Darling import TestAndersonDarling
from analizador import AnalizadorDeDatos

class PropositorDeDistribucion:
    def __init__(self, datos):
        self.datos = datos  

    def proponer_distribucion(self, columna):
        f = Fitter(self.datos[columna].dropna())  
        f.fit()
        resumen = f.summary()
        mejor_distribucion = f.get_best(method = 'sumsquare_error')
        return mejor_distribucion

propositor = PropositorDeDistribucion(df)  

# Proponiendo una distribución para una columna específica 
# (reemplaza 'columna' con el nombre real de tu columna)
mejor_distribucion = propositor.proponer_distribucion('columna')

print("Mejor Distribución Propuesta:", mejor_distribucion)

analizador = AnalizadorDeDatos(df)
test_ad = TestAndersonDarling(analizador, ['columna'])
distribuciones = [mejor_distribucion['name']] 
resultados = test_ad.realizar_test(distribuciones)
test_ad.imprimir_resultados(resultados)
